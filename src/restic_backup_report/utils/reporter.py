import threading
import traceback

from datetime import datetime, timedelta
from queue import Queue
from zoneinfo import ZoneInfo

from operator import itemgetter

from restic_backup_report.models.general_config import GeneralConfig
from restic_backup_report.models.snapshot_report import SnapshotReport
from restic_backup_report.models.storage import Storage
from restic_backup_report.models.storage_report import UsageState
from restic_backup_report.reports.base_report import Report

from restic_backup_report.targets.base_target import Target

from restic_backup_report.utils.restic import Repository, ResticManager

from restic_backup_report.models.repository import Repository, ReportType
from restic_backup_report.models.snapshot import Snapshot
from restic_backup_report.utils.storage import get_folder_size, get_mountpoint_of_partition, get_partition_of_folder, get_partition_size, get_partition_usage


class Reporter:


    def __init__(self, general_config: GeneralConfig, repos: list[Repository], targets: list[Target], storages: list[Storage], log_queue: Queue[str] | None):
        self.general_config = general_config
        self.repos = repos
        self.targets = targets
        self.storages = storages

        self.reports: dict[type[Report], Report] = {}
        self.done = threading.Event()

        self.log_queue = log_queue

        self.__prepare_progress_reporting()


    def __prepare_progress_reporting(self) -> float:
        return 1.0


    def _filter_snapshots(self, snapshots: list[Snapshot], report: ReportType, now: datetime) -> tuple[datetime, datetime, list[Snapshot]]:

        match report:

            case ReportType.DAILY:
                start = now.replace(hour=0, minute=0, second=0, microsecond=0)
                end = start + timedelta(days=1)

            case ReportType.WEEKLY:
                start = (
                    now - timedelta(days=now.weekday())
                ).replace(
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                )
                end = start + timedelta(days=7)

            case ReportType.MONTHLY:
                start = now.replace(
                    day=1, hour=0, minute=0, second=0, microsecond=0
                )

                if start.month == 12:
                    end = start.replace(year=start.year + 1, month=1)
                else:
                    end = start.replace(month=start.month + 1)

            case ReportType.YEARLY:
                start = now.replace(
                    month=1, day=1,
                    hour=0, minute=0, second=0, microsecond=0
                )
                end = start.replace(year=start.year + 1)

            case _:
                raise ValueError(f"Unsupported report: {report}")

        return (start, end, [
            snapshot
            for snapshot in snapshots
            if start <= snapshot.time < end
        ])


    def _get_expected_backups(self, repository: Repository, start: datetime, end: datetime) -> list[datetime]:

        return repository.frequency.between(start, end)

    
    def _match_snapshots(self, repository: Repository, snapshots: list[Snapshot], expected: list[datetime]) -> dict[datetime, list[Snapshot]]:

        matches: dict[datetime, list[Snapshot]] = {}

        tolerance = timedelta(hours=repository.tolerance)
        snapshots = sorted(snapshots, key=lambda snapshot: snapshot.time)
            
        for expected_time in expected:
            start = expected_time - tolerance
            end = expected_time + tolerance

            matches[expected_time] = [
                snapshot
                for snapshot in snapshots
                if start <= snapshot.time < end
            ]

        return matches     


    def _create_snapshot_reports(self, matches: dict[datetime, list[Snapshot]]) -> dict[datetime, list[SnapshotReport]]:

        result: dict[datetime, list[SnapshotReport]] = {}

        for time, snapshots in matches.items():

            if not snapshots:
                result[time] = list()
                continue

            snapshots = sorted(snapshots, key=lambda snapshot: snapshot.time)

            for i in range(len(snapshots)):
                result[time] = SnapshotReport(
                    snapshot=snapshots[i],
                    relevant=(i == len(snapshots) - 1)
                )

        return result
                     


    def run(self):
        try:
            ## Create reports

            for target in self.targets:
                format = target.format
                if not format in self.reports.keys():
                    self.reports[format] = format()

            ## Fill reports

            # Repository
            for repository in self.repos:

                for report in self.reports.values():
                    report.append_repository(repository)

                try:
                    if not ResticManager.is_repo_compatible(repository):
                        for report in self.reports.values():
                            report.set_repository_incompatible(repository)
                            report.finish_repository(repository, False)
                        continue

                    integrity = ResticManager.check_repo_integrity(repository)
                    for report in self.reports.values():
                        report.set_repository_integrity(repository, integrity)
                    
                    if integrity:
                        start, end, snapshots = self._filter_snapshots(
                            ResticManager.get_snapshots(repository),
                            repository.report,
                            datetime.now(ZoneInfo(key=self.general_config.timezone))
                        )

                        snapshot_reports = self._create_snapshot_reports(
                            self._match_snapshots(
                                repository, snapshots, self._get_expected_backups(
                                    repository, start, end
                                )
                            )
                        )

                        for report in self.reports.values():
                            report.set_repository_snapshot_reports(
                                repository, snapshot_reports
                            )

                    else:
                        for report in self.reports.values():
                            report.finish_repository(repository, False)

                except Exception as e:
                    print(e)
                    for report in self.reports.values():
                        report.finish_repository(repository, False)
                    continue

            # Storage
            for storage in self.storages:

                for report in self.reports.values():
                    report.append_storage(storage)

                try:
                    folder_size = get_folder_size(storage.path)

                    partition = get_partition_of_folder(storage.path)
                    mountpoint = get_mountpoint_of_partition(partition)
                    partition_size = get_partition_size(partition)

                    usage = get_partition_usage(partition)
                    usage_state = UsageState.NONE

                    if usage >= ((float) (storage.warning_percent / 100)):
                        usage_state = UsageState.WARNING

                    if usage >= ((float) (storage.warning_percent / 100)):
                        usage_state = UsageState.CRITICAL

                    for report in self.reports.values():

                        report.set_storage_folder(storage, storage.path)
                        report.set_storage_folder_size(storage, folder_size)

                        report.set_storage_partition(storage, partition)
                        report.set_storage_mountpoint(storage, mountpoint)
                        report.set_storage_partition_size(storage, partition_size)
                        report.set_storage_usage(storage, usage)
                        report.set_storage_usage_state(storage, usage_state)

                        report.finish_storage(storage)

                except Exception as e:
                    print(e)
                    for report in self.reports.values():
                        report.finish_storage(storage, False)
                    continue

            ##  Send reports

            for target in self.targets:
                try:
                    target.send(self.reports[target.format])
                except Exception as e:
                    print(e)
                    continue
        finally:
            self.done.set()
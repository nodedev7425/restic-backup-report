import threading

from datetime import datetime, timedelta
from queue import Queue
from zoneinfo import ZoneInfo

from restic_backup_report.reports.base_report import Report

from restic_backup_report.targets.base_target import Target

from restic_backup_report.utils.restic import Repository, ResticManager

from restic_backup_report.models.repository import Repository, BackupFrequency, ReportType
from restic_backup_report.models.snapshot import Snapshot


class Reporter:


    def __init__(self, repos: list[Repository], targets: list[Target], log_queue: Queue[str] | None):
        self.repos = repos
        self.targets = targets

        self.reports: dict[type[Report], Report] = {}
        self.done = threading.Event()

        self.log_queue = log_queue

        self.__prepare_progress_reporting()


    def __prepare_progress_reporting(self) -> float:
        return 1.0


    def _filter_snapshots(self, snapshots: list[Snapshot], frequency: BackupFrequency, now: datetime) -> list[Snapshot]:

        match frequency:

            case BackupFrequency.DAILY:
                start = now.replace(hour=0, minute=0, second=0, microsecond=0)
                end = start + timedelta(days=1)

            case BackupFrequency.WEEKLY:
                start = (
                    now - timedelta(days=now.weekday())
                ).replace(
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                )
                end = start + timedelta(days=7)

            case BackupFrequency.MONTHLY:
                start = now.replace(
                    day=1, hour=0, minute=0, second=0, microsecond=0
                )

                if start.month == 12:
                    end = start.replace(year=start.year + 1, month=1)
                else:
                    end = start.replace(month=start.month + 1)

            case BackupFrequency.YEARLY:
                start = now.replace(
                    month=1, day=1,
                    hour=0, minute=0, second=0, microsecond=0
                )
                end = start.replace(year=start.year + 1)

            case _:
                raise ValueError(f"Unsupported frequency: {frequency}")

        return [
            snapshot
            for snapshot in snapshots
            if start <= snapshot.time < end
        ]
    

    def _backups_complete(self, repository: Repository, snapshots: list[Snapshot]) -> tuple[int, int]:

        for snapshot in snapshots:

            # IF: program_version 

            pass

        return [10, 10]                


    def run(self):
        try:
            # Create reports

            for target in self.targets:
                format = target.format
                if not format in self.reports.keys():
                    self.reports[format] = format()

            # Fill reports

            for repository in self.repos:

                for report in self.reports.values():
                    report.append_repository(repository)

                try:
                    if not ResticManager.is_repo_compatible(repository):
                        for report in self.reports.values():
                            report.set_repository_incompatible(repository)
                            report.finish(repository, False)
                        continue

                    integrity = ResticManager.check_repo_integrity(repository)
                    for report in self.reports.values():
                        report.set_repository_integrity(repository, integrity)
                    
                    if integrity:
                        snapshots: list[Snapshot] = self._filter_snapshots(
                            ResticManager.get_snapshots(repository),
                            repository.frequency,
                            datetime.now(ZoneInfo("Europe/Berlin"))
                        )

                        backups_complete = self._backups_complete(repository, snapshots)

                        for report in self.reports.values():
                            pass

                    else:
                        report.finish(repository, False)

                except Exception as e:
                    print(e)
                    report.finish(repository, False)
                    continue

            #  Send reports

            for target in self.targets:
                try:
                    target.send(self.reports[target.format])
                except:
                    pass
        finally:
            self.done.set()




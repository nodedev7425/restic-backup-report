from queue import Queue
import threading

from restic_backup_report.report.base_report import Report
from restic_backup_report.targets.base_target import Target
from restic_backup_report.utils.restic import Repository, ResticManager


class Reporter:


    def __init__(self, repos: list[Repository], targets: list[Target], log_queue: Queue[str] | None):
        self.repos = repos
        self.targets = targets

        self.reports: dict[type[Report], Report] = {}
        self.done = threading.Event()

        

        self.__prepare_progress_reporting()


    def __prepare_progress_reporting(self):
        pass


    def run(self):
        try:
            for target in self.targets:
                format = target.format
                if not format in self.reports.keys():
                    self.reports[format] = format()

            for repository in self.repos:

                for report in self.reports.values():
                    report.append_repository(repository)

                if not ResticManager.is_repo_compatible(repository):
                    for report in self.reports.values():
                        report.set_repository_incompatible(repository.get_name())
                    continue

                integrity = ResticManager.check_repo_integrity(repository)
                report.set_repository_integrity(repository.get_name(), integrity)
                
                if integrity:
                    for report in self.reports.values():
                        pass
        finally:
            self.done.set()




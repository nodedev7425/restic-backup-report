import threading

from src.restic_backup_report.targets.base_target import Target
from src.restic_backup_report.utils.restic import Repository


class Report:
    pass


class Reporter:


    def __init__(self, repos: list[Repository], targets: list[Target]):
        self.repos = repos
        self.targets = targets

        self.done = threading.Event()


    def run(self):
        try:
            pass
        finally:
            self.done.set()




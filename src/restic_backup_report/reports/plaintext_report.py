from restic_backup_report.report.base_report import Report

from restic_backup_report.reports. as repo_template

class PlaintextReport(Report):


    def render(self) -> str:

        for repo in self.repositories.keys():

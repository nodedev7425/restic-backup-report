from restic_backup_report.reports.base_report import Report

from restic_backup_report.templates.report.plaintext_repository_format import template as repo_template

class PlaintextReport(Report):


    def render(self) -> str:

        for repo in self.repositories.keys():
            pass
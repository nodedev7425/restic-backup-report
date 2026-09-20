from restic_backup_report.reports.base_report import Report

from src.restic_backup_report.templates.report.plaintext_format import template

class PlaintextReport(Report):


    def render(self) -> str:
        return template.render({ "data": self.repositories })


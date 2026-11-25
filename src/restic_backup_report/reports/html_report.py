from restic_backup_report.reports.base_report import Report

from src.restic_backup_report.templates.report.html_format import template

class HtmlReport(Report):


    def render(self) -> str:
        return template.render({ "repos": self.repositories, "storages": self.storages })
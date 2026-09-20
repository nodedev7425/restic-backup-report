from restic_backup_report.reports.base_report import Report

from restic_backup_report.templates.report.plaintext_repository_format import template as repo_template
from restic_backup_report.templates.report.plaintext_base_format import template as base_template

class PlaintextReport(Report):


    def render(self) -> str:

        repos: list[str] = []
        for repo in self.repositories.keys():

            report = self.repositories[repo]

            data: dict = {
                "repository_display_name": repo.display_name,
                "repository_name": repo.name,
                "repository_report_incompatible": report.incompatible,
                "repository_report_integrity": report.integrity
            }

            repos.append(repo_template.render(**data))

        return base_template.render({
            "repositories": repos
        })
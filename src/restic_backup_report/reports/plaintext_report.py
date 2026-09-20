from restic_backup_report.reports.base_report import Report

from restic_backup_report.templates.report.plaintext_repository_format import template as repo_template
from restic_backup_report.templates.report.plaintext_base_format import template as base_template

class PlaintextReport(Report):


    def render(self) -> str:

        repos: list[str] = []
        for repo in self.repositories.keys():

            data: dict = {
                "repository_display_name": repo.display_name,
                "repository_name": repo.name
            }

            repos.append(repo_template.render(**data))

        return base_template.render({
            "repositories": repos
        })
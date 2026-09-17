from restic_backup_report.report.base_report import Report


class PlaintextReport(Report):


    def parse(self) -> str:
            return "Test"

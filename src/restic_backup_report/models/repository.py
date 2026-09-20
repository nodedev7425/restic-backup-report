from enum import Enum, auto


class ReportType(Enum):
    DAILY = auto()
    WEEKLY = auto()
    MONTHLY = auto()
    YEARLY = auto()


class BackupFrequency(Enum):
    DAILY = auto()
    WEEKLY = auto()
    MONTHLY = auto()
    YEARLY = auto()


class Repository:


    def __init__(self, name: str, display_name: str, path: str, password: str, report: ReportType, frequency: BackupFrequency, tolerance: int):
        self.name = name
        self.display_name = display_name
        self.path = path
        self.password = password

        self.report = report
        self.frequency = frequency
        self.tolerance = tolerance
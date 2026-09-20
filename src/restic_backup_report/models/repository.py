from dataclasses import dataclass
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


@dataclass(frozen=True)
class Repository:
    name: str
    display_name: str
    path: str
    password: str
    report: ReportType
    frequency: BackupFrequency
    tolerance: int
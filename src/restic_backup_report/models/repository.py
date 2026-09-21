from dataclasses import dataclass
from enum import StrEnum


class ReportType(StrEnum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class BackupFrequency(StrEnum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


@dataclass(frozen=True)
class Repository:
    name: str
    display_name: str
    path: str
    password: str
    report: ReportType
    frequency: BackupFrequency
    tolerance: int
from dataclasses import dataclass
from enum import Enum, auto


class UsageState(Enum):
    NONE = auto()
    WARNING = auto()
    CRITICAL = auto()


@dataclass
class StorageReport:


    success: bool = True
    path: str = ""
    folder_size: str = ""
    partition: str = ""
    partition_size: str = ""
    mountpoint: str = ""
    usage: float = 0.0
    usageState: UsageState = UsageState.NONE
from dataclasses import dataclass, field
from datetime import datetime

from restic_backup_report.models.snapshot_report import SnapshotReport


@dataclass
class RepositoryReport:

    
    success: bool = True
    incompatible: bool = False
    integrity: bool | None = None
    snapshots: dict[datetime, list[SnapshotReport]] = field(default_factory=dict)
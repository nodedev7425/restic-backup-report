from dataclasses import dataclass
from datetime import datetime

from restic_backup_report.models.snapshot import Snapshot


@dataclass
class SnapshotReport:


    relevant: bool = True
    snapshot: Snapshot = None
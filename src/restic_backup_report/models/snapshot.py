from dataclasses import dataclass

from datetime import datetime


@dataclass
class SnapshotSummary:
    backup_start: datetime
    backup_end: datetime
    files_new: int
    files_changed: int
    files_unmodified: int
    dirs_new: int
    dirs_changed: int
    dirs_unmodified: int
    data_blobs: int
    tree_blobs: int
    data_added: int
    data_added_packed: int
    total_files_processed: int
    total_bytes_processed: int


@dataclass
class Snapshot:
    time: datetime
    tree: str
    paths: list[str]
    hostname: str
    username: str
    uid: int
    gid: int
    program_version: str
    summary: SnapshotSummary
    id: str
    short_id: str

    @classmethod
    def from_dict(cls, data: dict) -> "Snapshot":
        return cls(
            time=datetime.fromisoformat(data["time"]),
            tree=data["tree"],
            paths=data["paths"],
            hostname=data["hostname"],
            username=data["username"],
            uid=data["uid"],
            gid=data["gid"],
            program_version=data["program_version"],
            summary=SnapshotSummary(
                backup_start=datetime.fromisoformat(
                    data["summary"]["backup_start"]
                ),
                backup_end=datetime.fromisoformat(
                    data["summary"]["backup_end"]
                ),
                files_new=data["summary"]["files_new"],
                files_changed=data["summary"]["files_changed"],
                files_unmodified=data["summary"]["files_unmodified"],
                dirs_new=data["summary"]["dirs_new"],
                dirs_changed=data["summary"]["dirs_changed"],
                dirs_unmodified=data["summary"]["dirs_unmodified"],
                data_blobs=data["summary"]["data_blobs"],
                tree_blobs=data["summary"]["tree_blobs"],
                data_added=data["summary"]["data_added"],
                data_added_packed=data["summary"]["data_added_packed"],
                total_files_processed=data["summary"]["total_files_processed"],
                total_bytes_processed=data["summary"]["total_bytes_processed"]
            ),
            id=data["id"],
            short_id=data["short_id"],
        )
    
import os

from restic_backup_report.utils.console import print_error


class MasterKeyError(Exception):
    pass


def get_master_key() -> str | None:
    path = os.environ.get("RESTIC_BACKUP_REPORT_MASTER_KEY_FILE")

    if not path:
        raise MasterKeyError(
            "RESTIC_BACKUP_REPORT_MASTER_KEY_FILE is not set."
        )

    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.readline().strip()
    except (FileNotFoundError, PermissionError, OSError) as exc:
        raise MasterKeyError(
            "RESTIC_BACKUP_REPORT_MASTER_KEY_FILE is not accessible: "
            f"{exc}"
        ) from exc
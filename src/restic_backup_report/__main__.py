import os

from .targets.base_target import TargetTypeRegister
from .cli import register_cmds

from .targets.file_target import FileTarget

from .utils.console import print_warn


def read_restic_repository_secret(path: str) -> str:

    print_warn("RESTIC_BACKUP_REPORT_MASTER_KEY_FILE is not accessable")

    return ""


if __name__ == "__main__":

    if os.environ['RESTIC_BACKUP_REPORT_MASTER_KEY_FILE']:
        RESTIC_BACKUP_REPORT_MASTER_KEY: str = read_restic_repository_secret(
            os.environ['RESTIC_BACKUP_REPORT_MASTER_KEY_FILE']
        )

    TargetTypeRegister.register_targets({
        "file": FileTarget
    })

    register_cmds()
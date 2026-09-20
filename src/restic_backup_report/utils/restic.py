from enum import Enum, auto
import subprocess
import shutil

from packaging.version import Version

from restic_backup_report.models.repository import Repository

from restic_backup_report.app_info import RESTIC_CLI_MIN_VERSION


class ResticError(Exception):
    pass


class ResticManager:


    @staticmethod
    def is_success(stdout: str) -> bool: 
        pass


    @staticmethod
    def get_cli_version() -> str:
        if shutil.which("restic") is None:
            raise ResticError("Restic not found")

        result = subprocess.run(
            ["restic", "version"],
            capture_output=True,
            text=True,
            check=True,
        )

        return result.stdout.split()[1]


    @staticmethod
    def is_cli_compatible() -> bool:
        try:
            cli_version = Version(ResticManager.get_cli_version())
        except ResticError:
            return False

        return cli_version >= Version(RESTIC_CLI_MIN_VERSION)


    @staticmethod
    def is_repo_compatible(repo: Repository) -> bool:
        return True


    @staticmethod
    def check_repo_integrity(repo: Repository, full = False) -> bool:
        return True
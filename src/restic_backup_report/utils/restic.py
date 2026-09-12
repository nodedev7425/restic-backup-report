import subprocess
import shutil

from packaging.version import Version

from restic_backup_report.app_info import RESTIC_CLI_MIN_VERSION


class ResticError(Exception):
    pass


class Repository:


    def __init__(self, name: str, path: str, password: str):
        self.name = name
        self.path = path
        self.password = password


class ResticManager:


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
        pass

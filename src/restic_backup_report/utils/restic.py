from enum import Enum, auto
import subprocess
import shutil

from packaging.version import Version

from restic_backup_report.app_info import RESTIC_CLI_MIN_VERSION


class ResticError(Exception):
    pass


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


class Repository:


    def __init__(self, name: str, path: str, password: str, report: ReportType, frequency: BackupFrequency, tolerance: int):
        self.__name = name
        self.__path = path
        self.__password = password

        self.__report = report
        self.__frequency = frequency
        self.__tolerance = tolerance


    def get_name(self):
        return self.__name


    def get_path(self):
        return self.__path


    def get_password(self):
        return self.__password


    def get_report(self):
        return self.__report


    def get_frequency(self):
        return self.__frequency


    def get_tolerance(self):
        return self.__tolerance


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

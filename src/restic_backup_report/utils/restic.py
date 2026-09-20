import os
import subprocess
import shutil
import json

from enum import IntEnum

from packaging.version import Version

from restic_backup_report.models.repository import Repository

from restic_backup_report.app_info import RESTIC_CLI_MIN_VERSION, RESTIC_REPO_MIN_VERSION


class ResticErrorCode(IntEnum):
    REPOSITORY_NOT_FOUND = 10
    WRONG_PASSWORD = 12


class ResticError(Exception):
    pass


class ResticManager:


    @staticmethod
    def check_result(stdout: str) -> dict:

        try:
            data = json.loads(stdout)
        except json.decoder.JSONDecodeError:
            raise ResticError("Unexpected response format")

        if ('message_type' in data) and (data['message_type'] == 'exit_error'):

            if ('code' in data) and (data['code'] == ResticErrorCode.REPOSITORY_NOT_FOUND):
                raise ResticError("Repository does not exist")

            if ('code' in data) and (data['code'] == ResticErrorCode.WRONG_PASSWORD):
                raise ResticError("Wrong password or no key found")

        return data


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

        env = None

        if repo.password is not None:
            env = os.environ.copy()
            env["RESTIC_PASSWORD"] = repo.password

        result = subprocess.run(
            ["restic", "-r", repo.path, "cat", "config", "--json"],
            capture_output=True,
            text=True,
            check=False,
            env=env
        )

        data = ResticManager.check_result(result.stdout)

        return data["version"] >= RESTIC_REPO_MIN_VERSION


    @staticmethod
    def check_repo_integrity(repo: Repository, full = False) -> bool:

        env = None

        if repo.password is not None:
            env = os.environ.copy()
            env["RESTIC_PASSWORD"] = repo.password

        cmd = ["restic", "-r", repo.path, "check", "--json"]

        if full:
            cmd.append("--read-data")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )

        data = ResticManager.check_result(result.stdout)

        return data.get("num_errors", 0) == 0
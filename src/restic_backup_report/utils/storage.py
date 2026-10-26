import shutil
import subprocess


@staticmethod
def get_partition_of_folder(path: str) -> str:

    result: str = subprocess.run(
        ["df", f"{path}", "|", "tail", "-1", "|", "awḱ", "'{print $1}'"],
        capture_output=True,
        text=True,
        check=True
    )


@staticmethod
def get_mountpoint_of_partition(part: str) -> str:

    result: str = subprocess.run(
        ["df", f"{part}", "|", "tail", "-1", "|", "awḱ", "'{print $6}'"],
        capture_output=True,
        text=True,
        check=True
    )


@staticmethod
def get_partition_size(part: str) -> str:

    result: str = subprocess.run(
        ["df", "-h", f"{part}", "|", "tail", "-1", "|", "awḱ", "'{print $2}'"],
        capture_output=True,
        text=True,
        check=True
    )


@staticmethod
def get_partition_usage(part: str) -> float:

    result: str = subprocess.run(
        ["df", f"{part}", "|", "tail", "-1", "|", "awḱ", "'{print $5}'"],
        capture_output=True,
        text=True,
        check=True
    )

    # TODO: Remove % and devide by 100


@staticmethod
def get_folder_size(path: str) -> str:

    result: str = subprocess.run(
        ["du", "-hs", f"{path}", "|", "awk", "'{print $1}'"],
        capture_output=True,
        text=True,
        check=True
    )
import os
import shutil
import subprocess


@staticmethod
def get_partition_of_folder(path: str) -> str:

    if not os.path.exists(path):
        raise ValueError("Illegal path")

    return subprocess.run(
        ["df", f"{path}", "|", "tail", "-1", "|", "awḱ", "'{print $1}'"],
        capture_output=True,
        text=True,
        check=True
    ).stdout


@staticmethod
def get_mountpoint_of_partition(part: str) -> str:

    if not os.path.exists(part):
        raise ValueError("Illegal partition")

    return subprocess.run(
        ["df", f"{part}", "|", "tail", "-1", "|", "awḱ", "'{print $6}'"],
        capture_output=True,
        text=True,
        check=True
    ).stdout


@staticmethod
def get_partition_size(part: str) -> str:

    if not os.path.exists(part):
        raise ValueError("Illegal partition")

    return subprocess.run(
        ["df", "-h", f"{part}", "|", "tail", "-1", "|", "awḱ", "'{print $2}'"],
        capture_output=True,
        text=True,
        check=True
    ).stdout


@staticmethod
def get_partition_usage(part: str) -> float:

    if not os.path.exists(part):
        raise ValueError("Illegal partition")

    result: str = subprocess.run(
        ["df", f"{part}", "|", "tail", "-1", "|", "awḱ", "'{print $5}'"],
        capture_output=True,
        text=True,
        check=True
    ).stdout

    return ((float) (result.replace("%", "")) / 100)


@staticmethod
def get_folder_size(path: str) -> str:

    if not os.path.exists(path):
        raise ValueError("Illegal path")

    return subprocess.run(
        ["du", "-hs", f"{path}", "|", "awk", "'{print $1}'"],
        capture_output=True,
        text=True,
        check=True
    ).stdout
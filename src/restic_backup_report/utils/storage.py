import os
import shutil
import subprocess


@staticmethod
def get_partition_of_folder(path: str) -> str:

    if not os.path.exists(path):
        raise ValueError("Illegal path")

    result: str = subprocess.run(
        ["df", path],
        capture_output=True,
        text=True,
        check=True
    ).stdout

    return result.splitlines()[-1].split()[0]

@staticmethod
def get_mountpoint_of_partition(part: str) -> str:

    if not os.path.exists(part):
        raise ValueError("Illegal partition")

    result: str = subprocess.run(
        ["df", part],
        capture_output=True,
        text=True,
        check=True
    ).stdout

    return result.splitlines()[-1].split()[5]


@staticmethod
def get_partition_size(part: str) -> str:

    if not os.path.exists(part):
        raise ValueError("Illegal partition")

    result: str = subprocess.run(
        ["df", "-h", part],
        capture_output=True,
        text=True,
        check=True
    ).stdout

    return result.splitlines()[-1].split()[1]


@staticmethod
def get_partition_usage(part: str) -> float:

    if not os.path.exists(part):
        raise ValueError("Illegal partition")

    result: str = subprocess.run(
        ["df", part],
        capture_output=True,
        text=True,
        check=True
    ).stdout

    result = result.splitlines()[-1].split()[4]

    return float(result.replace("%", "")) / 100


@staticmethod
def get_folder_size(path: str) -> str:

    if not os.path.exists(path):
        raise ValueError("Illegal path")

    result: str = subprocess.run(
        ["du", "-hs", path],
        capture_output=True,
        text=True,
        check=True
    ).stdout

    return result.split()[0]
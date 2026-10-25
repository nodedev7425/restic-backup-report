import shutil
import subprocess


@staticmethod
def get_partition_of_folder(path: str):

    result:str = subprocess.run(
        ["df", f"{path}"],
        capture_output=True,
        text=True,
        check=True,
    )

    result.split()


@staticmethod
def get_partition_size(part: str):
    pass


@staticmethod
def get_folder_size(path: str):
    pass
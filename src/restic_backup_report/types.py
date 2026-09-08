import argparse

import os


# Validation: argparse

def file_path(path):
    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_file:{path} is not a valid file") 


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


# Validation: questionary

def is_integer(value: str) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


def is_file(value: str) -> bool:
    return os.path.isfile(value)


def is_directory(value: str) -> bool:
    return os.path.isdir(value)
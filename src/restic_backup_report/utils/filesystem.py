import os


def is_writable(path: str) -> bool:
    if os.path.exists(path):
        return os.path.isfile(path) and os.access(path, os.W_OK)

    parent = os.path.dirname(os.path.abspath(path))
    return os.path.isdir(parent) and os.access(parent, os.W_OK)
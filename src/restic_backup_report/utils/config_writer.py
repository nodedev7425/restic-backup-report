import os
import yaml

from enum import Enum, auto

from restic_backup_report.utils.filesystem import is_writable


class ConfigSection(Enum):
    TARGET=auto()


class ConfigWriter:


    def __init__(self, path: str, generate = False) -> None:

        if not is_writable(path):
            raise PermissionError(f"Cannot write to {path}")

        self.path = path
        self.generate = generate


    def __write_new_target(self, name: str, type: str, yaml: dict):
        pass


    def save(self, section: ConfigSection, args: list[str], yaml: dict):

        match section: 
            case TARGET:
                self.__write_new_target(args[0], args[1], yaml)

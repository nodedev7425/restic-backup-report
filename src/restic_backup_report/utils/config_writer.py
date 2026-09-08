import os
import yaml

import restic_backup_report.app_info

from restic_backup_report.utils.filesystem import is_writable

from restic_backup_report.targets.base_target import Target


class ConfigWriter:


    def __init__(self, path: str) -> None:

        if not is_writable(path):
            raise PermissionError(f"Cannot write to {path}")

        self.path = path


    def __write_target(self, target: Target):
        pass


    def new(self):
        pass
    

    def add_target(self, target: Target) -> None:
        pass


    

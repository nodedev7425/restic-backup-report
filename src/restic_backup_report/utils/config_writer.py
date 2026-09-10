import os
import yaml
import secrets

from argon2 import PasswordHasher

from restic_backup_report.app_info import CONFIG_STANDARD

from restic_backup_report.utils.filesystem import is_writable

from restic_backup_report.targets.base_target import Target

from restic_backup_report.templates.config_template import template as config_template


class ConfigWriter:


    def __init__(self, path: str) -> None:

        if not is_writable(path):
            raise PermissionError(f"Cannot write to {path}")

        self.path = path


    def __write_target(self, target: Target):
        pass


    def new_config(self) -> str:

        ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)

        master_key = secrets.token_hex(32)
        hash_salt = secrets.token_hex(8)

        hashed_password = ph.hash(master_key, salt=str.encode(hash_salt))

        data = {
            "config_standard": CONFIG_STANDARD,
            "master_key_checksum": hashed_password,
            "master_key_checksum_salt": hash_salt,
        }

        rendered = config_template.render(**data)

        with open(self.path, "w") as f:
            f.write(rendered)

        return master_key
    

    def add_repository(self):
        pass


    def add_target(self, target: Target) -> None:
        pass


    

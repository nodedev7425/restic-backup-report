import base64
import os
import secrets

from ruamel.yaml import YAML

from argon2 import PasswordHasher

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from restic_backup_report.app_info import CONFIG_STANDARD

from restic_backup_report.utils.filesystem import is_writable

from restic_backup_report.targets.base_target import Target

from restic_backup_report.templates.config_template import template as config_template
from restic_backup_report.templates.repository_template import template as repository_template


class ConfigValidationError(Exception):
    pass


class ConfigWriter:


    def __init__(self, path: str) -> None:

        if not is_writable(path):
            raise PermissionError(f"Cannot write to {path}")

        self.path = path


    def is_secret_valid(self, master_key: str) -> None:
        # IF: Secret is None
        # IF: Secret is wrong
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
    

    def add_repository(self, master_key: str, name:str, path: str, password: str,
        report: str, frequency: str, tolerance: int):

        nonce = os.urandom(12)
        aesgcm = AESGCM(bytes.fromhex(master_key))

        encrypted_password = aesgcm.encrypt(
            nonce,
            password.encode("utf-8"),
            None,
        )

        data = {
            "repository_name": name,
            "repository_path": path,
            "repository_password": base64.b64encode(encrypted_password).decode("ascii"),
            "repository_password_nonce": base64.b64encode(nonce).decode("ascii"),
            "report_interval": report,
            "backup_frequency": frequency,
            "backup_tolerance": tolerance
        }

        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.indent(mapping=2, sequence=2, offset=0)
        yaml.width = 4096

        rendered = repository_template.render(**data)
        repository = yaml.load(rendered)

        with open(self.path, "r", encoding="utf-8") as f:
            config = yaml.load(f)

        if config is None:
            config = {}

        if "repositories" not in config:
            config["repositories"] = []
        config["repositories"].append(repository)

        with open(self.path, "w", encoding="utf-8") as f:
            yaml.dump(config, f)


    def add_target(self, target: Target) -> None:
        pass


    

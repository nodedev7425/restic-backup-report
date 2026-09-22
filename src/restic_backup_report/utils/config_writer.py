import base64
import os
import secrets

from ruamel.yaml import YAML

from argon2 import PasswordHasher

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from restic_backup_report.app_info import CONFIG_STANDARD

from restic_backup_report.models.general_config import GeneralConfig
from restic_backup_report.reports.base_report import ReportFormatRegister
from restic_backup_report.utils.filesystem import is_writable

from restic_backup_report.targets.base_target import Target, TargetTypeRegister

from src.restic_backup_report.templates.config.config_template import template as config_template
from src.restic_backup_report.templates.config.repository_template import template as repository_template
from src.restic_backup_report.templates.config.target_base_template import template as target_base_template

from restic_backup_report.utils.yaml import find_item, get_nested, get_parent, set_nested
from src.restic_backup_report.models.repository import Repository


class ConfigValidationError(Exception):
    pass


class ConfigWriter:


    def __init__(self, path: str) -> None:

        if not is_writable(path):
            raise PermissionError(f"Cannot write to {path}")

        self.path = path


    def _encrypt(self, value: str, master_key: str) -> tuple[str, str]:
        aesgcm = AESGCM(bytes.fromhex(master_key))
        nonce = os.urandom(12)

        ciphertext = aesgcm.encrypt(
            nonce,
            value.encode("utf-8"),
            None,
        )

        return (
            base64.b64encode(ciphertext).decode("ascii"),
            base64.b64encode(nonce).decode("ascii"),
        )


    def _decrypt(self, ciphertext: str, nonce: str, master_key: str,) -> str:
        aesgcm = AESGCM(bytes.fromhex(master_key))

        plaintext = aesgcm.decrypt(
            base64.b64decode(nonce),
            base64.b64decode(ciphertext),
            None,
        )

        return plaintext.decode("utf-8")


    """
        Global
    """    


    def is_secret_valid(self, master_key: str) -> bool:
        # IF: Secret is None
        # IF: Secret is wrong
        return True


    def new_config(self, general_config: GeneralConfig) -> str:

        ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)

        master_key = secrets.token_hex(32)
        hash_salt = secrets.token_hex(8)

        hashed_password = ph.hash(master_key, salt=str.encode(hash_salt))

        data = {
            "config_standard": CONFIG_STANDARD,
            "general_config": general_config,
            "master_key_checksum": hashed_password,
            "master_key_checksum_salt": hash_salt,
        }

        rendered = config_template.render(**data)

        with open(self.path, "w") as f:
            f.write(rendered)

        return master_key


    def read_general_config(self) -> GeneralConfig:

        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.indent(mapping=2, sequence=2, offset=0)
        yaml.width = 4096   

        with open(self.path, "r") as f:
            config = yaml.load(f)

        return GeneralConfig.from_dict(
            config["general"]
        )


    """
        Repository
    """    


    def has_repository(self, name: str) -> bool:
        return False


    def add_repository(self, master_key: str, name: str, display_name: str, path: str, password: str,
        report: str, frequency: str, tolerance: int):

        nonce = os.urandom(12)
        aesgcm = AESGCM(bytes.fromhex(master_key))

        encrypted_password, password_nonce = self._encrypt(
            password,
            master_key,
        )

        data = {
            "repository_name": name,
            "repository_display_name": display_name,
            "repository_path": path,
            "repository_password": encrypted_password,
            "repository_password_nonce": password_nonce,
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


    def get_all_repositories(self, master_key: str) -> list[Repository]:

        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.indent(mapping=2, sequence=2, offset=0)
        yaml.width = 4096

        with open(self.path, "r", encoding="utf-8") as f:
            config = yaml.load(f)
        
        if "repositories" not in config:
            raise ConfigValidationError("No repositories defined")

        repositories = list[Repository]()
        for repository in config["repositories"]:

            repositories.append(
                Repository(
                    name=repository["name"],
                    display_name=repository["display_name"],
                    path=repository["path"],
                    password=self._decrypt(
                        repository["password"],
                        repository["password_nonce"],
                        master_key
                    ),
                    report=repository["report"],
                    frequency=repository["backup"]["frequency"],
                    tolerance=repository["backup"]["tolerance"]
                )
            )

        return repositories


    """
        Target
    """    


    def has_target(self, name: str) -> bool:
        return False


    def add_target(self, target: Target, master_key: str) -> None:

        encrypted_fields = target.type.encrypted_fields() # type: ignore
        
        data = {
            "target_name": target.name,
            "target_type": TargetTypeRegister.get_name(target.type),
            "target_format": ReportFormatRegister.get_name(target.format),
        }

        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.indent(mapping=2, sequence=2, offset=0)
        yaml.width = 4096

        rendered = target_base_template.render(**data)

        target_root = yaml.load(rendered)
        target_config = yaml.load(target.to_yaml())

        for yaml_key in encrypted_fields.values():

            parent, field = get_parent(target_config, yaml_key)

            nonce = os.urandom(12)

            encrypted_value, nonce = self._encrypt(
                target_config[yaml_key],
                master_key
            )

            parent[f"{field}_nonce"] = encrypted_value
            parent[field] = nonce

        target_root["config"] = target_config

        with open(self.path, "r", encoding="utf-8") as f:
            config = yaml.load(f)

        if config is None:
            config = {}

        if "targets" not in config:
            config["targets"] = []
        config["targets"].append(target_root)

        with open(self.path, "w", encoding="utf-8") as f:
            yaml.dump(config, f)


    def get_target(self, name: str, master_key: str) -> Target:

        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.indent(mapping=2, sequence=2, offset=0)
        yaml.width = 4096

        with open(self.path, "r", encoding="utf-8") as f:
            config = yaml.load(f)
        
        if "targets" not in config:
            raise ConfigValidationError("No targets defined")

        yaml_target = find_item(
            config["targets"], "name", name
        )

        if yaml_target is None:
            raise KeyError(f"No target with the name '{name}' found")

        if not TargetTypeRegister.has(yaml_target["type"]):
            raise ConfigValidationError("Target type is unknown")
        target_type = TargetTypeRegister.get(yaml_target["type"])

        encrypted_fields = target_type.encrypted_fields() # type: ignore

        for yaml_key in encrypted_fields.values():

            parent, field = get_parent(yaml_target, yaml_key)

            parent[field] = self._decrypt(
                parent[field], 
                parent[f"{field}_nonce"], 
                master_key
            )

        return target_type(yaml_target)


        

    

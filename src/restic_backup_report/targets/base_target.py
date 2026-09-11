from abc import ABC, abstractmethod
from io import StringIO
from typing import Any

from ruamel.yaml import YAML

from restic_backup_report.types import is_directory, is_integer
from restic_backup_report.utils.console import InputType, request_attribute
from restic_backup_report.utils.filesystem import is_writable  


class Target(ABC):


    def __init__(self, definition: dict | None = None) -> None:
        if definition is None:
            self._inputs()
        else:
            self._create(definition)


    @abstractmethod
    def validator_schema(self) -> dict:
        raise NotImplementedError


    @abstractmethod
    def _inputs(self) -> None:
        self.name = request_attribute("name", InputType.TEXT)
        self.type = type(self)


    @abstractmethod
    def _create(self, inputs: dict) -> None:
        raise NotImplementedError


    @abstractmethod
    def send(self) -> None:
        raise NotImplementedError


    @abstractmethod
    def encrypted_fields(self) -> dict[str, str]:   # field name, yaml path
        raise NotImplementedError


    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError


    def to_yaml(self) -> str:
        yaml = YAML()
        stream = StringIO()
        yaml.dump(self.to_dict(), stream)
        return stream.getvalue()



class TargetTypeRegister:


    _target_types: dict[str, type[Target]] = {}


    @classmethod
    def register(cls, name: str, target: type[Target]) -> None:
        if name in cls._target_types:
            raise ValueError(f"Target type '{name}' is already registered")

        if target in cls._target_types.values():
            raise ValueError(
                f"Target type '{target.__name__}' is already registered"
            )

        cls._target_types[name] = target


    @classmethod
    def register_targets(cls, types: dict[str, type[Target]]):
        for key in types.keys():
            cls.register(key, types[key])


    @classmethod
    def get(cls, name: str) -> type[Target]:
        try:
            return cls._target_types[name]
        except KeyError:
            raise KeyError(f"Target type '{name}' is not registered")


    @classmethod
    def get_name(cls, target: type[Target]) -> str:
        for name, registered_target in cls._target_types.items():
            if registered_target is target:
                return name

        raise KeyError(
            f"Target type '{target.__name__}' is not registered"
        )


    @classmethod
    def names(cls) -> list[str]:
        return list(cls._target_types)


    @classmethod
    def has(cls, name: str) -> bool:
        return name in cls._target_types
import os

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Sequence

import questionary

from restic_backup_report.types import is_directory, is_integer
from restic_backup_report.utils.filesystem import is_writable  


class InputType(Enum):
    TEXT = auto()
    PASSWORD = auto()
    INTEGER = auto()
    BOOLEAN = auto()
    SELECT = auto()
    FILE = auto()
    DIRECTORY = auto()


class Target(ABC):

    @staticmethod
    def request_attribute(name: str, input_type: InputType,
        values: Sequence[str] | None = None) -> Any:

        match input_type:
            case InputType.TEXT:
                return questionary.text(f"{name}:").ask()

            case InputType.PASSWORD:
                return questionary.password(f"{name}:").ask()

            case InputType.INTEGER:
                return questionary.text(f"{name}:", validate=is_integer).ask()

            case InputType.BOOLEAN:
                return questionary.confirm(f"{name}:").ask()

            case InputType.SELECT:
                if values is None:
                    raise ValueError(
                        f"Input '{name}' requires values"
                    )

                return questionary.select(
                    f"{name}:",
                    choices=values,
                ).ask()

            case InputType.FILE:
                return questionary.path(f"{name}:", validate=is_writable).ask()

            case InputType.DIRECTORY:
                return questionary.path(f"{name}:", validate=is_directory).ask()

            case _:
                raise ValueError(f"Unsupported input type: {input_type}")


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
        self.name = Target.request_attribute("name", InputType.TEXT)
        self.type = type(self)

    @abstractmethod
    def _create(self, inputs: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def to_yaml(self) -> dict:
        raise NotImplementedError


class TargetTypeRegister:

    _target_types: dict[str, type[Target]] = {}

    @classmethod
    def register(cls, name: str, target: type[Target]) -> None:
        if name in cls._target_types:
            raise ValueError(f"Target type '{name}' is already registered")

        cls._target_types[name] = target

    @classmethod
    def get(cls, name: str) -> type[Target]:
        try:
            return cls._target_types[name]
        except KeyError:
            raise KeyError(f"Target type '{name}' is not registered")

    @classmethod
    def names(cls) -> list[str]:
        return list(cls._target_types.keys())

    @classmethod
    def has(cls, name: str) -> bool:
        return name in cls._target_types


def register_targets(types: dict[str, type[Target]]):
    for key in types.keys():
        TargetTypeRegister.register(key, types[key])
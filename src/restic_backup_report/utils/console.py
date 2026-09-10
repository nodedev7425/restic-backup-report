from enum import Enum, auto
from typing import Any, Sequence

import questionary

from rich import print

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


def print_error(error: str):
    print(f"FEHLER: {error}")


def print_warn(warn: str):
    print(f"WARN: {warn}")


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
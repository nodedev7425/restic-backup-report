from datetime import datetime
from enum import Enum, StrEnum, auto
from typing import Any, Sequence
from zoneinfo import ZoneInfo

import questionary

from rich import print

from tzlocal import get_localzone_name

from dateutil.rrule import rrule, SECONDLY, MINUTELY, HOURLY, DAILY, WEEKLY, MONTHLY, YEARLY

from restic_backup_report.types import is_directory, is_integer, is_timezone, is_unsigned_int
from restic_backup_report.utils.filesystem import is_writable


class InputType(Enum):
    TEXT = auto()
    PASSWORD = auto()
    INTEGER = auto()
    BOOLEAN = auto()
    SELECT = auto()
    FILE = auto()
    DIRECTORY = auto()
    RRULE = auto()
    TIMEZONE = auto()


class RRuleFreqInput(StrEnum):
    SECONDLY = "Secondly"
    MINUTELY = "Minutely"
    HOURLY = "Hourly"
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    YEARLY = "Yearly"


def print_error(error: str):
    print(f"FEHLER: {error}")


def print_warn(warn: str):
    print(f"WARN: {warn}")


def request_attribute(name: str, input_type: InputType,
    values: Sequence[str] | None = None, timezone: ZoneInfo | None = None) -> Any:

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

        case InputType.RRULE:

            print(f"In the following we will define '{name}':")

            confirmed = False
            while not confirmed:

                frequence = questionary.select(
                    "Please select the frequence of the repeating task:",
                    [el.value for el in RRuleFreqInput]
                ).ask()

                match frequence:
                    case RRuleFreqInput.SECONDLY:
                        frequence = SECONDLY
                    case RRuleFreqInput.MINUTELY:
                        frequence = MINUTELY
                    case RRuleFreqInput.HOURLY:
                        frequence = HOURLY
                    case RRuleFreqInput.DAILY:
                        frequence = DAILY
                    case RRuleFreqInput.WEEKLY:
                        frequence = WEEKLY
                    case RRuleFreqInput.MONTHLY:
                        frequence = MONTHLY
                    case RRuleFreqInput.YEARLY:
                        frequence = YEARLY

                if questionary.confirm(f"Do you want to set an interval, other then one?").ask():
                    interval = int(questionary.text(
                        "Enter the interval:", validate=is_unsigned_int
                    ).ask())
                else:
                   interval=1 

                # todo: Implement BYxxx

                recurrent = rrule(
                    dtstart=datetime.now(timezone),
                    freq=frequence, 
                    interval=interval
                )

                print(f"The recurrent rule: '{''.join(str(recurrent).splitlines())}'")

                confirmed = questionary.confirm(
                    "Do you want to confirm the values (yes), or enter different values (no)?"
                ).ask()

            return recurrent


            

        case InputType.TIMEZONE:
            return questionary.text(
                f"Choose a valid timezone for {name}\n"
                f"See the full list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones\n"
                f"e.g. your system is currently using: {get_localzone_name()}\n"
                f"> ",
                validate=is_timezone).ask()

        case _:
            raise ValueError(f"Unsupported input type: {input_type}")
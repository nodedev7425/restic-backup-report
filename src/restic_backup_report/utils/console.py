from datetime import date, time, datetime, timedelta
from enum import Enum, StrEnum, auto
from typing import Any, Sequence
from zoneinfo import ZoneInfo

import questionary

from rich import print

from tzlocal import get_localzone_name

from dateutil.rrule import rrule, SECONDLY, MINUTELY, HOURLY, DAILY, WEEKLY, MONTHLY, YEARLY

from restic_backup_report.types import is_day, is_directory, is_hour, is_integer, is_integer_between, is_minute, is_month, is_second, is_timezone, is_unsigned_int, is_year
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
    TIME = auto()
    DATE = auto()
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


def request_attribute(name: str, input_type: InputType, range: tuple[int, int] | None = None,
    values: Sequence[str] | None = None, timezone: ZoneInfo | None = None) -> Any:

    match input_type:
        case InputType.TEXT:
            return questionary.text(f"{name}:").ask()

        case InputType.PASSWORD:
            return questionary.password(f"{name}:").ask()

        case InputType.INTEGER:

            if range is None:
                return questionary.text(f"{name}:", validate=is_integer).ask()
            else:
                return questionary.text(f"{name}:", 
                    validate=lambda value: is_integer_between(value, range[0], range[1])
                ).ask()

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

            if timezone is None:
                raise ValueError("For 'RRule' is the timezone required.")

            print(f"Please configure the recurrence rule for '{name}':")

            confirmed = False
            while not confirmed:

                start_date: date = request_attribute(
                    "Select the start date",
                    InputType.DATE
                )

                start_time: time = request_attribute(
                    "Select the start time",
                    InputType.TIME,
                    timezone=timezone
                )

                dtstart = datetime.combine(start_date, start_time, tzinfo=timezone)

                if dtstart > datetime.now(tz=timezone):
                    print_warn("The next reports may be empty.")

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

                if questionary.confirm(f"Do you want to specify an interval other than 1?").ask():
                    interval = int(questionary.text(
                        "Enter the recurrence interval:", validate=is_unsigned_int
                    ).ask())
                else:
                   interval=1 

                # todo: Implement BYxxx

                recurrent = rrule(
                    dtstart=dtstart,
                    freq=frequence, 
                    interval=interval
                )

                print(f"The recurrent rule: '{''.join(str(recurrent).splitlines())}'")

                confirmed = questionary.confirm(
                    "Do you want to confirm these values?"
                ).ask()

            return recurrent


        case InputType.TIME:

            if timezone is None:
                raise ValueError("For 'Time' is the timezone required.")

            print(f"{name}\nPlease enter a time in the '{timezone.key}' timezone (not UTC unless specified).")

            confirmed = False
            while not confirmed:
             
                hour = int(questionary.text(
                    "Enter the hour (0-23):",
                    validate=is_hour
                ).ask())

                minute = int(questionary.text(
                      "Enter the minute (0-59):",
                      validate=is_minute          
                ).ask())

                second = int(questionary.text(
                    "Enter the second (0-59):",
                    validate=is_second         
                ).ask())

                dtime = time(
                    hour=hour,
                    minute=minute,
                    second=second
                )

                print(f"Selected time: {dtime}")

                confirmed = questionary.confirm(
                    "Do you want to confirm these values?"
                ).ask()

            return dtime

        case InputType.DATE:

            print(f"{name}\nPlease enter a date.")

            confirmed = False
            while not confirmed:
             
                day = int(questionary.text(
                    "Enter the day (1-31):",
                    validate=is_day
                ).ask())

                month = int(questionary.text(
                    "Enter the month (1-12):",
                    validate=is_month
                ).ask())

                year = int(questionary.text(
                    "Enter the year (e.g. 2026):",
                    validate=is_year
                ).ask())

                try:
                    ddate = datetime(
                        year=year,
                        month=month,
                        day=day
                    )
                except ValueError:
                    print_error("Invalid date. Please enter a valid calendar date.")
                    continue

                print(f"Selected date: {ddate}")

                confirmed = questionary.confirm(
                    "Do you want to confirm these values?"
                ).ask()

            return ddate.date()

        case InputType.TIMEZONE:
            return questionary.text(
                f"Choose a valid timezone for {name}\n"
                f"See the full list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones\n"
                f"e.g. your system is currently using: {get_localzone_name()}\n"
                f"> ",
                validate=is_timezone).ask()

        case _:
            raise ValueError(f"Unsupported input type: {input_type}")
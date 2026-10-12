import argparse

import os

from dateutil.rrule import rrule, rrulestr
from zoneinfo import ZoneInfo, available_timezones


# Validation: argparse

def file_path(path):
    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_file:{path} is not a valid file") 


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


# Validation: questionary

def is_integer(value: str) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


def is_unsigned_int(value: str) -> bool:
    return is_integer(value) and int(value) >= 0


def is_integer_between(value: str, min: int, max: int) -> bool | str:
    try:
        number = int(value)
        return True if (number >= min and number < max + 1) else f"Number has to in range {min}-{max}."
    except ValueError:
        return f"'{value}' is not a number."


def is_file(value: str) -> bool:
    return os.path.isfile(value)


def is_directory(value: str) -> bool:
    return os.path.isdir(value)


def is_timezone(value: str) -> bool | str:
    value = value.strip()
    if value in available_timezones():
        return True
    return f"'{value}' is not a valid timezone. Example: Europe/Berlin"


def is_day(value: str) -> bool | str:
    return is_integer_between(
        value, 1, 31
    )


def is_month(value: str) -> bool | str:
    return is_integer_between(
        value, 1, 12
    )


def is_year(value: str) -> bool | str:
    return is_integer_between(
        value,
        1900,
        9999
    )


def is_second(value: str) -> bool | str:
    return is_integer_between(
        value, 0, 59
    )


def is_minute(value: str) -> bool | str:
    return is_integer_between(
        value, 0, 59
    )


def is_hour(value: str) -> bool | str:
    return is_integer_between(
        value, 0, 23
    )


def restore_rrule_timezone(
    rule_string: str,
    timezone: ZoneInfo,
) -> rrule:
    """
    Restore the configured timezone of a serialized RRULE.

    The DTSTART is interpreted as local time in the configured timezone.
    All recurrence parameters are preserved.
    """

    parsed_rule = rrulestr(rule_string)

    # Restore the timezone of DTSTART.
    dtstart = parsed_rule._dtstart.replace(tzinfo=timezone)

    # Rebuild the rule with the original recurrence parameters.
    return rrule(
        freq=parsed_rule._freq,
        dtstart=dtstart,
        interval=parsed_rule._interval,
        wkst=parsed_rule._wkst,
        count=parsed_rule._count,
        until=parsed_rule._until,
        bysetpos=parsed_rule._bysetpos,
        bymonth=parsed_rule._bymonth,
        bymonthday=parsed_rule._bymonthday,
        byyearday=parsed_rule._byyearday,
        byeaster=parsed_rule._byeaster,
        byweekno=parsed_rule._byweekno,
        byweekday=parsed_rule._byweekday,
        byhour=parsed_rule._byhour,
        byminute=parsed_rule._byminute,
        bysecond=parsed_rule._bysecond
    )
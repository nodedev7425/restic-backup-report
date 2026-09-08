import os
import sys

import questionary

from restic_backup_report.utils.config_writer import ConfigWriter

from restic_backup_report.utils.console import print_error


def show(args) -> None:
    print("config: show")


def validate(args) -> None:
    print("config: validate")


def generate(args) -> None:
    try:
        if os.path.exists(args.config):
            if not questionary.confirm(
                "File already exists. Do you want to override its content?"
            ).ask():
                return

        writer = ConfigWriter(args.config)
        writer.new()

    except PermissionError as e:
        print_error(str(e))

    except Exception as e:
        print_error(
            f"Unexpected error. Please report this issue:\n{e}"
        )


def set_secret(args) -> None:
    print("config: set_secret")
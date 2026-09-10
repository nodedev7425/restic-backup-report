import os
import tempfile

import questionary

from restic_backup_report.__main__ import RESTIC_BACKUP_REPORT_MASTER_KEY

from restic_backup_report.utils.config_writer import ConfigValidationError, ConfigWriter

from restic_backup_report.utils.console import print_error, InputType, request_attribute


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
        master_key = writer.new_config()

        new_file, filename = tempfile.mkstemp()
        os.write(new_file, str.encode(master_key))
        os.close(new_file)

        print(
            "Master key generated successfully.\n"
            f"Temporare file: {filename}\n"
            "Store it securely; it cannot be recovered."
        )

    except PermissionError as e:
        print_error(str(e))

    except Exception as e:
        print_error(
            f"Unexpected error. Please report this issue:\n{e}"
        )


def add(args) -> None:
    try:
        writer = ConfigWriter(args.config)
        writer.can_change_config()

        name = request_attribute("repository name", InputType.TEXT)
        path = request_attribute("repository path", InputType.DIRECTORY)
        password = request_attribute("repository password", InputType.PASSWORD)
        report = request_attribute("repository name", InputType.SELECT, [])
        frequency = request_attribute("repository name", InputType.SELECT, [])
        tolerance = request_attribute("repository name", InputType.INTEGER)

        writer.add_repository(
            RESTIC_BACKUP_REPORT_MASTER_KEY, 
            name, path, password, report, frequency, tolerance
        )

    except ConfigValidationError as e:
        print_error(
            f"\n{e}"
        ) 
    except Exception as e:
        print_error(
            f"Unexpected error. Please report this issue:\n{e}"
        )


def remove(args) -> None:
    print("config: remove")
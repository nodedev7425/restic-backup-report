import os
import sys

from .app_info import RESTIC_CLI_MIN_VERSION

from .utils.restic import ResticManager

from .targets.base_target import TargetTypeRegister
from .formats.base_format import FormatRegister

from .cli import register_cmds

from .targets.file_target import FileTarget

from .formats.plaintext_format import PlaintextFormat

from .utils.console import print_error


def main() -> int:
    if not ResticManager.is_cli_compatible():
        print_error(
            f"This application requires Restic "
            f"{RESTIC_CLI_MIN_VERSION} or newer."
        )
        return 1

    FormatRegister.register_formats({
        "plaintext": PlaintextFormat
    })

    TargetTypeRegister.register_targets({
        "file": FileTarget
    })

    register_cmds()

    return 0


if __name__ == "__main__":
    sys.exit(main())

import os
import sys

from restic_backup_report.logging_config import setup_logging
from restic_backup_report.reports.html_report import HtmlReport

from .reports.base_report import ReportFormatRegister
from .reports.plaintext_report import PlaintextReport

from .app_info import RESTIC_CLI_MIN_VERSION

from .utils.restic import ResticManager

from .targets.base_target import TargetTypeRegister

from .cli import run_cli

from .targets.file_target import FileTarget
from .targets.email_target import EmailTarget

from .utils.console import print_error


def main() -> int:

    setup_logging(debug=os.environ.get("DEBUG", False))

    if not ResticManager.is_cli_compatible():
        print_error(
            f"This application requires Restic "
            f"{RESTIC_CLI_MIN_VERSION} or newer."
        )
        return 1

    ReportFormatRegister.register_formats({
        "plaintext": PlaintextReport,
        "html": HtmlReport
    })

    TargetTypeRegister.register_targets({
        "file": FileTarget,
        "email": EmailTarget
    })

    return run_cli()


if __name__ == "__main__":
    sys.exit(main())

import argparse

from typing import Any

from .types import file_path

from .commands.config import show, validate, generate, add, remove
from .commands.report import report
from .commands.target import setup, test

from .targets.base_target import TargetTypeRegister


def parse_args(parser: argparse.ArgumentParser) -> Any:

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    ## Command: config

    config_parser = subparsers.add_parser("config")

    config_subparsers = config_parser.add_subparsers(
        dest="config_command", 
        required=True
    )

    config_parser.add_argument(
        '-c', '--config',
        type=file_path,
        required=True
    )

    config_show_parser = config_subparsers.add_parser("show")
    config_show_parser.set_defaults(func=show)

    config_validate_parser = config_subparsers.add_parser("validate")
    config_validate_parser.set_defaults(func=validate)

    config_generate_parser = config_subparsers.add_parser("generate")
    config_generate_parser.set_defaults(func=generate)

    config_add_parser = config_subparsers.add_parser("add")
    config_add_parser.set_defaults(func=add)

    config_add_parser.add_argument(
        "add_type",
        choices=["repository", "storage"]
    )

    config_remove_parser = config_subparsers.add_parser("remove")
    config_remove_parser.set_defaults(func=remove)

    config_remove_parser.add_argument(
        "remove_type",
        choices=["repository", "storage"]
    )

    ## Command: report

    report_parser = subparsers.add_parser("report")
    report_parser.set_defaults(func=report)

    report_parser.add_argument(
        '-c', '--config',
        type=file_path,
        required=True
    )

    report_parser.add_argument(
        '-t', '--target',
        nargs = '+',
        required=True
    )

    report_parser.add_argument(
        '--silent',
        action='store_true'
    )

    ## Command: target

    target_parser = subparsers.add_parser("target")

    target_parser.add_argument(
        '-c', '--config',
        type=file_path,
        required=True
    )

    target_subparsers = target_parser.add_subparsers(
        dest="target_command", 
        required=True
    )

    target_setup_parser = target_subparsers.add_parser("setup")
    target_setup_parser.set_defaults(func=setup)

    target_setup_parser.add_argument(
        "target_type",
        choices=TargetTypeRegister.names()
    )

    target_test_parser = target_subparsers.add_parser("test")
    target_test_parser.set_defaults(func=test)

    target_test_parser.add_argument(
        '-t', '--target',
        required=True
    )

    return parser.parse_args()


def run_cli() -> int:
    parser = argparse.ArgumentParser(
        prog="restic-backup-report",
        description="Monitoring and reporting tool for Restic backups.",
    )

    try:
        args = parse_args(parser)
        return args.func(args) or 0
    except Exception:
        return 1

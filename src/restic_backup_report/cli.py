import argparse

from typing import Any

from .types import file_path

from .commands.config import show, validate, generate, set_secret
from .commands.report import report
from .commands.target import setup, test

from .targets.target import TargetTypeRegister


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

    config_set_secret_parser = config_subparsers.add_parser("set-secret")
    config_set_secret_parser.set_defaults(func=set_secret)

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
        choices=TargetTypeRegister.names(),
    )

    target_test_parser = target_subparsers.add_parser("test")
    target_test_parser.set_defaults(func=test)

    target_test_parser.add_argument(
        '-t', '--target',
        required=True
    )

    return parser.parse_args()


def register_cmds():

    parser = argparse.ArgumentParser(
        prog="restic-backup-report",
        description="Monitoring and reporting tool for Restic backups."
    )

    args = parse_args(parser)
    args.func(args)

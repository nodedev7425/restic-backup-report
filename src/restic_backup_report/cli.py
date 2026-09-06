import argparse

from .commands.help import help


def parse_args(parser: argparse.ArgumentParser) -> any:

    subparsers = parser.add_subparsers(dest="command", required=True)

    ## Command: Help

    report_parser = subparsers.add_parser("help")

    return parser.parse_args()


def main():

    parser = argparse.ArgumentParser(
        prog="restic-backup-report",
        description="Monitoring and reporting tool for Restic backups."
    )

    args = parse_args(parser)

    if args.command == "help":
        help()

from restic_backup_report.targets.base_target import Target, TargetTypeRegister

from restic_backup_report.utils.config_writer import ConfigWriter
from restic_backup_report.utils.console import print_error


def setup(args) -> None:

    target_type: type[Target] = TargetTypeRegister.get(args.target_type)
    target = target_type()

    try:
        writer = ConfigWriter(args.config)

        writer.add_target(target)

    except PermissionError as e:
        print_error(e.args[0])
    

def test(args) -> None:
    print("report")
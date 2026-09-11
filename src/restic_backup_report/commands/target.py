from restic_backup_report.env import get_master_key

from restic_backup_report.targets.base_target import Target, TargetTypeRegister

from restic_backup_report.utils.config_writer import ConfigValidationError, ConfigWriter
from restic_backup_report.utils.console import print_error


def setup(args) -> None:

    target_type: type[Target] = TargetTypeRegister.get(args.target_type)
    target = target_type()

    try:
        writer = ConfigWriter(args.config)

        if len(target.encrypted_fields()) > 0:
            master_key = get_master_key()
            writer.is_secret_valid(master_key) # type: ignore
        else:
            master_key = None

        if writer.has_target(target.name):
            raise ConfigValidationError("Target already exists")

        writer.add_target(target, master_key)

    except PermissionError as e:
        print_error(e.args[0])
    

def test(args) -> None:
    print("report")
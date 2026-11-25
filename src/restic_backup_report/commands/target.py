import traceback

from restic_backup_report.env import MasterKeyError, get_master_key

from restic_backup_report.errors.configuration_error import ConfigurationError
from restic_backup_report.targets.base_target import Target, TargetTypeRegister

from restic_backup_report.utils.config_writer import ConfigValidationError, ConfigWriter
from restic_backup_report.utils.console import print_error


def setup(args) -> None:

    target_type: type[Target] = TargetTypeRegister.get(args.target_type)
    target = target_type()

    writer = ConfigWriter(args.config)

    if len(target_type.encrypted_fields()) > 0: # type: ignore

        master_key = get_master_key()

        if not writer.is_secret_valid(master_key):
            raise MasterKeyError("Invalid Master Key")

    else:
        master_key = None

    if writer.has_target(target.name):
        raise ConfigValidationError("Target already exists")

    writer.add_target(target, master_key) # type: ignore
    

def test(args) -> None:
    print("report")
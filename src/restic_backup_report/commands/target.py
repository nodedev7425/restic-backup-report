from restic_backup_report.targets.target import Target, TargetTypeRegister


def setup(args) -> None:

    target_type: type[Target] = TargetTypeRegister.get(args.target_type)
    target = target_type()


def test(args) -> None:
    print("report")
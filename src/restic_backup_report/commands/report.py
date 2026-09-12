import threading
import time

from src.restic_backup_report.env import get_master_key
from src.restic_backup_report.utils.config_writer import ConfigWriter
from src.restic_backup_report.utils.console import print_error
from src.restic_backup_report.utils.reporter import Reporter


def report(args) -> None:
    try:
        writer = ConfigWriter(args.config)
        master_key = get_master_key()

        targets = []
        for target in args.target:
            targets.append(
                writer.get_target(target, master_key)
            )

        repositories = writer.get_all_repositories(master_key)

        if len(repositories) > 0:
            raise ValueError("No repositories in config found")

        reporter = Reporter(repositories, targets)

        reporter_thread = threading.Thread(
            target=reporter.run,
            daemon=True,
        )
        reporter_thread.start()

        while not reporter.done.is_set():
            if not args.silent:
                print("verbose")

            time.sleep(0.1)

        reporter_thread.join()
        
    except ValueError as e:
        print_error(
            f"\n{e}"
        )
    except Exception as e:
        pass
import threading
import time
from typing import Text

from rich.progress import BarColumn, Progress, TaskProgressColumn, Live, Group

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
            
        if not args.silent:
            status = Text("Starting...")

            progress = Progress(
                BarColumn(),
                TaskProgressColumn(),
            )

            task = progress.add_task(
                "Report",
                total=len(repositories),
            )

            with Live(
                Group(status, progress),
                refresh_per_second=10,
            ):
                while not reporter.done.wait(0.1):
                    pass

        else:
            reporter.done.wait()

        reporter_thread.join()
        
    except ValueError as e:
        print_error(
            f"\n{e}"
        )
    except Exception as e:
        pass
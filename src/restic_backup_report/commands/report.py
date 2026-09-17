from queue import Empty, Queue
import threading

from rich.progress import BarColumn, Progress, TaskID, TaskProgressColumn
from rich.live import Live
from rich.console import Group
from rich.text import Text

from src.restic_backup_report.env import get_master_key
from src.restic_backup_report.utils.config_writer import ConfigWriter
from src.restic_backup_report.utils.console import print_error
from src.restic_backup_report.utils.reporter import Reporter


def _process_events(log_queue: Queue[str], status: Text, progress_bar: Progress, task: TaskID, progress: float) -> None:
    while True:
        try:
            message = log_queue.get_nowait()
        except Empty:
            break

        status.plain = message
        progress_bar.advance(task, progress - progress_bar.tasks[task].completed)


def report(args) -> None:
    try:
        writer = ConfigWriter(args.config)
        master_key = get_master_key()

        targets = []
        for target in args.target:
            targets.append(
                writer.get_target(target, master_key) # type: ignore
            )

        repositories = writer.get_all_repositories(master_key) # type: ignore

        if len(repositories) == 0:
            raise ValueError("No repositories in config found")

        log_queue: Queue[str] | None = (
            Queue() if not args.silent else None
        )

        reporter = Reporter(repositories, targets, log_queue)

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
                    _process_events(
                        log_queue, # type: ignore
                        status,
                        progress,
                        task,
                    )

                _process_events(
                    log_queue, # type: ignore
                    status,
                    progress,
                    task,
                )
        else:
            reporter.done.wait()

        reporter_thread.join()
        
    except ValueError as e:
        print_error(
            f"\n{e}"
        )
    except Exception as e:
        pass
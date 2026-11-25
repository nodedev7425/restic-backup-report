import logging
from pathlib import Path


def setup_logging(
    log_file: str = "restic_backup_report.log",
    debug: bool = False
) -> None:

    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8")
        ],
        force=True
    )
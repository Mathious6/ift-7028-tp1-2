import logging
import sys
from typing import Optional


def configure_root_logger(level: int = logging.DEBUG) -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)


def setup_logger(name: Optional[str] = None) -> logging.Logger:

    return logging.getLogger(name)


configure_root_logger(level=logging.INFO)

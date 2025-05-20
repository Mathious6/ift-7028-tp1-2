import logging
import sys
from typing import Optional


def configure_root_logger(level: int = logging.DEBUG) -> None:
    """Configure the root logger with a single handler."""
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)


def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger with the specified name.
    The root logger should be configured first using configure_root_logger().
    """
    return logging.getLogger(name)


# DEBUG TIP: Use DEBUG level to see all the logs
configure_root_logger(level=logging.INFO)

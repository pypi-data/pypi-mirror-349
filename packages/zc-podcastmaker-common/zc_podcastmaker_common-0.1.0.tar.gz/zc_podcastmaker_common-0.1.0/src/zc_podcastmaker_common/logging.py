"""
Logging configuration utilities for PodcastMaker components.

This module provides standardized logging configuration that can be easily used
by all PodcastMaker components. It includes functions to configure logging with
customizable levels, formats, and handlers, as well as a helper function to get
a logger with the configured settings.
"""

import logging
import sys


def configure_logging(
    level: int = logging.INFO,
    log_format: str | None = None,
    date_format: str | None = None,
    handlers: list[logging.Handler] | None = None,
    propagate: bool = True,
) -> None:
    """
    Configure logging with customizable level, format, and handlers.

    Args:
        level: The logging level (default: logging.INFO)
        log_format: Custom log format string (default: uses a standard format with
            timestamp, level, and message)
        date_format: Custom date format string (default: ISO format)
        handlers: List of logging handlers to use (default: StreamHandler to stdout)
        propagate: Whether to propagate logs to parent loggers (default: True)

    Returns:
        None
    """
    # Set default format if not provided
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Set default date format if not provided
    if date_format is None:
        date_format = "%Y-%m-%d %H:%M:%S"

    # Set default handlers if not provided
    if handlers is None:
        handlers = [logging.StreamHandler(sys.stdout)]

    # Configure root logger
    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt=date_format,
        handlers=handlers,
    )

    # Set propagation for the zc_podcastmaker namespace
    logger = logging.getLogger("zc_podcastmaker")
    logger.propagate = propagate
    logger.setLevel(level)

    # Add handlers to the logger if they're not already there
    for handler in handlers:
        if handler not in logger.handlers:
            logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the configured settings.

    Args:
        name: The name of the logger, typically __name__ from the calling module

    Returns:
        logging.Logger: A configured logger instance
    """
    # If the name doesn't start with zc_podcastmaker, prefix it
    if not name.startswith("zc_podcastmaker"):
        name = f"zc_podcastmaker.{name}"

    return logging.getLogger(name)

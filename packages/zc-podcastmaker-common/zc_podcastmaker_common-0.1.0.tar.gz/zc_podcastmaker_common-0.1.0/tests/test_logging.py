"""
Tests for the logging module.
"""

import io
import logging

from zc_podcastmaker_common.logging import configure_logging, get_logger


def test_configure_logging_default() -> None:
    """Test configure_logging with default parameters."""
    # Reset the root logger to default state
    root = logging.getLogger()
    for handler in root.handlers[:]:
        root.removeHandler(handler)

    # Configure logging with defaults
    configure_logging()

    # Check that the root logger has the correct level
    assert root.level == logging.INFO

    # Check that there's at least one handler
    assert len(root.handlers) > 0

    # Check that the zc_podcastmaker logger is configured
    logger = logging.getLogger("zc_podcastmaker")
    assert logger.level == logging.INFO
    assert logger.propagate is True


def test_configure_logging_custom() -> None:
    """Test configure_logging with custom parameters."""
    # Reset the root logger to default state
    root = logging.getLogger()
    for handler in root.handlers[:]:
        root.removeHandler(handler)

    # Create a custom handler
    string_io = io.StringIO()
    custom_handler = logging.StreamHandler(string_io)

    # Configure logging with custom parameters
    custom_format = "%(levelname)s: %(message)s"
    configure_logging(
        level=logging.DEBUG,
        log_format=custom_format,
        date_format="%H:%M:%S",
        handlers=[custom_handler],
        propagate=False,
    )

    # Check that the root logger has the correct level
    assert root.level == logging.DEBUG

    # Check that the zc_podcastmaker logger is configured correctly
    logger = logging.getLogger("zc_podcastmaker")
    assert logger.level == logging.DEBUG
    assert logger.propagate is False

    # Test logging output format
    logger.debug("Test message")
    log_output = string_io.getvalue()
    assert "DEBUG: Test message" in log_output


def test_get_logger_with_prefix() -> None:
    """Test get_logger with a name that already has the prefix."""
    logger = get_logger("zc_podcastmaker.test")
    assert logger.name == "zc_podcastmaker.test"


def test_get_logger_without_prefix() -> None:
    """Test get_logger with a name that doesn't have the prefix."""
    logger = get_logger("test")
    assert logger.name == "zc_podcastmaker.test"


def test_logger_integration() -> None:
    """Test that loggers work together correctly."""
    # Reset the root logger to default state
    root = logging.getLogger()
    for handler in root.handlers[:]:
        root.removeHandler(handler)

    # Configure logging with a string IO handler to capture output
    string_io = io.StringIO()
    handler = logging.StreamHandler(string_io)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

    configure_logging(level=logging.INFO, handlers=[handler])

    # Get a logger and log a message
    logger = get_logger("test_module")
    logger.info("Test info message")
    logger.debug("This debug message should not appear")

    # Check the output
    log_output = string_io.getvalue()
    assert "INFO: Test info message" in log_output
    assert "This debug message should not appear" not in log_output

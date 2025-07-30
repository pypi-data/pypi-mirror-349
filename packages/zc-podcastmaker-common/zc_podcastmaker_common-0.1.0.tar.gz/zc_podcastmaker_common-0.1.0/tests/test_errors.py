"""
Tests for the error handling module.
"""

import logging
from unittest.mock import MagicMock, patch

import pytest

from zc_podcastmaker_common.errors import (
    ConfigError,
    ConfigNotFoundError,
    LLMError,
    MessageBusError,
    PodcastMakerError,
    StorageError,
    handle_error,
)


class TestCustomExceptions:
    """Tests for custom exception classes."""

    def test_base_exception(self):
        """Test the base PodcastMakerError exception."""
        error = PodcastMakerError("Test error message")
        assert str(error) == "Test error message"
        assert error.message == "Test error message"
        assert error.details == {}

    def test_base_exception_with_details(self):
        """Test the base PodcastMakerError exception with details."""
        details = {"key": "value"}
        error = PodcastMakerError("Test error message", details)
        assert str(error) == "Test error message"
        assert error.message == "Test error message"
        assert error.details == details

    def test_config_error(self):
        """Test the ConfigError exception."""
        error = ConfigError("Config error", "test.key")
        assert str(error) == "Config error"
        assert error.message == "Config error"
        assert error.details == {"config_key": "test.key"}

    def test_config_not_found_error(self):
        """Test the ConfigNotFoundError exception."""
        error = ConfigNotFoundError("Config not found", "missing.key")
        assert str(error) == "Config not found"
        assert error.message == "Config not found"
        assert error.details == {"config_key": "missing.key"}
        assert isinstance(error, ConfigError)
        assert isinstance(error, PodcastMakerError)

    def test_storage_error(self):
        """Test the StorageError exception."""
        error = StorageError("Storage error", bucket="test-bucket", key="test-key")
        assert str(error) == "Storage error"
        assert error.message == "Storage error"
        assert error.details == {"bucket": "test-bucket", "object_key": "test-key"}

    def test_llm_error(self):
        """Test the LLMError exception."""
        error = LLMError("LLM error", model_alias="claude", provider="anthropic")
        assert str(error) == "LLM error"
        assert error.message == "LLM error"
        assert error.details == {"model_alias": "claude", "provider": "anthropic"}

    def test_message_bus_error(self):
        """Test the MessageBusError exception."""
        error = MessageBusError(
            "Message bus error", queue="test-queue", exchange="test-exchange"
        )
        assert str(error) == "Message bus error"
        assert error.message == "Message bus error"
        assert error.details == {"queue": "test-queue", "exchange": "test-exchange"}


class TestHandleError:
    """Tests for the handle_error utility function."""

    @patch("zc_podcastmaker_common.errors.logger")
    def test_handle_error_logging(self, mock_logger):
        """Test that handle_error logs the error correctly."""
        original_error = ValueError("Original error")
        handle_error(
            func_name="test_func",
            error=original_error,
            raise_error=False,
            log_level=logging.WARNING,
        )

        # Check that the error was logged
        mock_logger.log.assert_called_once()
        args, kwargs = mock_logger.log.call_args
        assert args[0] == logging.WARNING
        assert "test_func: Original error" in args[1]

    def test_handle_error_raise(self):
        """Test that handle_error raises the correct exception."""
        original_error = ValueError("Original error")
        with pytest.raises(PodcastMakerError) as excinfo:
            handle_error(func_name="test_func", error=original_error, raise_error=True)

        assert "test_func: Original error" in str(excinfo.value)
        assert excinfo.value.details["original_error"] == "Original error"
        assert excinfo.value.details["error_type"] == "ValueError"

    def test_handle_error_custom_exception(self):
        """Test that handle_error raises the specified custom exception."""
        original_error = ValueError("Original error")
        with pytest.raises(ConfigError) as excinfo:
            handle_error(
                func_name="test_func",
                error=original_error,
                error_class=ConfigError,
                raise_error=True,
            )

        assert "test_func: Original error" in str(excinfo.value)
        assert isinstance(excinfo.value, ConfigError)

    def test_handle_error_return_value(self):
        """Test that handle_error returns the correct value when not raising."""
        original_error = ValueError("Original error")
        result = handle_error(
            func_name="test_func", error=original_error, raise_error=False
        )

        assert result["error"] is True
        assert "test_func: Original error" in result["message"]
        assert result["details"]["original_error"] == "Original error"

    def test_handle_error_default_return(self):
        """Test that handle_error returns the specified default value."""
        original_error = ValueError("Original error")
        default_return = {"status": "error"}
        result = handle_error(
            func_name="test_func",
            error=original_error,
            raise_error=False,
            default_return=default_return,
        )

        assert result is default_return

    @patch("zc_podcastmaker_common.errors.logger")
    def test_handle_error_retry_success(self, mock_logger):
        """Test that handle_error retries the function and succeeds."""
        original_error = ValueError("Original error")
        retry_func = MagicMock(return_value="success")

        result = handle_error(
            func_name="test_func",
            error=original_error,
            raise_error=False,
            retry_func=retry_func,
            max_retries=3,
        )

        assert result == "success"
        retry_func.assert_called_once()

    @patch("zc_podcastmaker_common.errors.logger")
    def test_handle_error_retry_failure(self, mock_logger):
        """Test that handle_error retries the function and fails."""
        original_error = ValueError("Original error")
        retry_error = ValueError("Retry error")
        retry_func = MagicMock(side_effect=retry_error)

        with pytest.raises(PodcastMakerError) as excinfo:
            handle_error(
                func_name="test_func",
                error=original_error,
                raise_error=True,
                retry_func=retry_func,
                max_retries=2,
            )

        assert retry_func.call_count == 2
        assert "Retry error" in str(excinfo.value)

    def test_handle_error_with_podcast_maker_error(self):
        """Test that handle_error re-raises PodcastMakerError instances."""
        original_error = ConfigError("Config error", "test.key")

        with pytest.raises(ConfigError) as excinfo:
            handle_error(func_name="test_func", error=original_error, raise_error=True)

        assert excinfo.value is original_error

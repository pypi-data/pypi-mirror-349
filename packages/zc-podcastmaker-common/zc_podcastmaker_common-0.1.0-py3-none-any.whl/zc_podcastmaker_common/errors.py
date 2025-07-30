"""
Error Handling Module
"""

import logging
import traceback
from collections.abc import Callable
from typing import Any

# Set up logging
logger = logging.getLogger(__name__)


class PodcastMakerError(Exception):
    """Base exception class for all podcast maker errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)


class ConfigError(PodcastMakerError):
    """Exception raised for errors related to configuration."""

    def __init__(
        self,
        message: str,
        config_key: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        error_details = details or {}
        if config_key and "config_key" not in error_details:
            error_details["config_key"] = config_key
        super().__init__(message, error_details)


class ConfigNotFoundError(ConfigError):
    """Exception raised when a required configuration value is not found."""

    pass


class ConfigValidationError(ConfigError):
    """Exception raised when configuration validation fails."""

    pass


class StorageError(PodcastMakerError):
    """Exception raised for errors related to object storage operations."""

    def __init__(
        self,
        message: str,
        bucket: str | None = None,
        key: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        error_details = details or {}
        if bucket:
            error_details["bucket"] = bucket
        if key:
            error_details["object_key"] = key
        super().__init__(message, error_details)


class StorageUploadError(StorageError):
    """Exception raised when an upload to object storage fails."""

    pass


class StorageDownloadError(StorageError):
    """Exception raised when a download from object storage fails."""

    pass


class StorageNotFoundError(StorageError):
    """Exception raised when an object is not found in storage."""

    pass


class LLMError(PodcastMakerError):
    """Exception raised for errors related to language model operations."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        model_alias: str | None = None,
        provider: str | None = None,
    ):
        error_details = details or {}
        if model_alias:
            error_details["model_alias"] = model_alias
        if provider:
            error_details["provider"] = provider
        super().__init__(message, error_details)


class LLMAuthenticationError(LLMError):
    """Exception raised when authentication with the LLM provider fails."""

    pass


class LLMRateLimitError(LLMError):
    """Exception raised when the LLM provider rate limit is exceeded."""

    pass


class LLMResponseError(LLMError):
    """Exception raised when there's an error in the LLM response."""

    pass


class MessageBusError(PodcastMakerError):
    """Exception raised for errors related to message bus operations."""

    def __init__(
        self,
        message: str,
        queue: str | None = None,
        exchange: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        error_details = details or {}
        if queue:
            error_details["queue"] = queue
        if exchange:
            error_details["exchange"] = exchange
        super().__init__(message, error_details)


class MessageBusConnectionError(MessageBusError):
    """Exception raised when connection to the message bus fails."""

    pass


class MessageBusPublishError(MessageBusError):
    """Exception raised when publishing a message fails."""

    pass


class MessageBusConsumeError(MessageBusError):
    """Exception raised when consuming a message fails."""

    pass


def handle_error(
    func_name: str,
    error: Exception,
    error_class: type[PodcastMakerError] = PodcastMakerError,
    message: str | None = None,
    log_level: int = logging.ERROR,
    raise_error: bool = True,
    details: dict[str, Any] | None = None,
    default_return: Any = None,
    retry_func: Callable | None = None,
    max_retries: int = 3,
) -> Any:
    """
    Handle an error with standardized logging and optional error raising.
    """
    error_message = message or str(error)
    full_message = f"{func_name}: {error_message}"

    # Initialize error_details with the passed 'details' or an empty dict
    error_details = details.copy() if details is not None else {}

    # Add standard fields, potentially overwriting if they were in 'details'
    error_details["original_error"] = str(error)
    error_details["error_type"] = type(error).__name__

    tb_str = traceback.format_exc()
    error_details["traceback"] = tb_str

    log_message = f"{full_message} | Details: {error_details}"
    logger.log(log_level, log_message)

    if retry_func and max_retries > 0:
        try:
            logger.info(f"Retrying function {func_name} ({max_retries} attempts left)")
            return retry_func()
        except Exception as retry_error:
            return handle_error(
                func_name=func_name,
                error=retry_error,
                error_class=error_class,
                message=message,  # Use original message for retried error
                log_level=log_level,
                raise_error=raise_error,
                details=details,  # Pass original details for retry context
                default_return=default_return,
                retry_func=retry_func,
                max_retries=max_retries - 1,
            )

    if raise_error:
        if isinstance(error, PodcastMakerError):
            # Si hay una prueba que espera que el error lanzado sea exactamente el mismo
            # objeto que se pasó, debemos simplemente relanzar el error original tal
            # cual
            raise error
        else:
            raise error_class(full_message, error_details) from error

    return (
        default_return
        if default_return is not None
        else {"error": True, "message": full_message, "details": error_details}
    )

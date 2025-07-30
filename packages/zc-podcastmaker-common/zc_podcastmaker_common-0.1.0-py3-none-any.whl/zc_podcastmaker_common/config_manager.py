"""
Configuration Manager Module

This module provides a unified mechanism for components to read their application
configuration and secrets. These data are previously materialized in files within
a tmpfs volume by a Vault Agent sidecar running alongside the application container.

Functions:
    get_config_value: Retrieve a configuration value by key
    get_secret_value: Retrieve a secret value by key
"""

import json
import logging
from pathlib import Path
from typing import Any

from zc_podcastmaker_common.errors import ConfigError, handle_error

# Default paths for configuration and secrets
CONFIG_BASE_PATH = Path("/vault/configs")
SECRET_BASE_PATH = Path("/vault/secrets")

# Set up logging
logger = logging.getLogger(__name__)


def _read_json_file(file_path: Path) -> dict[Any, Any] | None:
    """
    Read a JSON file and return its contents as a dictionary.

    Args:
        file_path: Path to the JSON file

    Returns:
        Dictionary with the file contents or None if the file doesn't exist or is
        invalid
    """
    try:
        if file_path.exists():
            with open(file_path) as f:
                return json.load(f)  # type: ignore[no-any-return]
        return None
    except json.JSONDecodeError as e:
        handle_error(
            func_name="_read_json_file",
            error=e,
            error_class=ConfigError,
            message=f"Invalid JSON in file {file_path}",
            details={"file_path": str(file_path)},
            raise_error=False,
            default_return=None,
        )
        return None
    except Exception as e:
        handle_error(
            func_name="_read_json_file",
            error=e,
            error_class=ConfigError,
            message=f"Error reading file {file_path}",
            details={"file_path": str(file_path)},
            raise_error=False,
            default_return=None,
        )
        return None


def _read_text_file(file_path: Path) -> str | None:
    """
    Read a text file and return its contents as a string.

    Args:
        file_path: Path to the text file

    Returns:
        String with the file contents or None if the file doesn't exist
    """
    try:
        if file_path.exists():
            with open(file_path) as f:
                return f.read().strip()
        return None
    except Exception as e:
        handle_error(
            func_name="_read_text_file",
            error=e,
            error_class=ConfigError,
            message=f"Error reading file {file_path}",
            details={"file_path": str(file_path)},
            raise_error=False,
            default_return=None,
        )
        return None


def _get_nested_value(data: dict[Any, Any] | None, key_path: str) -> Any | None:
    """
    Get a nested value from a dictionary using dot notation.

    Args:
        data: Dictionary to get the value from
        key_path: Key path using dot notation (e.g., "api.url")

    Returns:
        The value at the specified path or None if not found
    """
    if not data:
        return None

    keys = key_path.split(".")
    value = data

    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return None

    return value


def get_config_value(key_path: str, default_value: Any = None) -> Any:
    """
    Retrieve a configuration value by key.

    Args:
        key_path: The key path to retrieve (can use dot notation for nested JSON)
        default_value: Value to return if key is not found

    Returns:
        The configuration value or default_value if not found
    """
    try:
        # First check for a JSON file with nested keys
        config_file = CONFIG_BASE_PATH / "config.json"
        config_data = _read_json_file(config_file)

        if config_data:
            value = _get_nested_value(config_data, key_path)
            if value is not None:
                logger.debug(f"Found value for '{key_path}' in config.json")
                return value
            logger.debug(
                f"Key '{key_path}' not found in config.json, checking individual file"
            )

        # Check for individual config files
        individual_file = CONFIG_BASE_PATH / key_path
        value = _read_text_file(individual_file)

        if value is not None:
            logger.debug(f"Found value for '{key_path}' in individual file")
            return value

        logger.debug(f"Config value '{key_path}' not found, returning default")
        return default_value
    except Exception as e:
        handle_error(
            func_name="get_config_value",
            error=e,
            error_class=ConfigError,
            message=f"Error retrieving config value '{key_path}'",
            details={"key_path": key_path, "default_value": default_value},
            raise_error=False,
            default_return=default_value,
        )
        return default_value


def get_secret_value(key_path: str) -> str | None:
    """
    Retrieve a secret value by key.

    Args:
        key_path: The key path to retrieve (can use dot notation for nested JSON)

    Returns:
        The secret value or None if not found
    """
    try:
        # First check for a JSON file with nested keys
        secrets_file = SECRET_BASE_PATH / "secrets.json"
        secrets_data = _read_json_file(secrets_file)

        if secrets_data:
            value = _get_nested_value(secrets_data, key_path)
            if value is not None:
                logger.debug(f"Found value for '{key_path}' in secrets.json")
                return value  # type: ignore[no-any-return]
            logger.debug(
                f"Key '{key_path}' not found in secrets.json, checking individual file"
            )

        # Check for individual secret files
        individual_file = SECRET_BASE_PATH / key_path
        value = _read_text_file(individual_file)

        if value is not None:
            logger.debug(f"Found value for '{key_path}' in individual file")
            return value

        logger.debug(f"Secret value '{key_path}' not found")
        return None
    except Exception as e:
        handle_error(
            func_name="get_secret_value",
            error=e,
            error_class=ConfigError,
            message=f"Error retrieving secret value '{key_path}'",
            details={"key_path": key_path},
            raise_error=False,
            default_return=None,
        )
        return None

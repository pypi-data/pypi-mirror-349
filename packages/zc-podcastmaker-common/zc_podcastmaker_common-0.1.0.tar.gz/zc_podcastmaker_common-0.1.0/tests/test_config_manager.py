"""
Tests for the config_manager module.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

from zc_podcastmaker_common.config_manager import (
    CONFIG_BASE_PATH,
    SECRET_BASE_PATH,
    _get_nested_value,
    _read_json_file,
    _read_text_file,
    get_config_value,
    get_secret_value,
)


class CustomMockOpen:
    """Custom mock for open() that can return different values for different calls."""

    def __init__(self, read_data):
        self.read_data = read_data
        self.mock = mock_open(read_data=read_data)

    def __call__(self, *args, **kwargs):
        return self.mock(*args, **kwargs)

    def set_read_data(self, read_data):
        """Set the data to be returned by the mock."""
        self.read_data = read_data
        self.mock.return_value.read.return_value = read_data


class TestConfigManager:
    """Tests for the config_manager module."""

    def test_get_nested_value(self) -> None:
        """Test getting a nested value from a dictionary."""
        # Test data
        data = {"api": {"url": "http://example.com", "version": "1.0"}}

        # Test getting a value that exists
        result = _get_nested_value(data, "api.url")
        assert result == "http://example.com"

        # Test getting a value that doesn't exist
        result = _get_nested_value(data, "api.key")
        assert result is None

        # Test with empty data
        result = _get_nested_value(None, "api.url")
        assert result is None

    @patch("zc_podcastmaker_common.config_manager._read_json_file")
    @patch("zc_podcastmaker_common.config_manager._read_text_file")
    def test_get_config_value_from_json(
        self, mock_read_text: MagicMock, mock_read_json: MagicMock
    ) -> None:
        """Test getting a config value from a JSON file."""
        # Mock the _read_json_file function to return a dictionary
        mock_read_json.return_value = {"api": {"url": "http://example.com"}}
        mock_read_text.return_value = None

        # Test getting a value that exists
        result = get_config_value("api.url")
        assert result == "http://example.com"

        # Test getting a value that doesn't exist
        result = get_config_value("api.key", "default_key")
        assert result == "default_key"

        # Verify the functions were called with the correct arguments
        mock_read_json.assert_called_with(CONFIG_BASE_PATH / "config.json")

    @patch("zc_podcastmaker_common.config_manager._read_json_file")
    @patch("zc_podcastmaker_common.config_manager._read_text_file")
    def test_get_config_value_from_file(
        self, mock_read_text: MagicMock, mock_read_json: MagicMock
    ) -> None:
        """Test getting a config value from an individual file."""
        # Mock the functions to simulate a missing JSON file but an existing
        # individual file
        mock_read_json.return_value = None
        mock_read_text.return_value = "http://example.com"

        result = get_config_value("api.url")
        assert result == "http://example.com"

        # Verify the functions were called with the correct arguments
        mock_read_json.assert_called_with(CONFIG_BASE_PATH / "config.json")
        mock_read_text.assert_called_with(CONFIG_BASE_PATH / "api.url")

    @patch("zc_podcastmaker_common.config_manager._read_json_file")
    @patch("zc_podcastmaker_common.config_manager._read_text_file")
    def test_get_config_value_not_found(
        self, mock_read_text: MagicMock, mock_read_json: MagicMock
    ) -> None:
        """Test getting a config value that doesn't exist."""
        # Mock the functions to simulate missing files
        mock_read_json.return_value = None
        mock_read_text.return_value = None

        # Should return the default value
        result = get_config_value("api.url", "default_url")
        assert result == "default_url"

        # Should return None if no default is provided
        result = get_config_value("api.url")
        assert result is None

    @patch("zc_podcastmaker_common.config_manager._read_json_file")
    def test_get_config_value_exception(self, mock_read_json: MagicMock) -> None:
        """Test handling of exceptions when retrieving config value."""
        # Mock the function to raise an exception
        mock_read_json.side_effect = Exception("Test exception")

        # Should return the default value when an exception occurs
        result = get_config_value("api.url", "default_url")
        assert result == "default_url"

    @patch("zc_podcastmaker_common.config_manager._read_json_file")
    @patch("zc_podcastmaker_common.config_manager._read_text_file")
    def test_get_secret_value_from_json(
        self, mock_read_text: MagicMock, mock_read_json: MagicMock
    ) -> None:
        """Test getting a secret value from a JSON file."""
        # Mock the _read_json_file function to return a dictionary
        mock_read_json.return_value = {"api": {"key": "secret_api_key"}}
        mock_read_text.return_value = None

        # Test getting a value that exists
        result = get_secret_value("api.key")
        assert result == "secret_api_key"

        # Test getting a value that doesn't exist
        result = get_secret_value("api.token")
        assert result is None

        # Verify the functions were called with the correct arguments
        mock_read_json.assert_called_with(SECRET_BASE_PATH / "secrets.json")

    @patch("zc_podcastmaker_common.config_manager._read_json_file")
    @patch("zc_podcastmaker_common.config_manager._read_text_file")
    def test_get_secret_value_from_file(
        self, mock_read_text: MagicMock, mock_read_json: MagicMock
    ) -> None:
        """Test getting a secret value from an individual file."""
        # Mock the functions to simulate a missing JSON file but an existing
        # individual file
        mock_read_json.return_value = None
        mock_read_text.return_value = "secret_api_key"

        result = get_secret_value("api.key")
        assert result == "secret_api_key"

        # Verify the functions were called with the correct arguments
        mock_read_json.assert_called_with(SECRET_BASE_PATH / "secrets.json")
        mock_read_text.assert_called_with(SECRET_BASE_PATH / "api.key")

    @patch("zc_podcastmaker_common.config_manager._read_json_file")
    @patch("zc_podcastmaker_common.config_manager._read_text_file")
    def test_get_secret_value_not_found(
        self, mock_read_text: MagicMock, mock_read_json: MagicMock
    ) -> None:
        """Test getting a secret value that doesn't exist."""
        # Mock the functions to simulate missing files
        mock_read_json.return_value = None
        mock_read_text.return_value = None

        result = get_secret_value("api.key")
        assert result is None

    @patch("zc_podcastmaker_common.config_manager._read_json_file")
    def test_get_secret_value_exception(self, mock_read_json: MagicMock) -> None:
        """Test handling of exceptions when retrieving secret value."""
        # Mock the function to raise an exception
        mock_read_json.side_effect = Exception("Test exception")

        result = get_secret_value("api.key")
        assert result is None

    @patch("pathlib.Path.exists")
    @patch(
        "builtins.open", new_callable=mock_open, read_data=json.dumps({"test": "value"})
    )
    def test_read_json_file_success(
        self, mock_file: MagicMock, mock_exists: MagicMock
    ) -> None:
        """Test reading a JSON file successfully."""
        mock_exists.return_value = True

        result = _read_json_file(Path("/tmp/test.json"))
        assert result == {"test": "value"}

    @patch("pathlib.Path.exists")
    def test_read_json_file_not_found(self, mock_exists: MagicMock) -> None:
        """Test reading a JSON file that doesn't exist."""
        mock_exists.return_value = False

        result = _read_json_file(Path("/tmp/test.json"))
        assert result is None

    @patch("pathlib.Path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    def test_read_json_file_invalid_json(
        self, mock_file: MagicMock, mock_exists: MagicMock
    ) -> None:
        """Test reading an invalid JSON file."""
        mock_exists.return_value = True

        result = _read_json_file(Path("/tmp/test.json"))
        assert result is None

    @patch("pathlib.Path.exists")
    @patch("builtins.open")
    def test_read_json_file_exception(
        self, mock_file: MagicMock, mock_exists: MagicMock
    ) -> None:
        """Test handling exceptions when reading a JSON file."""
        mock_exists.return_value = True
        mock_file.side_effect = Exception("Test exception")

        result = _read_json_file(Path("/tmp/test.json"))
        assert result is None

    @patch("pathlib.Path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="test value")
    def test_read_text_file_success(
        self, mock_file: MagicMock, mock_exists: MagicMock
    ) -> None:
        """Test reading a text file successfully."""
        mock_exists.return_value = True

        result = _read_text_file(Path("/tmp/test.txt"))
        assert result == "test value"

    @patch("pathlib.Path.exists")
    def test_read_text_file_not_found(self, mock_exists: MagicMock) -> None:
        """Test reading a text file that doesn't exist."""
        mock_exists.return_value = False

        result = _read_text_file(Path("/tmp/test.txt"))
        assert result is None

    @patch("pathlib.Path.exists")
    @patch("builtins.open")
    def test_read_text_file_exception(
        self, mock_file: MagicMock, mock_exists: MagicMock
    ) -> None:
        """Test handling exceptions when reading a text file."""
        mock_exists.return_value = True
        mock_file.side_effect = Exception("Test exception")

        result = _read_text_file(Path("/tmp/test.txt"))
        assert result is None

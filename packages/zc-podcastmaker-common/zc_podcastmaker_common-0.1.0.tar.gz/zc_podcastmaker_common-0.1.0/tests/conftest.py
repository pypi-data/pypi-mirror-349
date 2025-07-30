"""
Common test fixtures and utilities for all test modules.
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_config_values():
    """
    Fixture to mock config values.

    Returns a function that can be used to set up mocked config values.
    """

    def _config_values(values_dict):
        def mock_get_config_value(key, default=None):
            return values_dict.get(key, default)

        return mock_get_config_value

    return _config_values


@pytest.fixture
def mock_secret_values():
    """
    Fixture to mock secret values.

    Returns a function that can be used to set up mocked secret values.
    """

    def _secret_values(values_dict):
        def mock_get_secret_value(key):
            return values_dict.get(key)

        return mock_get_secret_value

    return _secret_values


@pytest.fixture
def mock_s3_client():
    """
    Fixture to create a mocked S3 client.
    """
    with patch("boto3.client") as mock_client:
        s3_client = MagicMock()
        mock_client.return_value = s3_client
        yield s3_client


@pytest.fixture
def mock_rabbitmq_connection():
    """
    Fixture to create a mocked RabbitMQ connection.
    """
    with patch(
        "zc_podcastmaker_common.message_bus_client._get_rabbitmq_connection"
    ) as mock_get_connection:
        connection = MagicMock()
        channel = MagicMock()
        connection.channel.return_value = channel
        mock_get_connection.return_value = connection
        yield connection, channel


@pytest.fixture
def mock_anthropic_client():
    """
    Fixture to create a mocked Anthropic client.
    """
    with patch("anthropic.Anthropic") as mock_client:
        client = MagicMock()
        messages = MagicMock()
        client.messages = messages
        mock_client.return_value = client

        # Set up the response structure
        message_response = MagicMock()
        content_item = MagicMock()
        content_item.text = "Mocked response text"
        message_response.content = [content_item]
        messages.create.return_value = message_response

        yield client


@pytest.fixture
def temp_file():
    """
    Fixture to create a temporary file.

    Returns a tuple of (file_path, file_content).
    """
    content = "Test file content"
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(content.encode("utf-8"))
        temp_path = temp.name

    yield Path(temp_path), content

    # Cleanup
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def temp_json_file():
    """
    Fixture to create a temporary JSON file.

    Returns a tuple of (file_path, file_content as dict).
    """
    content = {"key": "value", "nested": {"inner_key": "inner_value"}}
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp:
        temp.write(json.dumps(content).encode("utf-8"))
        temp_path = temp.name

    yield Path(temp_path), content

    # Cleanup
    Path(temp_path).unlink(missing_ok=True)

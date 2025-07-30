"""
Tests for the message_bus_client module.
"""

import json
from unittest.mock import MagicMock, patch

import pika
import pytest

from zc_podcastmaker_common.errors import MessageBusConsumeError
from zc_podcastmaker_common.message_bus_client import (
    MessageConsumer,
    _get_rabbitmq_connection,
    create_consumer,
    publish_message,
)


class TestMessageBusClient:
    """Tests for the message_bus_client module."""

    @patch("zc_podcastmaker_common.message_bus_client.get_config_value")
    @patch("zc_podcastmaker_common.message_bus_client.get_secret_value")
    @patch("pika.ConnectionParameters")
    @patch("pika.PlainCredentials")
    @patch("pika.BlockingConnection")
    def test_get_rabbitmq_connection_with_credentials(
        self,
        mock_blocking_connection: MagicMock,
        mock_credentials: MagicMock,
        mock_parameters: MagicMock,
        mock_get_secret_value: MagicMock,
        mock_get_config_value: MagicMock,
    ) -> None:
        """Test creating a RabbitMQ connection with credentials."""
        # Mock configuration values
        mock_get_config_value.side_effect = lambda key, default: {
            "rabbitmq.host": "rabbitmq.example.com",
            "rabbitmq.port": 5672,
            "rabbitmq.virtual_host": "/test",
        }.get(key, default)

        # Mock secret values
        mock_get_secret_value.side_effect = lambda key: {
            "rabbitmq.username": "test_user",
            "rabbitmq.password": "test_password",
        }.get(key)

        # Mock credentials and connection
        mock_creds = MagicMock()
        mock_credentials.return_value = mock_creds
        mock_params = MagicMock()
        mock_parameters.return_value = mock_params
        mock_conn = MagicMock()
        mock_blocking_connection.return_value = mock_conn

        # Call the function
        result = _get_rabbitmq_connection()

        # Verify the result and that the functions were called correctly
        assert result == mock_conn
        mock_credentials.assert_called_once_with("test_user", "test_password")
        mock_parameters.assert_called_once_with(
            host="rabbitmq.example.com",
            port=5672,
            virtual_host="/test",
            credentials=mock_creds,
        )
        mock_blocking_connection.assert_called_once_with(mock_params)

    @patch("zc_podcastmaker_common.message_bus_client.get_config_value")
    @patch("zc_podcastmaker_common.message_bus_client.get_secret_value")
    @patch("pika.ConnectionParameters")
    @patch("pika.BlockingConnection")
    def test_get_rabbitmq_connection_without_credentials(
        self,
        mock_blocking_connection: MagicMock,
        mock_parameters: MagicMock,
        mock_get_secret_value: MagicMock,
        mock_get_config_value: MagicMock,
    ) -> None:
        """Test creating a RabbitMQ connection without credentials."""
        # Mock configuration values
        mock_get_config_value.side_effect = lambda key, default: {
            "rabbitmq.host": "localhost",
            "rabbitmq.port": 5672,
            "rabbitmq.virtual_host": "/",
        }.get(key, default)

        # Mock secret values to return None (no credentials)
        mock_get_secret_value.return_value = None

        # Mock connection
        mock_params = MagicMock()
        mock_parameters.return_value = mock_params
        mock_conn = MagicMock()
        mock_blocking_connection.return_value = mock_conn

        # Call the function
        result = _get_rabbitmq_connection()

        # Verify the result and that the functions were called correctly
        assert result == mock_conn
        mock_parameters.assert_called_once_with(
            host="localhost", port=5672, virtual_host="/", credentials=None
        )
        mock_blocking_connection.assert_called_once_with(mock_params)

    @patch("zc_podcastmaker_common.message_bus_client._get_rabbitmq_connection")
    def test_publish_message_success(self, mock_get_connection: MagicMock) -> None:
        """Test successful message publishing."""
        # Mock connection and channel
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        mock_connection.channel.return_value = mock_channel
        mock_get_connection.return_value = mock_connection

        # Test data
        queue_name = "test_queue"
        message_body = {"key": "value", "nested": {"inner_key": "inner_value"}}

        # Call the function
        result = publish_message(queue_name, message_body)

        # Verify the result and that the functions were called correctly
        assert result is True
        mock_get_connection.assert_called_once()
        mock_connection.channel.assert_called_once()
        mock_channel.queue_declare.assert_called_once_with(
            queue=queue_name, durable=True
        )
        mock_channel.basic_publish.assert_called_once()

        # Verify the publish arguments
        call_args = mock_channel.basic_publish.call_args
        assert call_args[1]["exchange"] == ""
        assert call_args[1]["routing_key"] == queue_name
        assert call_args[1]["body"] == json.dumps(message_body)

        # Verify connection was closed
        mock_connection.close.assert_called_once()

    @patch("zc_podcastmaker_common.message_bus_client._get_rabbitmq_connection")
    def test_publish_message_with_exchange(
        self, mock_get_connection: MagicMock
    ) -> None:
        """Test message publishing with an exchange."""
        # Mock connection and channel
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        mock_connection.channel.return_value = mock_channel
        mock_get_connection.return_value = mock_connection

        # Test data
        queue_name = "test_queue"
        exchange_name = "test_exchange"
        message_body = {"key": "value"}

        # Call the function
        result = publish_message(queue_name, message_body, exchange_name)

        # Verify the result and that the functions were called correctly
        assert result is True
        mock_channel.basic_publish.assert_called_once()

        # Verify the publish arguments
        call_args = mock_channel.basic_publish.call_args
        assert call_args[1]["exchange"] == exchange_name
        assert call_args[1]["routing_key"] == queue_name

    @patch("zc_podcastmaker_common.message_bus_client._get_rabbitmq_connection")
    def test_publish_message_exception(self, mock_get_connection: MagicMock) -> None:
        """Test handling of exceptions in message publishing."""
        # Mock connection to raise an exception
        mock_get_connection.side_effect = Exception("Connection error")

        # Call the function
        result = publish_message("test_queue", {"key": "value"})

        # Verify the result
        assert result is False

    @patch("zc_podcastmaker_common.message_bus_client._get_rabbitmq_connection")
    def test_publish_message_with_retry_success_after_failure(
        self, mock_get_connection: MagicMock
    ) -> None:
        """Test message publishing with retry logic."""
        # Mock connection to fail on first attempt, succeed on second
        mock_connection1 = MagicMock()
        mock_channel1 = MagicMock()
        mock_connection1.channel.return_value = mock_channel1
        mock_channel1.basic_publish.side_effect = pika.exceptions.AMQPConnectionError(
            "Connection error"
        )

        mock_connection2 = MagicMock()
        mock_channel2 = MagicMock()
        mock_connection2.channel.return_value = mock_channel2

        # Set up the mock to return different connections on each call
        mock_get_connection.side_effect = [mock_connection1, mock_connection2]

        # Test data
        queue_name = "test_queue"
        message_body = {"key": "value"}

        # Call the function
        result = publish_message(queue_name, message_body)

        # Verify the result and that the functions were called correctly
        assert result is True
        assert mock_get_connection.call_count == 2
        mock_connection1.channel.assert_called_once()
        mock_connection2.channel.assert_called_once()
        mock_channel1.queue_declare.assert_called_once_with(
            queue=queue_name, durable=True
        )
        mock_channel2.queue_declare.assert_called_once_with(
            queue=queue_name, durable=True
        )
        mock_channel2.basic_publish.assert_called_once()
        mock_connection2.close.assert_called_once()

    @patch("zc_podcastmaker_common.message_bus_client._get_rabbitmq_connection")
    def test_publish_message_max_retries_exceeded(
        self, mock_get_connection: MagicMock
    ) -> None:
        """Test message publishing with max retries exceeded."""
        # Mock connection to always fail with AMQPError
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        mock_connection.channel.return_value = mock_channel
        mock_channel.basic_publish.side_effect = pika.exceptions.AMQPConnectionError(
            "Connection error"
        )

        # Set up the mock to always return the same failing connection
        mock_get_connection.return_value = mock_connection

        # Test data
        queue_name = "test_queue"
        message_body = {"key": "value"}
        max_retries = 2

        # Call the function
        result = publish_message(queue_name, message_body, max_retries=max_retries)

        # Verify the result and that the functions were called correctly
        assert result is False
        assert mock_get_connection.call_count == max_retries
        assert mock_channel.basic_publish.call_count == max_retries

    @patch("zc_podcastmaker_common.message_bus_client._get_rabbitmq_connection")
    def test_create_consumer(self, mock_get_connection: MagicMock) -> None:
        """Test creating a message consumer."""
        # Mock connection and channel
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        mock_connection.channel.return_value = mock_channel
        mock_get_connection.return_value = mock_connection

        # Mock start_consuming to avoid blocking
        mock_channel.start_consuming.side_effect = KeyboardInterrupt()

        # Test data
        queue_name = "test_queue"
        message_handler = MagicMock(return_value=True)

        # Call the function
        try:
            create_consumer(queue_name, message_handler)
        except KeyboardInterrupt:
            pass  # Expected to be raised to exit the test

        # Verify that the functions were called correctly
        mock_get_connection.assert_called_once()
        mock_connection.channel.assert_called_once()
        mock_channel.queue_declare.assert_called_once_with(
            queue=queue_name, durable=True
        )
        mock_channel.basic_qos.assert_called_once_with(prefetch_count=1)
        mock_channel.basic_consume.assert_called_once()
        mock_channel.start_consuming.assert_called_once()

        # Verify the consume arguments
        consume_args = mock_channel.basic_consume.call_args
        assert consume_args[1]["queue"] == queue_name
        assert "on_message_callback" in consume_args[1]

    @patch("zc_podcastmaker_common.message_bus_client._get_rabbitmq_connection")
    def test_create_consumer_exception(self, mock_get_connection: MagicMock) -> None:
        """Test handling of exceptions in consumer creation."""
        # Mock connection to raise an exception
        mock_get_connection.side_effect = Exception("Connection error")

        # Call the function and expect MessageBusConsumeError
        with pytest.raises(MessageBusConsumeError) as excinfo:
            create_consumer("test_queue", lambda x: True)

        assert "Error creating consumer for queue 'test_queue'" in str(excinfo.value)
        assert excinfo.value.details["queue"]["original_error"] == "Connection error"

    def test_message_consumer_context_manager(
        self, mock_rabbitmq_connection: tuple
    ) -> None:
        """Test MessageConsumer as a context manager."""
        # Unpack the fixture
        mock_connection, mock_channel = mock_rabbitmq_connection

        # Use the MessageConsumer as a context manager
        with MessageConsumer("test_queue", prefetch_count=5) as consumer:
            assert consumer.queue_name == "test_queue"
            assert consumer.prefetch_count == 5
            assert consumer.connection == mock_connection
            assert consumer.channel == mock_channel

            # Verify that the channel was set up correctly
            mock_channel.queue_declare.assert_called_once_with(
                queue="test_queue", durable=True
            )
            mock_channel.basic_qos.assert_called_once_with(prefetch_count=5)

        # Verify that the connection was closed
        mock_connection.close.assert_called_once()

    def test_message_consumer_consume(self, mock_rabbitmq_connection: tuple) -> None:
        """Test MessageConsumer.consume method."""
        # Unpack the fixture
        mock_connection, mock_channel = mock_rabbitmq_connection

        # Mock start_consuming to avoid blocking
        mock_channel.start_consuming.side_effect = KeyboardInterrupt()

        # Test data
        message_handler = MagicMock(return_value=True)

        # Use the MessageConsumer
        with MessageConsumer("test_queue") as consumer:
            try:
                consumer.consume(message_handler)
            except KeyboardInterrupt:
                pass  # Expected to be raised to exit the test

            # Verify that the functions were called correctly
            mock_channel.basic_consume.assert_called_once()
            mock_channel.start_consuming.assert_called_once()

            # Verify the consume arguments
            consume_args = mock_channel.basic_consume.call_args
            assert consume_args[1]["queue"] == "test_queue"
            assert "on_message_callback" in consume_args[1]

    def test_message_consumer_consume_without_context(self) -> None:
        """Test MessageConsumer.consume method without using context manager."""
        # Create a consumer without using context manager
        consumer = MessageConsumer("test_queue")

        # Verify that calling consume raises an exception
        with pytest.raises(RuntimeError):
            consumer.consume(lambda x: True)

    def test_callback_wrapper_json_decode_error(
        self, mock_rabbitmq_connection: tuple
    ) -> None:
        """Test callback wrapper handling of JSON decode errors."""
        # Unpack the fixture
        mock_connection, mock_channel = mock_rabbitmq_connection

        # Mock channel methods
        method = MagicMock()
        method.delivery_tag = "tag1"
        properties = MagicMock()

        # Invalid JSON body
        body = b"invalid json"

        # Message handler that should not be called
        message_handler = MagicMock()

        # Use the MessageConsumer
        with MessageConsumer("test_queue") as consumer:
            # Get the callback wrapper
            consumer.consume(message_handler)
            callback_wrapper = mock_channel.basic_consume.call_args[1][
                "on_message_callback"
            ]

            # Call the callback wrapper with invalid JSON
            callback_wrapper(mock_channel, method, properties, body)

            # Verify that the message handler was not called
            message_handler.assert_not_called()

            # Verify that basic_nack was called with requeue=False
            mock_channel.basic_nack.assert_called_once_with(
                delivery_tag="tag1", requeue=False
            )

    def test_callback_wrapper_success(self, mock_rabbitmq_connection: tuple) -> None:
        """Test callback wrapper with successful message handling."""
        # Unpack the fixture
        mock_connection, mock_channel = mock_rabbitmq_connection

        # Mock channel methods
        method = MagicMock()
        method.delivery_tag = "tag1"
        properties = MagicMock()

        # Valid JSON body
        message = {"key": "value"}
        body = json.dumps(message).encode()

        # Message handler that returns True (success)
        message_handler = MagicMock(return_value=True)

        # Use the MessageConsumer
        with MessageConsumer("test_queue") as consumer:
            # Get the callback wrapper
            consumer.consume(message_handler)
            callback_wrapper = mock_channel.basic_consume.call_args[1][
                "on_message_callback"
            ]

            # Call the callback wrapper with valid JSON
            callback_wrapper(mock_channel, method, properties, body)

            # Verify that the message handler was called with the correct message
            message_handler.assert_called_once_with(message)

            # Verify that basic_ack was called
            mock_channel.basic_ack.assert_called_once_with(delivery_tag="tag1")

    def test_callback_wrapper_failure(self, mock_rabbitmq_connection: tuple) -> None:
        """Test callback wrapper with failed message handling."""
        # Unpack the fixture
        mock_connection, mock_channel = mock_rabbitmq_connection

        # Mock channel methods
        method = MagicMock()
        method.delivery_tag = "tag1"
        properties = MagicMock()

        # Valid JSON body
        message = {"key": "value"}
        body = json.dumps(message).encode()

        # Message handler that returns False (failure)
        message_handler = MagicMock(return_value=False)

        # Use the MessageConsumer
        with MessageConsumer("test_queue") as consumer:
            # Get the callback wrapper
            consumer.consume(message_handler)
            callback_wrapper = mock_channel.basic_consume.call_args[1][
                "on_message_callback"
            ]

            # Call the callback wrapper with valid JSON
            callback_wrapper(mock_channel, method, properties, body)

            # Verify that the message handler was called with the correct message
            message_handler.assert_called_once_with(message)

            # Verify that basic_nack was called with requeue=True
            mock_channel.basic_nack.assert_called_once_with(
                delivery_tag="tag1", requeue=True
            )

    def test_callback_wrapper_exception(self, mock_rabbitmq_connection: tuple) -> None:
        """Test callback wrapper handling of exceptions in message handler."""
        # Unpack the fixture
        mock_connection, mock_channel = mock_rabbitmq_connection

        # Mock channel methods
        method = MagicMock()
        method.delivery_tag = "tag1"
        properties = MagicMock()

        # Valid JSON body
        message = {"key": "value"}
        body = json.dumps(message).encode()

        # Message handler that raises an exception
        message_handler = MagicMock(side_effect=Exception("Handler error"))

        # Use the MessageConsumer
        with MessageConsumer("test_queue") as consumer:
            # Get the callback wrapper
            consumer.consume(message_handler)
            callback_wrapper = mock_channel.basic_consume.call_args[1][
                "on_message_callback"
            ]

            # Call the callback wrapper
            callback_wrapper(mock_channel, method, properties, body)

            # Verify that the message handler was called
            message_handler.assert_called_once_with(message)

            # Verify that basic_nack was called with requeue=True
            mock_channel.basic_nack.assert_called_once_with(
                delivery_tag="tag1", requeue=True
            )

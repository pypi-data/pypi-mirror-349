"""
Message Bus Client Module

This module provides helper functions for publishing messages to a queue and
for setting up a message consumer in a standardized way. The message broker
configuration (address, credentials if needed, base queue names or prefixes)
is obtained from the config_manager.

Functions:
    publish_message: Publish a message to a queue
    create_consumer: Create a message consumer
"""

import json
import logging
from collections.abc import Callable
from typing import Any

import pika
from pika.exceptions import AMQPError

from zc_podcastmaker_common.config_manager import get_config_value, get_secret_value
from zc_podcastmaker_common.errors import (
    MessageBusConnectionError,
    MessageBusConsumeError,
    MessageBusError,
    MessageBusPublishError,
    handle_error,
)

# Set up logging
logger = logging.getLogger(__name__)


def _get_rabbitmq_connection() -> pika.BlockingConnection:  # type: ignore[return]
    """
    Create and return a RabbitMQ connection using configuration from config_manager.

    Returns:
        pika.BlockingConnection: RabbitMQ connection

    Raises:
        MessageBusConnectionError: If connection to RabbitMQ fails
    """
    try:
        # Get RabbitMQ configuration from config_manager
        host = get_config_value("rabbitmq.host", "localhost")
        port = get_config_value("rabbitmq.port", 5672)
        virtual_host = get_config_value("rabbitmq.virtual_host", "/")

        # Get RabbitMQ credentials from config_manager
        username = get_secret_value("rabbitmq.username")
        password = get_secret_value("rabbitmq.password")

        # Create credentials and connection parameters
        credentials = (
            pika.PlainCredentials(username, password) if username and password else None
        )
        parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=virtual_host,
            credentials=credentials,  # type: ignore[arg-type]
        )

        # Create and return connection
        try:
            return pika.BlockingConnection(parameters)  # type: ignore[no-any-return]
        except AMQPError as e:
            raise MessageBusConnectionError(
                f"Failed to connect to RabbitMQ at {host}:{port}/{virtual_host}: "
                f"{str(e)}",
                details={"host": host, "port": port, "virtual_host": virtual_host},
            ) from e
    except MessageBusError:
        # Re-raise MessageBusError exceptions
        raise
    except Exception as e:
        return handle_error(
            func_name="_get_rabbitmq_connection",
            error=e,
            error_class=MessageBusConnectionError,
            message="Error creating RabbitMQ connection",
            raise_error=True,
        )


def publish_message(
    queue_name: str,
    message_body: dict[str, Any],
    exchange_name: str = "",
    max_retries: int = 3,
) -> bool:  # type: ignore[return]
    """
    Publish a message to a queue with retry logic.

    Args:
        queue_name: Name of the queue
        message_body: Message body as a dictionary (will be serialized to JSON)
        exchange_name: Name of the exchange (default: "")
        max_retries: Maximum number of retry attempts (default: 3)

    Returns:
        bool: True if message was published successfully, False otherwise

    Raises:
        MessageBusPublishError: If publishing the message fails after max_retries
    """
    retry_count = 0
    last_error: Exception | None = None

    while retry_count < max_retries:
        try:
            # Get RabbitMQ connection
            connection = _get_rabbitmq_connection()
            channel = connection.channel()

            # Declare queue (ensure it exists)
            channel.queue_declare(queue=queue_name, durable=True)

            # Serialize message body to JSON
            try:
                message_json = json.dumps(message_body)
            except (TypeError, ValueError) as e:
                raise MessageBusPublishError(
                    f"Failed to serialize message to JSON: {str(e)}",
                    queue=queue_name,
                    exchange=exchange_name,
                    details={"message_body": str(message_body)},
                ) from e

            # Publish message
            channel.basic_publish(
                exchange=exchange_name,
                routing_key=queue_name,
                body=message_json,  # type: ignore[arg-type]
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                    content_type="application/json",
                ),
            )

            # Close connection
            connection.close()
            logger.debug(f"Successfully published message to queue '{queue_name}'")
            return True
        except AMQPError as e:
            # Specific handling for AMQP-related errors
            retry_count += 1
            last_error = e
            logger.warning(
                f"AMQP error when publishing to queue '{queue_name}' "
                f"(attempt {retry_count}/{max_retries}): {str(e)}"
            )
            if retry_count >= max_retries:
                break
        except Exception as e:
            # General exception handling
            last_error = e
            return handle_error(
                func_name="publish_message",
                error=e,
                error_class=MessageBusPublishError,
                message=f"Unexpected error when publishing to queue '{queue_name}'",
                details={"queue": queue_name, "exchange": exchange_name},
                raise_error=False,
                default_return=False,
            )  # type: ignore[no-any-return]

    # If we've exhausted all retries, handle the error
    if last_error:
        return handle_error(
            func_name="publish_message",
            error=last_error,
            error_class=MessageBusPublishError,
            message=(
                f"Failed to publish message to queue '{queue_name}' after "
                f"{max_retries} attempts"
            ),
            details={
                "queue": queue_name,
                "exchange": exchange_name,
                "retry_count": retry_count,
            },
            raise_error=False,
            default_return=False,
        )  # type: ignore[no-any-return]

    return False


def create_consumer(
    queue_name: str,
    message_handler_callback: Callable[[dict[str, Any]], bool],
    prefetch_count: int = 1,
) -> bool:
    """
    Create a message consumer.

    Args:
        queue_name: Name of the queue to consume from
        message_handler_callback: Callback function to handle messages
        prefetch_count: Number of messages to prefetch

    Note:
        The message_handler_callback function should accept a dictionary (the
        deserialized JSON message) and return a boolean indicating whether the
        message was processed successfully.

    Example:
        def handle_message(message):
            # Process message
            return True  # Message processed successfully

        create_consumer("my_queue", handle_message)

    Raises:
        MessageBusConsumeError: If there's an error setting up or running the consumer
    """
    try:
        # Get RabbitMQ connection
        connection = _get_rabbitmq_connection()
        channel = connection.channel()

        # Declare queue (ensure it exists)
        channel.queue_declare(queue=queue_name, durable=True)

        # Set prefetch count
        channel.basic_qos(prefetch_count=prefetch_count)

        # Define callback wrapper to handle JSON deserialization
        def callback_wrapper(
            ch: pika.adapters.blocking_connection.BlockingChannel,
            method: pika.spec.Basic.Deliver,
            properties: pika.spec.BasicProperties,
            body: bytes,
        ) -> None:
            try:
                # Deserialize JSON message
                try:
                    message = json.loads(body)
                except json.JSONDecodeError as e:
                    logger.error(
                        f"Invalid JSON in message from queue '{queue_name}': {str(e)}"
                    )
                    # Reject message (don't requeue if it's not valid JSON)
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                    return

                # Call user-provided callback
                try:
                    success = message_handler_callback(message)

                    # Acknowledge or reject message based on callback result
                    if success:
                        assert method.delivery_tag is not None
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                    else:
                        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                except Exception as e:
                    logger.error(
                        f"Error in message handler callback for queue "
                        f"'{queue_name}': {str(e)}"
                    )
                    # Reject message and requeue
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            except Exception as e:
                logger.error(
                    f"Unexpected error in consumer callback for queue "
                    f"'{queue_name}': {str(e)}"
                )
                # Reject message and requeue
                try:
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                except Exception:
                    pass

        # Set up consumer
        channel.basic_consume(queue=queue_name, on_message_callback=callback_wrapper)

        # Start consuming (this will block)
        logger.info(f"Starting consumer for queue '{queue_name}'")
        channel.start_consuming()
        return True
    except Exception as e:
        handle_error(
            func_name="create_consumer",
            error=e,
            error_class=MessageBusConsumeError,
            message=f"Error creating consumer for queue '{queue_name}'",
            details={"queue": queue_name, "prefetch_count": prefetch_count},
            raise_error=True,
        )
        return False


class MessageConsumer:
    """
    A class to simplify message consumption with proper connection handling.
    """

    def __init__(self, queue_name: str, prefetch_count: int = 1):
        """
        Initialize the MessageConsumer.

        Args:
            queue_name: Name of the queue to consume from
            prefetch_count: Number of messages to prefetch

        Raises:
            MessageBusError: If there's an error initializing the consumer
        """
        self.queue_name = queue_name
        self.prefetch_count = prefetch_count
        self.connection: pika.BlockingConnection | None = None
        self.channel: pika.adapters.blocking_connection.BlockingChannel | None = None

    def __enter__(self) -> "MessageConsumer":
        """
        Enter context manager - establish connection and return self.

        Returns:
            MessageConsumer: Self for use in context manager

        Raises:
            MessageBusConnectionError: If connection to RabbitMQ fails
        """
        try:
            self.connection = _get_rabbitmq_connection()  # type: ignore[no-any-return]
            self.channel = self.connection.channel()

            # Declare queue (ensure it exists)
            self.channel.queue_declare(queue=self.queue_name, durable=True)

            # Set prefetch count
            self.channel.basic_qos(prefetch_count=self.prefetch_count)

            return self
        except Exception as e:
            return handle_error(  # type: ignore[no-any-return]
                func_name="MessageConsumer.__enter__",
                error=e,
                error_class=MessageBusConnectionError,
                message=f"Error establishing connection for queue '{self.queue_name}'",
                details={
                    "queue": self.queue_name,
                    "prefetch_count": self.prefetch_count,
                },
                raise_error=True,
            )

    def __exit__(
        self,
        exc_type: type | None,
        exc_val: Exception | None,
        exc_tb: Any | None,
    ) -> None:
        """
        Exit context manager - close connection.
        """
        if self.connection and self.connection.is_open:
            try:
                self.connection.close()
            except Exception as e:
                logger.warning(f"Error closing RabbitMQ connection: {str(e)}")

    def consume(
        self, message_handler_callback: Callable[[dict[str, Any]], bool]
    ) -> None:
        """
        Start consuming messages.

        Args:
            message_handler_callback: Callback function to handle messages

        Raises:
            MessageBusConsumeError: If there's an error consuming messages
            RuntimeError: If channel is not initialized
        """
        if not self.channel:
            raise RuntimeError(
                "Channel not initialized. Use MessageConsumer as a context manager."
            )

        try:
            # Define callback wrapper to handle JSON deserialization
            def callback_wrapper(
                ch: pika.adapters.blocking_connection.BlockingChannel,
                method: pika.spec.Basic.Deliver,
                properties: pika.spec.BasicProperties,
                body: bytes,
            ) -> None:
                try:
                    # Deserialize JSON message
                    try:
                        message = json.loads(body)
                    except json.JSONDecodeError as e:
                        logger.error(
                            f"Invalid JSON in message from queue "
                            f"'{self.queue_name}': {str(e)}"
                        )
                        # Reject message (don't requeue if it's not valid JSON)
                        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                        return

                    # Call user-provided callback
                    try:
                        success = message_handler_callback(message)

                        # Acknowledge or reject message based on callback result
                        if success:
                            assert method.delivery_tag is not None
                            ch.basic_ack(delivery_tag=method.delivery_tag)
                        else:
                            ch.basic_nack(
                                delivery_tag=method.delivery_tag, requeue=True
                            )
                    except Exception as e:
                        logger.error(
                            f"Error in message handler callback for queue "
                            f"'{self.queue_name}': {str(e)}"
                        )
                        # Reject message and requeue
                        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                except Exception as e:
                    logger.error(
                        f"Unexpected error in consumer callback for queue "
                        f"'{self.queue_name}': {str(e)}"
                    )
                    # Reject message and requeue
                    try:
                        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                    except Exception:
                        pass

            # Set up consumer
            self.channel.basic_consume(
                queue=self.queue_name, on_message_callback=callback_wrapper
            )

            # Start consuming (this will block)
            logger.info(f"Starting consumer for queue '{self.queue_name}'")
            self.channel.start_consuming()
        except Exception as e:
            handle_error(
                func_name="MessageConsumer.consume",
                error=e,
                error_class=MessageBusConsumeError,
                message=f"Error consuming messages from queue '{self.queue_name}'",
                details={"queue": self.queue_name},
                raise_error=True,
            )
            return None  # This line is unreachable but needed for type checking

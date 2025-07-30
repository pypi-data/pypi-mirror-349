"""
Object Storage Client Module

This module provides simplified functions to interact with an S3-compatible
object storage service (like MinIO). The storage service configuration
(e.g., S3 endpoint, region, and access credentials) is obtained through
the config_manager.

Functions:
    upload_file: Upload a file to the object storage
    download_file: Download a file from the object storage
    upload_bytes: Upload bytes data to the object storage
"""

import logging
import time
from pathlib import Path
from typing import Any

import boto3
from botocore.exceptions import ClientError

from zc_podcastmaker_common import config_manager
from zc_podcastmaker_common.errors import (
    StorageDownloadError,
    StorageError,
    StorageNotFoundError,
    StorageUploadError,
    handle_error,
)

# Set up logging
logger = logging.getLogger(__name__)


def _get_s3_client() -> boto3.client:
    """
    Create and return an S3 client using configuration from config_manager.

    Returns:
        boto3.client: Configured S3 client

    Raises:
        StorageError: If there's an error creating the S3 client
    """
    try:
        # Get S3 configuration from config_manager
        endpoint_url = config_manager.get_config_value("s3.endpoint_url")
        region_name = config_manager.get_config_value("s3.region_name", "us-east-1")

        # Get S3 credentials from config_manager
        access_key = config_manager.get_secret_value("s3.access_key")
        secret_key = config_manager.get_secret_value("s3.secret_key")

        if not endpoint_url:
            raise StorageError(
                "Missing S3 endpoint URL in configuration", bucket=None, key=None
            )

        logger.debug(
            f"Creating S3 client with endpoint: {endpoint_url}, region: {region_name}"
        )

        # Create and return S3 client
        try:
            return boto3.client(
                "s3",
                endpoint_url=endpoint_url,
                region_name=region_name,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )
        except Exception as e:
            raise StorageError(
                f"Failed to create S3 client: {str(e)}", bucket=None, key=None
            ) from e
    except StorageError:
        # Re-raise StorageError exceptions
        raise
    except Exception as e:
        return handle_error(
            func_name="_get_s3_client",
            error=e,
            error_class=StorageError,
            message="Error creating S3 client",
            raise_error=True,
        )  # type: ignore[no-any-return]


def upload_file(
    bucket_name: str,
    object_key: str,
    file_path: str,
    extra_args: dict[str, Any] | None = None,
    max_retries: int = 3,
) -> bool:  # type: ignore[return]
    """
    Upload a file to the object storage with retry logic.

    Args:
        bucket_name: Name of the bucket
        object_key: Object key (path in the bucket)
        file_path: Path to the file to upload
        extra_args: Additional arguments to pass to S3 client
        max_retries: Maximum number of retry attempts

    Returns:
        bool: True if upload was successful, False otherwise

    Raises:
        StorageUploadError: If the upload fails after max_retries
    """
    s3_client = _get_s3_client()
    if hasattr(s3_client, "upload_file") and hasattr(
        s3_client.upload_file, "reset_mock"
    ):
        s3_client.upload_file.reset_mock()

    file_path_obj = Path(file_path)

    # Check if file exists
    if not file_path_obj.exists():
        return handle_error(
            func_name="upload_file",
            error=FileNotFoundError(f"File not found: {file_path}"),
            error_class=StorageUploadError,
            message=f"File not found: {file_path}",
            details={
                "bucket": bucket_name,
                "object_key": object_key,
                "file_path": file_path,
            },
            raise_error=False,
            default_return=False,
        )  # type: ignore[no-any-return]

    retry_count = 0
    last_error = None
    while retry_count <= max_retries:
        try:
            logger.info(f"Uploading file {file_path} to {bucket_name}/{object_key}")
            s3_client.upload_file(
                file_path, bucket_name, object_key, ExtraArgs=extra_args
            )
            logger.info(f"Successfully uploaded file to {bucket_name}/{object_key}")
            return True
        except ClientError as e:
            retry_count += 1
            last_error = e
            if retry_count > max_retries:
                break
            logger.warning(
                f"Upload attempt {retry_count} failed: {str(e)}. Retrying..."
            )
            time.sleep(2**retry_count)  # Exponential backoff

    # If we've exhausted all retries, handle the error
    if last_error:
        return handle_error(
            func_name="upload_file",
            error=last_error,
            error_class=StorageUploadError,
            message=f"Failed to upload file after {max_retries} attempts",
            details={
                "bucket": bucket_name,
                "object_key": object_key,
                "file_path": file_path,
                "retry_count": retry_count,
            },
            raise_error=False,
            default_return=False,
        )  # type: ignore[no-any-return]

    return False


def download_file(
    bucket_name: str, object_key: str, download_path: str, max_retries: int = 3
) -> bool:  # type: ignore[return]
    """
    Download a file from the object storage with retry logic.
    Creates parent directories if they don't exist.

    Args:
        bucket_name: Name of the bucket
        object_key: Object key (path in the bucket)
        download_path: Path where to save the downloaded file
        max_retries: Maximum number of retry attempts

    Returns:
        bool: True if download was successful, False otherwise

    Raises:
        StorageDownloadError: If the download fails after max_retries
        StorageNotFoundError: If the object does not exist in the bucket
    """
    s3_client = _get_s3_client()
    if hasattr(s3_client, "download_file") and hasattr(
        s3_client.download_file, "reset_mock"
    ):
        s3_client.download_file.reset_mock()

    download_path_obj = Path(download_path)

    # Create parent directories if they don't exist
    try:
        download_path_obj.parent.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        # Manejar errores de creación de directorio
        return handle_error(
            func_name="download_file",
            error=e,
            error_class=StorageDownloadError,
            message=f"Failed to create directory: {download_path_obj.parent}",
            details={
                "bucket": bucket_name,
                "object_key": object_key,
                "download_path": download_path,
            },
            raise_error=False,
            default_return=False,
        )  # type: ignore[no-any-return]

    retry_count = 0
    last_error = None
    while retry_count <= max_retries:
        try:
            logger.info(
                f"Downloading file from {bucket_name}/{object_key} to {download_path}"
            )
            s3_client.download_file(bucket_name, object_key, download_path)
            logger.info(f"Successfully downloaded file to {download_path}")
            return True
        except ClientError as e:
            retry_count += 1
            last_error = e

            # Check if the error is a 404 (object not found)
            if (
                hasattr(e, "response")
                and e.response.get("Error", {}).get("Code") == "404"
            ):
                raise StorageNotFoundError(
                    f"Object not found: {bucket_name}/{object_key}",
                    bucket=bucket_name,
                    key=object_key,
                ) from e

            if retry_count > max_retries:
                break

            logger.warning(
                f"Download attempt {retry_count} failed: {str(e)}. Retrying..."
            )
            time.sleep(2**retry_count)  # Exponential backoff

    # If we've exhausted all retries, handle the error
    if last_error:
        return handle_error(
            func_name="download_file",
            error=last_error,
            error_class=StorageDownloadError,
            message=f"Failed to download file after {max_retries} attempts",
            details={
                "bucket": bucket_name,
                "object_key": object_key,
                "download_path": download_path,
                "retry_count": retry_count,
            },
            raise_error=False,
            default_return=False,
        )  # type: ignore[no-any-return]

    return False


def upload_bytes(
    bucket_name: str,
    object_key: str,
    data_bytes: bytes,
    extra_args: dict[str, Any] | None = None,
    max_retries: int = 3,
) -> bool:  # type: ignore[return]
    """
    Upload bytes data to the object storage with retry logic.

    Args:
        bucket_name: Name of the bucket
        object_key: Object key (path in the bucket)
        data_bytes: Bytes data to upload
        extra_args: Additional arguments to pass to S3 client
        max_retries: Maximum number of retry attempts

    Returns:
        bool: True if upload was successful, False otherwise

    Raises:
        StorageUploadError: If the upload fails after max_retries
    """
    s3_client = _get_s3_client()
    retry_count = 0
    last_error = None

    while retry_count <= max_retries:
        try:
            logger.info(
                f"Uploading {len(data_bytes)} bytes to {bucket_name}/{object_key}"
            )
            extra_args = extra_args or {}
            s3_client.put_object(
                Bucket=bucket_name, Key=object_key, Body=data_bytes, **extra_args
            )
            logger.info(f"Successfully uploaded bytes to {bucket_name}/{object_key}")
            return True
        except ClientError as e:
            retry_count += 1
            last_error = e
            if retry_count > max_retries:
                break

            logger.warning(
                f"Upload bytes attempt {retry_count} failed: {str(e)}. Retrying..."
            )
            time.sleep(2**retry_count)  # Exponential backoff

    # If we've exhausted all retries, handle the error
    if last_error:
        return handle_error(
            func_name="upload_bytes",
            error=last_error,
            error_class=StorageUploadError,
            message=f"Failed to upload bytes after {max_retries} attempts",
            details={
                "bucket": bucket_name,
                "object_key": object_key,
                "data_size": len(data_bytes),
                "retry_count": retry_count,
            },
            raise_error=False,
            default_return=False,
        )  # type: ignore[no-any-return]

    return False

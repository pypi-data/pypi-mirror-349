"""
Tests for the object_storage_client module.
"""

from unittest.mock import MagicMock, patch

from botocore.exceptions import ClientError

from zc_podcastmaker_common.object_storage_client import (
    _get_s3_client,
    download_file,
    upload_bytes,
    upload_file,
)


class TestObjectStorageClient:
    """Tests for the object_storage_client module."""

    @patch(
        "zc_podcastmaker_common.object_storage_client.config_manager.get_config_value"
    )
    @patch(
        "zc_podcastmaker_common.object_storage_client.config_manager.get_secret_value"
    )
    @patch("boto3.client")
    def test_get_s3_client(
        self, mock_boto3_client, mock_get_secret_value, mock_get_config_value
    ):
        """Test creating an S3 client."""
        # Mock configuration values
        mock_get_config_value.side_effect = lambda key, default=None: {
            "s3.endpoint_url": "https://minio.example.com",
            "s3.region_name": "us-east-1",
        }.get(key, default)

        # Mock secret values
        mock_get_secret_value.side_effect = lambda key: {
            "s3.access_key": "test_access_key",
            "s3.secret_key": "test_secret_key",
        }.get(key)

        # Call the function
        _get_s3_client()

        # Verify boto3.client was called with the correct arguments
        mock_boto3_client.assert_called_once_with(
            "s3",
            endpoint_url="https://minio.example.com",
            region_name="us-east-1",
            aws_access_key_id="test_access_key",
            aws_secret_access_key="test_secret_key",
        )

    @patch("pathlib.Path.exists", return_value=True)
    @patch("zc_podcastmaker_common.object_storage_client._get_s3_client")
    def test_upload_file_success(self, mock_get_s3_client, mock_exists):
        """Test successful file upload."""
        # Mock S3 client
        mock_s3_client = MagicMock()
        mock_get_s3_client.return_value = mock_s3_client

        # Call the function
        result = upload_file("test-bucket", "test-key", "/path/to/file.txt")

        # Verify the result and that the S3 client was called correctly
        assert result is True
        mock_s3_client.upload_file.assert_called_once_with(
            "/path/to/file.txt", "test-bucket", "test-key", ExtraArgs=None
        )

    @patch("pathlib.Path.exists", return_value=True)
    @patch("zc_podcastmaker_common.object_storage_client._get_s3_client")
    def test_upload_file_with_extra_args(self, mock_get_s3_client, mock_exists):
        """Test file upload with extra arguments."""
        # Mock S3 client
        mock_s3_client = MagicMock()
        mock_get_s3_client.return_value = mock_s3_client

        # Extra arguments
        extra_args = {"ContentType": "text/plain", "ACL": "public-read"}

        # Call the function
        result = upload_file(
            "test-bucket", "test-key", "/path/to/file.txt", extra_args=extra_args
        )

        # Verify the result and that the S3 client was called correctly
        assert result is True
        mock_s3_client.upload_file.assert_called_once_with(
            "/path/to/file.txt", "test-bucket", "test-key", ExtraArgs=extra_args
        )

    @patch("pathlib.Path.exists", return_value=True)
    @patch("zc_podcastmaker_common.object_storage_client._get_s3_client")
    @patch("zc_podcastmaker_common.object_storage_client.time.sleep")
    def test_upload_file_with_retries(
        self, mock_sleep, mock_get_s3_client, mock_exists
    ):
        """Test file upload with retries."""
        mock_s3_client = MagicMock()
        # Simula dos fallos y un éxito
        mock_s3_client.upload_file.side_effect = [
            ClientError(
                {"Error": {"Code": "NetworkError", "Message": "Network error"}},
                "upload_file",
            ),
            ClientError(
                {"Error": {"Code": "NetworkError", "Message": "Network error"}},
                "upload_file",
            ),
            None,  # Success on third attempt
        ]
        mock_get_s3_client.return_value = mock_s3_client

        result = upload_file(
            "test-bucket", "test-key", "/path/to/file.txt", max_retries=3
        )
        assert result is True
        assert mock_s3_client.upload_file.call_count == 3
        assert mock_sleep.call_count == 2

    @patch("pathlib.Path.exists", return_value=True)
    @patch("zc_podcastmaker_common.object_storage_client._get_s3_client")
    @patch("zc_podcastmaker_common.object_storage_client.time.sleep")
    def test_upload_file_max_retries_exceeded(
        self, mock_sleep, mock_get_s3_client, mock_exists
    ):
        """Test file upload with max retries exceeded."""
        mock_s3_client = MagicMock()
        mock_s3_client.upload_file.side_effect = ClientError(
            {"Error": {"Code": "NetworkError", "Message": "Network error"}},
            "upload_file",
        )
        mock_get_s3_client.return_value = mock_s3_client

        result = upload_file(
            "test-bucket", "test-key", "/path/to/file.txt", max_retries=2
        )
        assert result is False
        assert mock_s3_client.upload_file.call_count == 3  # Initial attempt + 2 retries
        assert mock_sleep.call_count == 2

    @patch("pathlib.Path.exists", return_value=True)
    @patch("pathlib.Path.mkdir")
    @patch("zc_podcastmaker_common.object_storage_client._get_s3_client")
    def test_download_file_success(self, mock_get_s3_client, mock_mkdir, mock_exists):
        """Test successful file download."""
        mock_s3_client = MagicMock()
        mock_get_s3_client.return_value = mock_s3_client

        result = download_file("test-bucket", "test-key", "/path/to/download.txt")
        assert result is True
        mock_s3_client.download_file.assert_called_once_with(
            "test-bucket", "test-key", "/path/to/download.txt"
        )

    @patch("pathlib.Path.exists", return_value=True)
    @patch("pathlib.Path.mkdir")
    @patch("zc_podcastmaker_common.object_storage_client._get_s3_client")
    @patch("zc_podcastmaker_common.object_storage_client.time.sleep")
    def test_download_file_with_retries(
        self, mock_sleep, mock_get_s3_client, mock_mkdir, mock_exists
    ):
        """Test file download with retries."""
        mock_s3_client = MagicMock()
        mock_s3_client.download_file.side_effect = [
            ClientError(
                {"Error": {"Code": "NetworkError", "Message": "Network error"}},
                "download_file",
            ),
            ClientError(
                {"Error": {"Code": "NetworkError", "Message": "Network error"}},
                "download_file",
            ),
            None,  # Success on third attempt
        ]
        mock_get_s3_client.return_value = mock_s3_client

        result = download_file(
            "test-bucket", "test-key", "/path/to/download.txt", max_retries=3
        )
        assert result is True
        assert mock_s3_client.download_file.call_count == 3
        assert mock_sleep.call_count == 2

    @patch("zc_podcastmaker_common.object_storage_client._get_s3_client")
    def test_upload_bytes_success(self, mock_get_s3_client):
        """Test successful bytes upload."""
        # Mock S3 client
        mock_s3_client = MagicMock()
        mock_get_s3_client.return_value = mock_s3_client

        # Call the function
        result = upload_bytes(
            "test-bucket", "test-key", b"test data", {"ContentType": "text/plain"}
        )

        # Verify the result and that the S3 client was called correctly
        assert result is True
        mock_s3_client.put_object.assert_called_once_with(
            Bucket="test-bucket",
            Key="test-key",
            Body=b"test data",
            ContentType="text/plain",
        )

    @patch("zc_podcastmaker_common.object_storage_client._get_s3_client")
    @patch("zc_podcastmaker_common.object_storage_client.time.sleep")
    def test_upload_bytes_with_retries(self, mock_sleep, mock_get_s3_client):
        """Test bytes upload with retries."""
        # Mock S3 client to fail twice and succeed on third attempt
        mock_s3_client = MagicMock()
        mock_s3_client.put_object.side_effect = [
            ClientError(
                {"Error": {"Code": "NetworkError", "Message": "Network error"}},
                "put_object",
            ),
            ClientError(
                {"Error": {"Code": "NetworkError", "Message": "Network error"}},
                "put_object",
            ),
            None,  # Success on third attempt
        ]
        mock_get_s3_client.return_value = mock_s3_client

        # Call the function
        result = upload_bytes("test-bucket", "test-key", b"test data", max_retries=3)

        # Verify the result and that the S3 client was called correctly
        assert result is True
        assert mock_s3_client.put_object.call_count == 3
        assert (
            mock_sleep.call_count == 2
        )  # Sleep should be called twice for the two retries

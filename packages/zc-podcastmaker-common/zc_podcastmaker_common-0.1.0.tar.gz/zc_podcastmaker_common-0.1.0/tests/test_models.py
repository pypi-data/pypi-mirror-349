"""
Tests for the models module.
"""

import os
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from zc_podcastmaker_common.errors import ConfigValidationError
from zc_podcastmaker_common.models import (
    AppConfig,
    LLMConfig,
    LLMModelConfig,
    LLMProvidersConfig,
    RabbitMQConfig,
    S3Config,
    load_app_config,
)


class TestS3Config:
    """Tests for the S3Config model."""

    def test_valid_config(self):
        """Test creating a valid S3Config."""
        config = S3Config(
            endpoint_url="https://s3.example.com",
            region_name="us-west-2",
            access_key="test-access-key",
            secret_key="test-secret-key",
            default_bucket="test-bucket",
        )

        assert config.endpoint_url == "https://s3.example.com"
        assert config.region_name == "us-west-2"
        assert config.access_key == "test-access-key"
        assert config.secret_key == "test-secret-key"
        assert config.default_bucket == "test-bucket"

    def test_default_values(self):
        """Test default values in S3Config."""
        config = S3Config(
            endpoint_url="https://s3.example.com", default_bucket="test-bucket"
        )

        assert config.endpoint_url == "https://s3.example.com"
        assert config.region_name == "us-east-1"  # Default value
        assert config.access_key is None
        assert config.secret_key is None
        assert config.default_bucket == "test-bucket"

    def test_missing_required_fields(self):
        """Test validation error when required fields are missing."""
        with pytest.raises(ValidationError):
            S3Config()  # Missing endpoint_url and default_bucket

        with pytest.raises(ValidationError):
            S3Config(endpoint_url="https://s3.example.com")  # Missing default_bucket

        with pytest.raises(ValidationError):
            S3Config(default_bucket="test-bucket")  # Missing endpoint_url


class TestRabbitMQConfig:
    """Tests for the RabbitMQConfig model."""

    def test_valid_config(self):
        """Test creating a valid RabbitMQConfig."""
        config = RabbitMQConfig(
            host="rabbitmq.example.com",
            port=5672,
            virtual_host="/test",
            username="test-user",
            password="test-password",
            queue_prefix="test-prefix",
        )

        assert config.host == "rabbitmq.example.com"
        assert config.port == 5672
        assert config.virtual_host == "/test"
        assert config.username == "test-user"
        assert config.password == "test-password"
        assert config.queue_prefix == "test-prefix"

    def test_default_values(self):
        """Test default values in RabbitMQConfig."""
        config = RabbitMQConfig()

        assert config.host == "localhost"
        assert config.port == 5672
        assert config.virtual_host == "/"
        assert config.username is None
        assert config.password is None
        assert config.queue_prefix == ""


class TestLLMModelConfig:
    """Tests for the LLMModelConfig model."""

    def test_valid_config(self):
        """Test creating a valid LLMModelConfig."""
        config = LLMModelConfig(
            type="anthropic",
            model_name="claude-3-opus-20240229",
            api_key="test-api-key",
            max_tokens=2000,
            temperature=0.5,
        )

        assert config.type == "anthropic"
        assert config.model_name == "claude-3-opus-20240229"
        assert config.api_key == "test-api-key"
        assert config.max_tokens == 2000
        assert config.temperature == 0.5

    def test_default_values(self):
        """Test default values in LLMModelConfig."""
        config = LLMModelConfig(type="anthropic", model_name="claude-3-opus-20240229")

        assert config.type == "anthropic"
        assert config.model_name == "claude-3-opus-20240229"
        assert config.api_key is None
        assert config.max_tokens == 1000
        assert config.temperature == 0.7

    def test_missing_required_fields(self):
        """Test validation error when required fields are missing."""
        with pytest.raises(ValidationError):
            LLMModelConfig()  # Missing type and model_name

        with pytest.raises(ValidationError):
            LLMModelConfig(type="anthropic")  # Missing model_name

        with pytest.raises(ValidationError):
            LLMModelConfig(model_name="claude-3-opus-20240229")  # Missing type

    def test_temperature_validation(self):
        """Test temperature validation."""
        # Valid temperature
        config = LLMModelConfig(
            type="anthropic", model_name="claude-3-opus-20240229", temperature=0.5
        )
        assert config.temperature == 0.5

        # Invalid temperature (too low)
        with pytest.raises(ValidationError):
            LLMModelConfig(
                type="anthropic", model_name="claude-3-opus-20240229", temperature=-0.1
            )

        # Invalid temperature (too high)
        with pytest.raises(ValidationError):
            LLMModelConfig(
                type="anthropic", model_name="claude-3-opus-20240229", temperature=1.1
            )


class TestLLMConfig:
    """Tests for the LLMConfig model."""

    def test_valid_config(self):
        """Test creating a valid LLMConfig."""
        config = LLMConfig(
            default_model="claude_default",
            models={
                "claude_default": LLMModelConfig(
                    type="anthropic",
                    model_name="claude-3-opus-20240229",
                    api_key="test-api-key",
                    max_tokens=2000,
                    temperature=0.5,
                ),
                "gpt4": LLMModelConfig(
                    type="openai",
                    model_name="gpt-4",
                    api_key="test-openai-key",
                    max_tokens=1500,
                    temperature=0.7,
                ),
            },
            providers=LLMProvidersConfig(
                anthropic={"base_url": "https://api.anthropic.com"},
                openai={"base_url": "https://api.openai.com"},
            ),
        )

        assert config.default_model == "claude_default"
        assert len(config.models) == 2
        assert config.models["claude_default"].type == "anthropic"
        assert config.models["gpt4"].type == "openai"
        assert config.providers.anthropic == {"base_url": "https://api.anthropic.com"}
        assert config.providers.openai == {"base_url": "https://api.openai.com"}

    def test_default_values(self):
        """Test default values in LLMConfig."""
        config = LLMConfig(
            models={
                "claude_default": LLMModelConfig(
                    type="anthropic", model_name="claude-3-opus-20240229"
                )
            }
        )

        assert config.default_model == "claude_default"
        assert len(config.models) == 1
        assert config.providers is None

    def test_missing_required_fields(self):
        """Test validation error when required fields are missing."""
        with pytest.raises(ValidationError):
            LLMConfig()  # Missing models

        with pytest.raises(ValidationError):
            LLMConfig(default_model="claude_default")  # Missing models


class TestAppConfig:
    """Tests for the AppConfig model."""

    def test_valid_config(self):
        """Test creating a valid AppConfig."""
        config = AppConfig(
            app_name="podcast-ai-component",
            environment="production",
            log_level="INFO",
            s3=S3Config(
                endpoint_url="https://s3.example.com",
                region_name="us-west-2",
                access_key="test-access-key",
                secret_key="test-secret-key",
                default_bucket="test-bucket",
            ),
            rabbitmq=RabbitMQConfig(
                host="rabbitmq.example.com",
                port=5672,
                virtual_host="/test",
                username="test-user",
                password="test-password",
                queue_prefix="test-prefix",
            ),
            llm=LLMConfig(
                default_model="claude_default",
                models={
                    "claude_default": LLMModelConfig(
                        type="anthropic",
                        model_name="claude-3-opus-20240229",
                        api_key="test-api-key",
                    )
                },
            ),
            additional_config={"feature_flags": {"enable_new_feature": True}},
        )

        assert config.app_name == "podcast-ai-component"
        assert config.environment == "production"
        assert config.log_level == "INFO"
        assert config.s3.endpoint_url == "https://s3.example.com"
        assert config.rabbitmq.host == "rabbitmq.example.com"
        assert config.llm.default_model == "claude_default"
        assert config.additional_config["feature_flags"]["enable_new_feature"] is True

    def test_default_values(self):
        """Test default values in AppConfig."""
        config = AppConfig(
            app_name="podcast-ai-component",
            s3=S3Config(
                endpoint_url="https://s3.example.com", default_bucket="test-bucket"
            ),
            rabbitmq=RabbitMQConfig(),
            llm=LLMConfig(
                models={
                    "claude_default": LLMModelConfig(
                        type="anthropic", model_name="claude-3-opus-20240229"
                    )
                }
            ),
        )

        assert config.app_name == "podcast-ai-component"
        assert config.environment == "development"  # Default value
        assert config.log_level == "INFO"  # Default value
        assert config.additional_config is None

    def test_missing_required_fields(self):
        """Test validation error when required fields are missing."""
        with pytest.raises(ValidationError):
            AppConfig()  # Missing all required fields

        with pytest.raises(ValidationError):
            AppConfig(
                app_name="podcast-ai-component",
                rabbitmq=RabbitMQConfig(),
                llm=LLMConfig(
                    models={
                        "claude_default": LLMModelConfig(
                            type="anthropic", model_name="claude-3-opus-20240229"
                        )
                    }
                ),
            )  # Missing s3


class TestLoadAppConfig:
    """Tests for the load_app_config function."""

    @patch("zc_podcastmaker_common.models._read_json_file")
    @patch("zc_podcastmaker_common.models._get_nested_value")
    def test_load_app_config_success(self, mock_get_nested_value, mock_read_json_file):
        """Test loading app config successfully."""
        # Mock configuration data
        config_data = {
            "app_name": "podcast-ai-component",
            "environment": "production",
            "log_level": "INFO",
            "s3": {
                "endpoint_url": "https://s3.example.com",
                "region_name": "us-west-2",
                "default_bucket": "test-bucket",
            },
            "rabbitmq": {
                "host": "rabbitmq.example.com",
                "port": 5672,
                "virtual_host": "/test",
                "queue_prefix": "test-prefix",
            },
            "llm": {
                "default_model": "claude_default",
                "models": {
                    "claude_default": {
                        "type": "anthropic",
                        "model_name": "claude-3-opus-20240229",
                        "max_tokens": 2000,
                        "temperature": 0.5,
                    }
                },
            },
        }

        # Mock secrets data (via _get_nested_value)
        def mock_get_nested_value_impl(data, key_path):
            if key_path == "s3.access_key":
                return "test-access-key"
            elif key_path == "s3.secret_key":
                return "test-secret-key"
            elif key_path == "rabbitmq.username":
                return "test-user"
            elif key_path == "rabbitmq.password":
                return "test-password"
            elif key_path == "llm.claude_default.api_key":
                return "test-api-key"
            return None

        mock_read_json_file.side_effect = [config_data, {}]  # config.json, secrets.json
        mock_get_nested_value.side_effect = mock_get_nested_value_impl

        # Test loading app config
        with patch.dict(os.environ, {}, clear=True):  # Ensure no environment variables
            config = load_app_config()

        assert config.app_name == "podcast-ai-component"
        assert config.environment == "production"
        assert config.s3.endpoint_url == "https://s3.example.com"
        assert config.s3.access_key == "test-access-key"
        assert config.rabbitmq.username == "test-user"
        assert config.llm.models["claude_default"].api_key == "test-api-key"

    @patch("zc_podcastmaker_common.models._read_json_file")
    @patch("zc_podcastmaker_common.models._get_nested_value")
    def test_load_app_config_with_env_vars(
        self, mock_get_nested_value, mock_read_json_file
    ):
        """Test loading app config with environment variables."""
        # Mock configuration data
        config_data = {
            "app_name": "podcast-ai-component",
            "environment": "production",
            "s3": {
                "endpoint_url": "https://s3.example.com",
                "default_bucket": "test-bucket",
            },
            "rabbitmq": {"host": "rabbitmq.example.com"},
            "llm": {
                "default_model": "claude_default",
                "models": {
                    "claude_default": {
                        "type": "anthropic",
                        "model_name": "claude-3-opus-20240229",
                    }
                },
            },
        }

        mock_read_json_file.side_effect = [config_data, {}]  # config.json, secrets.json
        mock_get_nested_value.return_value = None

        # Test loading app config with environment variables
        env_vars = {
            "APP_ENVIRONMENT": "staging",
            "APP_S3_REGION_NAME": "eu-west-1",
            "APP_RABBITMQ_PORT": "5673",
            "APP_LLM_DEFAULT_MODEL": "gpt4",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = load_app_config()

        assert config.app_name == "podcast-ai-component"
        assert config.environment == "staging"  # Overridden by env var
        assert config.s3.region_name == "eu-west-1"  # Overridden by env var
        assert config.rabbitmq.port == 5673  # Overridden by env var (converted to int)
        assert config.llm.default_model == "gpt4"  # Overridden by env var

    @patch("zc_podcastmaker_common.models._read_json_file")
    def test_load_app_config_missing_required(self, mock_read_json_file):
        """Test loading app config with missing required fields."""
        # Mock empty configuration data
        mock_read_json_file.side_effect = [{}, {}]  # config.json, secrets.json

        # Test loading app config with missing required fields
        with pytest.raises(ConfigValidationError):
            load_app_config()

    @patch("zc_podcastmaker_common.models._read_json_file")
    def test_load_app_config_exception(self, mock_read_json_file):
        """Test exception handling in load_app_config."""
        # Mock exception
        mock_read_json_file.side_effect = Exception("Test exception")

        # Test exception handling
        from zc_podcastmaker_common.errors import ConfigValidationError

        with pytest.raises(ConfigValidationError):
            load_app_config()

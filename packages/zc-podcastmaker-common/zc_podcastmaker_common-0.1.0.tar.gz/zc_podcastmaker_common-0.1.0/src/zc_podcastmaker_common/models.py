"""
Configuration Models Module

This module defines Pydantic models for configuration structures to ensure type
safety and validation.
These models represent the configuration structures used by the various
components of the podcast AI system.

Classes:
    S3Config: Configuration for S3-compatible object storage
    RabbitMQConfig: Configuration for RabbitMQ message broker
    LLMModelConfig: Configuration for a specific LLM model
    LLMProvidersConfig: Configuration for LLM providers
    LLMConfig: Overall LLM configuration
    AppConfig: Overall application configuration
"""

import logging
import os
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from zc_podcastmaker_common.config_manager import (
    CONFIG_BASE_PATH,
    SECRET_BASE_PATH,
    _get_nested_value,
    _read_json_file,
)
from zc_podcastmaker_common.errors import (
    ConfigValidationError,
    handle_error,
)

# Set up logging
logger = logging.getLogger(__name__)


class S3Config(BaseModel):
    """
    Configuration for S3-compatible object storage.
    """

    endpoint_url: str = Field(..., description="S3 endpoint URL")
    region_name: str = Field("us-east-1", description="S3 region name")
    access_key: str | None = Field(None, description="S3 access key")
    secret_key: str | None = Field(None, description="S3 secret key")
    default_bucket: str = Field(..., description="Default S3 bucket name")

    model_config = ConfigDict(extra="ignore")


class RabbitMQConfig(BaseModel):
    """
    Configuration for RabbitMQ message broker.
    """

    host: str = Field("localhost", description="RabbitMQ host")
    port: int = Field(5672, description="RabbitMQ port")
    virtual_host: str = Field("/", description="RabbitMQ virtual host")
    username: str | None = Field(None, description="RabbitMQ username")
    password: str | None = Field(None, description="RabbitMQ password")
    queue_prefix: str = Field("", description="Prefix for queue names")

    model_config = ConfigDict(extra="ignore")


class LLMModelConfig(BaseModel):
    """
    Configuration for a specific LLM model.
    """

    type: str = Field(
        ..., description="LLM provider type (e.g., 'anthropic', 'openai')"
    )
    model_name: str = Field(..., description="Model name or identifier")
    api_key: str | None = Field(None, description="API key for the LLM provider")
    max_tokens: int = Field(1000, description="Maximum number of tokens to generate")
    temperature: float = Field(0.7, description="Temperature for text generation")

    @field_validator("temperature")
    def validate_temperature(cls, v: float) -> float:
        """Validate that temperature is between 0 and 1."""
        if not (0 <= v <= 1):
            raise ValueError("Temperature must be between 0 and 1")
        return v

    model_config = ConfigDict(extra="ignore")


class LLMProvidersConfig(BaseModel):
    """
    Configuration for LLM providers.
    """

    anthropic: dict[str, Any] | None = Field(
        None, description="Anthropic-specific configuration"
    )
    openai: dict[str, Any] | None = Field(
        None, description="OpenAI-specific configuration"
    )

    model_config = ConfigDict(extra="ignore")


class LLMConfig(BaseModel):
    """
    Overall LLM configuration.
    """

    default_model: str = Field(
        "claude_default", description="Default model alias to use"
    )
    models: dict[str, LLMModelConfig] = Field(
        ..., description="Dictionary of model configurations by alias"
    )
    providers: LLMProvidersConfig | None = Field(
        None, description="Provider-specific configurations"
    )

    model_config = ConfigDict(extra="ignore")


class AppConfig(BaseModel):
    """
    Overall application configuration.
    """

    app_name: str = Field(..., description="Application name")
    environment: str = Field("development", description="Deployment environment")
    log_level: str = Field("INFO", description="Logging level")
    s3: S3Config = Field(..., description="S3 configuration")
    rabbitmq: RabbitMQConfig = Field(..., description="RabbitMQ configuration")
    llm: LLMConfig = Field(..., description="LLM configuration")

    # Additional application-specific configuration
    additional_config: dict[str, Any] | None = Field(
        None, description="Additional configuration"
    )

    model_config = ConfigDict(extra="ignore")


def _load_base_config() -> dict:
    config_file = CONFIG_BASE_PATH / "config.json"
    return _read_json_file(config_file) or {}


def _load_secrets() -> dict:
    secrets_file = SECRET_BASE_PATH / "secrets.json"
    return _read_json_file(secrets_file) or {}


def _merge_s3_secrets(merged_data: dict, secrets_data: dict) -> None:
    if "s3" not in merged_data:
        merged_data["s3"] = {}
    s3_access_key = _get_nested_value(secrets_data, "s3.access_key")
    s3_secret_key = _get_nested_value(secrets_data, "s3.secret_key")
    if s3_access_key:
        merged_data["s3"]["access_key"] = s3_access_key
    if s3_secret_key:
        merged_data["s3"]["secret_key"] = s3_secret_key


def _merge_rabbitmq_secrets(merged_data: dict, secrets_data: dict) -> None:
    if "rabbitmq" not in merged_data:
        merged_data["rabbitmq"] = {}
    rabbitmq_username = _get_nested_value(secrets_data, "rabbitmq.username")
    rabbitmq_password = _get_nested_value(secrets_data, "rabbitmq.password")
    if rabbitmq_username:
        merged_data["rabbitmq"]["username"] = rabbitmq_username
    if rabbitmq_password:
        merged_data["rabbitmq"]["password"] = rabbitmq_password


def _merge_llm_secrets(merged_data: dict, secrets_data: dict) -> None:
    if "llm" not in merged_data:
        merged_data["llm"] = {"models": {}}
    elif "models" not in merged_data["llm"]:
        merged_data["llm"]["models"] = {}
    for model_alias, model_config_data in merged_data["llm"].get("models", {}).items():
        api_key_path = f"llm.{model_alias}.api_key"
        api_key = _get_nested_value(secrets_data, api_key_path)
        if api_key and isinstance(model_config_data, dict):
            model_config_data["api_key"] = api_key


def _merge_secrets_into_config(config_data: dict, secrets_data: dict) -> dict:
    merged_data = config_data.copy()
    _merge_s3_secrets(merged_data, secrets_data)
    _merge_rabbitmq_secrets(merged_data, secrets_data)
    _merge_llm_secrets(merged_data, secrets_data)
    return merged_data


def _apply_special_env_override(
    env_name: str, env_value: str, merged_data: dict
) -> bool:
    if env_name == "APP_S3_REGION_NAME":
        if "s3" not in merged_data:
            merged_data["s3"] = {}
        merged_data["s3"]["region_name"] = env_value
        return True
    elif env_name == "APP_LLM_DEFAULT_MODEL":
        if "llm" not in merged_data:
            merged_data["llm"] = {"models": {}}
        merged_data["llm"]["default_model"] = env_value
        return True
    return False


def _apply_general_env_override(
    env_name: str, env_value: str, merged_data: dict
) -> None:
    config_path = env_name[4:].lower().replace("_", ".")
    keys = config_path.split(".")
    current = merged_data
    for i, key in enumerate(keys):
        if i == len(keys) - 1:
            if key == "port" and env_value.isdigit():
                current[key] = int(env_value)
            else:
                current[key] = env_value
        else:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]


def _apply_env_overrides(merged_data: dict) -> dict:
    for env_name, env_value in os.environ.items():
        if env_name.startswith("APP_"):
            # Marcar las variables específicas para asegurar que se procesen
            # correctamente
            if _apply_special_env_override(env_name, env_value, merged_data):
                continue
            _apply_general_env_override(env_name, env_value, merged_data)
    return merged_data


def _finalize_app_config(merged_data: dict) -> AppConfig:
    try:
        return AppConfig(**merged_data)
    except Exception as e:
        raise ConfigValidationError(
            f"Invalid application configuration: {str(e)}",
            details={"config_data": merged_data},
        ) from e


def load_app_config() -> AppConfig:
    """
    Load application configuration from files and environment variables.
    """
    try:
        config_data = _load_base_config()
        secrets_data = _load_secrets()
        merged_data = _merge_secrets_into_config(config_data, secrets_data)
        merged_data = _apply_env_overrides(merged_data)
        return _finalize_app_config(merged_data)
    except Exception as e:
        handle_error(
            func_name="load_app_config",
            error=e,
            error_class=ConfigValidationError,
            message="Error loading application configuration",
            raise_error=True,
        )
        raise AssertionError(
            "Should be unreachable as handle_error will raise"
        ) from None

# mypy: disable-error-code=arg-type
"""
Generative LLM Client Module

This module provides a simplified interface for making calls to generative
language models (initially focused on Anthropic Claude). The specific model
configuration (e.g., API key, model identifier) is obtained through the
config_manager using a model alias.

Functions:
    _get_llm_config: Get LLM configuration for a specific model alias
    get_text_completion: Get a text completion from a generative LLM
    _get_anthropic_completion: Get a text completion from Anthropic Claude
"""

import logging
import time
from typing import Any

# Import Anthropic client for Claude
import anthropic  # type: ignore

from zc_podcastmaker_common import config_manager
from zc_podcastmaker_common.errors import (
    LLMAuthenticationError,
    LLMError,
    LLMRateLimitError,
    LLMResponseError,
    handle_error,
)

# Set up logging
logger = logging.getLogger(__name__)


def _get_llm_config(model_alias: str) -> dict[str, Any]:
    """
    Get LLM configuration for a specific model alias.

    Args:
        model_alias: Alias of the model to use (e.g., "claude_default")

    Returns:
        dict[str, Any]: Dictionary with the model configuration

    Raises:
        LLMError: If there's an error retrieving the configuration
    """
    try:
        model_type = config_manager.get_config_value(
            f"llm.{model_alias}.type", "anthropic"
        )
        model_name = config_manager.get_config_value(
            f"llm.{model_alias}.model_name", "claude-3-opus-20240229"
        )
        max_tokens = config_manager.get_config_value(
            f"llm.{model_alias}.max_tokens", 1000
        )
        temperature = config_manager.get_config_value(
            f"llm.{model_alias}.temperature", 0.7
        )

        # Get API key from secrets
        api_key = config_manager.get_secret_value(f"llm.{model_alias}.api_key")

        if not api_key:  # This will be a string or None
            raise LLMAuthenticationError(
                f"Missing API key for model alias: {model_alias}",
                details={
                    "model_alias": model_alias,
                    "provider": "anthropic (config)",
                },  # Corrected details
            )

        return {
            "type": model_type,
            "model_name": model_name,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "api_key": api_key,
        }
    except LLMError:  # Includes LLMAuthenticationError
        # Re-raise LLMError exceptions
        raise
    except Exception as e:
        # This will now primarily catch errors from config_manager if they are not
        # PodcastMakerErrors
        handle_error(
            func_name="_get_llm_config",
            error=e,
            error_class=LLMError,  # General LLMError for unexpected issues in
            # config retrieval
            message=(
                f"Unexpected error getting LLM configuration for model alias: "
                f"{model_alias}"
            ),
            details={"model_alias": model_alias},  # Pass original details
            raise_error=True,
        )
        # This line should be unreachable due to handle_error raising
        raise AssertionError(
            "Should be unreachable as handle_error will raise"
        ) from None


def get_text_completion(
    prompt: str,
    model_alias: str = "claude_default",
    params: dict[str, Any] | None = None,
    max_retries: int = 3,
) -> str | None:
    """
    Get a text completion from a generative LLM.
    """
    config = _get_llm_config(
        model_alias
    )  # Can raise LLMAuthenticationError or LLMError
    model_type = config["type"]

    retry_count = 0
    last_error = None

    while retry_count <= max_retries:
        try:
            if model_type == "anthropic":
                return _get_anthropic_completion(prompt, model_alias, params)
            else:
                # No pasar por el bucle de reintentos para modelos no soportados
                # Lo lanzamos directamente para que el test pueda verificar el
                # mensaje exacto
                raise LLMError(
                    f"Unsupported model type: {model_type}",
                    model_alias=model_alias,
                    provider=model_type,
                )
        except LLMError:
            raise
        except Exception as e:
            last_error = e
            retry_count += 1
            if retry_count > max_retries:
                break
            wait_time = min(2**retry_count + (0.1 * retry_count), 60)
            logger.warning(
                f"Error getting text completion (attempt {retry_count}/{max_retries}): "
                f"{str(e)}. "
                f"Retrying in {wait_time:.2f} seconds..."
            )
            time.sleep(wait_time)

    if last_error is not None:
        handle_error(
            func_name="get_text_completion",
            error=last_error,
            error_class=LLMError,
            message=(f"Failed to get text completion after {max_retries} retries"),
            details={
                "model_alias": model_alias,
                "model_type": model_type,
                "retry_count": retry_count,
            },
            raise_error=True,
        )
        raise AssertionError(
            "Should be unreachable as handle_error will raise"
        ) from None

    return None


def _get_anthropic_completion(
    prompt: str, model_alias: str, params: dict[str, Any] | None = None
) -> str | None:
    """
    Get a text completion from Anthropic Claude.
    """
    config = _get_llm_config(model_alias)

    api_key = config.get(
        "api_key"
    )  # Use .get for safety from _get_llm_config if it was mocked
    model_name = config.get("model_name")
    max_tokens = config.get("max_tokens")
    temperature = config.get("temperature")

    # If api_key is still None here, _get_llm_config did not raise
    # LLMAuthenticationError as expected or it was mocked to return api_key: None.
    if not api_key:
        raise LLMAuthenticationError(
            f"API key is missing or invalid for model alias: {model_alias} "
            f"(checked in _get_anthropic_completion)",
            details={
                "model_alias": model_alias,
                "provider": "anthropic",
                "original_error": "API key was None.",
            },
        )

    request_params = {"max_tokens": max_tokens, "temperature": temperature}
    if params:
        request_params.update(params)

    try:
        logger.debug(f"Calling Anthropic API with model: {model_name}")
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            **request_params,
        )  # type: ignore
        logger.debug("Successfully received response from Anthropic API")
        return message.content[0].text  # type: ignore
    except TypeError as e:
        if "None is not a valid API key" in str(
            e
        ) or "Could not resolve authentication method" in str(e):
            raise LLMAuthenticationError(
                f"Anthropic client failed due to invalid API key for model alias "
                f"{model_alias}: {str(e)}",
                details={
                    "model_alias": model_alias,
                    "provider": "anthropic",
                    "original_error": str(e),
                    "error_type": type(e).__name__,
                },
            ) from e
        # For other TypeErrors, let them be caught by the generic Exception
        # handler below
        raise LLMError(
            f"TypeError during Anthropic API call for model alias {model_alias}: "
            f"{str(e)}",
            details={
                "model_alias": model_alias,
                "provider": "anthropic",
                "original_error": str(e),
                "error_type": type(e).__name__,
            },
        ) from e
    except anthropic.AuthenticationError as e:
        raise LLMAuthenticationError(
            f"Anthropic API authentication error for model alias {model_alias}: "
            f"{str(e)}",
            details={
                "model_alias": model_alias,
                "provider": "anthropic",
                "original_error": str(e),
                "error_type": type(e).__name__,
            },
        ) from e
    except anthropic.RateLimitError as e:
        raise LLMRateLimitError(
            f"Anthropic API rate limit exceeded for model alias {model_alias}: "
            f"{str(e)}",
            details={
                "model_alias": model_alias,
                "provider": "anthropic",
                "original_error": str(e),
                "error_type": type(e).__name__,
            },
        ) from e
    except anthropic.APIError as e:
        raise LLMResponseError(
            f"Anthropic API error for model alias {model_alias}: {str(e)}",
            details={
                "model_alias": model_alias,
                "provider": "anthropic",
                "original_error": str(e),
                "error_type": type(e).__name__,
            },
        ) from e
    except Exception as e:
        handle_error(
            func_name="_get_anthropic_completion",
            error=e,
            error_class=LLMError,
            message=(
                f"Unexpected error calling Anthropic API for model alias {model_alias}"
            ),  # More specific message
            details={
                "model_alias": model_alias,
                "model_name": model_name,  # model_name might be None if config was bad
                "provider": "anthropic",
                # original_error and error_type will be added by handle_error
            },
            raise_error=True,
        )
        raise AssertionError(
            "Should be unreachable as handle_error will raise"
        ) from None

"""
Tests for the generative_llm_client module.
"""

from unittest.mock import MagicMock, call, patch

import pytest

from zc_podcastmaker_common.errors import LLMAuthenticationError, LLMError
from zc_podcastmaker_common.generative_llm_client import (
    _get_anthropic_completion,
    _get_llm_config,
    get_text_completion,
)


class TestGenerativeLLMClient:
    """Tests for the generative_llm_client module."""

    @patch("zc_podcastmaker_common.config_manager.get_config_value")
    @patch("zc_podcastmaker_common.config_manager.get_secret_value")
    def test_get_llm_config(self, mock_get_secret_value, mock_get_config_value):
        """Test getting LLM configuration."""
        mock_get_config_value.side_effect = lambda key, default: {
            "llm.claude_default.type": "anthropic",
            "llm.claude_default.model_name": "claude-3-opus-20240229",
            "llm.claude_default.max_tokens": 1000,
            "llm.claude_default.temperature": 0.7,
        }.get(key, default)
        mock_get_secret_value.return_value = "test_api_key"

        config = _get_llm_config("claude_default")
        assert config == {
            "type": "anthropic",
            "model_name": "claude-3-opus-20240229",
            "max_tokens": 1000,
            "temperature": 0.7,
            "api_key": "test_api_key",
        }

    @patch("zc_podcastmaker_common.config_manager.get_config_value")
    @patch("zc_podcastmaker_common.config_manager.get_secret_value")
    def test_get_llm_config_direct(self, mock_get_secret_value, mock_get_config_value):
        """Test getting LLM configuration directly from config manager."""
        mock_get_config_value.side_effect = lambda key, default: {
            "llm.claude_default.type": "anthropic",
            "llm.claude_default.model_name": "claude-3-opus-20240229",
            "llm.claude_default.max_tokens": 1000,
            "llm.claude_default.temperature": 0.7,
        }.get(key, default)
        mock_get_secret_value.return_value = "test_api_key"

        config = _get_llm_config("claude_default")
        assert config == {
            "type": "anthropic",
            "model_name": "claude-3-opus-20240229",
            "max_tokens": 1000,
            "temperature": 0.7,
            "api_key": "test_api_key",
        }
        mock_get_config_value.assert_has_calls(
            [
                call("llm.claude_default.type", "anthropic"),
                call("llm.claude_default.model_name", "claude-3-opus-20240229"),
                call("llm.claude_default.max_tokens", 1000),
                call("llm.claude_default.temperature", 0.7),
            ]
        )
        mock_get_secret_value.assert_called_once_with("llm.claude_default.api_key")

    @patch("zc_podcastmaker_common.generative_llm_client._get_anthropic_completion")
    @patch("zc_podcastmaker_common.generative_llm_client._get_llm_config")
    def test_get_text_completion_anthropic(
        self, mock_get_llm_config, mock_get_anthropic_completion
    ):
        mock_get_llm_config.return_value = {
            "type": "anthropic",
            "model_name": "claude-3-opus-20240229",
            "max_tokens": 1000,
            "temperature": 0.7,
            "api_key": "test_api_key",
        }
        mock_get_anthropic_completion.return_value = "Generated text response"
        result = get_text_completion("Test prompt", "claude_default")
        assert result == "Generated text response"
        mock_get_anthropic_completion.assert_called_once_with(
            "Test prompt", "claude_default", None
        )
        mock_get_llm_config.assert_called_once_with("claude_default")

    @patch("zc_podcastmaker_common.generative_llm_client._get_anthropic_completion")
    @patch("zc_podcastmaker_common.generative_llm_client._get_llm_config")
    def test_get_text_completion_unsupported_model(
        self, mock_get_llm_config, mock_get_anthropic_completion
    ):
        mock_get_llm_config.return_value = {
            "type": "unsupported_model",
            "model_name": "unsupported-model",
            "max_tokens": 1000,
            "temperature": 0.7,
            "api_key": "test_api_key",
        }
        with pytest.raises(LLMError) as excinfo:
            get_text_completion("Test prompt", "unsupported_model")
        assert "Unsupported model type: unsupported_model" in str(excinfo.value)
        mock_get_anthropic_completion.assert_not_called()

    @patch("time.sleep")
    @patch("zc_podcastmaker_common.generative_llm_client._get_anthropic_completion")
    @patch("zc_podcastmaker_common.generative_llm_client._get_llm_config")
    def test_get_text_completion_with_retries(
        self, mock_get_llm_config, mock_get_anthropic_completion, mock_sleep
    ):
        mock_get_llm_config.return_value = {
            "type": "anthropic",
            "model_name": "claude-3-opus-20240229",
            "max_tokens": 1000,
            "temperature": 0.7,
            "api_key": "test_api_key",
        }
        mock_get_anthropic_completion.side_effect = [
            Exception("API error"),
            Exception("API error"),
            "Generated text response",
        ]
        result = get_text_completion("Test prompt", "claude_default", max_retries=3)
        assert result == "Generated text response"
        assert mock_get_anthropic_completion.call_count == 3
        assert mock_sleep.call_count == 2

    @patch("time.sleep")
    @patch("zc_podcastmaker_common.generative_llm_client._get_anthropic_completion")
    @patch("zc_podcastmaker_common.generative_llm_client._get_llm_config")
    def test_get_text_completion_max_retries_exceeded(
        self, mock_get_llm_config, mock_get_anthropic_completion, mock_sleep
    ):
        mock_get_llm_config.return_value = {
            "type": "anthropic",
            "model_name": "claude-3-opus-20240229",
            "max_tokens": 1000,
            "temperature": 0.7,
            "api_key": "test_api_key",
        }
        mock_get_anthropic_completion.side_effect = Exception("API error")
        with pytest.raises(LLMError) as excinfo:
            get_text_completion("Test prompt", "claude_default", max_retries=2)
        assert "Failed to get text completion after 2 retries" in str(excinfo.value)
        assert mock_get_anthropic_completion.call_count == 3
        assert mock_sleep.call_count == 2

    @patch("zc_podcastmaker_common.generative_llm_client._get_llm_config")
    def test_get_anthropic_completion_missing_api_key(self, mock_get_llm_config):
        mock_get_llm_config.return_value = {
            "type": "anthropic",
            "model_name": "claude-3-opus-20240229",
            "max_tokens": 1000,
            "temperature": 0.7,
            "api_key": None,
        }
        with pytest.raises(LLMAuthenticationError) as excinfo:
            _get_anthropic_completion("Test prompt", "claude_default")

        assert (
            "API key is missing or invalid for model alias: "
            "claude_default (checked in _get_anthropic_completion)"
            in str(excinfo.value)
        )
        assert excinfo.value.details.get("original_error") == "API key was None."

    @patch("anthropic.Anthropic")
    @patch("zc_podcastmaker_common.generative_llm_client._get_llm_config")
    def test_get_anthropic_completion_success(
        self, mock_get_llm_config, mock_anthropic
    ):
        mock_get_llm_config.return_value = {
            "type": "anthropic",
            "model_name": "claude-3-opus-20240229",
            "max_tokens": 1000,
            "temperature": 0.7,
            "api_key": "test_api_key",
        }
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        message_response = MagicMock()
        content_item = MagicMock()
        content_item.text = "Generated text response"
        message_response.content = [content_item]
        mock_client.messages.create.return_value = message_response
        result = _get_anthropic_completion("Test prompt", "claude_default")
        assert result == "Generated text response"
        mock_anthropic.assert_called_once_with(api_key="test_api_key")
        mock_client.messages.create.assert_called_once_with(
            model="claude-3-opus-20240229",
            messages=[{"role": "user", "content": "Test prompt"}],
            max_tokens=1000,
            temperature=0.7,
        )

    @patch("anthropic.Anthropic")
    @patch("zc_podcastmaker_common.generative_llm_client._get_llm_config")
    def test_get_anthropic_completion_with_params(
        self, mock_get_llm_config, mock_anthropic
    ):
        mock_get_llm_config.return_value = {
            "type": "anthropic",
            "model_name": "claude-3-opus-20240229",
            "max_tokens": 1000,
            "temperature": 0.7,
            "api_key": "test_api_key",
        }
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        message_response = MagicMock()
        content_item = MagicMock()
        content_item.text = "Generated text response"
        message_response.content = [content_item]
        mock_client.messages.create.return_value = message_response
        custom_params = {"max_tokens": 2000, "temperature": 0.5, "top_p": 0.9}
        result = _get_anthropic_completion(
            "Test prompt", "claude_default", custom_params
        )
        assert result == "Generated text response"
        mock_anthropic.assert_called_once_with(api_key="test_api_key")
        mock_client.messages.create.assert_called_once_with(
            model="claude-3-opus-20240229",
            messages=[{"role": "user", "content": "Test prompt"}],
            max_tokens=2000,
            temperature=0.5,
            top_p=0.9,
        )

    @patch("anthropic.Anthropic")
    @patch("zc_podcastmaker_common.generative_llm_client._get_llm_config")
    def test_get_anthropic_completion_exception(
        self, mock_get_llm_config, mock_anthropic
    ):
        mock_get_llm_config.return_value = {
            "type": "anthropic",
            "model_name": "claude-3-opus-20240229",
            "max_tokens": 1000,
            "temperature": 0.7,
            "api_key": "test_api_key",
        }
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.side_effect = Exception("API error")

        with pytest.raises(LLMError) as excinfo:
            _get_anthropic_completion("Test prompt", "claude_default")

        assert (
            "Unexpected error calling Anthropic API for model alias claude_default"
            in str(excinfo.value)
        )
        assert excinfo.value.details["original_error"] == "API error"
        assert excinfo.value.details["error_type"] == "Exception"
        assert excinfo.value.details["model_alias"] == "claude_default"

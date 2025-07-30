"""
zc-podcastmaker-common - Common utilities library for PodcastMaker components.

This package provides shared functionality for all PodcastMaker components, including:
- Configuration management
- Object storage client
- Generative LLM client
- Message bus client
- Configuration models (Pydantic)
- Error handling and custom exceptions
- Logging configuration utilities
"""

__version__ = "0.1.0"

# Import logging configuration for easier access
from zc_podcastmaker_common.logging import configure_logging

# Configure default logging
configure_logging()

# -------------------------------------------------------------------------------- #
# Supported Models Constants
# -------------------------------------------------------------------------------- #

"""
Constants for supported models.

This module contains the constants for the supported models.
"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in imports
from typing import List, Dict

# Project-specific imports
from astral_ai.typing.models import ModelName

# -------------------------------------------------------------------------------- #
# Constants
# -------------------------------------------------------------------------------- #

MODEL_ALIASES: Dict[ModelName, str] = {
    "claude-3-5-haiku-20241022": "claude-3-haiku",
    "claude-3-5-sonnet-20241022": "claude-3-5-sonnet",
    "claude-3-opus-20240229": "claude-3-opus",
    "gpt-4o-01-10-24": "gpt-4o",
    "gpt-4o-01-15-24": "gpt-4o",
    "gpt-4o-12-17-24": "gpt-4o",
    "o1-01-10-24": "o1",
    "o1-01-15-24": "o1",
    "o1-12-17-24": "o1",
    "o1-mini-01-10-24": "o1-mini",
    "o1-mini-01-15-24": "o1-mini",
    "o1-mini-12-17-24": "o1-mini",
    "o3-mini-2025-01-31": "o3-mini",
}

REASONING_EFFORT_SUPPORTED_MODELS: List[ModelName] = [
    "o1",
    "o1-01-10-24",
    "o1-01-15-24",
    "o1-12-17-24",
    "o3-mini",
    "o3-mini-2025-01-31",
]

STRUCTURED_OUTPUT_SUPPORTED_MODELS: List[ModelName] = [
    "claude-3-5-haiku-20241022",
    "claude-3-5-sonnet",
    "claude-3-5-sonnet-20241022",
    "claude-3-haiku",
    "claude-3-opus",
    "claude-3-opus-20240229",
    "gpt-4o",
    "gpt-4o-01-10-24",
    "gpt-4o-01-15-24",
    "gpt-4o-12-17-24",
    "o1",
    "o1-01-10-24",
    "o1-01-15-24",
    "o1-12-17-24",
    "o1-mini",
    "o1-mini-01-10-24",
    "o1-mini-01-15-24",
    "o1-mini-12-17-24",
    "o3-mini",
    "o3-mini-2025-01-31",
]

IMAGE_INGESTION_SUPPORTED_MODELS: List[ModelName] = [
    "claude-3-5-sonnet",
    "claude-3-5-sonnet-20241022",
    "claude-3-opus",
    "claude-3-opus-20240229",
    "gpt-4o",
    "gpt-4o-01-10-24",
    "gpt-4o-01-15-24",
    "gpt-4o-12-17-24",
    "o1",
    "o1-01-10-24",
    "o1-01-15-24",
    "o1-12-17-24",
]

FUNCTION_CALL_SUPPORTED_MODELS: List[ModelName] = [
    "claude-3-5-haiku-20241022",
    "claude-3-5-sonnet",
    "claude-3-5-sonnet-20241022",
    "claude-3-haiku",
    "claude-3-opus",
    "claude-3-opus-20240229",
    "gpt-4o",
    "gpt-4o-01-10-24",
    "gpt-4o-01-15-24",
    "gpt-4o-12-17-24",
    "o1",
    "o1-01-10-24",
    "o1-01-15-24",
    "o1-12-17-24",
    "o1-mini",
    "o1-mini-01-10-24",
    "o1-mini-01-15-24",
    "o1-mini-12-17-24",
    "o3-mini",
    "o3-mini-2025-01-31",
]

SYSTEM_MESSAGE_SUPPORTED_MODELS: List[ModelName] = [
    "claude-3-5-sonnet",
    "claude-3-5-sonnet-20241022",
    "claude-3-opus",
    "claude-3-opus-20240229",
    "gpt-4o",
    "gpt-4o-01-10-24",
    "gpt-4o-01-15-24",
    "gpt-4o-12-17-24",
]

DEVELOPER_MESSAGE_SUPPORTED_MODELS: List[ModelName] = [
    "o1",
    "o1-01-10-24",
    "o1-01-15-24",
    "o1-12-17-24",
    "o3-mini",
    "o3-mini-2025-01-31",
]

ONLY_USER_MESSAGE_SUPPORTED_MODELS: List[ModelName] = [
    "claude-3-5-haiku-20241022",
    "claude-3-haiku",
    "o1-mini",
    "o1-mini-01-10-24",
    "o1-mini-01-15-24",
    "o1-mini-12-17-24",
]

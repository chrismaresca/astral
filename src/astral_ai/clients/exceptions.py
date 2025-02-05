# -------------------------------------------------------------------------------- #
#  Agent Exceptions
# -------------------------------------------------------------------------------- #

"""
Agent Exceptions

This module contains the exceptions that are raised by the agent when a requested
feature is not supported by a model. It also provides helper functions to check
if a model supports a given feature.
"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in
from typing import List, Any

# Project
from astral_ai.constants.supported_models import (
    REASONING_EFFORT_SUPPORTED_MODELS,
    IMAGE_INGESTION_SUPPORTED_MODELS,
    FUNCTION_CALL_SUPPORTED_MODELS,
    STRUCTURED_OUTPUT_SUPPORTED_MODELS,
)
from astral_ai.typing.models import ModelName

# -------------------------------------------------------------------------------- #
# Helper Function
# -------------------------------------------------------------------------------- #


def get_model_message_not_supported_error(model_name: ModelName, supported_models: List[ModelName]) -> str:
    """
    Get the error message for a model that does not support a feature.

    Args:
        model_name: The model name that does not support the feature.
        supported_models: The list of model names that support the feature.

    Returns:
        A formatted error message.
    """
    return (
        f"Feature not supported for model '{model_name}'. "
        f"This feature is only supported for the following models: {', '.join(supported_models)}."
    )


# -------------------------------------------------------------------------------- #
# LLM Client Exceptions
# -------------------------------------------------------------------------------- #

class LLMResponseError(Exception):
    """
    Exception raised for errors in the LLM response.
    """

    def __init__(self, message: str = "An error occurred in the LLM response."):
        self.message = message
        super().__init__(self.message)

class LLMResponseParseError(Exception):
    """
    Exception raised for errors in the LLM response parsing.
    """

    def __init__(self, message: str = "An error occurred in the LLM response parsing."):
        self.message = message
        super().__init__(self.message)

class LLMResponseCompletionError(Exception):
    """
    Exception raised for errors in the LLM response completion.
    """

    def __init__(self, message: str = "An error occurred in the LLM response parsing."):
        self.message = message
        super().__init__(self.message)
# class AsyncClientError(Exception):
#     """
#     Exception raised for errors in the async client.
#     """

#     def __init__(self, message: str = "Async method called on sync client."):
#         self.message = message
#         super().__init__(self.message)


# class SyncClientError(Exception):
#     """
#     Exception raised for errors in the sync client.
#     """

#     def __init__(self, message: str = "Sync method called on async client."):
#         self.message = message
#         super().__init__(self.message)

# -------------------------------------------------------------------------------- #
# Model Feature Not Supported Exceptions
# -------------------------------------------------------------------------------- #


class StructuredOutputNotSupportedError(Exception):
    """Exception raised when the structured output feature is not supported by the model."""

    def __init__(self, model_name: ModelName):
        self.message = get_model_message_not_supported_error(model_name, STRUCTURED_OUTPUT_SUPPORTED_MODELS)
        super().__init__(self.message)


class ReasoningEffortNotSupportedError(Exception):
    """Exception raised when the reasoning effort feature is not supported by the model."""

    def __init__(self, model_name: ModelName):
        self.message = get_model_message_not_supported_error(model_name, REASONING_EFFORT_SUPPORTED_MODELS)
        super().__init__(self.message)


class ImageIngestionNotSupportedError(Exception):
    """Exception raised when the image ingestion feature is not supported by the model."""

    def __init__(self, model_name: ModelName):
        self.message = get_model_message_not_supported_error(model_name, IMAGE_INGESTION_SUPPORTED_MODELS)
        super().__init__(self.message)


class ToolsNotSupportedError(Exception):
    """Exception raised when the tool feature is not supported by the model."""

    def __init__(self, model_name: ModelName):
        self.message = get_model_message_not_supported_error(model_name, FUNCTION_CALL_SUPPORTED_MODELS)
        super().__init__(self.message)


class InvalidToolError(Exception):
    """Exception raised when the tool is invalid."""

    def __init__(self, invalid_tools: List[Any]):
        self.message = f"Invalid tools provided: {invalid_tools}"
        super().__init__(self.message)


# -------------------------------------------------------------------------------- #
# Message Handling Exceptions
# -------------------------------------------------------------------------------- #


class MessagesNotProvidedError(Exception):
    """Exception raised when no messages are provided to the model."""

    def __init__(self, model_name: ModelName):
        self.message = f"No messages provided to the model {model_name}."
        super().__init__(self.message)


class InvalidMessageError(Exception):
    """Exception raised when the message is invalid."""

    def __init__(self, message_type: str):
        self.message = f"Invalid message or message list type provided: {message_type}"
        super().__init__(self.message)

class InvalidMessageRoleError(Exception):
    """Exception raised when the message role is invalid."""

    def __init__(self, message: str = "Invalid message role provided."):
        self.message = message
        super().__init__(self.message)

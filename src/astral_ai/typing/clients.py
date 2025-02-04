# -------------------------------------------------------------------------------- #
# LLM Client Types
# -------------------------------------------------------------------------------- #

"""
This module contains the types for the LLM client.
"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in imports
from typing import TypeAlias, TypeVar

# OpenAI imports
from openai import OpenAI, AsyncOpenAI, AzureOpenAI, AsyncAzureOpenAI

# Anthropic imports
# from anthropic import Anthropic, AsyncAnthropic

# -------------------------------------------------------------------------------- #
# LLM Client Types
# -------------------------------------------------------------------------------- #

# OpenAI LLM Client Type
type OpenAILLMClientT =  OpenAI | AsyncOpenAI

# Azure LLM Client Type
type AzureLLMClientT = AzureOpenAI | AsyncAzureOpenAI

# LLM Client Type
type LLMClientT = OpenAILLMClientT | AzureLLMClientT


# -------------------------------------------------------------------------------- #
# LLM Client Types
# -------------------------------------------------------------------------------- #

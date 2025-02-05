# -------------------------------------------------------------------------------- #
# Provider Params
# -------------------------------------------------------------------------------- #

"""

This module contains the base call parameters for LLM calls.

"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in imports
from typing import List, Optional, Dict, Any, TypedDict, overload, Literal

# Pydantic imports
from pydantic import BaseModel, Field

# Astral AI imports
from astral_ai.typing.messages import MessageListT, Message
from astral_ai.typing.models import ModelName
from astral_ai.clients.types import (
    ReasoningEffort,
    Tool,
    ToolChoiceOption,
)


# Model Provider
from astral_ai.typing.models import ModelProvider


# -------------------------------------------------------------------------------- #
# Base LLM Call Params
# -------------------------------------------------------------------------------- #


class BaseLLMCallParams(BaseModel):
    """
    Base call parameters for LLM calls.
    """
    messages: MessageListT = Field(description="The messages to be sent to the LLM.")
    model: ModelName = Field(description="The model to be used for the LLM call.")
    user: Optional[str] = Field(description="The user to be used for the LLM call.")
    tools: Optional[List[Tool]] = Field(description="The tools to be used for the LLM call.")
    tool_choice: Optional[ToolChoiceOption] = Field(description="The tool choice to be used for the LLM call.")
    reasoning_effort: Optional[ReasoningEffort] = Field(description="The reasoning effort to be used for the LLM call.")


# -------------------------------------------------------------------------------- #
# Validated Base LLM Call Params
# -------------------------------------------------------------------------------- #


class ValidatedBaseLLMCallParams(BaseLLMCallParams):
    """
    Validated base call parameters for LLM calls.
    """
    messages: List[Message]
    tool_choice: ToolChoiceOption


# -------------------------------------------------------------------------------- #
# Provider Params
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# OpenAI Params and Overloads
# -------------------------------------------------------------------------------- #

class OpenAICompletionParams(TypedDict):
    messages: List[Dict[str, Any]]
    model: ModelName
    user: Optional[str]
    tools: Optional[List]
    tool_choice: Optional[ToolChoiceOption]
    reasoning_effort: Optional[ReasoningEffort]


@overload
def to_provider_format(validated_llm_params: ValidatedBaseLLMCallParams, provider_name: Literal["openai"]) -> OpenAICompletionParams:
    ...

# -------------------------------------------------------------------------------- #
# Anthropic Params and Overloads
# -------------------------------------------------------------------------------- #


class AnthropicCompletionParams(TypedDict):
    messages: List[Dict[str, Any]]
    model: ModelName
    user: Optional[str]
    tools: Optional[List]
    tool_choice: Optional[ToolChoiceOption]
    reasoning_capability: Optional[ReasoningEffort]


@overload
def to_provider_format(validated_llm_params: ValidatedBaseLLMCallParams, provider_name: Literal["anthropic"]) -> AnthropicCompletionParams:
    ...


# -------------------------------------------------------------------------------- #
# Provider Params Type
# -------------------------------------------------------------------------------- #


type ProviderParamsT = OpenAICompletionParams | AnthropicCompletionParams


# -----------------------------------------------------------------------------
# Conversion Functions for Each Provider
# -----------------------------------------------------------------------------

def to_openai_format(
    validated_llm_params: ValidatedBaseLLMCallParams
) -> OpenAICompletionParams:
    """
    Convert the validated LLM parameters into OpenAI-specific parameters.
    """
    # ... implementation for OpenAI parameters ...
    raise NotImplementedError("to_openai_format is not implemented yet.")


def to_anthropic_format(
    validated_llm_params: ValidatedBaseLLMCallParams
) -> AnthropicCompletionParams:
    """
    Convert the validated LLM parameters into Anthropic-specific parameters.
    """
    # ... implementation for Anthropic parameters ...
    raise NotImplementedError("to_anthropic_format is not implemented yet.")



# -------------------------------------------------------------------------------- #
# To Provider Format Main Function
# -------------------------------------------------------------------------------- #


def to_provider_format(validated_llm_params: ValidatedBaseLLMCallParams, provider_name: ModelProvider) -> OpenAICompletionParams | AnthropicCompletionParams:
    """
    Convert message(s) into a dictionary of provider-specific parameters.

    The return type depends on the provider specified:

      - "openai"    -> OpenAICompletionParams
      - "anthropic" -> AnthropicCompletionParams
    """
    if provider_name == "openai":
        return to_openai_format(validated_llm_params)
    elif provider_name == "anthropic":
        return to_anthropic_format(validated_llm_params)
    else:
        raise ValueError(f"Unsupported provider: {provider_name}")

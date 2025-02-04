"""
This module contains the base call parameters for LLM calls.
"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #
from typing import (
    List,
    Optional,
    Dict,
    Any,
    TypedDict,
    Literal,
    overload,
    Union
)

# Astral Model Types
from astral_ai.typing.models import ModelName, PROVIDER_MODEL_NAMES, ModelProvider, OpenAIModels, AnthropicModels

# Astral Agent Types
from astral_ai.agents.types import ReasoningEffort, Tool, ToolChoiceOption, ValidatedBaseLLMCallParams


# -------------------------------------------------------------------------------- #
# Provider CompletionParams TypedDicts
# -------------------------------------------------------------------------------- #

# OpenAI
class OpenAICompletionParams(TypedDict):
    messages: List[Dict[str, Any]]
    model: OpenAIModels
    user: Optional[str]
    tools: Optional[List[Any]]
    tool_choice: Optional[ToolChoiceOption]
    reasoning_effort: Optional[ReasoningEffort]


# Anthropic
class AnthropicCompletionParams(TypedDict):
    messages: List[Dict[str, Any]]
    model: AnthropicModels
    user: Optional[str]
    tools: Optional[List[Any]]
    tool_choice: Optional[ToolChoiceOption]
    reasoning_capability: Optional[ReasoningEffort]


type ProviderCompletionParams = OpenAICompletionParams | AnthropicCompletionParams

# -------------------------------------------------------------------------------- #
# Overloads for to_provider_format
# -------------------------------------------------------------------------------- #
# These overloads use Literal types for the known model names for each provider.


@overload
def to_provider_format(
    validated_llm_params: ValidatedBaseLLMCallParams,
    model_name: OpenAIModels
) -> OpenAICompletionParams: ...


@overload
def to_provider_format(
    validated_llm_params: ValidatedBaseLLMCallParams,
    model_name: AnthropicModels
) -> AnthropicCompletionParams: ...


# -----------------------------------------------------------------------------
# Conversion Functions for Each Provider
# -----------------------------------------------------------------------------

from astral_ai.logger import logger

def to_openai_format(params: ValidatedBaseLLMCallParams) -> OpenAICompletionParams:
    """
    Convert validated LLM parameters into a dictionary of OpenAI-specific parameters.
    """
    from astral_ai.messages.provider_transformers import to_openai_format_messages
    messages = to_openai_format_messages(params.messages)

    params_dict = params.model_dump(exclude={"messages"}, exclude_none=True)

    logger.debug(f"The parameters HEREEE are: {params_dict}")

    return {
        "messages": messages,
        **params_dict
    }



def to_anthropic_format(params: ValidatedBaseLLMCallParams) -> AnthropicCompletionParams:
    """
    Convert validated LLM parameters into a dictionary of Anthropic-specific parameters.
    """
    pass


# -------------------------------------------------------------------------------- #
# Main Function
# -------------------------------------------------------------------------------- #

# def to_provider_format(validated_llm_params: ValidatedBaseLLMCallParams, model_name: ModelName) -> ProviderCompletionParams:
#     """
#     Convert validated LLM parameters into a dictionary of provider-specific parameters.
#     """

#     # Get the provider name from the model name.
#     provider_name = PROVIDER_MODEL_NAMES[model_name]

#     if provider_name == "openai":
#         return to_openai_format(validated_llm_params)
#     elif provider_name == "anthropic":
#         return to_anthropic_format(validated_llm_params)
#     else:
#         raise ValueError(f"Unsupported provider for model: {provider_name}")
 


# -------------------------------------------------------------------------------- #
# Message Transformers
# -------------------------------------------------------------------------------- #

"""
Contains helper functions to transform Message objects into various vendor-specific formats,
such as OpenAI, Anthropic, etc.
"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

from typing import Any, Dict, Union, List

# Astral AI imports: Import the two new message classes.
from ..typing.messages import MessageList, Message, TextMessage, ImageMessage

from astral_ai.typing.models import ModelProvider
# from astral_ai.agents.clients.openai import OpenAICompletionParams, AnthropicCompletionParams, ProviderParamsT


# # -------------------------------------------------------------------------------- #
# # OpenAI Transformer
# # -------------------------------------------------------------------------------- #


def to_openai_format_messages(messages: Union[MessageList, List[Message], Message]) -> List[Dict[str, Any]]:
    """
    Convert message(s) into a list of dicts suitable for OpenAI's Chat endpoints.

    For a TextMessage, each dict might look like:
        {
            "role": "user",
            "content": [{"type": "text", "text": "..."}]
        }

    For an ImageMessage, it might look like:
        {
            "role": "user", 
            "content": [{"type": "image_url", "image_url": {"url": "...", "detail": "..."}}]
        }
    """
    if isinstance(messages, Message):
        message_list = [messages]
    elif isinstance(messages, MessageList):
        message_list = messages.messages
    else:
        message_list = messages

    formatted_messages = []

    for message in message_list:
        content_blocks = []

        if isinstance(message, TextMessage):
            content_blocks.append({
                "type": "text",
                "text": message.text
            })
        elif isinstance(message, ImageMessage):
            content_blocks.append({
                "type": "image_url",
                "image_url": {
                    "url": message.image_url,
                    "detail": message.image_detail
                }
            })
        else:
            raise TypeError("Unsupported message type for OpenAI format conversion.")

        formatted_messages.append({
            "role": message.role,
            "content": content_blocks
        })

    return formatted_messages


# from pydantic import BaseModel, Field
# from typing import Optional, List, TypedDict

# from astral_ai.typing.models import ModelName
# # Agent Types
# from astral_ai.agents.types import (
#     ReasoningEffort,
#     Tool,
#     ToolChoiceOption,
#     ModelSettings,
# )


# type MessageListT = MessageList | List[Message] | Message


# class OpenAICompletionParams(TypedDict):
#     messages: Union[MessageList, List[Message], Message]
#     model: ModelName
#     user: Optional[str]
#     tools: Optional[List]
#     tool_choice: Optional[ToolChoiceOption]
#     reasoning_effort: Optional[ReasoningEffort]


# class AnthropicCompletionParams(TypedDict):
#     messages: List[Dict[str, Any]]
#     model: ModelName
#     unique_user_id: Optional[str]
#     tools: Optional[List]
#     tool_choice: Optional[ToolChoiceOption]
#     reasoning_capability: Optional[ReasoningEffort]


# type ProviderParamsT = OpenAICompletionParams | AnthropicCompletionParams


# class BaseLLMCallParams(BaseModel):
#     """
#     Base call parameters for LLM calls.
#     """
#     messages: MessageListT = Field(description="The messages to be sent to the LLM.")
#     model: ModelName = Field(description="The model to be used for the LLM call.")
#     user: Optional[str] = Field(description="The user to be used for the LLM call.")
#     tools: Optional[List[Tool]] = Field(description="The tools to be used for the LLM call.")
#     tool_choice: Optional[ToolChoiceOption] = Field(description="The tool choice to be used for the LLM call.")
#     reasoning_effort: Optional[ReasoningEffort] = Field(description="The reasoning effort to be used for the LLM call.")


# class ValidatedBaseLLMCallParams(BaseLLMCallParams):
#     """
#     Validated base call parameters for LLM calls.
#     """
#     messages: List[Message]
#     tool_choice: ToolChoiceOption



# def to_openai_format(validated_llm_params: ValidatedBaseLLMCallParams) -> OpenAICompletionParams:   
#     """
#     Convert message(s) into a list of dicts suitable for OpenAI's Chat endpoints.
#     """
#     pass


# def to_anthropic_format(validated_llm_params: ValidatedBaseLLMCallParams) -> AnthropicCompletionParams:
#     """
#     Convert message(s) into a list of dicts suitable for Anthropic's Chat endpoints.
#     """
#     pass


# def to_provider_format[ProviderParamsT](validated_llm_params: ValidatedBaseLLMCallParams, provider_name: ModelProvider) -> ProviderParamsT:
#     """
#     Convert message(s) into a dictionary of provider-specific parameters.
#     """
#     if provider_name == "anthropic":
#         return to_anthropic_format(validated_llm_params)
#     elif provider_name == "openai":
#         return to_openai_format(validated_llm_params)
#     else:
#         raise ValueError(f"Unsupported provider: {provider_name}")


# if __name__ == "__main__":
#     # Test the to_openai_format function
#     messages = [
#         TextMessage(text="Hello, how are you?"),
#         TextMessage(text="I'm doing well, thank you!")
#     ]
#     validated_params = ValidatedBaseLLMCallParams(messages=messages, model="gpt-4o-mini", user="test_user")
#     params = to_provider_format[AnthropicCompletionParams](validated_params, provider_name="anthropic")
#     print(params)
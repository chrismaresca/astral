# -------------------------------------------------------------------------------- #
# Agent Types
# -------------------------------------------------------------------------------- #

"""

This module contains the types for agent configuration.

"""
# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in imports
from typing import Any, Dict, List, Optional, Union, TypeAlias, Literal, Generic

# Pydantic imports
from pydantic import BaseModel, Field

# Astral Message Types
from astral_ai.typing.messages import MessageListT, Message

# Astral Model Types
from astral_ai.typing.models import ModelName

# Astral Model Response Types
from astral_ai.typing.model_response import StructuredOutputResponse


# -------------------------------------------------------------------------------- #
# Base Types
# -------------------------------------------------------------------------------- #

ReasoningEffort: TypeAlias = Literal["low", "medium", "high"]
ToolChoiceType: TypeAlias = Literal["function"]


# -------------------------------------------------------------------------------- #
# Tool Types
# -------------------------------------------------------------------------------- #

class Tool(BaseModel):
    """
    A tool is a function that can be called by the LLM.
    """
    type: Literal[ToolChoiceType]
    name: str
    description: str
    parameters: Dict[str, Any]
    strict: bool


class ToolChoice(BaseModel):
    """
    The tool choice for the LLM.
    """
    type: ToolChoiceType
    function_name: Optional[str] = None


ToolChoiceOption: TypeAlias = Literal["auto"] | None | ToolChoice

# -------------------------------------------------------------------------------- #
# Model Settings Types
# -------------------------------------------------------------------------------- #


class ModelSettings(BaseModel):
    """
    The settings for the model.
    """
    temperature: Optional[float] = None
    top_p: Optional[float] = None


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
    structured_model: Optional[StructuredOutputResponse] = Field(description="The structured model to be used for the LLM call.")

# -------------------------------------------------------------------------------- #
# Validated Base LLM Call Params
# -------------------------------------------------------------------------------- #

class ValidatedBaseLLMCallParams(BaseLLMCallParams):
    """
    Validated base call parameters for LLM calls.
    """
    messages: List[Message] = Field(description="The messages to be sent to the LLM.")
    tool_choice: ToolChoiceOption = Field(description="The tool choice to be used for the LLM call.")
    structured_model: Optional[StructuredOutputResponse] = Field(description="The structured model to be used for the LLM call.")

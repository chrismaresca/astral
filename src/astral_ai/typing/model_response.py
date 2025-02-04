# -------------------------------------------------------------------------------- #
# Structured Output Response
# -------------------------------------------------------------------------------- #


# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Pydantic imports
from pydantic import BaseModel

# Built-in imports
from typing import TypeVar, TypeAlias

# OpenAI imports
from openai.types.chat import ChatCompletion

# -------------------------------------------------------------------------------- #
# Structured Output Generic Type
# -------------------------------------------------------------------------------- #

StructuredOutputResponse = TypeVar('StructuredOutputResponse', bound=BaseModel)

ChatResponse = TypeVar('ChatResponse', bound=ChatCompletion)


# -------------------------------------------------------------------------------- #
# OpenAI Output Responses
# -------------------------------------------------------------------------------- #

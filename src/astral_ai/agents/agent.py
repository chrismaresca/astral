# -------------------------------------------------------------------------------- #
# Agent Class
# -------------------------------------------------------------------------------- #

"""
This class is responsible for initializing and validating the LLM client,
merging the default parameters with runtime keyword arguments, and providing
a template for client-specific call implementations.
"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in
from typing import Any, Dict, List, Optional, Union

# Astral Models
from astral_ai.typing.models import ModelName, PROVIDER_MODEL_NAMES

# Astral AI Agent Types
from astral_ai.agents.types import ReasoningEffort, Tool, ToolChoiceOption

# Astral AI LLM Clients
from astral_ai.agents.clients.base import BaseLLMClient

# Astral AI Constants (provider mapping)
from astral_ai.constants.mappings import PROVIDER_MAPPING

# Astral AI Message Types
from astral_ai.typing.messages import Message, MessageList

# Astral AI Models
from astral_ai.typing.model_response import ChatResponse, StructuredOutputResponse

# Astral AI Logger
from astral_ai.logger import logger

# -------------------------------------------------------------------------------- #
# Agent Class
# -------------------------------------------------------------------------------- #


class Agent:
    def __init__(self,
                 model_name: ModelName,
                 messages: Optional[Union[MessageList, List[Message], Message]] = None,
                 reasoning_effort: Optional[ReasoningEffort] = None,
                 tools: Optional[List[Tool]] = None,
                 tool_choice: Optional[ToolChoiceOption] = None,
                 user: Optional[str] = None,
                 use_async: bool = False,
                 return_usage: bool = True,
                 return_cost: bool = True,
                 **kwargs: Any):
        self.model_name = model_name
        self.messages = messages
        self.reasoning_effort = reasoning_effort
        self.tools = tools
        self.tool_choice = tool_choice
        self.user = user
        self.use_async = use_async
        self.return_usage = return_usage
        self.return_cost = return_cost
        # Store any additional keyword arguments if needed
        self.extra_kwargs = kwargs

        # Initialize the client based on the model name.
        self.client = self._initialize_client(model_name)

    # -------------------------------------------------------------------------------- #
    # Private Methods
    # -------------------------------------------------------------------------------- #

    def _initialize_client(self, model_name: ModelName) -> BaseLLMClient:
        # Look up the provider for this model using the mapping of model names to providers.
        provider = PROVIDER_MODEL_NAMES.get(model_name)
        if not provider:
            raise ValueError(f"Model name {model_name} is not supported")

        # Look up the corresponding client class for the provider.
        client_class = PROVIDER_MAPPING.get(provider)
        if not client_class:
            raise ValueError(f"No client available for provider: {provider}")

        # Initialize and return the client instance.
        return client_class(
            model_name=model_name,
            messages=self.messages,
            reasoning_effort=self.reasoning_effort,
            tools=self.tools,
            tool_choice=self.tool_choice,
            user=self.user,
            **self.extra_kwargs  # pass any extra kwargs along if needed
        )

    # -------------------------------------------------------------------------------- #
    # Public Methods
    # -------------------------------------------------------------------------------- #

    def run(self, messages: Union[MessageList, List[Message], Message], return_usage: bool = True, return_cost: bool = True) -> ChatResponse:
        return self.client.run(messages, return_usage, return_cost)

    def run_structured(self, structured_model: StructuredOutputResponse, messages: Union[MessageList, List[Message], Message], return_usage: bool = True, return_cost: bool = True) -> StructuredOutputResponse:
        return self.client.run_structured(structured_model, messages, return_usage, return_cost)

    def run_async(self, messages: Union[MessageList, List[Message], Message], return_usage: bool = True, return_cost: bool = True) -> ChatResponse:
        return self.client.run_async(messages, return_usage, return_cost)

    def run_structured_async(self, structured_model: StructuredOutputResponse, messages: Union[MessageList, List[Message], Message], return_usage: bool = True, return_cost: bool = True) -> StructuredOutputResponse:
        return self.client.run_structured_async(structured_model, messages, return_usage, return_cost)



# -------------------------------------------------------------------------------- #
# Test Cases
# -------------------------------------------------------------------------------- #

if __name__ == "__main__":
    agent = Agent(model_name="o1-mini")

    from astral_ai.typing.messages import TextMessage

    messages = [
        TextMessage(role="developer", text="You are a helpful assistant that can answer questions and help with tasks."),
        TextMessage(role="user", text="What is the capital of the moon?")
    ]

    response = agent.run(messages=messages, return_usage=False, return_cost=False)
    print(response)






# -------------------------------------------------------------------------------- #
# OpenAILLMClient
# -------------------------------------------------------------------------------- #

"""
OpenAILLMClient

Responsible for initializing and validating the OpenAI client (sync or async),
validating model features, and making calls using flexible keyword arguments.
"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in imports
from pydantic import BaseModel
from typing import Any, List, Optional, Union, Tuple
from dotenv import load_dotenv
import os

# OpenAI Client Types
from openai import AsyncOpenAI, OpenAI

# OpenAI Types
from openai.types.chat import ChatCompletion, ParsedChatCompletion

# Project Types

# Base Client Types
from astral_ai.clients.providers.base import BaseLLMCallParams

# Provider Types
from astral_ai.clients.provider_params import OpenAICompletionParams

# Astral AI Types
from astral_ai.typing.models import ModelName

# Astral AI Model Response Types
from astral_ai.typing.model_response import StructuredOutputResponse, ChatResponse

# Astral AI Message Types
from astral_ai.typing.messages import Message, MessageList

# Astral AI Client Types
from astral_ai.typing.clients import OpenAILLMClientT

# Decorators
from astral_ai.clients.decorators.usage import calculate_cost_and_usage

# Base Exceptions
from astral_ai.exceptions import APIKeyNotFoundError
from astral_ai.clients.exceptions import LLMResponseError, LLMResponseParseError, LLMResponseCompletionError

# Agent Types
from astral_ai.clients.types import ReasoningEffort, ModelSettings, Tool, ToolChoiceOption


# Astral AI imports
from astral_ai.clients.providers.base import BaseLLMClient

# Logger
from astral_ai.logger import AIModuleLogger


logger = AIModuleLogger()


# -------------------------------------------------------------------------------- #
# Class Definition
# -------------------------------------------------------------------------------- #


class OpenAILLMClient(BaseLLMClient[OpenAILLMClientT]):
    """
    Responsible for initializing and validating the OpenAI client (sync or async),
    validating model features, and making calls using flexible keyword arguments.
    """

    def __init__(
        self,
        model_name: ModelName,
        messages: Optional[Union[MessageList, List[Message], Message]] = None,
        reasoning_effort: Optional[ReasoningEffort] = None,
        tools: Optional[List[Tool]] = None,
        tool_choice: Optional[ToolChoiceOption] = None,
        # model_settings: Optional[ModelSettings] = None,
        # metadata: Optional[Dict[str, Any]] = None,
        user: Optional[str] = None,
        use_async: bool = False,
        api_key: Optional[str] = None,
        **kwargs: Any,  # Extra keyword arguments for flexibility.
    ):
        """
        Initialize the OpenAILLMClient.
        """
        logger.debug(
            f"Initializing OpenAILLMClient with model={model_name}, user={user}, reasoning_effort={reasoning_effort}, async={use_async}"
        )

        # Initialize the API key.
        self.api_key = api_key

        # Initialize the base class.
        super().__init__(
            model_name=model_name,
            messages=messages,
            reasoning_effort=reasoning_effort,
            tools=tools,
            tool_choice=tool_choice,
            # model_settings=model_settings,
            # metadata=metadata,
            user=user,
            use_async=use_async,
            **kwargs
        )

        # TODO: extend the init client to include other parameters (org id, etc.)

        logger.info(f"Successfully initialized {'async' if use_async else 'sync'} OpenAI client with the following parameters: {kwargs}")

    # -------------------------------------------------------------------------------- #
    # Initialize Client
    # -------------------------------------------------------------------------------- #
    def _init_client(self, use_async: bool, **kwargs: Any) -> OpenAILLMClientT:
        """
        Initialize the OpenAI client (sync or async).

        Loads the API key from the provided argument or the environment.
        """

        load_dotenv()
        api_key = kwargs.get("api_key", self.api_key) or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise APIKeyNotFoundError("OpenAI API key not found in arguments or environment variables")
        logger.debug(f"Initializing {'async' if use_async else 'sync'} OpenAI client with API key.")
        return AsyncOpenAI(api_key=api_key) if use_async else OpenAI(api_key=api_key)

    # -------------------------------------------------------------------------------- #
    # Prepare Parameters for Provider
    # -------------------------------------------------------------------------------- #

    def _prepare_params_for_provider(self, base_params: BaseLLMCallParams, structured_model: Optional[StructuredOutputResponse] = None) -> OpenAICompletionParams:
        """
        Convert the base parameters to OpenAI format.
        """

        # Validate the base parameters.
        validated_params = self._validate_and_unpack_parameters(base_params, structured_model)

        from astral_ai.clients.provider_params import to_openai_format

        return to_openai_format(validated_params)

    # -------------------------------------------------------------------------------- #
    # Call Private Methods
    # -------------------------------------------------------------------------------- #

    @calculate_cost_and_usage
    def _call_api_sync(self, model_name: ModelName, params: BaseLLMCallParams, return_usage: bool = True, return_cost: bool = True) -> ChatCompletion:
        """
        Call the OpenAI API synchronously using the client.

        Args:
            model_name (ModelName): The model name to use for the API call.
            params (BaseLLMCallParams): The parameters for the API call.

        Returns:
            Tuple[ChatResponse, AIUsage, AICost]: The API response, usage, and cost.
        """


        # Prepare the parameters for the provider.
        openai_params = self._prepare_params_for_provider(params)

        logger.debug(f"The OpenAI parameters are: {openai_params}")

        # Call the API.
        try:
            response = self.client.chat.completions.create(**openai_params)
        except Exception as e:
            logger.error(f"Error during OpenAI API synchronous call: {e}")
            raise LLMResponseCompletionError(f"Error during OpenAI API synchronous call: {e}")

        # Validate the response.
        if not response.choices:
            logger.error("LLM returned no choices in synchronous response")
            raise LLMResponseCompletionError(f"LLM returned no choices in synchronous response: {e}")

        if not getattr(response.choices[0].message, "content", None):
            logger.error("LLM returned no valid synchronous response")
            raise LLMResponseCompletionError(f"LLM returned no valid synchronous response: {e}")

        return response

    @calculate_cost_and_usage
    async def _call_api_async(self, model_name: ModelName, params: BaseLLMCallParams, return_usage: bool = True, return_cost: bool = True) -> ChatCompletion:
        """
        Call the OpenAI API asynchronously using the client.

        Args:
            params (BaseLLMCallParams): The parameters for the API call.

        Returns:
            Tuple[ChatResponse, AIUsage, AICost]: The API response, usage, and cost.
        """

        # Prepare the parameters for the provider.
        openai_params = self._prepare_params_for_provider(params)

        # Call the API.
        try:
            response = await self.client.chat.completions.create(**openai_params)
        except Exception as e:
            logger.error(f"Error during OpenAI API asynchronous call: {e}")
            raise LLMResponseCompletionError("Error during OpenAI API asynchronous call")

        # Validate the response.
        if not response.choices:
            logger.error("LLM returned no choices in async response")
            raise LLMResponseCompletionError("LLM returned no choices in async response")

        if not getattr(response.choices[0].message, "content", None):
            logger.error("LLM returned no valid async response")
            raise LLMResponseCompletionError("LLM returned no valid async response")

        return response

    @calculate_cost_and_usage
    def _call_api_structured(self, model_name: ModelName, structured_model: StructuredOutputResponse, params: BaseLLMCallParams, return_usage: bool = True, return_cost: bool = True) -> ParsedChatCompletion:
        """
        Call the OpenAI API synchronously for structured output using the client.

        Args:
            structured_model (StructuredOutputResponse): The structured output specification.
            params (BaseLLMCallParams): The parameters for the API call.

        Returns:
            Tuple[StructuredOutputResponse, AIUsage, AICost]: The structured response, usage, and cost.
        """

        # Prepare the parameters for the provider.
        openai_params = self._prepare_params_for_provider(params, structured_model)

        # Call the API.
        try:
            response = self.client.beta.chat.completions.parse(**openai_params)
        except Exception as e:
            logger.error(f"Error during OpenAI structured synchronous call: {e}")
            raise LLMResponseCompletionError("Error during OpenAI structured synchronous call")

        if not response.choices:
            logger.error("LLM returned no choices in structured response")
            raise LLMResponseParseError("LLM returned no choices in structured response")

        if not getattr(response.choices[0].message, "parsed", None):
            logger.error("LLM returned no valid structured response")
            raise LLMResponseParseError("LLM returned no valid structured response")

        logger.debug(f"Successfully parsed structured response from OpenAI: {response}")
        return response

    @calculate_cost_and_usage
    async def _call_api_structured_async(self, model_name: ModelName, structured_model: StructuredOutputResponse, params: BaseLLMCallParams, return_usage: bool = True, return_cost: bool = True) -> ParsedChatCompletion:
        """
        Call the OpenAI API asynchronously for structured output using the client.

        Args:
            structured_model (StructuredOutputResponse): The structured output specification.
            params (BaseLLMCallParams): The parameters for the API call.

        Returns:
            Tuple[StructuredOutputResponse, AIUsage, AICost]: The structured response, usage, and cost.
        """        # Prepare the parameters for the provider.
        openai_params = self._prepare_params_for_provider(params, structured_model)

        # Call the API.
        try:
            response = await self.client.beta.chat.completions.parse(**openai_params)
        except Exception as e:
            logger.error(f"Error during OpenAI structured asynchronous call: {e}")
            raise LLMResponseCompletionError("Error during OpenAI structured asynchronous call")

        if not response.choices:
            logger.error("LLM returned no choices in structured response")
            raise LLMResponseParseError("LLM returned no choices in structured response")

        if not getattr(response.choices[0].message, "parsed", None):
            logger.error("LLM returned no valid structured response")
            raise LLMResponseParseError("LLM returned no valid structured response")

        logger.debug(f"Successfully parsed structured response from OpenAI: {response}")
        return response

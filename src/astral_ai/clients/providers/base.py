# -------------------------------------------------------------------------------- #
# Base LLM Client
# -------------------------------------------------------------------------------- #

"""
This module contains the base class for the LLM client.
"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in imports
from typing import Any, Dict, List, Optional, Union, Tuple, cast, Generic, TypeVar
from abc import ABC, abstractmethod

# Pydantic Imports
from pydantic import BaseModel, Field

# Supported Models
from astral_ai.constants.supported_models import (
    REASONING_EFFORT_SUPPORTED_MODELS,
    FUNCTION_CALL_SUPPORTED_MODELS,
    SYSTEM_MESSAGE_SUPPORTED_MODELS,
    DEVELOPER_MESSAGE_SUPPORTED_MODELS,
    ONLY_USER_MESSAGE_SUPPORTED_MODELS,
    STRUCTURED_OUTPUT_SUPPORTED_MODELS,
)

# AI Cost Imports
from astral_ai.typing.usage import AIUsage, AICost

# Agent Types
from astral_ai.clients.types import (
    ReasoningEffort,
    Tool,
    ToolChoiceOption,
    ModelSettings,
    BaseLLMCallParams,
    ValidatedBaseLLMCallParams,
)

# Astral AI Utils
from astral_ai.clients.utils import (
    handle_no_messages,
    standardize_messages,
    count_message_roles,
    convert_message_roles,
)

# Astral AI Exceptions
from astral_ai.clients.exceptions import (
    ReasoningEffortNotSupportedError,
    ToolsNotSupportedError,
    StructuredOutputNotSupportedError,
    InvalidMessageError,
)

# Astral AI Providers
from astral_ai.clients.provider_params import  ProviderCompletionParams

# Astral AI imports
from astral_ai.typing.model_response import StructuredOutputResponse, ChatResponse

# Astral Models
from astral_ai.typing.models import ModelName

# Astral Message Types
from astral_ai.typing.messages import Message, MessageList, MessageListT

# LLM Client Types
from astral_ai.typing.clients import LLMClientT

# Logger
from astral_ai.logger import AIModuleLogger

# Define a type variable
LLMClientType = TypeVar('LLMClientType')

# -------------------------------------------------------------------------------- #
# BaseLLMClient Class
# -------------------------------------------------------------------------------- #

# Exceptions & Feature Checks

logger = AIModuleLogger()


class BaseLLMClient(ABC, Generic[LLMClientType]):
    """
    Base LLM Client abstract class.

    This class is responsible for initializing and validating the LLM client,
    merging the default parameters with runtime keyword arguments, and providing
    a template for client-specific call implementations.
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
        **kwargs: Any,
    ):
        """
        Initialize the BaseLLMClient.

        Args:
            model_name (ModelName): The model name to use.
            messages (Optional[Union[MessageList, List[Message], Message]], optional): 
                Initial messages. Defaults to None.
            reasoning_effort (Optional[ReasoningEffort], optional): The reasoning effort. Defaults to None.
            tools (Optional[List[Tool]], optional): List of tools. Defaults to None.
            tool_choice (Optional[ToolChoiceOption], optional): Tool choice option. Defaults to None.
            user (Optional[str], optional): The user identifier. Defaults to None.
            use_async (bool, optional): Whether to use an asynchronous client. Defaults to False.
            api_key (Optional[str], optional): API key if provided. Defaults to None.
            **kwargs: Additional keyword arguments.
        """
        self.model_name = model_name

        # Validate the messages.
        self.messages = self._set_messages(model_name, messages, init_call=True)

        # Set the reasoning effort.
        self.reasoning_effort = self._set_reasoning_effort(reasoning_effort, model_name)

        # Set the tools and tool choice.
        self.tools = self._set_tools(tools, model_name)
        self.tool_choice = self._set_tool_choice(tool_choice, tools)

        # TODO: add model_settings and metadata
        self.model_settings = None
        self.metadata = None

        # Initialize the user and async flags.
        self.user = user
        self.use_async = use_async

        # Initialize the extra parameters.
        self.extra_params = kwargs

        # Initialize the client.
        self.client: LLMClientT = self._init_client(use_async=use_async, **kwargs)

    # -------------------------------------------------------------------------------- #
    # Abstract Methods
    # -------------------------------------------------------------------------------- #

    @abstractmethod
    def _init_client(self, use_async: bool, **kwargs: Any) -> LLMClientT:
        """
        Abstract method for initializing the LLM client.
        Derived classes must implement this method.

        Args:
            use_async (bool): Whether to initialize an asynchronous client.
            api_key (Optional[str], optional): API key for the client.

        Returns:
            LLMClientT: The initialized client instance.
        """
        raise NotImplementedError("Subclasses must implement this method.")
    
    @abstractmethod
    def _prepare_params_for_provider(self, base_params: BaseLLMCallParams) -> ProviderCompletionParams:
        """
        Convert the base parameters to provider-specific format.

        Args:
            base_params (BaseLLMCallParams): The base parameters.
            structured_model (Optional[StructuredOutputResponse], optional): The structured model. Defaults to None.

        Returns:
            ProviderCompletionParams: The provider-specific parameters. 
        """
        raise NotImplementedError("Subclasses must implement this method.")


    # -------------------------------------------------------------------------------- #
    # Client Type Validation
    # -------------------------------------------------------------------------------- #

    def _validate_client(self, use_async: bool, **kwargs: Any) -> None:
        """
        Validate that the client instance matches the requested call type.
        If there's a mismatch, reinitialize the client with the correct type.

        Args:
            use_async (bool): Whether to use an asynchronous client
            **kwargs: Additional client initialization parameters that may vary by implementation
        """
        if use_async and not self.use_async:
            logger.warning("Client type mismatch detected. Reinitializing sync client as async.")
            self.client = self._init_client(use_async=True, **kwargs)
            self.use_async = True
        elif not use_async and self.use_async:
            logger.warning("Client type mismatch detected. Reinitializing async client as sync.")
            self.client = self._init_client(use_async=False, **kwargs)
            self.use_async = False

        logger.debug(
            f"Client reinitialized as {'async' if self.use_async else 'sync'} "
            f"with the following parameters: {kwargs}"
        )

    # -------------------------------------------------------------------------------- #
    # Message Validation (Provider-Specific)
    # -------------------------------------------------------------------------------- #
    def _set_messages(
        self,
        model_name: ModelName,
        messages: Union[MessageList, List[Message], Message],
        init_call: bool = False
    ) -> List[Message]:
        """
        Validate and potentially transform the messages in the parameters.
        This should be implemented by provider-specific subclasses.

        Args:
            messages (Union[MessageList, List[Message], Message]): The messages to validate.
            init_call (bool): Flag indicating if this is an initial call.

        Returns:
            List[Message]: The validated and potentially modified messages.
        """

        logger.debug(f"The messages are: {messages}")

        if not messages:
            return handle_no_messages(model_name, init_call=init_call)

        # Standardize the messages to a list of Message instances.
        messages = standardize_messages(messages)

        # Count the number of system and developer messages.
        system_count, developer_count = count_message_roles(messages)

        # Validate counts.
        if system_count > 1:
            raise InvalidMessageError("Invalid message role provided. More than one system message provided.")
        if developer_count > 1:
            raise InvalidMessageError("Invalid message role provided. More than one developer message provided.")
        if system_count >= 1 and developer_count >= 1:
            raise InvalidMessageError("Invalid message role provided. Both system and developer messages provided.")

        # Convert the message roles if needed.
        if system_count > 0:
            # If a system message is present:
            if model_name in DEVELOPER_MESSAGE_SUPPORTED_MODELS:
                convert_message_roles(messages, "developer", model_name)
            elif model_name in ONLY_USER_MESSAGE_SUPPORTED_MODELS:
                convert_message_roles(messages, "user", model_name)
        elif developer_count > 0:
            # If a developer message is present:
            if model_name in SYSTEM_MESSAGE_SUPPORTED_MODELS:
                convert_message_roles(messages, "system", model_name)
            elif model_name in ONLY_USER_MESSAGE_SUPPORTED_MODELS:
                convert_message_roles(messages, "user", model_name)

        # Return the messages.
        return messages
    
    def _set_reasoning_effort(self, reasoning_effort: Optional[ReasoningEffort], model_name: ModelName) -> Optional[ReasoningEffort]:
        """
        Validate that the model supports the requested reasoning effort.
        Raises ReasoningEffortNotSupportedError if not supported.
        """

        model_name = model_name or self.model_name

        # Return None if no reasoning effort is provided.
        if reasoning_effort is None:
            logger.debug(f"No reasoning effort provided for model {model_name}")
            return None

        # Validate the reasoning effort.
        if reasoning_effort is not None and model_name not in REASONING_EFFORT_SUPPORTED_MODELS:
            logger.error(f"Model {model_name} does not support reasoning effort.")
            raise ReasoningEffortNotSupportedError(model_name)
        logger.debug(f"Reasoning effort validation passed for model {model_name}.")

        # Return the reasoning effort.
        return reasoning_effort

    def _set_tools(self, tools: Optional[List[Any]], model_name: ModelName) -> Optional[List[Any]]:
        """
        Validate and set the tools for the client.

        Args:
            tools (Optional[List[Any]]): List of tools to validate

        Raises:
            ToolsNotSupportedError: If the model does not support tools
            ValueError: If tools is provided but not as a list
            ValueError: If any tool in the list is invalid
        """

        model_name = model_name or self.model_name

        if tools is None:
            logger.debug(f"No tools provided for model {model_name}")
            return None

        # Validate model supports tools
        if model_name not in FUNCTION_CALL_SUPPORTED_MODELS:
            logger.error(f"Model {model_name} does not support tools.")
            raise ToolsNotSupportedError(model_name)

        # Validate tools is a list
        if not isinstance(tools, list):
            logger.error("Tools must be provided as a list")
            raise ValueError("Tools must be provided as a list")

        # Validate each tool
        for tool in tools:
            if not hasattr(tool, "name") or not hasattr(tool, "description"):
                logger.error(f"Invalid tool format: {tool}")
                raise ValueError(f"Tool {tool} missing required attributes 'name' and 'description'")

        logger.debug(f"Successfully validated {len(tools)} tools for model {self.model_name}")
        return tools

    def _set_tool_choice(self, tool_choice: Optional[ToolChoiceOption], tools: Optional[List[Tool]] = None) -> ToolChoiceOption:
        """
        Validate and set the tool choice based on provided tools and tool_choice.

        Args:
            tool_choice (Optional[ToolChoiceOption]): The tool choice option to set
            tools (Optional[List[Tool]]): The list of available tools

        Sets self.tool_choice to:
            - "none" if no tools are provided (even if tool_choice is explicitly set)
            - "auto" if tools exist but no specific choice is made
            - The provided tool_choice if specified and tools exist
        """
        if tools is None:
            if tool_choice is not None:
                logger.warning("Tool choice was explicitly set but no tools were provided. Setting to None.")
            return None

        if tool_choice is None:
            logger.debug("No tool choice specified, defaulting to 'auto' since tools are present")
            return "auto"

        logger.debug(f"Setting explicit tool_choice to {tool_choice}")
        return tool_choice

    def _validate_structured_model(self, structured_model: Optional[StructuredOutputResponse], model_name: ModelName) -> Optional[StructuredOutputResponse]:
        """
        Validate that the model supports structured output.
        Raises StructuredOutputNotSupportedError if not supported.
        """
        model_name = model_name or self.model_name

        if structured_model is None:
            logger.debug(f"No structured model provided for model {model_name}")
            return

        if model_name not in STRUCTURED_OUTPUT_SUPPORTED_MODELS:
            logger.error(f"Model {self.model_name} does not support structured output.")
            raise StructuredOutputNotSupportedError(self.model_name)
        
        if not isinstance(structured_model, BaseModel):
            logger.error(f"Structured model must be a subclass of BaseModel. Got {type(structured_model)}.")
            raise ValueError("Structured model must be a subclass of BaseModel.")
        
        logger.debug(f"Successfully validated structured model for model {model_name}")
        return structured_model

    # -------------------------------------------------------------------------------- #
    # Parameter Validation (Provider-Specific)
    # -------------------------------------------------------------------------------- #

    def _validate_and_unpack_parameters(self, params: BaseLLMCallParams, structured_model: Optional[StructuredOutputResponse] = None) -> ValidatedBaseLLMCallParams:
        """
        Validate and potentially transform the parameters in the parameters.
        This should be implemented by provider-specific subclasses.

        Args:
            params (BaseLLMCallParams): The parameters to validate and unpack.

        Returns:
            BaseLLMCallParams: The validated and unpacked parameters.
        """
        # unpack the parameters
        model_name = params.model
        messages = params.messages
        user = params.user
        tools = params.tools
        tool_choice = params.tool_choice
        reasoning_effort = params.reasoning_effort

        # Get the validated parameters.
        validated_params = ValidatedBaseLLMCallParams(
            model=model_name,
            messages=self._set_messages(model_name=model_name, messages=messages, init_call=False),
            user=user,
            tools=self._set_tools(tools=tools, model_name=model_name),
            tool_choice=self._set_tool_choice(tool_choice=tool_choice, tools=tools),
            reasoning_effort=self._set_reasoning_effort(reasoning_effort=reasoning_effort, model_name=model_name),
            structured_model=self._validate_structured_model(structured_model=structured_model, model_name=model_name), 
        )

        return validated_params

        


    # -------------------------------------------------------------------------------- #
    # Parameter Merging and Overrides
    # -------------------------------------------------------------------------------- #

    def _merge_parameters(self, runtime: Dict[str, Any], merge_flags: Dict[str, bool]) -> BaseLLMCallParams:
        """
        Merge default parameters with runtime parameters using flexible strategies.

        The merge_flags dictionary can specify for each field whether to merge (True)
        or override (False). For example, if merge_flags.get("tools") is True and both
        the default and runtime values for "tools" are lists, they will be concatenated.

        Args:
            runtime (Dict[str, Any]): The runtime parameters.
            merge_flags (Dict[str, bool]): Dictionary specifying merging strategy per field.

        Returns:
            BaseLLMCallParams: The merged call parameters.
        """
        merged = {}

        # List of known fields.
        fields = list(BaseLLMCallParams.model_fields.keys())

        for field in fields:
            # Determine the default value.
            if field == "model":
                default_value = self.model_name
            elif field == "tools":
                default_value = self.tools
            elif field == "tool_choice":
                default_value = self.tool_choice
            elif field == "reasoning_effort":
                default_value = self.reasoning_effort
            elif field == "user":
                default_value = self.user
            elif field == "structured_model":
                default_value = None  # Must be provided in each call.
            else:
                default_value = None

            runtime_value = runtime.get(field)
            merge_flag = merge_flags.get(field, False)

            if merge_flag and default_value is not None and runtime_value is not None:
                # Merge lists or dictionaries.
                if isinstance(default_value, list) and isinstance(runtime_value, list):
                    merged[field] = default_value + runtime_value
                elif isinstance(default_value, dict) and isinstance(runtime_value, dict):
                    merged_dict = default_value.copy()
                    merged_dict.update(runtime_value)
                    merged[field] = merged_dict
                else:
                    # Fallback: runtime value overrides.
                    merged[field] = runtime_value
            else:
                # Use runtime value if provided; otherwise, the default.
                merged[field] = runtime_value if runtime_value is not None else default_value

        # Include any additional runtime parameters.
        for key, value in runtime.items():
            if key not in merged:
                merged[key] = value

        logger.debug(f"Merged parameters: {merged}")

        return BaseLLMCallParams(**merged)

    # -------------------------------------------------------------------------------- #
    # Abstract Call Methods
    # -------------------------------------------------------------------------------- #

    @abstractmethod
    def _call_api_sync(self, model_name: ModelName, params: Dict[str, Any], return_usage: bool = True, return_cost: bool = True) -> Tuple[ChatResponse, AIUsage, AICost]:
        """
        Abstract method to call and validate the underlying LLM API synchronously.
        Derived classes should implement this method.

        Args:
            params (Dict[str, Any]): The parameters to pass to the API.

        Returns:
            Tuple[ChatResponse, AIUsage, AICost]: The API response, usage, and cost.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    async def _call_api_async(self, model_name: ModelName, params: Dict[str, Any], return_usage: bool = True, return_cost: bool = True) -> Tuple[ChatResponse, AIUsage, AICost]:
        """
        Abstract method to call and validate the underlying LLM API asynchronously.
        Derived classes should implement this method.

        Args:
            params (Dict[str, Any]): The parameters to pass to the API.

        Returns:
            Tuple[ChatResponse, AIUsage, AICost]: The API response, usage, and cost.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def _call_api_structured(self, model_name: ModelName, structured_model: StructuredOutputResponse, params: Dict[str, Any], return_usage: bool = True, return_cost: bool = True) -> Tuple[StructuredOutputResponse, AIUsage, AICost]:
        """
        Abstract method to call and validate the underlying LLM API synchronously with structured output.
        Derived classes should implement this method.

        Args:
            params (Dict[str, Any]): The parameters to pass to the API.

        Returns:
            Tuple[StructuredOutputResponse, AIUsage, AICost]: The API response, usage, and cost.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    async def _call_api_structured_async(self, model_name: ModelName, structured_model: StructuredOutputResponse, params: Dict[str, Any], return_usage: bool = True, return_cost: bool = True) -> Tuple[StructuredOutputResponse, AIUsage, AICost]:
        """
        Abstract method to call and validate the underlying LLM API asynchronously with structured output.
        Derived classes should implement this method.

        Args:
            params (Dict[str, Any]): The parameters to pass to the API.

        Returns:
            Tuple[StructuredOutputResponse, AIUsage, AICost]: The API response, usage, and cost.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    # -------------------------------------------------------------------------------- #
    # Public Call Methods
    # -------------------------------------------------------------------------------- #

    def run(self, messages: Union[MessageList, List[Message], Message], return_usage: bool = True, return_cost: bool = True, **kwargs: Any) -> Tuple[ChatResponse, AIUsage, AICost]:
        """
        Synchronously call the LLM client using keyword arguments for flexibility.
        Merges initialized parameters with runtime parameters and performs the API call.

        A special key '__merge__' in kwargs can be provided as a dictionary to specify
        merge strategies for individual fields.

        Args:
            messages (Union[MessageList, List[Message], Message]): The messages for the call.
            **kwargs: Additional runtime parameters.

        Returns:
            Tuple[ChatResponse, AIUsage, AICost]: The API response, usage, and cost.
        """
        # Validate and reinitialize client if necessary.
        self._validate_client(use_async=False)

        # Copy the kwargs to avoid modifying the original.
        runtime_params = kwargs.copy()

        # Add the messages to the runtime parameters.
        runtime_params["messages"] = messages

        # Pop the merge flags.
        merge_flags = runtime_params.pop("__merge__", {})

        # Merge parameters.
        merged_params = self._merge_parameters(runtime_params, merge_flags)

        logger.debug(f"Making sync call with parameters: {merged_params}")

        # Now, pass the validated and filtered kwargs to the API call.
        chat_response, usage, cost = self._call_api_sync(model_name=merged_params.model, params=merged_params, return_usage=return_usage, return_cost=return_cost)

        # Return the response.
        return chat_response, usage, cost

    async def run_async(self, messages: Union[MessageList, List[Message], Message], return_usage: bool = True, return_cost: bool = True, **kwargs: Any) -> Tuple[ChatResponse, AIUsage, AICost]:
        """
        Asynchronously call the LLM client using keyword arguments for flexibility.
        Merges initialized parameters with runtime parameters and performs the API call.

        A special key '__merge__' in kwargs can be provided as a dictionary to specify
        merge strategies for individual fields.

        Args:
            messages (Union[MessageList, List[Message], Message]): The messages for the call.
            **kwargs: Additional runtime parameters.

        Returns:
            Tuple[ChatResponse, AIUsage, AICost]: The API response, usage, and cost.
        """
        # Validate and reinitialize client if necessary.
        self._validate_client(use_async=True)

        # Copy the kwargs to avoid modifying the original.
        runtime_params = kwargs.copy()

        # Add the messages to the runtime parameters.
        runtime_params["messages"] = messages

        # Pop the merge flags.
        merge_flags = runtime_params.pop("__merge__", {})

        # Merge parameters.
        merged_params = self._merge_parameters(runtime_params, merge_flags)

        logger.debug(f"Making async call with parameters: {merged_params}")

        # Now, pass the validated and filtered kwargs to the API call.
        chat_response, usage, cost = await self._call_api_async(model_name=merged_params.model, params=merged_params, return_usage=return_usage, return_cost=return_cost)

        # Return the response.
        return chat_response, usage, cost

    def run_structured(self, structured_model: StructuredOutputResponse, messages: Union[MessageList, List[Message], Message], return_usage: bool = True, return_cost: bool = True, **kwargs: Any) -> Tuple[StructuredOutputResponse, AIUsage, AICost]:
        """
        Synchronously call the LLM client with structured output using keyword arguments for flexibility.
        Merges initialized parameters with runtime parameters and performs the API call.

        A special key '__merge__' in kwargs can be provided as a dictionary to specify
        merge strategies for individual fields.

        Args:
            structured_model (StructuredOutputResponse): The model defining the structured output format.
            messages (Union[MessageList, List[Message], Message]): The messages for the call.
            **kwargs: Additional runtime parameters.

        Returns:
            Tuple[StructuredOutputResponse, AIUsage, AICost]: The API response, usage, and cost.
        """
        # Validate and reinitialize client if necessary.
        self._validate_client(use_async=False)

        # Copy the kwargs to avoid modifying the original.
        runtime_params = kwargs.copy()

        # Add the messages to the runtime parameters.
        runtime_params["messages"] = messages

        # Pop the merge flags.
        merge_flags = runtime_params.pop("__merge__", {})

        # Merge parameters.
        merged_params = self._merge_parameters(runtime_params, merge_flags)

        logger.debug(f"Making structured sync call with parameters: {merged_params}")

        # Now, pass the validated and filtered kwargs to the API call.
        structured_response, usage, cost = self._call_api_structured(model_name=merged_params.model, structured_model=structured_model, params=merged_params, return_usage=return_usage, return_cost=return_cost)

        # Return the response.
        return structured_response, usage, cost

    async def run_structured_async(self, structured_model: StructuredOutputResponse, messages: Union[MessageList, List[Message], Message], return_usage: bool = True, return_cost: bool = True, **kwargs: Any) -> Tuple[StructuredOutputResponse, AIUsage, AICost]:
        """
        Asynchronously call the LLM client with structured output using keyword arguments for flexibility.
        Merges initialized parameters with runtime parameters and performs the API call.

        A special key '__merge__' in kwargs can be provided as a dictionary to specify
        merge strategies for individual fields.

        Args:
            structured_model (StructuredOutputResponse): The model defining the structured output format.
            messages (Union[MessageList, List[Message], Message]): The messages for the call.
            **kwargs: Additional runtime parameters.

        Returns:
            Tuple[StructuredOutputResponse, AIUsage, AICost]: The API response, usage, and cost.
        """
        # Validate and reinitialize client if necessary.
        self._validate_client(use_async=True)

        # Copy the kwargs to avoid modifying the original.
        runtime_params = kwargs.copy()

        # Add the messages to the runtime parameters.
        runtime_params["messages"] = messages

        # Pop the merge flags.
        merge_flags = runtime_params.pop("__merge__", {})

        # Merge parameters.
        merged_params = self._merge_parameters(runtime_params, merge_flags)

        logger.debug(f"Making structured async call with parameters: {merged_params}")

        # Now, pass the validated and filtered kwargs to the API call.
        structured_response, usage, cost = await self._call_api_structured_async(model_name=merged_params.model, structured_model=structured_model, params=merged_params, return_usage=return_usage, return_cost=return_cost)

        # Return the response.
        return structured_response, usage, cost

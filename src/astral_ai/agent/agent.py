# -------------------------------------------------------------------------------- #
# Agent Class
# -------------------------------------------------------------------------------- #

"""
Agents are the main object of the 'intelligence' abstraction in Astral AI.
"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in Imports
from typing import Any, Dict, List, Optional, Union

# Pydantic Imports
from pydantic import BaseModel

# Astral AI Imports
from astral_ai.agent.base import BaseAgent
from astral_ai.clients.providers.base import BaseLLMClient
from astral_ai.typing.models import ModelName, PROVIDER_MODEL_NAMES
from astral_ai.constants.mappings import PROVIDER_MAPPING
from astral_ai.typing.messages import Message, MessageList
from astral_ai.workflow.actions.agent import AgentAction
from astral_ai.clients.types import ReasoningEffort, Tool, ToolChoiceOption

# -------------------------------------------------------------------------------- #
# AgentExpertise Class
# -------------------------------------------------------------------------------- #


class AgentExpertise(BaseModel):
    """
    The expertise of the agent.
    """
    pass

# -------------------------------------------------------------------------------- #
# Agent Class
# -------------------------------------------------------------------------------- #


class Agent(BaseAgent):
    """
    Agents are the main object of the 'intelligence' abstraction in Astral AI.
    """

    def __init__(self,
                 model_name: ModelName,
                 expertise: AgentExpertise,
                 reasoning_effort: Optional[ReasoningEffort] = None,
                 tools: Optional[List[Tool]] = None,
                 tool_choice: Optional[ToolChoiceOption] = None,
                 human: Optional[str] = None,
                 return_usage: bool = True,
                 return_cost: bool = True,
                 **kwargs: Any):
        """
        Initialize the agent.
        """
        super().__init__(model_name=model_name)

        self.expertise = expertise
        self.reasoning_effort = reasoning_effort
        self.tools = tools
        self.tool_choice = tool_choice
        self.human = human
        self.return_usage = return_usage
        self.return_cost = return_cost

        self.actions: Dict[str, AgentAction] = {}

        self.client_kwargs = kwargs
        self.client = self._initialize_client(model_name)

    # -------------------------------------------------------------------------------- #
    # Private Methods
    # -------------------------------------------------------------------------------- #
    def _initialize_client(self, model_name: ModelName) -> BaseLLMClient:
        provider = PROVIDER_MODEL_NAMES.get(model_name)
        if not provider:
            raise ValueError(f"Model name {model_name} is not supported")
        client_class = PROVIDER_MAPPING.get(provider)
        if not client_class:
            raise ValueError(f"No client available for provider: {provider}")
        return client_class(
            model_name=model_name,
            messages=self._expertise_to_message(self.expertise),
            reasoning_effort=self.reasoning_effort,
            tools=self.tools,
            tool_choice=self.tool_choice,
            user=self.human,
            **self.client_kwargs
        )

    # -------------------------------------------------------------------------------- #
    # Validation Methods
    # -------------------------------------------------------------------------------- #
    def _expertise_to_message(self, expertise: AgentExpertise) -> Message:
        """
        Validate the expertise of the agent.
        """
        if len(expertise) > 1:
            raise ValueError("Expertise must be a single message")
        expertise_message = Message(role="system", content=expertise)
        return expertise_message

    # -------------------------------------------------------------------------------- #
    # Public Methods
    # -------------------------------------------------------------------------------- #
    def create_action(
        self,
        action_name: str,
        task_template: Any,  # Replace Any with TaskTemplate if desired
        action_description: Optional[str] = None,
        template_kwargs: Optional[Dict[str, Any]] = None,
        task_reasoning_effort: Optional[ReasoningEffort] = None,
        task_tools: Optional[List[Tool]] = None,
        task_tool_choice: Optional[ToolChoiceOption] = None,
        human: Optional[str] = None,
    ) -> AgentAction:
        """
        Create an AgentAction and store it in the agent's actions.
        """
        agent_action = AgentAction(
            action_name=action_name,
            action_description=action_description,
            agent=self,
            task_template=task_template,
            template_kwargs=template_kwargs or {},
            task_reasoning_effort=task_reasoning_effort or self.reasoning_effort,
            task_tools=task_tools or self.tools,
            task_tool_choice=task_tool_choice or self.tool_choice,
            human=human or self.human
        )
        self.actions[action_name] = agent_action
        return agent_action

    def run(self, action_name: str) -> Any:
        """
        Run an action by its name.
        """
        if action_name not in self.actions:
            raise ValueError(f"Action '{action_name}' not found in agent '{self.model_name}'.")
        action = self.actions[action_name]
        return action.execute()

    def run_async(self, action_name: str) -> Any:
        """
        Run an action asynchronously by its name.
        """
        if action_name not in self.actions:
            raise ValueError(f"Action '{action_name}' not found in agent '{self.model_name}'.")
        action = self.actions[action_name]
        return action.execute_async()

    def run_agent(self) -> Any:
        """
        Run the agent.
        """
        pass

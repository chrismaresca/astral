# -------------------------------------------------------------------------------- #
# Agent Action
# -------------------------------------------------------------------------------- #

"""
Agent actions are actions that are executed by an agent.
"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in Imports
from typing import Any, Dict, List, Optional

# Pydantic Imports
from pydantic import BaseModel, Field, computed_field

# Astral AI Imports
from astral_ai.agent.base import BaseAgent
from astral_ai.clients.types import ReasoningEffort, Tool, ToolChoiceOption
from astral_ai.workflow.actions.base import BaseAction, TaskTemplate

# -------------------------------------------------------------------------------- #
# Agent Action
# -------------------------------------------------------------------------------- #


class AgentAction(BaseAction):
    """
    Agent actions are actions that are executed by an agent.
    """
    agent: BaseAgent = Field(..., description="The agent that owns this action")
    task_template: TaskTemplate = Field(..., description="The task template for the action")
    template_kwargs: Dict[str, Any] = Field(default_factory=dict, description="Keyword arguments for the task template")
    task_reasoning_effort: Optional[ReasoningEffort] = Field(None, description="The level of reasoning effort required")
    task_tools: Optional[List[Tool]] = Field(None, description="List of tools available to this action")
    task_tool_choice: Optional[ToolChoiceOption] = Field(None, description="Which tool to choose")
    human: Optional[str] = Field(None, description="Human who created the action")

    # -------------------------------------------------------------------------------- #
    # Metadata Methods
    # -------------------------------------------------------------------------------- #

    def get_metadata(self) -> Dict[str, Any]:
        """
        Return the metadata for the action.
        """
        return {
            "action_id": str(self.action_id),
            "action_type": self.action_type,
            "action_name": self.action_name,
            "action_description": self.action_description,
            "human": self.human,
            "model": self.agent.model_name,
            "reasoning_effort": self.task_reasoning_effort,
            "tools": self.task_tools,
            "tool_choice": self.task_tool_choice,
        }

    # -------------------------------------------------------------------------------- #
    # Dunder Methods
    # -------------------------------------------------------------------------------- #
    def __str__(self) -> str:
        """
        Return a string representation of the action.
        """
        return f"Agent Action: {self.action_name}\n" \
            f"Agent: {self.agent}\n" \
            f"Task Template: {self.task_template}\n" \
            f"Template Kwargs: {self.template_kwargs}\n" \
            f"Reasoning Effort: {self.task_reasoning_effort}\n" \
            f"Tools: {self.task_tools}\n" \
            f"Tool Choice: {self.task_tool_choice}\n" \
            f"User: {self.human}"

    def __repr__(self) -> str:
        """
        Return a string representation of the action.
        """
        return self.__str__()

    # -------------------------------------------------------------------------------- #
    # Execute
    # -------------------------------------------------------------------------------- #
    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the action. In a real implementation, this might call an LLM,
        run a function, or perform other complex behaviors.
        """
        print(f"Agent '{self.agent}' is executing action '{self.action_name}'")
        print(f"Task Template: {self.task_template}")
        print(f"Template Kwargs: {self.template_kwargs}")
        print(f"Reasoning Effort: {self.task_reasoning_effort}")
        print(f"Tools: {self.task_tools}")
        print(f"Tool Choice: {self.task_tool_choice}")
        print(f"User: {self.human}")
        return f"Executed {self.action_name} with template '{self.task_template}'"

    async def execute_async(self, *args, **kwargs) -> Any:
        """
        Execute the action asynchronously.
        """
        # For demonstration purposes, just call the synchronous version.
        return self.execute(*args, **kwargs)

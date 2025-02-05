# -------------------------------------------------------------------------------- #
# Base Step Class
# -------------------------------------------------------------------------------- #

"""
Base Step Class for Workflow Execution

This module defines the base step class for workflow execution.
"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in Imports
from typing import Any, Union
from uuid import uuid4, UUID
from abc import ABC, abstractmethod

# Pydantic Imports
from pydantic import BaseModel, Field, computed_field

# Astral AI Imports
from astral_ai.workflow.actions.base import BaseAction

# TODO: MOVE THESE


class StepOutput(BaseModel):
    """
    Output of a step.
    """
    pass


class StepOutputStructured(BaseModel):
    """
    Structured output of a step.
    """
    pass

# -------------------------------------------------------------------------------- #
# Base Step Class
# -------------------------------------------------------------------------------- #


# -------------------------------------------------------------------------------- #
# Base Step Class
# -------------------------------------------------------------------------------- #
class BaseStep(BaseModel, ABC):
    """
    Base class for workflow steps.

    Attributes:
        step_id (UUID): Unique identifier for the step.
        step_name (str): Name of the step.
        step_description (str): Description of the step.
        human (str): The human who created the step.
    """
    step_id: UUID = Field(default_factory=uuid4, description="A unique identifier for the step")
    step_name: str = Field(..., description="The name of the step")
    step_description: str = Field(..., description="A description of the step")
    human: str = Field(..., description="The human who created the step")
    action: BaseAction = Field(..., description="The action to execute")

    # -------------------------------------------------------------------------------- #
    # Config
    # -------------------------------------------------------------------------------- #
    class Config:
        arbitrary_types_allowed = True
        frozen = True
        allow_mutation = False

    # -------------------------------------------------------------------------------- #
    # Computed Fields
    # -------------------------------------------------------------------------------- #
    @computed_field
    def step_type(self) -> str:
        """
        Get the type of step.
        """
        return self.__class__.__name__

    @computed_field
    def step_metadata(self) -> dict[str, str]:
        """
        Get the metadata for the step.
        """
        return {
            "step_id": str(self.step_id),
            "step_type": self.step_type,
            "step_name": self.step_name,
            "step_description": self.step_description,
            "human": self.human,
        }

    # -------------------------------------------------------------------------------- #
    # Metadata Methods
    # -------------------------------------------------------------------------------- #
    def get_metadata(self) -> dict[str, str]:
        """
        Get the metadata for the step.
        """
        return self.step_metadata

    # -------------------------------------------------------------------------------- #
    # Dunder Methods
    # -------------------------------------------------------------------------------- #
    def __str__(self) -> str:
        """
        Return a visually appealing string representation of the step.
        """
        return (
            f"Step: {self.step_name}\n"
            f"Type: {self.step_type}\n"
            f"Description: {self.step_description}\n"
            f"Created by: {self.human}\n"
            f"Step ID: {self.step_id}"
        )

    def __repr__(self) -> str:
        """
        Return a string representation of the step.
        """
        return self.__str__()

    def __eq__(self, other: Any) -> bool:
        """
        Check if the step is equal to another step.
        """
        if not isinstance(other, BaseStep):
            return NotImplemented
        return self.step_id == other.step_id

    def __hash__(self) -> int:
        """
        Hash the step.
        """
        return hash(self.step_id)

    # -------------------------------------------------------------------------------- #
    # Abstract Methods
    # -------------------------------------------------------------------------------- #
    @abstractmethod
    def run(self) -> Union[StepOutput, StepOutputStructured]:
        """Run the step."""
        pass

    @abstractmethod
    async def run_async(self) -> Union[StepOutput, StepOutputStructured]:
        """Run the step asynchronously."""
        pass

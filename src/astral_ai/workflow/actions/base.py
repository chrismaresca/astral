# Need to use this for type checking
from __future__ import annotations
# -------------------------------------------------------------------------------- #
# Actions Class
# -------------------------------------------------------------------------------- #

"""
Action Base Models
"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in imports
from typing import Any, Dict, List, Optional, TypeVar
from uuid import uuid4, UUID
from abc import ABC, abstractmethod

# Pydantic imports
from pydantic import BaseModel, Field, computed_field

# Module imports
from astral_ai.workflow.steps.simple import SimpleStep
from astral_ai.workflow.steps.parallel import ParallelStep

# -------------------------------------------------------------------------------- #
# Type Variables
# -------------------------------------------------------------------------------- #
TaskTemplate = TypeVar("TaskTemplate")

# -------------------------------------------------------------------------------- #
# BaseAction Model
# -------------------------------------------------------------------------------- #
class BaseAction(BaseModel, ABC):
    """Base class for all actions in the workflow system."""
    
    action_id: UUID = Field(default_factory=uuid4, description="A unique identifier for the action")
    action_name: str = Field(..., description="The name of the action")
    action_description: Optional[str] = Field(None, description="A description of the action")
    human: Optional[str] = Field(None, description="Human who created the action")

    # -------------------------------------------------------------------------------- #
    # Computed Fields
    # -------------------------------------------------------------------------------- #
    @computed_field
    def action_type(self) -> str:
        """Returns the type of action."""
        return self.__class__.__name__

    # -------------------------------------------------------------------------------- #
    # Config
    # -------------------------------------------------------------------------------- #
    class Config:
        allow_mutation = False
        frozen = True
        arbitrary_types_allowed = True

    # -------------------------------------------------------------------------------- #
    # Metadata Methods
    # -------------------------------------------------------------------------------- #
    def get_metadata(self) -> Dict[str, Any]:
        """Returns metadata about the action."""
        return {
            "action_id": str(self.action_id),
            "action_type": self.action_type,
            "action_name": self.action_name,
            "action_description": self.action_description,
            "human": self.human,
        }

    # -------------------------------------------------------------------------------- #
    # Dunder Methods
    # -------------------------------------------------------------------------------- #
    def __str__(self) -> str:
        """Returns a string representation of the action."""
        return f"Action: {self.action_name}\n" \
               f"Type: {self.action_type}\n" \
               f"Description: {self.action_description}\n" \
               f"Created by: {self.human}"

    def __repr__(self) -> str:
        """Returns a string representation of the action."""
        return self.__str__()

    # -------------------------------------------------------------------------------- #
    # Helper Methods
    # -------------------------------------------------------------------------------- #
    def to_simple_step(self) -> SimpleStep:
        """Wrap this action in a SimpleStep."""
        return SimpleStep(action=self)

    def to_parallel_step(self, num_in_parallel: int = 2) -> ParallelStep:
        """Wrap this action in a ParallelStep."""
        return ParallelStep(action=self, num_in_parallel=num_in_parallel)

    # -------------------------------------------------------------------------------- #
    # Abstract Methods
    # -------------------------------------------------------------------------------- #
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """Execute the action."""
        pass

    @abstractmethod
    async def execute_async(self, *args, **kwargs) -> Any:
        """Execute the action asynchronously."""
        pass

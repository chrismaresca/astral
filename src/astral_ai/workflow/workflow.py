# -------------------------------------------------------------------------------- #
# Workflow Class
# -------------------------------------------------------------------------------- #

"""
Workflow Class

This class defines a workflow, which is a collection of steps to be executed.
Each workflow has its own metadata and execution methods.
"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #
from typing import Any, List
from uuid import uuid4, UUID
from pydantic import BaseModel, Field, computed_field
from astral_ai.workflow.steps.base import BaseStep

# -------------------------------------------------------------------------------- #
# Workflow Class
# -------------------------------------------------------------------------------- #


class Workflow(BaseModel):
    workflow_id: UUID = Field(default_factory=uuid4, description="A unique identifier for the workflow")
    name: str = Field(..., description="The name of the workflow")
    description: str = Field(..., description="A description of the workflow")
    human: str = Field(..., description="The human who created the workflow")
    steps: List[BaseStep] = Field(default_factory=list, description="The steps included in the workflow")

    # -------------------------------------------------------------------------------- #
    # Config
    # -------------------------------------------------------------------------------- #
    class Config:
        arbitrary_types_allowed = True
        # Workflows may be mutable so we don't mark them as frozen here.

    # -------------------------------------------------------------------------------- #
    # Computed Fields
    # -------------------------------------------------------------------------------- #
    @computed_field
    def workflow_metadata(self) -> dict[str, str]:
        """
        Returns the core metadata for the workflow.
        """
        return {
            "workflow_id": str(self.workflow_id),
            "name": self.name,
            "description": self.description,
            "human": self.human,
        }

    # -------------------------------------------------------------------------------- #
    # Metadata Methods
    # -------------------------------------------------------------------------------- #
    def get_metadata(self) -> dict[str, Any]:
        """
        Returns a dictionary of metadata for the workflow.
        This includes core metadata and a list of each step's id and type.
        """
        metadata = self.workflow_metadata.copy()
        steps_info = [
            {"step_id": str(step.step_id), "step_name": step.step_name, "step_type": step.step_type}
            for step in self.steps
        ]
        metadata["num_steps"] = len(self.steps)
        metadata["steps"] = steps_info
        return metadata

    # -------------------------------------------------------------------------------- #
    # Workflow Methods
    # -------------------------------------------------------------------------------- #
    def add_step(self, step: BaseStep) -> None:
        """
        Add a step to the workflow.
        """
        self.steps.append(step)

    def run(self) -> List[Any]:
        """
        Execute all steps in the workflow sequentially and collect their results.
        """
        results = []
        for step in self.steps:
            results.append(step.run())
        return results

    async def run_async(self) -> List[Any]:
        """
        Execute all steps in the workflow asynchronously and collect their results.
        """
        results = []
        for step in self.steps:
            results.append(await step.run_async())
        return results

    # -------------------------------------------------------------------------------- #
    # Dunder Methods
    # -------------------------------------------------------------------------------- #
    def __str__(self) -> str:
        """
        Return a visually appealing string representation of the workflow.
        """
        header = (
            f"Workflow: {self.name}\n"
            f"Description: {self.description}\n"
            f"Created by: {self.human}\n"
            f"Workflow ID: {self.workflow_id}\n"
            f"Steps Count: {len(self.steps)}\n"
            f"{'-'*40}\n"
        )
        steps_str = "\n".join(
            f"[{idx+1}] {step.step_name} ({step.step_type}) - {step.step_description}"
            for idx, step in enumerate(self.steps)
        )
        return header + steps_str

    def __repr__(self) -> str:
        """
        Return the string representation of the workflow.
        """
        return self.__str__()

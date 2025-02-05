# -------------------------------------------------------------------------------- #
# Parallel Step Class
# -------------------------------------------------------------------------------- #

"""
Parallel steps are steps that are executed in parallel.
"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #
# Built-in Imports

from typing import List, Optional, Union

# Pydantic Imports
from pydantic import BaseModel, Field

# Astral AI Imports
from astral_ai.workflow.steps.base import BaseStep, StepOutput, StepOutputStructured
from astral_ai.workflow.actions.base import BaseAction

# -------------------------------------------------------------------------------- #
# Parallel Step Class
# -------------------------------------------------------------------------------- #
class ParallelStep(BaseStep):
    """
    Parallel steps are steps that are executed in parallel.
    """
    action: BaseAction = Field(..., description="The action to execute")
    num_in_parallel: int = Field(default=2, description="The number of steps to execute in parallel")

    # -------------------------------------------------------------------------------- #
    # Methods
    # -------------------------------------------------------------------------------- #
    def run(self, num_in_parallel: Optional[int] = None) -> List[Union[StepOutput, StepOutputStructured]]:
        """
        Run the step by executing its associated action.
        """
        num = num_in_parallel or self.num_in_parallel
        results = [self.action.execute() for _ in range(num)]
        return results

    async def run_async(self, num_in_parallel: Optional[int] = None) -> List[Union[StepOutput, StepOutputStructured]]:
        """
        Run the step by executing its associated action asynchronously.
        """
        num = num_in_parallel or self.num_in_parallel
        results = [await self.action.execute_async() for _ in range(num)]
        return results

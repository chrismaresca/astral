# -------------------------------------------------------------------------------- #
# Simple Step Class
# -------------------------------------------------------------------------------- #

"""
Simple steps are steps that are executed in a linear manner.
"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #
from pydantic import BaseModel, Field
from astral_ai.workflow.steps.base import BaseStep
from astral_ai.workflow.actions.base import BaseAction

# -------------------------------------------------------------------------------- #
# Simple Step Class
# -------------------------------------------------------------------------------- #


class SimpleStep(BaseStep):
    """
    Simple steps are steps that are executed in a linear manner.
    """
    # -------------------------------------------------------------------------------- #
    # Methods
    # -------------------------------------------------------------------------------- #

    def run(self):
        """
        Run the step by executing its associated action.
        """
        return self.action.execute()

    def run_async(self):
        """
        Run the step by executing its associated action asynchronously.
        """
        return self.action.execute_async()

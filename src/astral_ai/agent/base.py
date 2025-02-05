# -------------------------------------------------------------------------------- #
# Base Agent Interface
# -------------------------------------------------------------------------------- #

"""
Defines a minimal agent interface that can be used in type annotations without
causing circular dependencies.
"""

from pydantic import BaseModel

class BaseAgent(BaseModel):
    """
    Minimal interface for an Agent.
    """
    model_name: str


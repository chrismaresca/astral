# -------------------------------------------------------------------------------- #
# AI Usage Models
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Base imports
from typing import TypeAlias

# Pydantic imports
from pydantic import BaseModel, Field

# -------------------------------------------------------------------------------- #
# Base Usage Types
# -------------------------------------------------------------------------------- #

TokenCount: TypeAlias = int
TokenCost: TypeAlias = float
Latency: TypeAlias = float


# -------------------------------------------------------------------------------- #
# AI Usage Model
# -------------------------------------------------------------------------------- #


class AIUsage(BaseModel):
    prompt_tokens: TokenCount = Field(description="The number of prompt tokens used", default=0)
    cached_prompt_tokens: TokenCount = Field(description="The number of cached prompt tokens used", default=0)
    completion_tokens: TokenCount = Field(description="The number of completion tokens used", default=0)
    total_tokens: TokenCount = Field(description="The total number of tokens used", default=0)
    latency: Latency = Field(description="The latency of the AI call", default=0)


# -------------------------------------------------------------------------------- #
# AI Cost Model
# -------------------------------------------------------------------------------- #


class AICost(BaseModel):
    input_cost: TokenCost = Field(description="The cost of the input tokens", default=0)
    cached_input_cost: TokenCost = Field(description="The cost of the cached input tokens", default=0)
    output_cost: TokenCost = Field(description="The cost of the output tokens", default=0)
    total_cost: TokenCost = Field(description="The total cost of the tokens", default=0)

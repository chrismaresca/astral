# -------------------------------------------------------------------------------- #
# Model Pricing Constants
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in imports
from typing import Dict, TypeAlias

# -------------------------------------------------------------------------------- #
# Type Aliases
# -------------------------------------------------------------------------------- #

Cost: TypeAlias = float

ModelCost: TypeAlias = Dict[str, Dict[str, Cost]]

# -------------------------------------------------------------------------------- #
# Constants
# -------------------------------------------------------------------------------- #

ONE_MILLION_TOKENS: float = 1000000.0

MODEL_PRICING: ModelCost = {
    "claude-3-5-sonnet": {'prompt_tokens': 0.0, 'cached_prompt_tokens': 0.0, 'output_tokens': 0.0},
    "claude-3-haiku": {'prompt_tokens': 0.0, 'cached_prompt_tokens': 0.0, 'output_tokens': 0.0},
    "claude-3-opus": {'prompt_tokens': 0.0, 'cached_prompt_tokens': 0.0, 'output_tokens': 0.0},
    "gpt-4o": {'prompt_tokens': 2.5, 'cached_prompt_tokens': 1.25, 'output_tokens': 10},
    "o1": {'prompt_tokens': 15, 'cached_prompt_tokens': 7.5, 'output_tokens': 60},
    "o1-mini": {'prompt_tokens': 3.0, 'cached_prompt_tokens': 1.5, 'output_tokens': 12},
    "o3-mini": {'prompt_tokens': 0.0, 'cached_prompt_tokens': 0.0, 'output_tokens': 0.0},
}

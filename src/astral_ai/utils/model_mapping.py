# model_mapping.py
"""
This module provides functions for mapping model aliases to specific model names and vice versa.
It also provides functions for retrieving the provider for a given model.
"""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from typing import Tuple
from astral_ai.typing.models import MODEL_DEFINITIONS

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------


def extract_date(model: str, alias: str) -> Tuple[int, int, int]:
    """
    Extract a date tuple (year, month, day) from a model name.

    Assumes the model name is in one of these formats:
      - "{alias}-{month}-{day}-{year}" (e.g., "gpt-4o-12-17-24")
      - "{alias}-{YYYYMMDD}" (e.g., "claude-3-opus-20240229")

    If parsing fails, returns (0, 0, 0) so that the model sorts lower.
    """
    # Remove the alias (and any hyphen) from the beginning.
    rest = model[len(alias):].lstrip("-")
    parts = rest.split("-")
    if len(parts) == 3:
        try:
            month = int(parts[0])
            day = int(parts[1])
            year = int(parts[2])
            if year < 100:
                year += 2000
            return (year, month, day)
        except ValueError:
            return (0, 0, 0)
    elif len(parts) == 1 and len(parts[0]) == 8:
        try:
            full_date = parts[0]
            year = int(full_date[:4])
            month = int(full_date[4:6])
            day = int(full_date[6:8])
            return (year, month, day)
        except ValueError:
            return (0, 0, 0)
    return (0, 0, 0)

# -----------------------------------------------------------------------------
# Resolve Model Name
# -----------------------------------------------------------------------------


def resolve_model_name(inp: str) -> str:
    """
    Given an input model identifier (alias or specific model name), return the resolved specific model name.

    If `inp` is an alias (i.e. a key in MODEL_DEFINITIONS), return the 'most_recent_model' from that definition.
    If `inp` is already a specific model and is present in one of the model definitions, it is returned unchanged.

    Raises:
        ValueError: If the model cannot be found.
    """
    if inp in MODEL_DEFINITIONS:
        return MODEL_DEFINITIONS[inp]["most_recent_model"]
    for alias, definition in MODEL_DEFINITIONS.items():
        if inp in definition["model_names"]:
            return inp
    raise ValueError(f"Model '{inp}' not found in available models.")

# -----------------------------------------------------------------------------
# Get Model Class
# -----------------------------------------------------------------------------


def get_model_class(inp: str) -> str:
    """
    For a given input (alias or specific model name), return the corresponding model class (alias).

    If the input is already an alias (i.e. a key in MODEL_DEFINITIONS), return it.
    If the input is a specific model name, search the model definitions for the alias that contains it.

    Raises:
        ValueError: If the model class cannot be determined.
    """
    if inp in MODEL_DEFINITIONS:
        return inp
    for alias, definition in MODEL_DEFINITIONS.items():
        if inp in definition["model_names"]:
            return alias
    raise ValueError(f"Could not resolve model class for input '{inp}'.")

# -----------------------------------------------------------------------------
# Get Provider
# -----------------------------------------------------------------------------


def get_provider(inp: str) -> str:
    """
    Given an input model identifier (alias or specific model name), return its provider.

    If `inp` is an alias, return the provider from the corresponding model definition.
    If `inp` is a specific model name, search the model definitions to find its provider.

    Raises:
        ValueError: If the provider cannot be determined.
    """
    if inp in MODEL_DEFINITIONS:
        return MODEL_DEFINITIONS[inp]["provider"]
    for alias, definition in MODEL_DEFINITIONS.items():
        if inp in definition["model_names"]:
            return definition["provider"]
    raise ValueError(f"Provider for model '{inp}' not found.")

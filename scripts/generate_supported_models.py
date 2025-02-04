#!/usr/bin/env python3
# scripts/generate_supported_models.py

"""
Build-time generator for supported models constants.

This script reads the single source-of-truth YAML file
(src/astral_ai/config/models.yaml) that contains details for each model,
including supported_features. For each feature flag that is set to true at the
model class level, it adds *all* models under that alias to the corresponding
constant list. The messaging support is now split between developer messages
and system messages. If neither is enabled, the model is added to the user-only
messages constant. Finally, it writes a formatted Python module with constants to
src/astral_ai/constants/supported_models.py.
"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #
import yaml
from pathlib import Path
import re

# -------------------------------------------------------------------------------- #
# Helper Function: extract_date
# -------------------------------------------------------------------------------- #
def extract_date(model: str, alias: str) -> tuple:
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

# -------------------------------------------------------------------------------- #
# Main Function
# -------------------------------------------------------------------------------- #
def main():
    # Load the YAML file from the config directory.
    yaml_path = Path("src/astral_ai/config/models.yaml")
    with yaml_path.open("r") as f:
        data = yaml.safe_load(f)
    models_data = data["models"]

    # Initialize lists for each supported feature.
    reasoning_effort_models = []
    structured_output_models = []
    image_ingestion_models = []
    function_call_models = []
    system_message_models = []
    developer_message_models = []
    only_user_message_models = []
    model_aliases = {}

    # Loop over each model definition.
    for m in models_data:
        alias = m["alias"]
        model_names = m["model_names"]
        features = m.get("supported_features", {})

        # Store model aliases.
        for model_name in model_names:
            model_aliases[model_name] = alias

        # Handle reasoning effort support.
        if features.get("reasoning_effort", False):
            reasoning_effort_models.extend(model_names + [alias])

        # Handle structured output support.
        if features.get("structured_output", False):
            structured_output_models.extend(model_names + [alias])

        # Handle image ingestion support.
        if features.get("image_ingestion", False):
            image_ingestion_models.extend(model_names + [alias])

        # Handle function call support.
        if features.get("function_call", False):
            function_call_models.extend(model_names + [alias])

        # Handle messaging support.
        # If a model supports developer messages, add it to that list.
        if features.get("developer_message", False):
            developer_message_models.extend(model_names + [alias])
        # If a model supports system messages, add it to that list.
        if features.get("system_message", False):
            system_message_models.extend(model_names + [alias])
        # If neither messaging feature is enabled, it supports only user messages.
        if not features.get("developer_message", False) and not features.get("system_message", False):
            only_user_message_models.extend(model_names + [alias])

    # Remove duplicates and sort the lists.
    reasoning_effort_models = sorted(set(reasoning_effort_models))
    structured_output_models = sorted(set(structured_output_models))
    image_ingestion_models = sorted(set(image_ingestion_models))
    function_call_models = sorted(set(function_call_models))
    system_message_models = sorted(set(system_message_models))
    developer_message_models = sorted(set(developer_message_models))
    only_user_message_models = sorted(set(only_user_message_models))

    # -------------------------------------------------------------------------------- #
    # Build Output Lines
    # -------------------------------------------------------------------------------- #
    output_lines = []
    output_lines.append("# -------------------------------------------------------------------------------- #\n")
    output_lines.append("# Supported Models Constants\n")
    output_lines.append("# -------------------------------------------------------------------------------- #\n\n")
    output_lines.append('"""\n')
    output_lines.append("Constants for supported models.\n\n")
    output_lines.append("This module contains the constants for the supported models.\n")
    output_lines.append('"""\n\n')
    output_lines.append("# -------------------------------------------------------------------------------- #\n")
    output_lines.append("# Imports\n")
    output_lines.append("# -------------------------------------------------------------------------------- #\n\n")
    output_lines.append("# Built-in imports\n")
    output_lines.append("from typing import List, Dict\n\n")
    output_lines.append("# Project-specific imports\n")
    output_lines.append("from astral_ai.typing.models import ModelName\n\n")
    output_lines.append("# -------------------------------------------------------------------------------- #\n")
    output_lines.append("# Constants\n")
    output_lines.append("# -------------------------------------------------------------------------------- #\n\n")
    
    # Write out model aliases first.
    output_lines.append("MODEL_ALIASES: Dict[ModelName, str] = {\n")
    for model, alias in sorted(model_aliases.items()):
        output_lines.append(f'    "{model}": "{alias}",\n')
    output_lines.append("}\n\n")
    
    # Write out each constant list.
    output_lines.append("REASONING_EFFORT_SUPPORTED_MODELS: List[ModelName] = [\n")
    for model in reasoning_effort_models:
        output_lines.append(f'    "{model}",\n')
    output_lines.append("]\n\n")
    
    output_lines.append("STRUCTURED_OUTPUT_SUPPORTED_MODELS: List[ModelName] = [\n")
    for model in structured_output_models:
        output_lines.append(f'    "{model}",\n')
    output_lines.append("]\n\n")
    
    output_lines.append("IMAGE_INGESTION_SUPPORTED_MODELS: List[ModelName] = [\n")
    for model in image_ingestion_models:
        output_lines.append(f'    "{model}",\n')
    output_lines.append("]\n\n")
    
    output_lines.append("FUNCTION_CALL_SUPPORTED_MODELS: List[ModelName] = [\n")
    for model in function_call_models:
        output_lines.append(f'    "{model}",\n')
    output_lines.append("]\n\n")
    
    output_lines.append("SYSTEM_MESSAGE_SUPPORTED_MODELS: List[ModelName] = [\n")
    for model in system_message_models:
        output_lines.append(f'    "{model}",\n')
    output_lines.append("]\n\n")
    
    output_lines.append("DEVELOPER_MESSAGE_SUPPORTED_MODELS: List[ModelName] = [\n")
    for model in developer_message_models:
        output_lines.append(f'    "{model}",\n')
    output_lines.append("]\n\n")
    
    output_lines.append("ONLY_USER_MESSAGE_SUPPORTED_MODELS: List[ModelName] = [\n")
    for model in only_user_message_models:
        output_lines.append(f'    "{model}",\n')
    output_lines.append("]\n")
    
    # -------------------------------------------------------------------------------- #
    # Write to Target File
    # -------------------------------------------------------------------------------- #
    target_path = Path("src/astral_ai/constants/supported_models.py")
    target_path.write_text("".join(output_lines))
    print(f"Generated {target_path}")

if __name__ == "__main__":
    main()

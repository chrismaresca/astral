#!/usr/bin/env python3
# scripts/generate_cost.py

import yaml
from pathlib import Path

def main():
    yaml_path = Path("src/astral_ai/config/providers.yaml")
    with yaml_path.open("r") as f:
        data = yaml.safe_load(f)
    providers_data = data["providers"]

    provider_mapping = {}
    for p in providers_data:
        provider = p["name"]
        llm_client = p["llm_client"]
        provider_mapping[provider] = llm_client

    output_lines = []
    output_lines.append("# -------------------------------------------------------------------------------- #\n")
    output_lines.append("# Provider Mappings\n")
    output_lines.append("# -------------------------------------------------------------------------------- #\n\n")
    output_lines.append("# -------------------------------------------------------------------------------- #\n")
    output_lines.append("# Imports\n")
    output_lines.append("# -------------------------------------------------------------------------------- #\n\n")
    output_lines.append("# Built-in imports\n")
    output_lines.append("from typing import Dict\n\n")
    output_lines.append("# Project-specific imports\n")
    output_lines.append("from astral_ai.agents.clients import *\n\n")
    output_lines.append("from astral_ai.typing.models import ModelProvider\n\n")
    output_lines.append("# -------------------------------------------------------------------------------- #\n")
    output_lines.append("# Mapping \n")
    output_lines.append("# -------------------------------------------------------------------------------- #\n\n")
    output_lines.append("ProviderMapping = Dict[ModelProvider, str]\n\n")
    output_lines.append("# -------------------------------------------------------------------------------- #\n")
    output_lines.append("# Constants\n")
    output_lines.append("# -------------------------------------------------------------------------------- #\n\n")
    output_lines.append("PROVIDER_MAPPING: ProviderMapping = {\n")
    for provider in sorted(provider_mapping.keys()):
        output_lines.append(f'    "{provider}": {provider_mapping[provider]},\n')
    output_lines.append("}\n")

    target_path = Path("src/astral_ai/constants/mappings.py")
    target_path.write_text("".join(output_lines))
    print(f"Generated {target_path}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# scripts/generate_cost.py

import yaml
from pathlib import Path

def main():
    yaml_path = Path("src/astral_ai/config/models.yaml")
    with yaml_path.open("r") as f:
        data = yaml.safe_load(f)
    models_data = data["models"]

    pricing_mapping = {}
    for m in models_data:
        alias = m["alias"]
        pricing = m["pricing"]
        # Build a pricing dict without the "per_million" field.
        pricing_mapping[alias] = {
            "prompt_tokens": pricing["prompt_tokens"],
            "cached_prompt_tokens": pricing["cached_prompt_tokens"],
            "output_tokens": pricing["output_tokens"],
        }

    output_lines = []
    output_lines.append("# -------------------------------------------------------------------------------- #\n")
    output_lines.append("# Model Pricing Constants\n")
    output_lines.append("# -------------------------------------------------------------------------------- #\n\n")
    output_lines.append("# -------------------------------------------------------------------------------- #\n")
    output_lines.append("# Imports\n")
    output_lines.append("# -------------------------------------------------------------------------------- #\n\n")
    output_lines.append("# Built-in imports\n")
    output_lines.append("from typing import Dict, TypeAlias\n\n")
    output_lines.append("# -------------------------------------------------------------------------------- #\n")
    output_lines.append("# Type Aliases\n")
    output_lines.append("# -------------------------------------------------------------------------------- #\n\n")
    output_lines.append("Cost: TypeAlias = float\n\n")
    output_lines.append("ModelCost: TypeAlias = Dict[str, Dict[str, Cost]]\n\n")
    output_lines.append("# -------------------------------------------------------------------------------- #\n")
    output_lines.append("# Constants\n")
    output_lines.append("# -------------------------------------------------------------------------------- #\n\n")
    output_lines.append("ONE_MILLION_TOKENS: float = 1000000.0\n\n")
    output_lines.append("MODEL_PRICING: ModelCost = {\n")
    for alias in sorted(pricing_mapping.keys()):
        output_lines.append(f'    "{alias}": {pricing_mapping[alias]},\n')
    output_lines.append("}\n")

    target_path = Path("src/astral_ai/constants/usage.py")
    target_path.write_text("".join(output_lines))
    print(f"Generated {target_path}")

if __name__ == "__main__":
    main()

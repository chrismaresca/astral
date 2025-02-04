#!/usr/bin/env python3
# scripts/generate_types.py

import yaml
from pathlib import Path
import re

def extract_date(model: str, alias: str) -> tuple:
    """
    Given a model name and its alias, extract a (year, month, day) tuple.
    Supports either a "MM-DD-YY" format (assumed to be two-digit year, 2000+) or
    a "YYYYMMDD" format after the alias.
    Returns (0,0,0) if extraction fails.
    """
    suffix = model[len(alias):].lstrip("-")
    parts = suffix.split("-")
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
    if re.fullmatch(r"\d{8}", suffix):
        try:
            year = int(suffix[:4])
            month = int(suffix[4:6])
            day = int(suffix[6:8])
            return (year, month, day)
        except ValueError:
            return (0, 0, 0)
    return (0, 0, 0)

def main():
    # Load the YAML file from the config directory.
    yaml_path = Path("src/astral_ai/config/models.yaml")
    with yaml_path.open("r") as f:
        data = yaml.safe_load(f)
    models_data = data["models"]

    providers_set = set()
    aliases_set = set()
    model_ids_set = set()  # These will be the raw model IDs (formerly model names)
    definitions = {}  # Map alias -> definition dictionary
    model_id_to_provider = {}  # Map model_id -> provider

    for m in models_data:
        provider = m["provider"]
        alias = m["alias"]
        model_ids = m["model_names"]  # From the YAML; these will become our ModelIds
        pricing = m["pricing"]

        providers_set.add(provider)
        aliases_set.add(alias)
        model_ids_set.update(model_ids)

        # Map each model ID to its provider
        for model_id in model_ids:
            model_id_to_provider[model_id] = provider

        # Compute most_recent_model by sorting the model_ids list by extracted date.
        try:
            sorted_ids = sorted(model_ids, key=lambda x: extract_date(x, alias))
            most_recent_model = sorted_ids[-1]
        except Exception:
            most_recent_model = model_ids[-1]

        definitions[alias] = {
            "provider": provider,
            "model_ids": model_ids,
            "pricing": {**pricing, "per_million": 1000000},
            "most_recent_model": most_recent_model,
        }

    output_lines = []
    output_lines.append("from typing import Literal, Dict, TypeAlias\n\n")
    output_lines.append("# Auto-generated types and constants\n\n")

    # ModelProvider literal.
    sorted_providers = sorted(providers_set)
    output_lines.append("ModelProvider = Literal[\n")
    for p in sorted_providers:
        output_lines.append(f'    "{p}",\n')
    output_lines.append("]\n\n")

    # ModelAlias literal.
    sorted_aliases = sorted(aliases_set)
    output_lines.append("ModelAlias = Literal[\n")
    for a in sorted_aliases:
        output_lines.append(f'    "{a}",\n')
    output_lines.append("]\n\n")

    # ModelId literal.
    sorted_model_ids = sorted(model_ids_set)
    output_lines.append("ModelId = Literal[\n")
    for mid in sorted_model_ids:
        output_lines.append(f'    "{mid}",\n')
    output_lines.append("]\n\n")

    # ModelName TypeAlias as the union of ModelId and ModelAlias.
    output_lines.append("ModelName: TypeAlias = Literal[ModelId, ModelAlias]\n\n")

    # MODEL_DEFINITIONS mapping.
    output_lines.append("MODEL_DEFINITIONS = {\n")
    for alias in sorted_aliases:
        defn = definitions[alias]
        provider = defn["provider"]
        model_ids = defn["model_ids"]
        pricing = defn["pricing"]
        most_recent = defn["most_recent_model"]
        output_lines.append(f'    "{alias}": {{\n')
        output_lines.append(f'        "provider": "{provider}",\n')
        output_lines.append(f'        "model_ids": {model_ids},\n')
        output_lines.append(f'        "pricing": {pricing},\n')
        output_lines.append(f'        "most_recent_model": "{most_recent}"\n')
        output_lines.append("    },\n")
    output_lines.append("}\n\n")

    # PROVIDER_MODEL_NAMES mapping: maps each model ID and alias to its provider.
    output_lines.append("PROVIDER_MODEL_NAMES: Dict[ModelName, ModelProvider] = {\n")
    for model_id in sorted_model_ids:
        provider = model_id_to_provider[model_id]
        output_lines.append(f'    "{model_id}": "{provider}",\n')

    for model_alias in sorted_aliases:
        provider = definitions[model_alias]["provider"]
        output_lines.append(f'    "{model_alias}": "{provider}",\n')
    output_lines.append("}\n\n")

    # Dynamically generate Literals for provider-specific models.
    # We'll collect all model names (model IDs and aliases) for each provider.
    provider_to_models = {p: set() for p in providers_set}
    for model_id in sorted_model_ids:
        provider = model_id_to_provider[model_id]
        provider_to_models[provider].add(model_id)
    for alias in sorted_aliases:
        provider = definitions[alias]["provider"]
        provider_to_models[provider].add(alias)

    # For example, for OpenAI and Anthropic, generate Literals.
    if "openai" in provider_to_models:
        openai_models = sorted(provider_to_models["openai"])
        output_lines.append("OpenAIModels = Literal[\n")
        for m in openai_models:
            output_lines.append(f'    "{m}",\n')
        output_lines.append("]\n\n")
    if "anthropic" in provider_to_models:
        anthropic_models = sorted(provider_to_models["anthropic"])
        output_lines.append("AnthropicModels = Literal[\n")
        for m in anthropic_models:
            output_lines.append(f'    "{m}",\n')
        output_lines.append("]\n\n")

    # Write to the target file.
    target_path = Path("src/astral_ai/typing/models.py")
    target_path.write_text("".join(output_lines))
    print(f"Generated {target_path}")

if __name__ == "__main__":
    main()

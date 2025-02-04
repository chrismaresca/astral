# -------------------------------------------------------------------------------- #
# Usage Utils
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in imports
from typing import Tuple
import time

# Pydantic imports
from pydantic import BaseModel

# OpenAI imports
from openai.types.chat.chat_completion import ChatCompletion

# AI imports
from astral_ai.typing.models import ModelName
from astral_ai.typing.usage import AIUsage, AICost
from astral_ai.constants.usage import MODEL_PRICING, ONE_MILLION_TOKENS

# Logger
from astral_ai.logger import AIModuleLogger

# -------------------------------------------------------------------------------- #
# Model Cost Functions
# -------------------------------------------------------------------------------- #

# Initialize logger
logger = AIModuleLogger()


def track_model_cost(model_name: ModelName, usage: AIUsage) -> AICost:
    """
    Tracks and calculates model cost for AI model calls.

    Args:
        model_name (str): Name of the AI model used
        usage (AIUsage): Usage statistics from the model call

    Returns:
        AICost: Calculated costs for the model usage
    """
    logger.debug(f"Starting cost calculation for model {model_name}")
    logger.debug(f"Input usage stats: {usage}")

    # Compute costs from usage
    cost_config = MODEL_PRICING[model_name]

    prompt_cost = (usage.prompt_tokens - usage.cached_prompt_tokens) / ONE_MILLION_TOKENS * cost_config["prompt_tokens"]
    cached_prompt_cost = (usage.cached_prompt_tokens / ONE_MILLION_TOKENS) * cost_config["cached_prompt_tokens"]
    output_cost = (usage.completion_tokens / ONE_MILLION_TOKENS) * cost_config["output_tokens"]
    total_cost = prompt_cost + cached_prompt_cost + output_cost

    ai_cost = AICost(input_cost=prompt_cost, cached_input_cost=cached_prompt_cost, output_cost=output_cost, total_cost=total_cost)

    # Log detailed usage and costs
    logger.info(
        f"[{model_name}] Usage & Cost Stats: "
        f"prompt_tokens used: {usage.prompt_tokens} and cost ${prompt_cost:.4f}, "
        f"cached_prompt_tokens used: {usage.cached_prompt_tokens} and cost ${cached_prompt_cost:.4f}, "
        f"completion_tokens used: {usage.completion_tokens} and cost ${output_cost:.4f}, "
        f"total_tokens used: {usage.total_tokens} and cost ${total_cost:.4f}"
    )

    return ai_cost


# -------------------------------------------------------------------------------- #
# Update AI Metrics Functions
# -------------------------------------------------------------------------------- #

def update_ai_metrics(
    current_ai_usage: AIUsage,
    current_ai_cost: AICost,
    increment_ai_usage: AIUsage,
    increment_ai_cost: AICost,
) -> Tuple[AIUsage, AICost]:
    """
    Sums the current AI usage and cost with the incremented AI usage and cost.
    """
    logger.debug("Starting metrics update")
    logger.debug(f"Current usage: {current_ai_usage}")
    logger.debug(f"Current cost: {current_ai_cost}")
    logger.debug(f"Increment usage: {increment_ai_usage}")
    logger.debug(f"Increment cost: {increment_ai_cost}")

    current_ai_usage.prompt_tokens += increment_ai_usage.prompt_tokens
    current_ai_usage.cached_prompt_tokens += increment_ai_usage.cached_prompt_tokens
    current_ai_usage.completion_tokens += increment_ai_usage.completion_tokens
    current_ai_usage.total_tokens += increment_ai_usage.total_tokens

    current_ai_cost.input_cost += increment_ai_cost.input_cost
    current_ai_cost.cached_input_cost += increment_ai_cost.cached_input_cost
    current_ai_cost.output_cost += increment_ai_cost.output_cost
    current_ai_cost.total_cost += increment_ai_cost.total_cost

    current_ai_usage.latency += increment_ai_usage.latency

    logger.debug(f"Updated usage: {current_ai_usage}")
    logger.debug(f"Updated cost: {current_ai_cost}")
    logger.info(f"Metrics updated - Total tokens: {current_ai_usage.total_tokens}, Total cost: ${current_ai_cost.total_cost:.4f}")

    return current_ai_usage, current_ai_cost


# -------------------------------------------------------------------------------- #
# Compute Usage and Cost Functions
# -------------------------------------------------------------------------------- #


def compute_usage_and_cost(response: ChatCompletion,
                           model_name: ModelName,
                           start_time: float) -> Tuple[AIUsage, AICost]:
    """
    Given a ChatCompletion and model info, compute usage and cost.
    """
    logger.debug(f"Starting usage and cost computation for model {model_name}")

    # End timer
    end_time = time.monotonic()

    # Compute latency
    latency = end_time - start_time
    logger.debug(f"Request latency: {latency:.4f}s")

    # Compute usage and cost
    usage = AIUsage(
        prompt_tokens=response.usage.prompt_tokens,
        cached_prompt_tokens=response.usage.prompt_tokens_details.cached_tokens,
        completion_tokens=response.usage.completion_tokens,
        total_tokens=response.usage.total_tokens,
        latency=latency
    )
    logger.debug(f"Computed usage: {usage}")

    # Compute cost
    cost = track_model_cost(model_name, usage)

    logger.info(f"Completed usage and cost computation - Model: {model_name}, Total tokens: {usage.total_tokens}, Total cost: ${cost.total_cost:.4f}, Latency: {latency:.4f}s")

    # Return usage and cost
    return usage, cost

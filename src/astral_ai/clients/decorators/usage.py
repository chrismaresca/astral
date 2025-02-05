# -------------------------------------------------------------------------------- #
# Usage Decorator
# -------------------------------------------------------------------------------- #

"""
This decorator is used to calculate the usage and cost for a chat completion request.
It times the execution of the decorated function, computes usage metrics
from the response, and then computes cost based on the model used.
"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in
import functools
import time
import asyncio
from typing import Tuple, Callable, Union, Any

# Astral AI
from astral_ai.utils.usage_utils import AIUsage, AICost, track_model_cost
from astral_ai.logger import logger

# OpenAI
from openai.types.chat import ChatCompletion, ParsedChatCompletion


# -------------------------------------------------------------------------------- #
# Usage Decorator
# -------------------------------------------------------------------------------- #

def calculate_cost_and_usage(
    func: Callable[..., Union[ChatCompletion, ParsedChatCompletion, Tuple[ChatCompletion, AIUsage], Tuple[ChatCompletion, AICost], Tuple[ChatCompletion, AIUsage, AICost]]]
) -> Callable[..., Tuple[ChatCompletion, Union[AIUsage, None], Union[AICost, None]]]:
    """
    Decorator that calculates the usage and cost for a chat completion request.
    It times the execution of the decorated function, computes usage metrics
    from the response, and then computes cost based on the model used.
    """

    def process_response(
        response: Union[ChatCompletion, ParsedChatCompletion],
        start_time: float,
        model_name: str,
        ret_usage: bool,
        ret_cost: bool,
        request_type: str
    ) -> Tuple[ChatCompletion, Union[AIUsage, None], Union[AICost, None]]:
        end_time = time.monotonic()
        latency = end_time - start_time
        logger.debug(f"{request_type.capitalize()} request latency: {latency:.4f}s")

        # If neither usage nor cost are requested, return the original response with None values
        if not (ret_usage or ret_cost):
            return response, None, None

        usage = AIUsage(
            prompt_tokens=response.usage.prompt_tokens,
            cached_prompt_tokens=response.usage.prompt_tokens_details.cached_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
            latency=latency
        ) if ret_usage else None
        
        if usage:
            logger.debug(f"Computed {request_type} usage: {usage}")

        cost = None
        if ret_cost:
            cost = track_model_cost(model_name, usage or AIUsage(
                prompt_tokens=response.usage.prompt_tokens,
                cached_prompt_tokens=response.usage.prompt_tokens_details.cached_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
                latency=latency
            ))
            logger.info(
                f"Completed {request_type} usage and cost computation - Model: {model_name}, "
                f"Total tokens: {usage.total_tokens if usage else 'N/A'}, Total cost: ${cost.total_cost:.4f}, "
                f"Latency: {latency:.4f}s"
            )

        return response, usage, cost

    # Async wrapper
    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Tuple[ChatCompletion, Union[AIUsage, None], Union[AICost, None]]:
            model_name = kwargs.get('model_name')

            if model_name is None:
                raise ValueError("The decorated function must be called with a 'model_name' keyword argument.")

            request_type = "async"
            logger.debug(f"Starting {request_type} request for model {model_name}")
            start_time = time.monotonic()

            # Await the original function.
            response: Union[ChatCompletion, ParsedChatCompletion] = await func(*args, **kwargs)

            return process_response(
                response,
                start_time,
                model_name,
                kwargs.get('return_usage', False),
                kwargs.get('return_cost', False),
                request_type
            )
        return async_wrapper

    # Synchronous wrapper
    else:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> Tuple[ChatCompletion, Union[AIUsage, None], Union[AICost, None]]:
            model_name = kwargs.get('model_name')
            if model_name is None:
                raise ValueError("The decorated function must be called with a 'model_name' keyword argument.")

            request_type = "sync"
            logger.debug(f"Starting {request_type} request for model {model_name}")
            start_time = time.monotonic()

            response: Union[ChatCompletion, ParsedChatCompletion] = func(*args, **kwargs)

            return process_response(
                response,
                start_time,
                model_name,
                kwargs.get('return_usage', False),
                kwargs.get('return_cost', False),
                request_type
            )
        return sync_wrapper

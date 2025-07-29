import asyncio
from typing import Coroutine, Any, TypeVar
import nest_asyncio

T = TypeVar("T")


def run_coroutine_in_appropriate_loop(coro: Coroutine[Any, Any, T]) -> T:
    """
    Runs a coroutine in the appropriate event loop context and returns its result.

    This handles three cases:
    1. Inside a running event loop - creates a future and waits for it
    2. Event loop exists but not running - runs until complete
    3. No event loop available - creates a new one with asyncio.run

    Returns:
        The result of the coroutine
    """
    # Try to run the coroutine in the current event loop if possible
    try:
        # only solution I found for running loop inside another loop:
        # https://github.com/python/cpython/issues/66435#issuecomment-2003904906
        nest_asyncio.apply()
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro)
    except RuntimeError as e:
        # if "There is no current event loop in thread"
        if "There is no current event loop in thread" in str(e):
            return asyncio.run(coro)
        else:
            raise e

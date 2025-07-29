import asyncio
from typing import Coroutine, Any, TypeVar
from ._async import allow_nested_run, run

T = TypeVar("T")


def async_to_sync(coro: Coroutine[Any, Any, T]) -> T:
    """
    Runs a coroutine through greenlet.

    Discovered this PR through: https://github.com/oremanj/greenback/issues/32
    which led to: https://github.com/ARM-software/devlib/pull/683
    which led to: https://raw.githubusercontent.com/ARM-software/devlib/refs/heads/master/devlib/utils/asyn.py
    which I directly copied to _async.py

    This handles three cases:
    1. Inside a running event loop - allow nested run with greenlet
    3. No event loop available - creates a new one with asyncio.run

    Returns:
        The result of the coroutine
    """
    # Try to run the coroutine in the current event loop if possible
    try:
        # triggers error if no event loop is available
        asyncio.get_event_loop()

        allow_nested_run(coro)
        result = run(coro)
        return result  # type: ignore
    except RuntimeError as e:
        # if "There is no current event loop in thread"
        if "There is no current event loop in thread" in str(e):
            return asyncio.run(coro)
        else:
            raise e

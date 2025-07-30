import asyncio
from collections.abc import Awaitable, Coroutine
from typing import Any, TypeVar

T = TypeVar("T")


async def run(coroutine: Coroutine[Any, Any, Awaitable[T]]) -> T:
    """Run a coroutine and return the result, using uvloop if available."""
    try:
        import uvloop  # type: ignore[import-not-found]

        return await uvloop.run(coroutine)
    except ImportError:
        return await asyncio.run(coroutine)

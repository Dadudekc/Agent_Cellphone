"""Utility functions for retrying operations with timeouts."""

from __future__ import annotations

import time
from functools import wraps
from typing import Any, Callable, Iterable, Tuple, Type


ExceptionTypes = Iterable[Type[BaseException]]


def retry(
    retries: int = 3,
    delay: float = 0.5,
    exceptions: ExceptionTypes = (Exception,),
    timeout: float | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Retry a function upon failure with optional timeout.

    Parameters
    ----------
    retries:
        Number of retry attempts before giving up.
    delay:
        Delay in seconds between attempts.
    exceptions:
        Exceptions that trigger a retry.
    timeout:
        Maximum total time in seconds for all attempts. ``None`` means no timeout.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            deadline = time.time() + timeout if timeout is not None else None
            attempt = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions:  # type: ignore[misc]
                    attempt += 1
                    if attempt > retries or (deadline and time.time() > deadline):
                        raise
                    time.sleep(delay)
        return wrapper

    return decorator

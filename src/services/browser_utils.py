"""Utility helpers for consistent browser/network operations.

This module centralizes common behaviours needed by high-volume web
scraping components:

* Exponential backoff with jitter for fragile network/DOM operations.
* Proxy and user-agent rotation to reduce blocks during scraping.
* Structured JSON logging with optional trace identifiers.

The helpers here are lightweight and have no external dependencies
beyond the Python standard library so they can be reused across both
server and client side modules.
"""

from __future__ import annotations

import json
import logging
import os
import random
import time
import uuid
from typing import Callable, Iterable, Optional, Tuple, Type, TypeVar


T = TypeVar("T")


# ---------------------------------------------------------------------------
# Proxy and User-Agent rotation
# ---------------------------------------------------------------------------

# Default user agents. These are intentionally minimal; callers may
# provide additional values via the ``SCRAPER_USER_AGENTS`` environment
# variable (comma separated).
DEFAULT_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
]


def _load_from_env(var: str) -> Iterable[str]:
    """Load comma separated values from environment variable."""

    value = os.getenv(var, "")
    if not value:
        return []
    return [v.strip() for v in value.split(",") if v.strip()]


USER_AGENTS = list(DEFAULT_USER_AGENTS) + list(_load_from_env("SCRAPER_USER_AGENTS"))
PROXIES = list(_load_from_env("SCRAPER_PROXIES"))


def get_next_user_agent() -> str:
    """Return a random user-agent string for outgoing requests."""

    if not USER_AGENTS:
        return "AgentCellPhone/1.0"
    return random.choice(USER_AGENTS)


def get_next_proxy() -> Optional[str]:
    """Return a random proxy address or ``None`` if no proxies configured."""

    return random.choice(PROXIES) if PROXIES else None


def get_request_kwargs() -> dict:
    """Return common keyword arguments for :mod:`requests` calls.

    Includes rotated user-agent and proxy configuration.  Modules that
    perform HTTP requests can simply update their arguments with the
    returned dictionary::

        requests.get(url, timeout=5, **get_request_kwargs())
    """

    headers = {"User-Agent": get_next_user_agent()}
    proxy = get_next_proxy()
    kwargs = {"headers": headers}
    if proxy:
        kwargs["proxies"] = {"http": proxy, "https": proxy}
    return kwargs


# ---------------------------------------------------------------------------
# Structured JSON logging
# ---------------------------------------------------------------------------


class _JsonFormatter(logging.Formatter):
    """Simple JSON log formatter used by :func:`get_logger`."""

    def format(self, record: logging.LogRecord) -> str:  # pragma: no cover -
        data = {
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, "trace_id"):
            data["trace_id"] = record.trace_id
        if hasattr(record, "data"):
            data.update(record.data)
        return json.dumps(data)


def get_logger(name: str = "browser") -> logging.Logger:
    """Return a logger configured for JSON output."""

    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(_JsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def log(logger: logging.Logger, level: int, message: str, **data) -> str:
    """Log ``message`` with structured JSON and return a trace identifier."""

    trace_id = data.pop("trace_id", str(uuid.uuid4()))
    logger.log(level, message, extra={"trace_id": trace_id, "data": data})
    return trace_id


# ---------------------------------------------------------------------------
# Retry helper with exponential backoff and jitter
# ---------------------------------------------------------------------------


def retry_with_backoff(
    func: Callable[..., T],
    *args,
    retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    logger: Optional[logging.Logger] = None,
    **kwargs,
) -> T:
    """Execute ``func`` with automatic retries on failure.

    Implements exponential backoff with jitter between attempts.  If all
    retries fail the final exception is raised.
    """

    delay = base_delay
    attempt = 0
    while True:
        try:
            return func(*args, **kwargs)
        except exceptions as exc:  # pragma: no cover - simple wrapper
            attempt += 1
            if attempt > retries:
                if logger:
                    log(logger, logging.ERROR, "max_retries_exceeded", error=str(exc))
                raise
            sleep = min(delay, max_delay) * random.uniform(0.5, 1.5)
            if logger:
                log(
                    logger,
                    logging.WARNING,
                    "retrying",
                    attempt=attempt,
                    delay=sleep,
                    error=str(exc),
                )
            time.sleep(sleep)
            delay *= 2


__all__ = [
    "retry_with_backoff",
    "get_next_proxy",
    "get_next_user_agent",
    "get_request_kwargs",
    "get_logger",
    "log",
]


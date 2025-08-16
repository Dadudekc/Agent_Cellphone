"""Integration layer leveraging the shared watchdog utility.

This module wires the generic :class:`~src.core.utils.watchdog.Watchdog`
into a simple progress-based monitor.  When no progress has been signalled
within the ``probe_timeout_ms`` from the provided autopolicy, a recovery
callback is invoked.  By delegating scheduling and threading concerns to
the existing watchdog utility we avoid duplicating infrastructure.
"""

from __future__ import annotations

import time
from typing import Callable, Mapping

from .utils.watchdog import Watchdog


class WatchdogIntegration:
    """Monitor progress and invoke a recovery action when stalled."""

    def __init__(self, autopolicy: Mapping[str, int], on_recover: Callable[[], None]) -> None:
        self.probe_timeout_ms = int(autopolicy.get("probe_timeout_ms", 1000))
        self.on_recover = on_recover
        self._last_progress = time.monotonic()

        timeout = self.probe_timeout_ms / 1000.0
        interval = min(0.1, timeout / 2)
        self._watchdog = Watchdog(interval, self._check)

    def signal_progress(self) -> None:
        """Record that some progress has been made."""
        self._last_progress = time.monotonic()

    def _check(self) -> None:
        if time.monotonic() - self._last_progress > self.probe_timeout_ms / 1000.0:
            self.on_recover()
            # Reset progress to avoid continuous triggering until action updates
            self.signal_progress()

    def start(self) -> None:
        """Start monitoring in a background thread via the shared watchdog."""
        self._watchdog.start()

    def stop(self) -> None:
        """Stop monitoring."""
        self._watchdog.stop()


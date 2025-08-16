"""High level guard utilities for ensuring agent autonomy processes do not stall."""

from __future__ import annotations

from typing import Callable, Mapping

from .watchdog_integration import WatchdogIntegration


def enforce(
    operation: Callable[[Callable[[], None]], None],
    autopolicy: Mapping[str, int],
    on_recover: Callable[[], None],
) -> None:
    """Run an operation while watching for stalls.

    Parameters
    ----------
    operation: Callable[[Callable[[], None]], None]
        Function representing a commit or test process. It receives a
        ``signal_progress`` callback and should invoke it whenever progress
        is made.
    autopolicy: Mapping[str, int]
        Policy configuration containing ``probe_timeout_ms``.
    on_recover: Callable[[], None]
        Callback invoked if the watchdog determines the operation has
        stalled.
    """

    watchdog = WatchdogIntegration(autopolicy, on_recover)
    watchdog.start()
    try:
        operation(watchdog.signal_progress)
    finally:
        watchdog.stop()

"""Simple watchdog monitoring utilities."""

from __future__ import annotations

import logging
import threading
import time
from typing import Callable


class Watchdog:
    """Periodically run a check function and report failures."""

    def __init__(
        self,
        interval: float,
        check_fn: Callable[[], None],
        alert_fn: Callable[[BaseException], None] | None = None,
    ) -> None:
        self.interval = interval
        self.check_fn = check_fn
        self.alert_fn = alert_fn or self._default_alert
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    @staticmethod
    def _default_alert(error: BaseException) -> None:  # pragma: no cover - logging
        logging.error("Watchdog detected failure: %s", error)

    def start(self) -> None:
        """Start the watchdog in a background thread."""
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop the watchdog thread."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=self.interval * 2)

    def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                self.check_fn()
            except Exception as exc:  # pragma: no cover - alert path
                self.alert_fn(exc)
            time.sleep(self.interval)

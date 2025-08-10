"""Simple event bus for publishing updates to interested subscribers.

The event bus implements a minimal observer pattern.  Components can
subscribe with a callback to receive events, and publishers can push
events to the bus.  The bus also keeps a short history of events which
can be exposed via the API for health/status reporting.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Any


class EventBus:
    """Light‑weight pub/sub event bus."""

    def __init__(self) -> None:
        self._subscribers: List[Callable[[Dict[str, Any]], None]] = []
        self._events: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    def publish(self, event: Dict[str, Any]) -> None:
        """Publish an event to all subscribers and store it."""

        self._events.append(event)
        for callback in list(self._subscribers):
            try:
                callback(event)
            except Exception:
                # Subscribers are isolated; errors are ignored so one bad
                # consumer doesn't break the others.
                pass

    # ------------------------------------------------------------------
    def subscribe(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    # ------------------------------------------------------------------
    def unsubscribe(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        if callback in self._subscribers:
            self._subscribers.remove(callback)

    # ------------------------------------------------------------------
    def get_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Return the most recent events."""

        if limit <= 0:
            return list(self._events)
        return self._events[-limit:]


# Global singleton used by the API and other components
event_bus = EventBus()


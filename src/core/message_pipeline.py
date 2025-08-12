from __future__ import annotations
from typing import Optional, Tuple
import queue


class MessagePipeline:
    """Phase 2 scaffold: minimal FIFO queue for inbound/outbound messages."""

    def __init__(self) -> None:
        self._q: "queue.Queue[Tuple[str, str]]" = queue.Queue()

    def enqueue(self, to_agent: str, message: str) -> None:
        self._q.put((to_agent, message))

    def process_once(self) -> Optional[Tuple[str, str]]:
        try:
            item = self._q.get_nowait()
            self._q.task_done()
            return item
        except queue.Empty:
            return None



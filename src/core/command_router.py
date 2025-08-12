from __future__ import annotations
from typing import Callable, Dict, Any


class CommandRouter:
    """Phase 2 scaffold: routes commands to registered handlers.

    Provides default handlers for 'ping', 'resume', and 'sync'.
    """

    def __init__(self) -> None:
        self._handlers: Dict[str, Callable[[Dict[str, Any]], Any]] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        self.register("ping", lambda payload: {"ok": True, "type": "pong", "echo": payload})

        def _resume(payload: Dict[str, Any]) -> Dict[str, Any]:
            agent = payload.get("agent") or payload.get("to") or "unknown"
            return {"ok": True, "agent": agent, "action": "resume", "status": "online"}

        def _sync(payload: Dict[str, Any]) -> Dict[str, Any]:
            agent = payload.get("agent") or payload.get("to") or "unknown"
            return {"ok": True, "agent": agent, "action": "sync", "status": "in-sync"}

        self.register("resume", _resume)
        self.register("sync", _sync)

        # FSM bridging commands (Phase 2)
        try:
            from overnight_runner.fsm_bridge import handle_fsm_request, handle_fsm_update  # type: ignore

            def _fsm_request(payload):
                return handle_fsm_request(payload)

            def _fsm_update(payload):
                return handle_fsm_update(payload)

            self.register("fsm_request", _fsm_request)
            self.register("fsm_update", _fsm_update)
        except Exception:
            # optional: not fatal if bridge not present
            pass

    def register(self, command: str, handler: Callable[[Dict[str, Any]], Any]) -> None:
        self._handlers[command] = handler

    def route(self, command: str, payload: Dict[str, Any]) -> Any:
        handler = self._handlers.get(command)
        if handler is None:
            raise KeyError(f"No handler for command: {command}")
        return handler(payload)



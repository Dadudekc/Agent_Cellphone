from __future__ import annotations

from typing import Any, Dict, Callable

from .command_router import CommandRouter


class DiscordCommandRouter(CommandRouter):
    """Command router that maps Discord slash commands to orchestrator modes."""

    def __init__(self, orchestrator: Any) -> None:
        super().__init__()
        self.orchestrator = orchestrator

        commands = {
            "/plan": "plan",
            "/tasks": "tasks",
            "/scaffold": "scaffold",
            "/ship": "ship",
            "/simplify": "simplify",
            "/release": "release",
            "/deploy": "deploy",
        }

        for cmd, mode in commands.items():
            self.register(cmd, self._make_handler(mode))

    def _make_handler(self, mode: str) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
        def handler(payload: Dict[str, Any]) -> Dict[str, Any]:
            if hasattr(self.orchestrator, "set_mode"):
                self.orchestrator.set_mode(mode)
            elif hasattr(self.orchestrator, mode):
                getattr(self.orchestrator, mode)()
            return {"ok": True, "mode": mode}

        return handler


__all__ = ["DiscordCommandRouter"]

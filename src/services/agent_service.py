"""Agent service abstractions used by the GUI.

The GUI interacts with the rest of the system via these service
interfaces rather than calling :mod:`agent_cell_phone` directly.  This
allows different implementations to be swapped (e.g. a local in-process
implementation or one that talks to a remote REST API).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple

# The local service depends on the core AgentCellPhone implementation
try:  # pragma: no cover - optional import for non-GUI tests
    from agent_cell_phone import AgentCellPhone, MsgTag
except Exception:  # pragma: no cover
    AgentCellPhone = None  # type: ignore
    MsgTag = None  # type: ignore

import requests


class AgentService(ABC):
    """Abstract base class defining messaging operations."""

    @abstractmethod
    def get_available_agents(self) -> List[str]:
        """Return list of available agents."""

    @abstractmethod
    def send_message(
        self, target: str, message: str, tag: str = "NORMAL"
    ) -> Tuple[bool, str]:
        """Send a message to a target agent."""

    @abstractmethod
    def send_command(
        self, target: str, command: str, args: Optional[List[str]] = None
    ) -> Tuple[bool, str]:
        """Send a command to a target agent."""

    @abstractmethod
    def get_system_status(self) -> Dict:
        """Return overall system status information."""


# ---------------------------------------------------------------------------
class LocalAgentService(AgentService):
    """Service implementation that uses AgentCellPhone directly."""

    def __init__(self, layout_mode: str = "8-agent", test_mode: bool = True) -> None:
        if AgentCellPhone is None:
            raise ImportError("agent_cell_phone module not available")
        self.acp = AgentCellPhone(layout_mode=layout_mode, test=test_mode)

    # ------------------------------------------------------------------
    def get_available_agents(self) -> List[str]:
        return self.acp.get_available_agents()

    # ------------------------------------------------------------------
    def send_message(self, target: str, message: str, tag: str = "NORMAL") -> Tuple[bool, str]:
        try:
            msg_tag = MsgTag[tag.upper()] if MsgTag else tag
        except KeyError:
            msg_tag = MsgTag.NORMAL if MsgTag else tag

        if target == "all":
            self.acp.broadcast(message, msg_tag)
            return True, "Message broadcast to all agents"
        else:
            self.acp.send(target, message, msg_tag)
            return True, f"Message sent to {target}"

    # ------------------------------------------------------------------
    def send_command(
        self, target: str, command: str, args: Optional[List[str]] = None
    ) -> Tuple[bool, str]:
        command_text = command
        if args:
            command_text += " " + " ".join(args)
        return self.send_message(target, command_text, "COMMAND")

    # ------------------------------------------------------------------
    def get_system_status(self) -> Dict:
        return {
            "layout_mode": self.acp.get_layout_mode(),
            "available_agents": self.acp.get_available_agents(),
            "available_layouts": self.acp.get_available_layouts(),
            "coordinates": getattr(self.acp, "_coords", {}),
        }


# ---------------------------------------------------------------------------
class APIAgentService(AgentService):
    """Service implementation that communicates with the REST API."""

    def __init__(self, base_url: str = "http://localhost:8000") -> None:
        self.base_url = base_url.rstrip("/")

    # ------------------------------------------------------------------
    def _post(self, endpoint: str, payload: Dict) -> Tuple[bool, str]:
        url = f"{self.base_url}{endpoint}"
        try:
            resp = requests.post(url, json=payload, timeout=5)
            if resp.ok:
                data = resp.json()
                return bool(data.get("success", False)), data.get("detail", "")
            return False, resp.text
        except Exception as exc:  # pragma: no cover - network failure
            return False, str(exc)

    # ------------------------------------------------------------------
    def get_available_agents(self) -> List[str]:
        status = self.get_system_status()
        return status.get("available_agents", [])

    # ------------------------------------------------------------------
    def send_message(self, target: str, message: str, tag: str = "NORMAL") -> Tuple[bool, str]:
        payload = {"target": target, "message": message, "tag": tag}
        endpoint = "/broadcast" if target == "all" else "/send"
        return self._post(endpoint, payload)

    # ------------------------------------------------------------------
    def send_command(
        self, target: str, command: str, args: Optional[List[str]] = None
    ) -> Tuple[bool, str]:
        cmd = command
        if args:
            cmd += " " + " ".join(args)
        return self.send_message(target, cmd, "COMMAND")

    # ------------------------------------------------------------------
    def get_system_status(self) -> Dict:
        url = f"{self.base_url}/status"
        try:
            resp = requests.get(url, timeout=5)
            if resp.ok:
                return resp.json()
            return {"error": resp.text}
        except Exception as exc:  # pragma: no cover - network failure
            return {"error": str(exc)}


__all__ = [
    "AgentService",
    "LocalAgentService",
    "APIAgentService",
]


"""Basic file based persistence for agent status information.

The full system persists a wealth of information about each agent.  For the
purposes of the tests we only need a minimal persistence layer which saves and
loads JSON files for individual agents.  Status files are stored under
``runtime/agent_monitors/<agent_id>/status.json`` relative to the repository
root.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional


STATUS_ROOT = Path("runtime/agent_monitors")


def save_agent_status(status: Dict[str, Any]) -> None:
    """Persist an agent's status to disk.

    The ``agent_id`` field is required and determines the file location.
    """

    agent_id = status.get("agent_id")
    if not agent_id:
        raise ValueError("status must include 'agent_id'")

    agent_dir = STATUS_ROOT / agent_id
    agent_dir.mkdir(parents=True, exist_ok=True)
    with open(agent_dir / "status.json", "w", encoding="utf-8") as fh:
        json.dump(status, fh)


def load_agent_status(agent_id: str) -> Optional[Dict[str, Any]]:
    """Load a previously saved status for ``agent_id``.

    Returns ``None`` if no status file exists.
    """

    path = STATUS_ROOT / agent_id / "status.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


__all__ = ["save_agent_status", "load_agent_status"]


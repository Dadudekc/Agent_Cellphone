from __future__ import annotations

"""Persistence utilities for agent statuses used in unit tests."""

from pathlib import Path
import json
from typing import Dict, Optional


def save_agent_status(status: Dict, directory: Path) -> Path:
    """Persist *status* as JSON in *directory* and return the file path."""
    directory.mkdir(parents=True, exist_ok=True)
    file = directory / f"{status['agent_id']}.json"
    file.write_text(json.dumps(status), encoding="utf-8")
    return file


def load_agent_status(agent_id: str, directory: Path) -> Optional[Dict]:
    """Load previously saved status for *agent_id* from *directory*."""
    file = directory / f"{agent_id}.json"
    if not file.exists():
        return None
    return json.loads(file.read_text(encoding="utf-8"))


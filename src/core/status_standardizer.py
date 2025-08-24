from __future__ import annotations

"""Utilities for normalizing agent status payloads.

These helpers provide a minimal implementation to support unit testing.
"""

from datetime import datetime
from typing import Any, Dict


def standardize_agent_status(status: Dict[str, Any]) -> Dict[str, Any]:
    """Return a standardized copy of *status*.

    The implementation normalizes casing of the ``status`` field, ensures a
    ``last_seen`` timestamp is present and leaves additional metadata untouched.
    """
    return {
        "agent_id": status["agent_id"],
        "status": status["status"].lower(),
        "last_seen": status.get("last_seen") or datetime.utcnow().isoformat(),
        "metadata": status.get("metadata", {}),
    }


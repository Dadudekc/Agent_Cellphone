"""Utility helpers for normalising agent status data.

The real project has a far more feature complete implementation but the
tests only rely on a very small surface area.  The functions below provide a
light‑weight version that mirrors the expected API so the test suite can run
without pulling in the rest of the system.
"""

from __future__ import annotations

from typing import Any, Dict


def standardize_agent_status(status: Dict[str, Any]) -> Dict[str, Any]:
    """Return a normalised copy of an agent status dictionary.

    Parameters
    ----------
    status:
        Arbitrary mapping containing status information.  Only a handful of
        keys are recognised; missing values are substituted with sensible
        defaults so callers can rely on their presence.

    Returns
    -------
    Dict[str, Any]
        A new dictionary with the keys ``agent_id``, ``status``, ``last_seen``
        and ``metadata`` always present.
    """

    return {
        "agent_id": status.get("agent_id", "unknown"),
        "status": str(status.get("status", "unknown")).lower(),
        "last_seen": status.get("last_seen"),
        "metadata": dict(status.get("metadata", {})),
    }


__all__ = ["standardize_agent_status"]


"""Aggregate counts of agent statuses.

This module provides a very small helper used by the test-suite to summarise
the number of agents in various states.  It intentionally keeps the
implementation compact and dependency free.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Dict


def aggregate_agent_statuses(agent_statuses: Dict[str, Dict[str, Any]]) -> Dict[str, int]:
    """Aggregate status information for a collection of agents.

    Parameters
    ----------
    agent_statuses:
        Mapping of agent identifiers to dictionaries containing a ``status``
        key.

    Returns
    -------
    Dict[str, int]
        A dictionary with counts for ``active``, ``idle``, ``offline`` and the
        ``total`` number of agents processed.
    """

    counter = Counter()
    for info in agent_statuses.values():
        state = str(info.get("status", "unknown")).lower()
        if state in {"active", "idle", "offline"}:
            counter[state] += 1
    counter["total"] = len(agent_statuses)
    # Ensure keys exist even if counts are zero
    return {k: counter.get(k, 0) for k in ["active", "idle", "offline", "total"]}


__all__ = ["aggregate_agent_statuses"]


from __future__ import annotations

"""Simple aggregation utilities for agent statuses."""

from typing import Dict


def aggregate_agent_statuses(statuses: Dict[str, Dict[str, str]]) -> Dict[str, int]:
    """Aggregate counts of agent ``status`` values.

    Unknown statuses are ignored but included in the total count.
    """
    summary = {"active": 0, "idle": 0, "offline": 0, "total": 0}
    for info in statuses.values():
        state = info.get("status", "").lower()
        summary["total"] += 1
        if state in summary:
            summary[state] += 1
    return summary


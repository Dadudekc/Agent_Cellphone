from __future__ import annotations

"""Validation helpers for agent metadata used in tests."""

from typing import Dict


REQUIRED_FIELDS = {"workspace", "cursor_version"}


def validate_metadata(metadata: Dict[str, str]) -> bool:
    """Validate *metadata* contains required fields with truthy values.

    ``cursor_version`` is expected to contain at least a ``major.minor.patch``
    style string.
    """
    if not REQUIRED_FIELDS.issubset(metadata):
        return False
    if not metadata["workspace"]:
        return False
    version = metadata["cursor_version"]
    if not isinstance(version, str) or version.count(".") < 2:
        return False
    return True


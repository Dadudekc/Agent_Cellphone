"""Simple validation helpers for agent metadata.

The project contains a rich metadata schema but the tests only need a couple
of sanity checks.  This module therefore implements a compact validator which
verifies that required fields are present and roughly well‑formed.
"""

from __future__ import annotations

import re
from typing import Any, Dict


_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


def validate_metadata(metadata: Dict[str, Any]) -> bool:
    """Validate a subset of metadata fields.

    Parameters
    ----------
    metadata:
        Dictionary containing metadata information.

    Returns
    -------
    bool
        ``True`` if the metadata passes basic validation, otherwise ``False``.
    """

    workspace = metadata.get("workspace")
    cursor_version = metadata.get("cursor_version")

    if not workspace or not isinstance(workspace, str):
        return False
    if not cursor_version or not _VERSION_PATTERN.match(str(cursor_version)):
        return False
    return True


__all__ = ["validate_metadata"]


"""Configuration validation utilities.

This module provides a simple validator that ensures required
configuration files exist and contain valid JSON. It is intended to
run during startup before any other components are initialized.
"""

from __future__ import annotations

import json
import os
from typing import Iterable

# Paths to configuration files that must exist for the application to run.
REQUIRED_FILES = [
    "config/agents/agent_coordinates.json",
    "config/agents/agent_roles.json",
    "config/system/system_config.json",
    "config/templates/agent_modes.json",
    "config/templates/message_templates.json",
]


def validate_config(files: Iterable[str] | None = None) -> bool:
    """Validate that required configuration files exist and are valid JSON.

    Parameters
    ----------
    files:
        Iterable of file paths to validate. If ``None``, ``REQUIRED_FILES``
        is used.

    Returns
    -------
    bool
        ``True`` if all files exist and contain valid JSON.

    Raises
    ------
    FileNotFoundError
        If any required file is missing.
    ValueError
        If any file contains invalid JSON.
    """

    files = files or REQUIRED_FILES
    for path in files:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing configuration file: {path}")
        try:
            with open(path, "r", encoding="utf-8") as f:
                json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in {path}: {exc.msg}") from exc
    return True


if __name__ == "__main__":
    validate_config()
    print("Configuration validated successfully.")

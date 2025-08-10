"""Configuration loading utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any


def _deep_update(base: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively update ``base`` dict with ``overrides`` dict."""
    for key, value in overrides.items():
        if (
            key in base
            and isinstance(base[key], dict)
            and isinstance(value, dict)
        ):
            _deep_update(base[key], value)
        else:
            base[key] = value
    return base


def load_config(env: str = "default") -> Dict[str, Any]:
    """Load the project configuration.

    Parameters
    ----------
    env:
        Optional environment name. If provided and a file named
        ``settings.<env>.json`` exists in the config directory, its values
        will overlay the defaults.

    Returns
    -------
    dict
        Dictionary containing merged configuration values.
    """
    repo_root = Path(__file__).resolve().parents[2]
    config_dir = repo_root / "config"

    base_file = config_dir / "settings.json"
    with base_file.open("r", encoding="utf-8") as f:
        config: Dict[str, Any] = json.load(f)

    # Expose repository root for consumers needing absolute paths
    config.setdefault("paths", {})["repo_root"] = str(repo_root)

    if env and env != "default":
        env_file = config_dir / f"settings.{env}.json"
        if env_file.exists():
            with env_file.open("r", encoding="utf-8") as f:
                env_config = json.load(f)
            _deep_update(config, env_config)

    return config

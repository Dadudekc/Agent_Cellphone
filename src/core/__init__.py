"""
Core System Module
=================
Defines the public API for `src.core` while avoiding heavy imports at package import time.
Modules are imported lazily on first attribute access to prevent optional dependency failures
when unrelated submodules are used.
"""

from __future__ import annotations
import importlib
from typing import Any

__all__ = [
    'MultimodalAgent',
    'DevAutomationAgent',
]

_LAZY_MAP = {
    'MultimodalAgent': '.multimodal_agent',
    'DevAutomationAgent': '.dev_automation_agent',
}


def __getattr__(name: str) -> Any:
    module_path = _LAZY_MAP.get(name)
    if module_path is None:
        raise AttributeError(name)
    module = importlib.import_module(module_path, __name__)
    return getattr(module, name)

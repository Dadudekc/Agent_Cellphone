"""Compatibility wrapper for package-style imports.

This small module re-exports the public API from
``src.agent_cell_phone`` so that existing code and tests that
import ``agent_cell_phone`` from the repository root continue to
work even after the project was reorganised into a ``src``
layout.
"""

from src.agent_cell_phone import *  # noqa: F401,F403


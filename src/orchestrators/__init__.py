"""Orchestrators package for Agent Cell Phone system.

This package contains orchestration logic for managing agent lifecycles,
overnight operations, and workflow coordination.
"""

from .lifecycle_orchestrator import LifecycleOrchestrator

# NOTE:
# ``overnight_runner`` has optional third-party dependencies (e.g. ``pyyaml``)
# that are not required for the core orchestrator functionality or for the
# unit tests. Importing it eagerly here caused ``ImportError``/``SystemExit``
# when those optional packages were missing, breaking consumers that only need
# ``LifecycleOrchestrator``.  To keep the package importable in a generic
# environment we avoid importing ``overnight_runner`` at module import time.

__all__ = ["LifecycleOrchestrator"]

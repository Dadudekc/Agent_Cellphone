"""Service layer providing APIs and abstractions for GUI integration.

This package exposes an HTTP API and client/service abstractions so that
the GUI can interact with the core AgentCellPhone functionality without
directly depending on the implementation details.  It enables different
service implementations (local or remote) to be swapped via dependency
injection.
"""

from .conversation_logger import (
    save_conversation,
    list_conversations,
    load_conversation,
    load_conversations,
)

__all__ = [
    "save_conversation",
    "list_conversations",
    "load_conversation",
    "load_conversations",
]


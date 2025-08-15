"""Service layer providing APIs and abstractions for GUI integration.

This package exposes an HTTP API and client/service abstractions so that
the GUI can interact with the core AgentCellPhone functionality without
directly depending on the implementation details.  It enables different
service implementations (local or remote) to be swapped via dependency
injection.
"""

from .browser_manager import BrowserManager
from .session_authenticator import SessionAuthenticator

__all__ = [
    "BrowserManager",
    "SessionAuthenticator",
]


"""
GUI tab implementations for Dream.OS.

Provides ready-to-use tabs for various system functions.

Public API:
- AgentMessengerTab
- CoordinatorTab
- OnboardingTab
"""

from .agent_messenger_tab import AgentMessengerTab
from .coordinator_tab import CoordinatorTab
from .onboarding_tab import OnboardingTab

__all__ = ["AgentMessengerTab", "CoordinatorTab", "OnboardingTab"]

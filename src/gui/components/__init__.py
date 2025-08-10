"""
Reusable GUI components for Dream.OS Cell Phone.

This package exposes reusable widgets used throughout the GUI.

Public API:
- TkCustomMessageWidget
- QtCustomMessageWidget
- OnboardingProgressWidget
- OnboardingStatusWidget
- OnboardingLogWidget
- OnboardingControlsWidget
- OnboardingChecklistWidget
- OnboardingManager
- QtOnboardingProgressWidget
- QtOnboardingStatusWidget
- QtOnboardingLogWidget
- QtOnboardingControlsWidget
- QtOnboardingChecklistWidget
- OnboardingDashboardWidget
"""

from .custom_message_widget import CustomMessageWidget as TkCustomMessageWidget
from .onboarding_components import (
    OnboardingProgressWidget,
    OnboardingStatusWidget,
    OnboardingLogWidget,
    OnboardingControlsWidget,
    OnboardingChecklistWidget,
    OnboardingManager,
)
from .onboarding_dashboard import OnboardingDashboardWidget

# Optional PyQt5 components
try:  # pragma: no cover - optional dependency
    from .custom_message_widget_qt import CustomMessageWidget as QtCustomMessageWidget
    from .onboarding_components_qt import (
        OnboardingProgressWidget as QtOnboardingProgressWidget,
        OnboardingStatusWidget as QtOnboardingStatusWidget,
        OnboardingLogWidget as QtOnboardingLogWidget,
        OnboardingControlsWidget as QtOnboardingControlsWidget,
        OnboardingChecklistWidget as QtOnboardingChecklistWidget,
    )
except Exception:  # ImportError, RuntimeError, etc.
    QtCustomMessageWidget = None
    QtOnboardingProgressWidget = None
    QtOnboardingStatusWidget = None
    QtOnboardingLogWidget = None
    QtOnboardingControlsWidget = None
    QtOnboardingChecklistWidget = None

__all__ = [
    "TkCustomMessageWidget",
    "QtCustomMessageWidget",
    "OnboardingProgressWidget",
    "OnboardingStatusWidget",
    "OnboardingLogWidget",
    "OnboardingControlsWidget",
    "OnboardingChecklistWidget",
    "OnboardingManager",
    "QtOnboardingProgressWidget",
    "QtOnboardingStatusWidget",
    "QtOnboardingLogWidget",
    "QtOnboardingControlsWidget",
    "QtOnboardingChecklistWidget",
    "OnboardingDashboardWidget",
]

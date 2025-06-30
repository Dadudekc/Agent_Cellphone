#!/usr/bin/env python3
"""
Dream.OS Cell Phone GUI Launcher
================================
This launcher performs three steps:
1. Shows a splash screen using `logo.png` as the full-window background.
2. Presents a mode-selection window that uses `1logo.png` as its background and
   offers four buttons to choose the agent layout mode.
3. Launches the main `DreamOSCellPhoneGUI` with the selected mode.

If any of the images are missing, the launcher gracefully falls back to a plain
window while still offering the same functionality.
"""

import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
)
from PyQt5.QtGui import QPixmap, QSplashScreen, QIcon
from PyQt5.QtCore import Qt, QTimer

# Import the main GUI (relative import works because we execute inside gui/)
from dream_os_gui import DreamOSCellPhoneGUI

# Absolute paths to assets
BASE_DIR = os.path.dirname(__file__)
SPLASH_IMAGE = os.path.join(BASE_DIR, "logo.png")  # Background for splash
MODE_BG_IMAGE = os.path.join(BASE_DIR, "1logo.png")  # Background for mode selector

class ModeSelector(QWidget):
    """Window that lets the user choose an agent layout mode."""

    def __init__(self):
        super().__init__()
        self.selected_mode = None
        self.setWindowTitle("Select Agent Mode")
        self.setFixedSize(640, 480)
        self._apply_background()
        self._build_ui()
        # Center the window on the screen
        self.move(
            QApplication.primaryScreen().geometry().center() - self.rect().center()
        )

    # ---------------------------------------------------------------------
    # UI Helpers
    # ---------------------------------------------------------------------
    def _apply_background(self):
        """Apply `1logo.png` as background if available."""
        if os.path.exists(MODE_BG_IMAGE):
            # Use a simple stylesheet for the background image
            escaped_path = MODE_BG_IMAGE.replace("\\", "/")
            self.setStyleSheet(
                f"background-image: url('{escaped_path}');"
                "background-repeat: no-repeat;"
                "background-position: center;"
            )

    def _build_ui(self):
        """Create four buttons for the available modes."""
        modes = [
            ("4 Agents", "4-agent"),
            ("6 Agents", "6-agent"),
            ("8 Agents", "8-agent"),
            ("Custom", "custom"),
        ]

        container = QVBoxLayout()
        container.addStretch()

        # Two rows, two buttons each
        for i in range(0, len(modes), 2):
            row = QHBoxLayout()
            row.addStretch()
            for label, mode in modes[i : i + 2]:
                row.addWidget(self._create_button(label, mode))
            row.addStretch()
            container.addLayout(row)
        container.addStretch()

        self.setLayout(container)

    def _create_button(self, text: str, mode: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setFixedSize(140, 60)
        btn.setStyleSheet(
            "QPushButton {"
            "  background-color: rgba(76, 175, 80, 0.85);"
            "  color: white;"
            "  border: none;"
            "  border-radius: 6px;"
            "  font-size: 14px;"
            "  font-weight: bold;"
            "}"
            "QPushButton:hover { background-color: rgba(69, 160, 73, 0.95); }"
            "QPushButton:pressed { background-color: rgba(61, 139, 64, 1.0); }"
        )
        btn.clicked.connect(lambda _=False, m=mode: self._select_mode(m))
        return btn

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------
    def _select_mode(self, mode: str):
        self.selected_mode = mode
        self.close()


def show_splash(app: QApplication):
    """Display a splash screen for two seconds (if image exists)."""
    if not os.path.exists(SPLASH_IMAGE):
        return None  # No splash image available

    pix = QPixmap(SPLASH_IMAGE)
    if pix.isNull():
        return None

    screen = app.primaryScreen()
    # Scale the pixmap to fit nicely on most screens (max 50% of min dimension)
    max_dim = int(min(screen.size().width(), screen.size().height()) * 0.5)
    pix = pix.scaled(max_dim, max_dim, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    splash = QSplashScreen(pix, Qt.WindowStaysOnTopHint)
    splash.show()
    # Close after 2 seconds automatically
    QTimer.singleShot(2000, splash.close)
    return splash


def main():
    app = QApplication(sys.argv)

    # Step 1: Splash Screen
    splash = show_splash(app)

    # Step 2: Mode Selector
    selector = ModeSelector()
    # Show selector after splash closes (or immediately if no splash)
    delay = 2100 if splash else 0
    QTimer.singleShot(delay, selector.show)

    # Wait until user selects a mode (blocking until selector closes)
    app.exec_()
    chosen_mode = selector.selected_mode or "8-agent"

    # Step 3: Launch Main GUI
    window = DreamOSCellPhoneGUI(layout_mode=chosen_mode)
    if os.path.exists(SPLASH_IMAGE):
        app.setWindowIcon(QIcon(SPLASH_IMAGE))
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 
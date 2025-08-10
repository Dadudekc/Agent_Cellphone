#!/usr/bin/env python3
"""
Dream.OS Splash Screen & Mode Selection GUI
===========================================
Splash screen with logo that leads to agent mode selection.
"""

import sys
import os
import warnings
from pathlib import Path

# Suppress PyQt5 deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="PyQt5")
warnings.filterwarnings("ignore", category=DeprecationWarning)

import time
try:
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar, QFrame, QMessageBox, QDialog
    from PyQt5.QtCore import Qt, QTimer
    from PyQt5.QtGui import QPixmap, QFont, QPainter
    print("✅ PyQt5 imported successfully in splash screen")
except ImportError as e:
    print(f"PyQt5 import error in splash screen: {e}")
    print("PyQt5 not available. Please install: pip install PyQt5")
    sys.exit(1)

# Import removed - two_agent_mode module deleted

class SplashScreen(QWidget):
    """Splash screen that uses gui/logo.png as the full-window background."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dream.OS Cell Phone - Loading...")
        self.setFixedSize(900, 650)  # Redesigned splash screen
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # Load background pixmap once
        bg_path = Path(__file__).with_name("logo.png")
        self.bg_pixmap = QPixmap(str(bg_path)) if bg_path.exists() else None
        if self.bg_pixmap and not self.bg_pixmap.isNull():
            self.setFixedSize(self.bg_pixmap.width(), self.bg_pixmap.height() + 20)  # slimmer footer
        self.setStyleSheet("background-color: #000000;")
        
        self.init_ui()
        self.start_loading_animation()
    
    def init_ui(self):
        """Initialize the splash screen UI."""
        layout = QVBoxLayout(self)
        # Reserve only 60px bottom space for loading widgets so image appears larger
        layout.setContentsMargins(10, 10, 10, 20)
        layout.addStretch()

        # Progress bar at bottom, subtle style
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(16)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid rgba(255,255,255,0.6);
                border-radius: 10px;
                background-color: rgba(0,0,0,0.4);
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: rgba(255,255,255,0.8);
                border-radius: 8px;
            }
        """)
        layout.addWidget(self.progress_bar)

        # Loading text small
        self.loading_label = QLabel("Loading...")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("font-size: 10px; color: #ffffff;")
        layout.addWidget(self.loading_label)
        
        # Version
        version_label = QLabel("v2.0 - Modern Interface")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("font-size: 14px; color: #BDC3C7;")  # Bigger version
        layout.addWidget(version_label)
        
        # Center on screen
        self.center_on_screen()
    
    def paintEvent(self, event):
        """Draw scaled background image."""
        if self.bg_pixmap and not self.bg_pixmap.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            painter.drawPixmap(0,0,self.bg_pixmap)
        super().paintEvent(event)
    
    def center_on_screen(self):
        """Center the splash screen on the screen."""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def start_loading_animation(self):
        """Start the loading animation."""
        self.progress = 0
        self.loading_steps = [
            "Initializing system...",
            "Loading agent coordinates...",
            "Establishing communication...",
            "Preparing interface...",
            "Ready!"
        ]
        self.current_step = 0
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_loading)
        self.timer.start(200)
    
    def update_loading(self):
        """Update the loading progress."""
        self.progress += 2
        self.progress_bar.setValue(self.progress)
        
        # Update loading text
        if self.progress % 20 == 0 and self.current_step < len(self.loading_steps) - 1:
            self.current_step += 1
            self.loading_label.setText(self.loading_steps[self.current_step])
        
        if self.progress >= 100:
            self.timer.stop()
            self.loading_label.setText("Ready!")
            QTimer.singleShot(500, self.show_mode_selection)
    
    def show_mode_selection(self):
        """Show the mode selection screen."""
        self.mode_selection = ModeSelectionScreen()
        self.mode_selection.show()
        self.close()

class ModeSelectionScreen(QWidget):
    """Mode selection screen with gui/1logo.png full-window background and 4 buttons."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dream.OS Cell Phone - Mode Selection")
        self.setFixedSize(900, 650)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # Load background pixmap once (1logo.png)
        bg_path = os.path.join(os.getcwd(), "gui", "1logo.png")
        self.bg_pixmap = QPixmap(bg_path) if os.path.exists(bg_path) else None
        if self.bg_pixmap and not self.bg_pixmap.isNull():
            self.setFixedSize(self.bg_pixmap.width(), self.bg_pixmap.height()+40)
        self.setStyleSheet("background-color: #000000;")
        
        self.init_ui()
        self.center_on_screen()
    
    def init_ui(self):
        """Initialize the mode selection UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 40)  # tighter top margin
        layout.addStretch()
        
        # Mode buttons (4 modes)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)
        
        modes = [("2",2),("4",4),("6",6),("8",8)]
        for label,num in modes:
            btn = QPushButton(f"{label} Agents")
            btn.setFixedSize(150,80)
            btn.clicked.connect(lambda checked, n=num: self.launch_gui(n))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(0,0,0,0.6);
                    color: white;
                    border: 2px solid #ffffff;
                    border-radius: 15px;
                    font-size: 20px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgba(255,255,255,0.2);
                }
            """)
            button_layout.addWidget(btn)
        
        layout.addLayout(button_layout)
        
        # Exit button
        exit_btn = QPushButton("Exit")
        exit_btn.setFixedHeight(60)
        exit_btn.clicked.connect(self.close)
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border-radius: 12px;
                font-size: 18px;
                font-weight: bold;
                border: 3px solid #C0392B;
            }
            QPushButton:hover {
                background-color: #C0392B;
                border-color: #A93226;
            }
        """)
        layout.addWidget(exit_btn)
    
    def paintEvent(self, event):
        if self.bg_pixmap and not self.bg_pixmap.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            painter.drawPixmap(0,0,self.bg_pixmap)
        super().paintEvent(event)
    
    def center_on_screen(self):
        """Center the mode selection screen on the screen."""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def launch_gui(self, num_agents):
        """Launch the appropriate GUI based on agent count."""
        try:
            import subprocess
            import sys
            
            # Close the splash screen
            self.close()
            
            # Determine which GUI to launch based on agent count
            if num_agents == 2:
                gui_path = os.path.join(os.getcwd(), "gui", "two_agent_horizontal_gui.py")
            elif num_agents == 4:
                gui_path = os.path.join(os.getcwd(), "gui", "four_agent_horizontal_gui.py")
            elif num_agents == 6:
                gui_path = os.path.join(os.getcwd(), "gui", "dream_os_gui_v2.py")
            elif num_agents == 8:
                gui_path = os.path.join(os.getcwd(), "gui", "dream_os_gui_v2.py")
            else:
                gui_path = os.path.join(os.getcwd(), "gui", "dream_os_gui_v2.py")
            
            if os.path.exists(gui_path):
                subprocess.Popen([sys.executable, gui_path])
            else:
                QMessageBox.critical(self, "Error", f"GUI file not found: {gui_path}")
                self.show()  # Show mode selection again
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to launch GUI: {e}")
            self.show()  # Show mode selection again

# Placeholder window shown when a mode is selected
class ComingSoonWindow(QWidget):
    def __init__(self, num_agents: int):
        super().__init__()
        self.setWindowTitle(f"{num_agents}-Agent Mode - Coming Soon")
        self.setFixedSize(400, 300)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(20)
        msg = QLabel(f"{num_agents}-Agent Mode\nComing Soon!")
        msg.setAlignment(Qt.AlignCenter)
        msg.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(msg)
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.back)
        back_btn.setFixedHeight(40)
        layout.addWidget(back_btn)

    def back(self):
        self.close()
        # reopen mode selection
        sel = ModeSelectionScreen()
        sel.show()

def main():
    """Main function to run the splash screen."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show splash screen
    splash = SplashScreen()
    splash.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 
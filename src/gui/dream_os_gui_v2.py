#!/usr/bin/env python3
"""
Dream.OS Cell Phone GUI v2.0
============================
Modern, redesigned GUI with better UX and component-by-component development.
Refactored to use BaseGUIController to eliminate code duplication.
"""

import sys
import os
import json
import threading
import time
from datetime import datetime
from typing import List, Dict, Optional

try:
    from core.utils.coordinate_finder import CoordinateFinder
    from core.framework.agent_autonomy_framework import AgentAutonomyFramework
    from gui.utils.base_gui_controller import BaseGUIController
except ImportError as e:
    print(f"Import error: {e}")
    print("Please run from the project root directory: python main.py")
    # Use shared classes as fallback
    try:
        from gui.utils.shared_classes import CoordinateFinder, AgentAutonomyFramework
    except ImportError:
        # Create minimal fallback classes
        class CoordinateFinder:
            def __init__(self):
                self.coordinates = {}
            def get_all_coordinates(self):
                return {f"agent-{i}": (100 + i*50, 100 + i*50) for i in range(1, 9)}
            def get_coordinates(self, agent_id):
                return (100, 100)
        
        class AgentAutonomyFramework:
            def __init__(self):
                pass
    
    # Create minimal base controller for fallback
    class BaseGUIController:
        def __init__(self, coordinate_finder=None, framework=None):
            self.coordinate_finder = coordinate_finder
            self.framework = framework
            self.selected_agents = []
            self.log_display = None
            self.status_timer = None
            self.agent_widgets = {}
        
        def log_message(self, sender: str, message: str):
            pass
        
        def execute_selected_agents_action(self, action_type: str, action_name: str, action_func=None):
            pass
        
        def broadcast_action(self, action_type: str, action_name: str, default_command=None, action_func=None):
            pass
        
        def setup_status_updates(self, update_interval: int = 5000):
            pass

try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                QHBoxLayout, QGridLayout, QLabel, QPushButton, 
                                QComboBox, QTextEdit, QLineEdit, QGroupBox, 
                                QSplitter, QTabWidget, QCheckBox, QListWidget,
                                QListWidgetItem, QProgressBar, QFrame, QScrollArea,
                                QMessageBox, QFileDialog, QSlider, QSpinBox)
    from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve
    from PyQt5.QtGui import QFont, QPixmap, QIcon, QPalette, QColor, QPainter, QBrush
except ImportError:
    print("PyQt5 not available. Please install: pip install PyQt5")
    sys.exit(1)

from .components.splash_screen import SplashScreen
from .components.agent_panel import AgentStatusWidget

class DreamOSCellPhoneGUIv2(QMainWindow, BaseGUIController):
    """Modern Dream.OS Cell Phone GUI v2.0."""
    
    def __init__(self):
        QMainWindow.__init__(self)
        BaseGUIController.__init__(self, CoordinateFinder(), AgentAutonomyFramework())
        
        self.init_ui()
        self.setup_status_updates()
    
    def init_ui(self):
        """Initialize the main UI."""
        self.setWindowTitle("Dream.OS Cell Phone v2.0 - Modern Interface")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1A1A1A;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Header
        self.create_header(main_layout)
        
        # Main content area
        content_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(content_splitter)
        
        # Left panel - Agent selection and controls
        left_panel = self.create_left_panel()
        content_splitter.addWidget(left_panel)
        
        # Right panel - Status and logs
        right_panel = self.create_right_panel()
        content_splitter.addWidget(right_panel)
        
        # Set splitter proportions
        content_splitter.setSizes([400, 800])
        
        # Status bar
        self.statusBar().showMessage("Ready - Dream.OS Cell Phone v2.0")
    
    def create_header(self, layout):
        """Create the header section."""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2C3E50, stop:1 #3498DB);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        header_layout = QHBoxLayout(header_frame)
        
        # Logo and title
        title_layout = QVBoxLayout()
        title_label = QLabel("📱 Dream.OS Cell Phone")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: white;
            }
        """)
        title_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Modern Agent Communication Interface")
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #BDC3C7;
            }
        """)
        title_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # System status
        status_layout = QVBoxLayout()
        self.system_status_label = QLabel("🟢 System Online")
        self.system_status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #27AE60;
                font-weight: bold;
            }
        """)
        status_layout.addWidget(self.system_status_label)
        
        self.agent_count_label = QLabel("8 Agents Connected")
        self.agent_count_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #BDC3C7;
            }
        """)
        status_layout.addWidget(self.agent_count_label)
        
        header_layout.addLayout(status_layout)
        
        layout.addWidget(header_frame)
    
    def create_left_panel(self):
        """Create the left panel with agent selection and controls."""
        panel = QWidget()
        panel.setMaximumWidth(400)
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # Agent Selection Group
        selection_group = QGroupBox("Agent Selection")
        selection_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: white;
                border: 2px solid #34495E;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        selection_layout = QVBoxLayout(selection_group)
        
        # Agent grid
        self.agent_grid = QGridLayout()
        self.agent_widgets = {}
        
        # Create agent widgets in a 4x2 grid
        row, col = 0, 0
        for i in range(1, 9):
            agent_id = f"agent-{i}"
            agent_widget = AgentStatusWidget(agent_id, main_gui=self)
            self.agent_widgets[agent_id] = agent_widget
            self.agent_grid.addWidget(agent_widget, row, col)
            
            col += 1
            if col > 3:  # 4 columns
                col = 0
                row += 1
        
        selection_layout.addLayout(self.agent_grid)
        
        # Selection controls
        selection_controls = QHBoxLayout()
        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(self.select_all_agents)
        select_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        
        clear_btn = QPushButton("Clear Selection")
        clear_btn.clicked.connect(self.clear_selection)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        
        selection_controls.addWidget(select_all_btn)
        selection_controls.addWidget(clear_btn)
        selection_layout.addLayout(selection_controls)
        
        layout.addWidget(selection_group)
        
        # Individual Controls Group
        individual_group = QGroupBox("Individual Controls")
        individual_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: white;
                border: 2px solid #34495E;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
        """)
        
        individual_layout = QVBoxLayout(individual_group)
        
        # Control buttons
        controls = [
            ("🔍 Ping", self.ping_selected_agents),
            ("📊 Status", self.get_status_selected_agents),
            ("▶️ Resume", self.resume_selected_agents),
            ("⏸️ Pause", self.pause_selected_agents),
            ("🔄 Sync", self.sync_selected_agents),
            ("🎯 Assign Task", self.assign_task_selected_agents)
        ]
        
        for text, callback in controls:
            btn = QPushButton(text)
            btn.clicked.connect(callback)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #34495E;
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                    font-weight: bold;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #2C3E50;
                }
            """)
            individual_layout.addWidget(btn)
        
        layout.addWidget(individual_group)
        
        # Broadcast Controls Group
        broadcast_group = QGroupBox("Broadcast Controls")
        broadcast_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: white;
                border: 2px solid #34495E;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
        """)
        
        broadcast_layout = QVBoxLayout(broadcast_group)
        
        # Broadcast buttons
        broadcast_controls = [
            ("📢 Broadcast Message", self.broadcast_message),
            ("🔍 Broadcast Ping", self.broadcast_ping),
            ("📊 Broadcast Status", self.broadcast_status),
            ("▶️ Broadcast Resume", self.broadcast_resume),
            ("🎯 Broadcast Task", self.broadcast_task)
        ]
        
        for text, callback in broadcast_controls:
            btn = QPushButton(text)
            btn.clicked.connect(callback)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #8E44AD;
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                    font-weight: bold;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #7D3C98;
                }
            """)
            broadcast_layout.addWidget(btn)
        
        layout.addWidget(broadcast_group)
        layout.addStretch()
        
        return panel
    
    def create_right_panel(self):
        """Create the right panel with status and logs."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # Status and Logs Group
        logs_group = QGroupBox("System Status & Logs")
        logs_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: white;
                border: 2px solid #34495E;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
        """)
        
        logs_layout = QVBoxLayout(logs_group)
        
        # Log display
        self.log_display = QTextEdit()
        self.log_display.setStyleSheet("""
            QTextEdit {
                background-color: #2C3E50;
                color: #ECF0F1;
                border: 1px solid #34495E;
                border-radius: 5px;
            }
        """)
        self.log_display.setReadOnly(True)
        logs_layout.addWidget(self.log_display)
        
        # Log controls
        log_controls = QHBoxLayout()
        
        clear_log_btn = QPushButton("🗑️ Clear Log")
        clear_log_btn.clicked.connect(self.clear_log)
        clear_log_btn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        
        save_log_btn = QPushButton("💾 Save Log")
        save_log_btn.clicked.connect(self.save_log)
        save_log_btn.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        
        log_controls.addWidget(clear_log_btn)
        log_controls.addWidget(save_log_btn)
        log_controls.addStretch()
        
        logs_layout.addLayout(log_controls)
        layout.addWidget(logs_group)
        
        return panel
    
    def setup_status_updates(self):
        """Setup periodic status updates."""
        # Call base class setup
        super().setup_status_updates(5000)  # Update every 5 seconds
        
        # Additional initialization specific to this GUI
        self.log_message("System", "Dream.OS Cell Phone v2.0 initialized")
        self.log_message("System", "Modern interface loaded successfully")
    
    # Override log_message to set log_display reference
    def log_message(self, sender: str, message: str):
        """Add a message to the log."""
        # Ensure log_display is set for base class methods
        if not hasattr(self, 'log_display') or self.log_display is None:
            return
            
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {sender}: {message}"
        self.log_display.append(log_entry)
        
        # Auto-scroll to bottom
        scrollbar = self.log_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def update_agent_statuses(self):
        """Update agent statuses periodically."""
        # Simulate status updates (replace with actual status checking)
        import random
        statuses = ["online", "busy", "offline"]
        
        for agent_id, widget in self.agent_widgets.items():
            # Simulate random status changes
            if random.random() < 0.1:  # 10% chance of status change
                new_status = random.choice(statuses)
                widget.update_status(new_status)
                self.log_message("Status", f"{agent_id} status: {new_status}")

    # Provide default handlers so base controller actions do something visible
    def _default_agent_action(self, agent_id: str, action_type: str):
        self.log_message("Action", f"{action_type} -> {agent_id}")
        # Optional: attempt coordinate-based keystroke for simple actions
        try:
            import pyautogui  # type: ignore
            coords = self.coordinate_finder.get_coordinates(agent_id) if self.coordinate_finder else None
            if coords:
                x, y = coords
                pyautogui.click(x, y)
                if action_type == "ping":
                    pyautogui.typewrite("[PING]")
                elif action_type == "status":
                    pyautogui.typewrite("status")
                elif action_type == "resume":
                    pyautogui.typewrite("resume")
                elif action_type == "pause":
                    pyautogui.typewrite("pause")
                elif action_type == "sync":
                    pyautogui.typewrite("sync")
                elif action_type == "task":
                    pyautogui.typewrite("task: focus highest leverage task")
                pyautogui.press('enter')
        except Exception:
            # Headless or missing dependencies: just log
            pass

    def _default_broadcast_action(self, action_type: str, default_command: str = None):
        self.log_message("Broadcast", f"{action_type} -> all agents")
        try:
            import pyautogui  # type: ignore
            for agent_id in self.agent_widgets.keys():
                coords = self.coordinate_finder.get_coordinates(agent_id) if self.coordinate_finder else None
                if not coords:
                    continue
                x, y = coords
                pyautogui.click(x, y)
                text = default_command or action_type
                if action_type == "message" and not default_command:
                    text = "Hello from GUI"
                pyautogui.typewrite(text)
                pyautogui.press('enter')
        except Exception:
            # Headless or missing dependencies: just log
            pass
    
    # Agent selection methods (inherited from BaseGUIController)
    # select_all_agents() and clear_selection() are now provided by the base class
    
    # Individual control methods (inherited from BaseGUIController)
    # The following methods are now provided by the base class:
    # - ping_selected_agents()
    # - get_status_selected_agents()
    # - resume_selected_agents()
    # - pause_selected_agents()
    # - sync_selected_agents()
    # - assign_task_selected_agents()
    # 
    # These methods use the generic execute_selected_agents_action() pattern
    # to eliminate code duplication.
    
    # Broadcast methods (inherited from BaseGUIController)
    # The following methods are now provided by the base class:
    # - broadcast_message()
    # - broadcast_ping()
    # - broadcast_status()
    # - broadcast_resume()
    # - broadcast_task()
    # 
    # These methods use the generic broadcast_action() pattern
    # to eliminate code duplication.
    
    # Log control methods (inherited from BaseGUIController)
    # clear_log() and save_log() are now provided by the base class
    
    # ============================================================================
    # ABSTRACT METHOD IMPLEMENTATIONS
    # ============================================================================
    
    def create_agent_widgets(self):
        """Create agent-specific widgets."""
        # This method is called during UI initialization to create agent widgets
        # The actual widget creation is handled in create_left_panel()
        pass

def main():
    """Main function."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show splash screen
    splash = SplashScreen()
    splash.show()
    
    # Create main window (will be shown after splash)
    main_window = DreamOSCellPhoneGUIv2()
    splash.main_window = main_window
    
    # Start the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 
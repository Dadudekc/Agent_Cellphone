#!/usr/bin/env python3
"""
Dream.OS Cell Phone GUI v2.0
============================
Modern, redesigned GUI with better UX and component-by-component development.
"""

import sys
import os
import json
import threading
import time
from datetime import datetime
from typing import List, Dict, Optional

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from src.utils.coordinate_finder import CoordinateFinder
    from src.framework.agent_autonomy_framework import AgentAutonomyFramework
except ImportError as e:
    print(f"Import error: {e}")
    print("Please run from the project root directory: python main.py")
    # Import coordinate finder from utils
    try:
        from src.utils.coordinate_finder import CoordinateFinder
    except ImportError:
        # Create dummy classes for fallback
        class CoordinateFinder:
            def __init__(self):
                self.coordinates = {}
            def get_all_coordinates(self):
                return {f"agent-{i}": (100 + i*50, 100 + i*50) for i in range(1, 9)}
            def get_coordinates(self, agent_id):
                return (100, 100)
    
    try:
        from src.framework.agent_autonomy_framework import AgentAutonomyFramework
    except ImportError:
        class AgentAutonomyFramework:
            def __init__(self):
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

class SplashScreen(QWidget):
    """Modern splash screen with loading animation."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dream.OS Cell Phone - Loading...")
        self.setFixedSize(600, 400)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.init_ui()
        self.start_loading_animation()
    
    def init_ui(self):
        """Initialize the splash screen UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Main container with background
        container = QFrame()
        container.setObjectName("splashContainer")
        container.setStyleSheet("""
            #splashContainer {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2C3E50, stop:1 #3498DB);
                border-radius: 20px;
                border: 2px solid #34495E;
            }
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(20)
        
        # Logo placeholder (you can replace with actual logo)
        logo_label = QLabel("📱")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("""
            QLabel {
                font-size: 80px;
                color: white;
                margin: 20px;
            }
        """)
        container_layout.addWidget(logo_label)
        
        # Title
        title_label = QLabel("Dream.OS Cell Phone")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: white;
                margin: 10px;
            }
        """)
        container_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Autonomous Agent Communication System")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #BDC3C7;
                margin: 5px;
            }
        """)
        container_layout.addWidget(subtitle_label)
        
        # Loading progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #34495E;
                border-radius: 10px;
                text-align: center;
                background-color: #2C3E50;
                color: white;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #E74C3C, stop:0.5 #F39C12, stop:1 #27AE60);
                border-radius: 8px;
            }
        """)
        self.progress_bar.setFixedHeight(20)
        container_layout.addWidget(self.progress_bar)
        
        # Loading text
        self.loading_label = QLabel("Initializing system...")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #BDC3C7;
                margin: 5px;
            }
        """)
        container_layout.addWidget(self.loading_label)
        
        # Version info
        version_label = QLabel("v2.0 - Modern Interface")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: #7F8C8D;
                margin: 5px;
            }
        """)
        container_layout.addWidget(version_label)
        
        layout.addWidget(container)
        
        # Center the splash screen
        self.center_on_screen()
    
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
        self.timer.start(200)  # Update every 200ms
    
    def update_loading(self):
        """Update the loading progress."""
        self.progress += 2
        self.progress_bar.setValue(self.progress)
        
        # Update loading text
        step_index = min(self.progress // 20, len(self.loading_steps) - 1)
        self.loading_label.setText(self.loading_steps[step_index])
        
        if self.progress >= 100:
            self.timer.stop()
            self.close()
            self.main_window.show()

class AgentStatusWidget(QWidget):
    """Individual agent status widget with modern design."""
    
    def __init__(self, agent_id: str, parent=None):
        super().__init__(parent)
        self.agent_id = agent_id
        self.status = "offline"
        self.init_ui()
    
    def init_ui(self):
        """Initialize the agent status widget UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Main container
        container = QFrame()
        container.setObjectName("agentContainer")
        container.setStyleSheet("""
            #agentContainer {
                background-color: #2C3E50;
                border-radius: 10px;
                border: 2px solid #34495E;
            }
            #agentContainer:hover {
                border-color: #3498DB;
            }
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(8)
        
        # Agent ID
        self.agent_label = QLabel(self.agent_id)
        self.agent_label.setAlignment(Qt.AlignCenter)
        self.agent_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: white;
            }
        """)
        container_layout.addWidget(self.agent_label)
        
        # Status indicator
        self.status_label = QLabel("🟢 Online")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #27AE60;
            }
        """)
        container_layout.addWidget(self.status_label)
        
        # Quick action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)
        
        # Ping button
        ping_btn = QPushButton("🔍")
        ping_btn.setToolTip("Ping Agent")
        ping_btn.setFixedSize(30, 30)
        ping_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                border-radius: 15px;
                color: white;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        button_layout.addWidget(ping_btn)
        
        # Status button
        status_btn = QPushButton("📊")
        status_btn.setToolTip("Get Status")
        status_btn.setFixedSize(30, 30)
        status_btn.setStyleSheet("""
            QPushButton {
                background-color: #F39C12;
                border-radius: 15px;
                color: white;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #E67E22;
            }
        """)
        button_layout.addWidget(status_btn)
        
        # Resume button
        resume_btn = QPushButton("▶️")
        resume_btn.setToolTip("Resume Agent")
        resume_btn.setFixedSize(30, 30)
        resume_btn.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                border-radius: 15px;
                color: white;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        button_layout.addWidget(resume_btn)
        
        container_layout.addLayout(button_layout)
        layout.addWidget(container)
    
    def update_status(self, status: str):
        """Update the agent status."""
        self.status = status
        if status == "online":
            self.status_label.setText("🟢 Online")
            self.status_label.setStyleSheet("color: #27AE60;")
        elif status == "busy":
            self.status_label.setText("🟡 Busy")
            self.status_label.setStyleSheet("color: #F39C12;")
        elif status == "error":
            self.status_label.setText("🔴 Error")
            self.status_label.setStyleSheet("color: #E74C3C;")
        else:
            self.status_label.setText("⚫ Offline")
            self.status_label.setStyleSheet("color: #7F8C8D;")

class DreamOSCellPhoneGUIv2(QMainWindow):
    """Modern Dream.OS Cell Phone GUI v2.0."""
    
    def __init__(self):
        super().__init__()
        self.coordinate_finder = CoordinateFinder()
        self.framework = AgentAutonomyFramework()
        self.selected_agents = []
        
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
            agent_widget = AgentStatusWidget(agent_id)
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
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_agent_statuses)
        self.status_timer.start(5000)  # Update every 5 seconds
        
        # Initial log message
        self.log_message("System", "Dream.OS Cell Phone v2.0 initialized")
        self.log_message("System", "Modern interface loaded successfully")
    
    def log_message(self, sender: str, message: str):
        """Add a message to the log."""
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
    
    # Agent selection methods
    def select_all_agents(self):
        """Select all agents."""
        self.selected_agents = list(self.agent_widgets.keys())
        self.log_message("Selection", f"Selected all {len(self.selected_agents)} agents")
    
    def clear_selection(self):
        """Clear agent selection."""
        self.selected_agents = []
        self.log_message("Selection", "Cleared agent selection")
    
    # Individual control methods
    def ping_selected_agents(self):
        """Ping selected agents."""
        if not self.selected_agents:
            self.log_message("Warning", "No agents selected for ping")
            return
        
        for agent_id in self.selected_agents:
            self.log_message("Ping", f"Pinging {agent_id}...")
            # Add actual ping logic here
    
    def get_status_selected_agents(self):
        """Get status of selected agents."""
        if not self.selected_agents:
            self.log_message("Warning", "No agents selected for status check")
            return
        
        for agent_id in self.selected_agents:
            self.log_message("Status", f"Getting status for {agent_id}...")
            # Add actual status logic here
    
    def resume_selected_agents(self):
        """Resume selected agents."""
        if not self.selected_agents:
            self.log_message("Warning", "No agents selected for resume")
            return
        
        for agent_id in self.selected_agents:
            self.log_message("Resume", f"Resuming {agent_id}...")
            # Add actual resume logic here
    
    def pause_selected_agents(self):
        """Pause selected agents."""
        if not self.selected_agents:
            self.log_message("Warning", "No agents selected for pause")
            return
        
        for agent_id in self.selected_agents:
            self.log_message("Pause", f"Pausing {agent_id}...")
            # Add actual pause logic here
    
    def sync_selected_agents(self):
        """Sync selected agents."""
        if not self.selected_agents:
            self.log_message("Warning", "No agents selected for sync")
            return
        
        for agent_id in self.selected_agents:
            self.log_message("Sync", f"Syncing {agent_id}...")
            # Add actual sync logic here
    
    def assign_task_selected_agents(self):
        """Assign task to selected agents."""
        if not self.selected_agents:
            self.log_message("Warning", "No agents selected for task assignment")
            return
        
        for agent_id in self.selected_agents:
            self.log_message("Task", f"Assigning task to {agent_id}...")
            # Add actual task assignment logic here
    
    # Broadcast methods
    def broadcast_message(self):
        """Broadcast message to all agents."""
        self.log_message("Broadcast", "Broadcasting message to all agents...")
        # Add actual broadcast logic here
    
    def broadcast_ping(self):
        """Broadcast ping to all agents."""
        self.log_message("Broadcast", "Broadcasting ping to all agents...")
        # Add actual broadcast ping logic here
    
    def broadcast_status(self):
        """Broadcast status request to all agents."""
        self.log_message("Broadcast", "Broadcasting status request to all agents...")
        # Add actual broadcast status logic here
    
    def broadcast_resume(self):
        """Broadcast resume command to all agents."""
        self.log_message("Broadcast", "Broadcasting resume command to all agents...")
        # Add actual broadcast resume logic here
    
    def broadcast_task(self):
        """Broadcast task to all agents."""
        self.log_message("Broadcast", "Broadcasting task to all agents...")
        # Add actual broadcast task logic here
    
    # Log control methods
    def clear_log(self):
        """Clear the log display."""
        self.log_display.clear()
        self.log_message("System", "Log cleared")
    
    def save_log(self):
        """Save the log to a file."""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Log", "", "Text Files (*.txt);;All Files (*)"
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.log_display.toPlainText())
                self.log_message("System", f"Log saved to {filename}")
            except Exception as e:
                self.log_message("Error", f"Failed to save log: {e}")

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
#!/usr/bin/env python3
"""
Dream.OS Two-Agent Horizontal GUI
=================================
Modern, clean interface for managing two agents in a horizontal layout.
Inspired by the v2 GUI design with simplified, focused functionality.
"""

import sys
import os
import warnings

# Suppress PyQt5 deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="PyQt5")
import json
import threading
import time
import pyautogui
import warnings
from datetime import datetime
from typing import List, Dict, Optional

# Suppress PyQt5 deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="PyQt5")

# Import PyQt5 first (before project imports)
try:
    import PyQt5
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                QHBoxLayout, QGridLayout, QLabel, QPushButton, 
                                QComboBox, QTextEdit, QLineEdit, QGroupBox, 
                                QSplitter, QTabWidget, QCheckBox, QListWidget,
                                QListWidgetItem, QProgressBar, QFrame, QScrollArea,
                                QMessageBox, QFileDialog, QSlider, QSpinBox, QInputDialog)
    from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve
    from PyQt5.QtGui import QFont, QPixmap, QIcon, QPalette, QColor, QPainter, QBrush, QTextCursor
    
    # QTextCursor registration is optional and not needed for basic functionality
    print("✅ PyQt5 imported successfully")
except ImportError as e:
    print(f"PyQt5 import error: {e}")
    print("PyQt5 not available. Please install: pip install PyQt5")
    sys.exit(1)

# Add multiple possible paths for imports
current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))

try:
    from src.utils.coordinate_finder import CoordinateFinder
    from src.framework.agent_autonomy_framework import AgentAutonomyFramework
except ImportError as e:
    print(f"Import error: {e}")
    print("Trying alternative import paths...")
    
    # Try direct import
    try:
        from utils.coordinate_finder import CoordinateFinder
        from framework.agent_autonomy_framework import AgentAutonomyFramework
        print("✅ Imported using direct path")
    except ImportError:
        print("Creating fallback classes...")
        # Create dummy classes for fallback
        class CoordinateFinder:
            def __init__(self):
                self.coordinates = {}
            def get_all_coordinates(self):
                return {f"agent-{i}": (100 + i*50, 100 + i*50) for i in range(1, 3)}
            def get_coordinates(self, agent_id):
                return (100, 100)
        
        class AgentAutonomyFramework:
            def __init__(self):
                pass

class AgentPanel(QWidget):
    """Individual agent panel with status and controls."""
    
    def __init__(self, agent_id: str, parent=None):
        super().__init__(parent)
        self.agent_id = agent_id
        self.status = "offline"
        self.current_task = "idle"
        self.last_update = "never"
        self.init_ui()
    
    def init_ui(self):
        """Initialize the agent panel UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)  # Smaller margins like 4-agent
        layout.setSpacing(10)
        
        # Main container
        container = QFrame()
        container.setObjectName("agentContainer")
        container.setStyleSheet("""
            #agentContainer {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2C3E50, stop:1 #34495E);
                border-radius: 12px;
                border: 2px solid #34495E;
                min-height: 350px;
            }
            #agentContainer:hover {
                border-color: #3498DB;
            }
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(10)
        
        # Agent header
        header_layout = QHBoxLayout()
        
        # Agent ID with medium font (like 4-agent)
        self.agent_label = QLabel(self.agent_id.upper())
        self.agent_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: white;
                padding: 8px;
            }
        """)
        header_layout.addWidget(self.agent_label)
        
        # Status indicator
        self.status_label = QLabel("⚫ OFFLINE")
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #7F8C8D;
                font-weight: bold;
                padding: 8px;
            }
        """)
        header_layout.addWidget(self.status_label)
        
        container_layout.addLayout(header_layout)
        
        # Status info section
        status_group = QGroupBox("Status")
        status_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: white;
                border: 2px solid #34495E;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px 0 4px;
            }
        """)
        
        status_layout = QVBoxLayout(status_group)
        
        # Current task
        self.task_label = QLabel("Task: idle")
        self.task_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #BDC3C7;
                padding: 3px;
            }
        """)
        status_layout.addWidget(self.task_label)
        
        # Last update
        self.update_label = QLabel("Updated: never")
        self.update_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #BDC3C7;
                padding: 3px;
            }
        """)
        status_layout.addWidget(self.update_label)
        
        container_layout.addWidget(status_group)
        
        # Control buttons
        controls_group = QGroupBox("Controls")
        controls_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: white;
                border: 2px solid #34495E;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 8px;
            }
        """)
        
        controls_layout = QVBoxLayout(controls_group)
        
        # Control buttons with tooltips (compact like 4-agent)
        controls = [
            ("🔍 Ping", "Test if agent is responsive", self.ping_agent),
            ("📊 Status", "Read agent's status.json file", self.get_status),
            ("▶️ Resume", "Tell agent to resume operations", self.resume_agent),
            ("⏸️ Pause", "Tell agent to pause operations", self.pause_agent),
            ("🎯 Task", "Send a specific task to agent", self.assign_task)
        ]
        
        for text, tooltip, callback in controls:
            btn = QPushButton(text)
            btn.setToolTip(tooltip)
            btn.clicked.connect(callback)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #34495E;
                    color: white;
                    border-radius: 6px;
                    padding: 8px;
                    font-weight: bold;
                    text-align: left;
                    font-size: 11px;
                    margin: 1px;
                }
                QPushButton:hover {
                    background-color: #2C3E50;
                }
            """)
            controls_layout.addWidget(btn)
        
        container_layout.addWidget(controls_group)
        layout.addWidget(container)
    
    def update_status(self, status: str, task: str = None, last_update: str = None):
        """Update the agent status."""
        self.status = status
        if task:
            self.current_task = task
        if last_update:
            self.last_update = last_update
        
        # Update status label
        if status == "online":
            self.status_label.setText("🟢 ONLINE")
            self.status_label.setStyleSheet("color: #27AE60; font-weight: bold; padding: 8px;")
        elif status == "busy":
            self.status_label.setText("🟡 BUSY")
            self.status_label.setStyleSheet("color: #F39C12; font-weight: bold; padding: 8px;")
        elif status == "error":
            self.status_label.setText("🔴 ERROR")
            self.status_label.setStyleSheet("color: #E74C3C; font-weight: bold; padding: 8px;")
        else:
            self.status_label.setText("⚫ OFFLINE")
            self.status_label.setStyleSheet("color: #7F8C8D; font-weight: bold; padding: 8px;")
        
        # Update task and update labels
        if task:
            self.task_label.setText(f"Task: {task[:30]}{'...' if len(task) > 30 else ''}")
        if last_update:
            self.update_label.setText(f"Updated: {last_update}")
    
    # Agent control methods (will be connected to main GUI)
    def ping_agent(self):
        """Ping this agent."""
        try:
            coords = self.main_gui.coordinate_finder.get_coordinates(self.agent_id)
            if coords:
                x, y = coords
                pyautogui.click(x, y)
                time.sleep(0.3)
                pyautogui.typewrite("ping")
                pyautogui.press('enter')
                self.main_gui.log_message("Control", f"Ping sent to {self.agent_id}")
            else:
                self.main_gui.log_message("Error", f"No coordinates found for {self.agent_id}")
        except Exception as e:
            self.main_gui.log_message("Error", f"Failed to ping {self.agent_id}: {e}")
    
    def get_status(self):
        """Get status of this agent."""
        try:
            status_file = os.path.join("agent_workspaces", self.agent_id, "status.json")
            if os.path.exists(status_file):
                with open(status_file, 'r') as f:
                    status_data = json.load(f)
                
                status = status_data.get('status', 'unknown')
                task = status_data.get('current_task', 'idle')
                last_update = status_data.get('last_update', 'unknown')
                
                self.main_gui.log_message("Status", f"{self.agent_id}: {status} - {task} (Last: {last_update})")
                self.update_status(status, task, last_update)
            else:
                self.main_gui.log_message("Status", f"{self.agent_id}: No status file found")
        except Exception as e:
            self.main_gui.log_message("Error", f"Failed to get {self.agent_id} status: {e}")
    
    def resume_agent(self):
        """Resume this agent."""
        try:
            coords = self.main_gui.coordinate_finder.get_coordinates(self.agent_id)
            if coords:
                x, y = coords
                pyautogui.click(x, y)
                time.sleep(0.3)
                pyautogui.typewrite("resume")
                pyautogui.press('enter')
                self.main_gui.log_message("Control", f"Resume command sent to {self.agent_id}")
            else:
                self.main_gui.log_message("Error", f"No coordinates found for {self.agent_id}")
        except Exception as e:
            self.main_gui.log_message("Error", f"Failed to resume {self.agent_id}: {e}")
    
    def pause_agent(self):
        """Pause this agent."""
        try:
            coords = self.main_gui.coordinate_finder.get_coordinates(self.agent_id)
            if coords:
                x, y = coords
                pyautogui.click(x, y)
                time.sleep(0.3)
                pyautogui.typewrite("pause")
                pyautogui.press('enter')
                self.main_gui.log_message("Control", f"Pause command sent to {self.agent_id}")
            else:
                self.main_gui.log_message("Error", f"No coordinates found for {self.agent_id}")
        except Exception as e:
            self.main_gui.log_message("Error", f"Failed to pause {self.agent_id}: {e}")
    
    def assign_task(self):
        """Assign task to this agent."""
        try:
            task, ok = QInputDialog.getText(
                self.main_gui, 
                f"Assign Task to {self.agent_id}", 
                f"Enter task for {self.agent_id}:",
                text="Complete assigned task"
            )
            
            if not ok or not task.strip():
                self.main_gui.log_message("Task", "Task assignment cancelled")
                return
            
            coords = self.main_gui.coordinate_finder.get_coordinates(self.agent_id)
            if coords:
                x, y = coords
                pyautogui.click(x, y)
                time.sleep(0.3)
                pyautogui.typewrite(f"task: {task}")
                pyautogui.press('enter')
                self.main_gui.log_message("Task", f"Task assigned to {self.agent_id}: {task}")
            else:
                self.main_gui.log_message("Error", f"No coordinates found for {self.agent_id}")
        except Exception as e:
            self.main_gui.log_message("Error", f"Failed to assign task to {self.agent_id}: {e}")

class TwoAgentHorizontalGUI(QMainWindow):
    """Modern two-agent horizontal GUI."""
    
    def __init__(self):
        super().__init__()
        self.coordinate_finder = CoordinateFinder()
        self.framework = AgentAutonomyFramework()
        self.agent_panels = {}
        
        self.init_ui()
        self.setup_status_updates()
    
    def init_ui(self):
        """Initialize the main UI."""
        self.setWindowTitle("Dream.OS Two-Agent Horizontal GUI")
        self.setGeometry(100, 100, 1400, 800)
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
        
        # Agent panels (horizontal layout)
        agent_layout = QHBoxLayout()
        agent_layout.setSpacing(20)
        
        # Agent 1 panel
        agent1_panel = AgentPanel("agent-1", self)
        agent1_panel.main_gui = self  # Direct reference to main GUI
        self.agent_panels["agent-1"] = agent1_panel
        agent_layout.addWidget(agent1_panel)
        
        # Agent 2 panel
        agent2_panel = AgentPanel("agent-2", self)
        agent2_panel.main_gui = self  # Direct reference to main GUI
        self.agent_panels["agent-2"] = agent2_panel
        agent_layout.addWidget(agent2_panel)
        
        main_layout.addLayout(agent_layout)
        
        # Shared controls
        self.create_shared_controls(main_layout)
        
        # Log area
        self.create_log_area(main_layout)
        
        # Status bar
        self.statusBar().showMessage("Ready - Two-Agent Horizontal GUI")
    
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
        title_layout = QHBoxLayout()
        
        # Try to load the actual logo for header
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        if os.path.exists(logo_path):
            try:
                pixmap = QPixmap(logo_path)
                if not pixmap.isNull():
                    # Scale the logo to appropriate size for header (32x32)
                    scaled_pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    header_logo = QLabel()
                    header_logo.setPixmap(scaled_pixmap)
                    header_logo.setStyleSheet("margin-right: 10px;")
                    title_layout.addWidget(header_logo)
            except Exception:
                # Fallback to emoji if image loading fails
                pass
        
        # Title text
        title_text_layout = QVBoxLayout()
        title_label = QLabel("Dream.OS Two-Agent System")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: white;
            }
        """)
        title_text_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Horizontal Layout - Modern Interface")
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #BDC3C7;
            }
        """)
        title_text_layout.addWidget(subtitle_label)
        
        title_layout.addLayout(title_text_layout)
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
        
        self.agent_count_label = QLabel("2 Agents Connected")
        self.agent_count_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #BDC3C7;
            }
        """)
        status_layout.addWidget(self.agent_count_label)
        
        header_layout.addLayout(status_layout)
        
        layout.addWidget(header_frame)
    
    def create_shared_controls(self, layout):
        """Create shared controls section."""
        controls_frame = QFrame()
        controls_frame.setStyleSheet("""
            QFrame {
                background-color: #2C3E50;
                border-radius: 10px;
                border: 2px solid #34495E;
            }
        """)
        
        controls_layout = QVBoxLayout(controls_frame)
        
        # Controls title
        controls_title = QLabel("Shared System Controls")
        controls_title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: white;
                padding: 10px;
            }
        """)
        controls_layout.addWidget(controls_title)
        
        # Control buttons in a grid
        controls_grid = QGridLayout()
        
        # Row 1: System controls
        onboard_btn = QPushButton("🚀 Onboard Agents")
        onboard_btn.setToolTip("Run onboarding sequence for both agents")
        onboard_btn.clicked.connect(self.onboard_agents)
        onboard_btn.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        
        restart_btn = QPushButton("🔄 Restart System")
        restart_btn.setToolTip("Restart the entire system")
        restart_btn.clicked.connect(self.restart_system)
        restart_btn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        
        coords_btn = QPushButton("🗺️ Coordinate Mapping")
        coords_btn.setToolTip("Test and manage agent coordinates")
        coords_btn.clicked.connect(self.test_coordinates)
        coords_btn.setStyleSheet("""
            QPushButton {
                background-color: #F39C12;
                color: white;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #E67E22;
            }
        """)
        
        controls_grid.addWidget(onboard_btn, 0, 0)
        controls_grid.addWidget(restart_btn, 0, 1)
        controls_grid.addWidget(coords_btn, 0, 2)
        
        # Row 2: Communication controls
        send_msg_btn = QPushButton("📤 Send Message")
        send_msg_btn.setToolTip("Send a message to both agents")
        send_msg_btn.clicked.connect(self.send_message)
        send_msg_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        
        broadcast_btn = QPushButton("📢 Broadcast")
        broadcast_btn.setToolTip("Send broadcast command to both agents")
        broadcast_btn.clicked.connect(self.broadcast_command)
        broadcast_btn.setStyleSheet("""
            QPushButton {
                background-color: #8E44AD;
                color: white;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #7D3C98;
            }
        """)
        
        status_btn = QPushButton("📊 System Status")
        status_btn.setToolTip("Get status from both agents")
        status_btn.clicked.connect(self.get_system_status)
        status_btn.setStyleSheet("""
            QPushButton {
                background-color: #34495E;
                color: white;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2C3E50;
            }
        """)
        
        controls_grid.addWidget(send_msg_btn, 1, 0)
        controls_grid.addWidget(broadcast_btn, 1, 1)
        controls_grid.addWidget(status_btn, 1, 2)
        
        controls_layout.addLayout(controls_grid)
        layout.addWidget(controls_frame)
    
    def create_log_area(self, layout):
        """Create the log display area."""
        log_frame = QFrame()
        log_frame.setStyleSheet("""
            QFrame {
                background-color: #2C3E50;
                border-radius: 10px;
                border: 2px solid #34495E;
            }
        """)
        
        log_layout = QVBoxLayout(log_frame)
        
        # Log title
        log_title = QLabel("System Activity Log")
        log_title.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: white;
                padding: 5px;
            }
        """)
        log_layout.addWidget(log_title)
        
        # Log display
        self.log_display = QTextEdit()
        self.log_display.setStyleSheet("""
            QTextEdit {
                background-color: #1A1A1A;
                color: #ECF0F1;
                border: 1px solid #34495E;
                border-radius: 5px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }
        """)
        self.log_display.setReadOnly(True)
        self.log_display.setMaximumHeight(200)
        log_layout.addWidget(self.log_display)
        
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
                font-size: 10px;
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
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        
        log_controls.addWidget(clear_log_btn)
        log_controls.addWidget(save_log_btn)
        log_controls.addStretch()
        
        log_layout.addLayout(log_controls)
        layout.addWidget(log_frame)
    
    def setup_status_updates(self):
        """Setup periodic status updates."""
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_agent_statuses)
        self.status_timer.start(5000)  # Update every 5 seconds
        
        # Initial log message
        self.log_message("System", "Two-Agent Horizontal GUI initialized")
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
        for agent_id in ["agent-1", "agent-2"]:
            try:
                # Check agent's status.json file
                status_file = os.path.join("agent_workspaces", agent_id, "status.json")
                if os.path.exists(status_file):
                    with open(status_file, 'r') as f:
                        status_data = json.load(f)
                    
                    status = status_data.get('status', 'unknown')
                    current_task = status_data.get('current_task', 'idle')
                    last_update = status_data.get('last_update', 'unknown')
                    
                    # Update the agent panel
                    if agent_id in self.agent_panels:
                        self.agent_panels[agent_id].update_status(status, current_task, last_update)
            except Exception as e:
                self.log_message("Error", f"Failed to update {agent_id} status: {e}")
    
    # Shared control methods
    def onboard_agents(self):
        """Onboard both agents."""
        self.log_message("System", "Starting agent onboarding...")
        try:
            # Import and run the onboarding sequence
            import subprocess
            import sys
            
            # Run the onboarding script for both agents
            onboarding_script = os.path.join(os.getcwd(), "scripts", "run_onboarding.py")
            if os.path.exists(onboarding_script):
                self.log_message("System", "Running onboarding sequence...")
                
                # Run onboarding in a separate thread to avoid blocking the GUI
                def run_onboarding():
                    try:
                        result = subprocess.run(
                            [sys.executable, onboarding_script],
                            capture_output=True,
                            text=True,
                            cwd=os.getcwd()
                        )
                        
                        if result.returncode == 0:
                            self.log_message("System", "Onboarding completed successfully")
                            # Update agent statuses after onboarding
                            self.update_agent_statuses()
                        else:
                            self.log_message("Error", f"Onboarding failed: {result.stderr}")
                    except Exception as e:
                        self.log_message("Error", f"Onboarding error: {e}")
                
                # Start onboarding in background thread
                onboarding_thread = threading.Thread(target=run_onboarding)
                onboarding_thread.daemon = True
                onboarding_thread.start()
                
            else:
                self.log_message("Error", f"Onboarding script not found: {onboarding_script}")
                
        except Exception as e:
            self.log_message("Error", f"Failed to start onboarding: {e}")
    
    def restart_system(self):
        """Restart the system."""
        self.log_message("System", "Restarting system...")
        # Add actual restart logic here
        self.log_message("System", "System restart completed")
    
    def test_coordinates(self):
        """Test agent coordinates."""
        self.log_message("System", "Testing coordinates...")
        for agent_id in ["agent-1", "agent-2"]:
            coords = self.coordinate_finder.get_coordinates(agent_id)
            if coords:
                x, y = coords
                self.log_message("System", f"{agent_id}: Coordinates ({x}, {y})")
            else:
                self.log_message("System", f"{agent_id}: No coordinates found")
        self.log_message("System", "Coordinate test completed")
    
    def send_message(self):
        """Send message to both agents."""
        message, ok = QInputDialog.getText(
            self, 
            "Send Message", 
            "Enter message to send to both agents:",
            text="Hello from GUI"
        )
        
        if not ok or not message.strip():
            self.log_message("Message", "Message cancelled")
            return
        
        self.log_message("Message", f"Sending message: {message}")
        for agent_id in ["agent-1", "agent-2"]:
            try:
                coords = self.coordinate_finder.get_coordinates(agent_id)
                if coords:
                    x, y = coords
                    pyautogui.click(x, y)
                    time.sleep(0.3)
                    pyautogui.typewrite(f"[MESSAGE] {message}")
                    pyautogui.press('enter')
                    self.log_message("Message", f"Message sent to {agent_id}")
            except Exception as e:
                self.log_message("Error", f"Failed to send message to {agent_id}: {e}")
    
    def broadcast_command(self):
        """Send broadcast command to both agents."""
        command, ok = QInputDialog.getText(
            self, 
            "Broadcast Command", 
            "Enter broadcast command:",
            text="status"
        )
        
        if not ok or not command.strip():
            self.log_message("Broadcast", "Broadcast cancelled")
            return
        
        self.log_message("Broadcast", f"Broadcasting command: {command}")
        for agent_id in ["agent-1", "agent-2"]:
            try:
                coords = self.coordinate_finder.get_coordinates(agent_id)
                if coords:
                    x, y = coords
                    pyautogui.click(x, y)
                    time.sleep(0.3)
                    pyautogui.typewrite(f"[BROADCAST] {command}")
                    pyautogui.press('enter')
                    self.log_message("Broadcast", f"Broadcast sent to {agent_id}")
            except Exception as e:
                self.log_message("Error", f"Failed to broadcast to {agent_id}: {e}")
    
    def get_system_status(self):
        """Get status from both agents."""
        self.log_message("System", "Getting system status...")
        for agent_id in ["agent-1", "agent-2"]:
            try:
                status_file = os.path.join("agent_workspaces", agent_id, "status.json")
                if os.path.exists(status_file):
                    with open(status_file, 'r') as f:
                        status_data = json.load(f)
                    
                    status = status_data.get('status', 'unknown')
                    task = status_data.get('current_task', 'idle')
                    self.log_message("Status", f"{agent_id}: {status} - {task}")
                else:
                    self.log_message("Status", f"{agent_id}: No status file found")
            except Exception as e:
                self.log_message("Error", f"Failed to get {agent_id} status: {e}")
    
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
    
    # Create and show main window
    main_window = TwoAgentHorizontalGUI()
    main_window.show()
    
    # Start the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 
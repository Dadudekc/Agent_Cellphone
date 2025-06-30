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
import pyautogui
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
    # Create dummy classes for fallback
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

try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                QHBoxLayout, QGridLayout, QLabel, QPushButton, 
                                QComboBox, QTextEdit, QLineEdit, QGroupBox, 
                                QSplitter, QTabWidget, QCheckBox, QListWidget,
                                QListWidgetItem, QProgressBar, QFrame, QScrollArea,
                                QMessageBox, QFileDialog, QSlider, QSpinBox, QInputDialog)
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
        
        # Logo - try to load actual logo.png, fallback to emoji
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("""
            QLabel {
                margin: 20px;
            }
        """)
        
        # Try to load the actual logo
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        if os.path.exists(logo_path):
            try:
                pixmap = QPixmap(logo_path)
                if not pixmap.isNull():
                    # Scale the logo to appropriate size (80x80)
                    scaled_pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    logo_label.setPixmap(scaled_pixmap)
                else:
                    # Fallback to emoji if image loading fails
                    logo_label.setText("📱")
                    logo_label.setStyleSheet("""
                        QLabel {
                            font-size: 80px;
                            color: white;
                            margin: 20px;
                        }
                    """)
            except Exception as e:
                print(f"Warning: Could not load logo.png: {e}")
                # Fallback to emoji
                logo_label.setText("📱")
                logo_label.setStyleSheet("""
                    QLabel {
                        font-size: 80px;
                        color: white;
                        margin: 20px;
                    }
                """)
        else:
            # Fallback to emoji if file doesn't exist
            logo_label.setText("📱")
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
        layout.setContentsMargins(15, 15, 15, 15)  # Increased margins
        layout.setSpacing(10)  # Increased spacing
        
        # Main container
        container = QFrame()
        container.setObjectName("agentContainer")
        container.setStyleSheet("""
            #agentContainer {
                background-color: #2C3E50;
                border-radius: 12px;
                border: 2px solid #34495E;
                min-height: 100px;
            }
            #agentContainer:hover {
                border-color: #3498DB;
                background-color: #34495E;
            }
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(12)  # Increased spacing
        
        # Agent ID
        self.agent_label = QLabel(self.agent_id)
        self.agent_label.setAlignment(Qt.AlignCenter)
        self.agent_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: white;
                padding: 5px;
            }
        """)
        container_layout.addWidget(self.agent_label)
        
        # Status indicator
        self.status_label = QLabel("🟢 Online")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #27AE60;
                padding: 3px;
            }
        """)
        container_layout.addWidget(self.status_label)
        
        # Task info
        self.task_label = QLabel("Task: idle")
        self.task_label.setAlignment(Qt.AlignCenter)
        self.task_label.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: #BDC3C7;
                padding: 2px;
            }
        """)
        container_layout.addWidget(self.task_label)
        
        # Last update info
        self.update_label = QLabel("Updated: now")
        self.update_label.setAlignment(Qt.AlignCenter)
        self.update_label.setStyleSheet("""
            QLabel {
                font-size: 9px;
                color: #7F8C8D;
                padding: 2px;
            }
        """)
        container_layout.addWidget(self.update_label)
        
        # Quick action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)  # Increased spacing
        
        # Ping button
        ping_btn = QPushButton("🔍")
        ping_btn.setToolTip("Ping Agent")
        ping_btn.setFixedSize(35, 35)  # Larger buttons
        ping_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                border-radius: 17px;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        button_layout.addWidget(ping_btn)
        
        # Status button
        status_btn = QPushButton("📊")
        status_btn.setToolTip("Get Status")
        status_btn.setFixedSize(35, 35)  # Larger buttons
        status_btn.setStyleSheet("""
            QPushButton {
                background-color: #F39C12;
                border-radius: 17px;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E67E22;
            }
        """)
        button_layout.addWidget(status_btn)
        
        # Resume button
        resume_btn = QPushButton("▶️")
        resume_btn.setToolTip("Resume Agent")
        resume_btn.setFixedSize(35, 35)  # Larger buttons
        resume_btn.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                border-radius: 17px;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        button_layout.addWidget(resume_btn)
        
        container_layout.addLayout(button_layout)
        layout.addWidget(container)
    
    def update_status(self, status: str, task: str = None, last_update: str = None):
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
        
        # Update task info
        if task:
            self.task_label.setText(f"Task: {task[:20]}{'...' if len(task) > 20 else ''}")
        
        # Update last update info
        if last_update:
            self.update_label.setText(f"Updated: {last_update}")
        else:
            self.update_label.setText("Updated: now")

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
        
        # Left panel - System status and logs (smaller)
        left_panel = self.create_left_panel()
        content_splitter.addWidget(left_panel)
        
        # Right panel - Agent selection and controls (larger)
        right_panel = self.create_right_panel()
        content_splitter.addWidget(right_panel)
        
        # Set splitter proportions (logs smaller, agents larger)
        content_splitter.setSizes([300, 900])
        
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
        title_label = QLabel("Dream.OS Cell Phone")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: white;
            }
        """)
        title_text_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Modern Agent Communication Interface")
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
        
        self.agent_count_label = QLabel("8 Agents Connected")
        self.agent_count_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #BDC3C7;
            }
        """)
        status_layout.addWidget(self.agent_count_label)
        
        # Current mode indicator
        self.mode_indicator_label = QLabel("Mode: 8 Agents")
        self.mode_indicator_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #F39C12;
                font-weight: bold;
                padding: 5px;
            }
        """)
        status_layout.addWidget(self.mode_indicator_label)
        
        header_layout.addLayout(status_layout)
        
        layout.addWidget(header_frame)
    
    def create_left_panel(self):
        """Create the left panel with system status and logs."""
        panel = QWidget()
        panel.setMaximumWidth(350)
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # System Status Group
        status_group = QGroupBox("System Status")
        status_group.setStyleSheet("""
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
        
        status_layout = QVBoxLayout(status_group)
        
        # System status indicators
        self.system_status_label = QLabel("🟢 System Online")
        self.system_status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #27AE60;
                font-weight: bold;
                padding: 5px;
            }
        """)
        status_layout.addWidget(self.system_status_label)
        
        self.agent_count_label = QLabel("8 Agents Connected")
        self.agent_count_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #BDC3C7;
                padding: 5px;
            }
        """)
        status_layout.addWidget(self.agent_count_label)
        
        # Current mode indicator
        self.mode_indicator_label = QLabel("Mode: 8 Agents")
        self.mode_indicator_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #F39C12;
                font-weight: bold;
                padding: 5px;
            }
        """)
        status_layout.addWidget(self.mode_indicator_label)
        
        # Quick system controls
        system_controls = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_system_status)
        refresh_btn.setStyleSheet("""
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
        
        system_controls.addWidget(refresh_btn)
        status_layout.addLayout(system_controls)
        
        layout.addWidget(status_group)
        
        # System Logs Group
        logs_group = QGroupBox("System Logs")
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
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 10px;
            }
        """)
        self.log_display.setReadOnly(True)
        self.log_display.setMaximumHeight(300)
        logs_layout.addWidget(self.log_display)
        
        # Log controls
        log_controls = QHBoxLayout()
        
        clear_log_btn = QPushButton("🗑️ Clear")
        clear_log_btn.clicked.connect(self.clear_log)
        clear_log_btn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border-radius: 5px;
                padding: 6px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        
        save_log_btn = QPushButton("💾 Save")
        save_log_btn.clicked.connect(self.save_log)
        save_log_btn.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                border-radius: 5px;
                padding: 6px;
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
        
        logs_layout.addLayout(log_controls)
        layout.addWidget(logs_group)
        
        # Coordinate Management Group
        coord_group = QGroupBox("Coordinate Management")
        coord_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: white;
                border: 2px solid #34495E;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
        """)
        
        coord_layout = QVBoxLayout(coord_group)
        
        # Coordinate info
        coord_info = QLabel("Agent coordinates are used to send commands via PyAutoGUI")
        coord_info.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: #BDC3C7;
                padding: 5px;
            }
        """)
        coord_layout.addWidget(coord_info)
        
        # Coordinate controls
        coord_controls = QHBoxLayout()
        
        test_coords_btn = QPushButton("🧪 Test Coordinates")
        test_coords_btn.setToolTip("Test if agent coordinates are working")
        test_coords_btn.clicked.connect(self.test_coordinates)
        test_coords_btn.setStyleSheet("""
            QPushButton {
                background-color: #F39C12;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #E67E22;
            }
        """)
        
        view_coords_btn = QPushButton("👁️ View Coordinates")
        view_coords_btn.setToolTip("View current agent coordinates")
        view_coords_btn.clicked.connect(self.view_coordinates)
        view_coords_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        
        coord_controls.addWidget(test_coords_btn)
        coord_controls.addWidget(view_coords_btn)
        coord_layout.addLayout(coord_controls)
        
        layout.addWidget(coord_group)
        layout.addStretch()
        
        return panel
    
    def create_right_panel(self):
        """Create the right panel with agent selection and controls."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)
        
        # Agent Selection Group
        selection_group = QGroupBox("Agent Selection & Management")
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
        
        # Mode Selection Controls
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Agent Mode:")
        mode_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: white;
                font-weight: bold;
                padding: 5px;
            }
        """)
        mode_layout.addWidget(mode_label)
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["2 Agents", "4 Agents", "8 Agents"])
        self.mode_combo.setCurrentText("8 Agents")  # Default to 8 agents
        self.mode_combo.setStyleSheet("""
            QComboBox {
                background-color: #34495E;
                color: white;
                border: 1px solid #2C3E50;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
                min-width: 120px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #2C3E50;
                color: white;
                selection-background-color: #3498DB;
            }
        """)
        self.mode_combo.currentTextChanged.connect(self.change_agent_mode)
        mode_layout.addWidget(self.mode_combo)
        
        mode_layout.addStretch()
        selection_layout.addLayout(mode_layout)
        
        # Agent grid with larger widgets
        self.agent_grid = QGridLayout()
        self.agent_grid.setSpacing(15)  # Increased spacing between agents
        self.agent_widgets = {}
        
        # Create agent widgets in a 4x2 grid with larger size
        row, col = 0, 0
        for i in range(1, 9):
            agent_id = f"agent-{i}"
            agent_widget = AgentStatusWidget(agent_id)
            agent_widget.setMinimumSize(150, 120)  # Larger minimum size
            agent_widget.setMaximumSize(200, 150)  # Larger maximum size
            self.agent_widgets[agent_id] = agent_widget
            self.agent_grid.addWidget(agent_widget, row, col)
            
            col += 1
            if col > 3:  # 4 columns
                col = 0
                row += 1
        
        selection_layout.addLayout(self.agent_grid)
        
        # Selection controls
        selection_controls = QHBoxLayout()
        select_all_btn = QPushButton("Select All Agents")
        select_all_btn.clicked.connect(self.select_all_agents)
        select_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
                font-size: 12px;
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
                padding: 10px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        
        selection_controls.addWidget(select_all_btn)
        selection_controls.addWidget(clear_btn)
        selection_controls.addStretch()
        
        selection_layout.addLayout(selection_controls)
        layout.addWidget(selection_group)
        
        # Individual Controls Group
        individual_group = QGroupBox("Individual Agent Controls")
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
        
        # Control buttons in a grid layout for better organization
        controls_grid = QGridLayout()
        controls = [
            ("🔍 Ping Agent", "Test if agent is responsive and get quick status", self.ping_selected_agents),
            ("📊 Get Status", "Read agent's status.json file for detailed info", self.get_status_selected_agents),
            ("▶️ Resume Agent", "Tell agent to resume normal operations", self.resume_selected_agents),
            ("⏸️ Pause Agent", "Tell agent to pause current operations", self.pause_selected_agents),
            ("🔄 Sync Agent", "Synchronize agent with system state", self.sync_selected_agents),
            ("🎯 Assign Task", "Send a specific task to the agent", self.assign_task_selected_agents)
        ]
        
        row, col = 0, 0
        for text, tooltip, callback in controls:
            btn = QPushButton(text)
            btn.setToolTip(tooltip)
            btn.clicked.connect(callback)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #34495E;
                    color: white;
                    border-radius: 5px;
                    padding: 12px;
                    font-weight: bold;
                    text-align: left;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #2C3E50;
                }
            """)
            controls_grid.addWidget(btn, row, col)
            
            col += 1
            if col > 2:  # 3 columns
                col = 0
                row += 1
        
        individual_layout.addLayout(controls_grid)
        layout.addWidget(individual_group)
        
        # Broadcast Controls Group
        broadcast_group = QGroupBox("Broadcast Controls (All Agents)")
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
        
        # Broadcast buttons in a grid layout
        broadcast_grid = QGridLayout()
        broadcast_controls = [
            ("📢 Broadcast Message", "Send a message to all active agents", self.broadcast_message),
            ("🔍 Broadcast Ping", "Ping all agents to check responsiveness", self.broadcast_ping),
            ("📊 Broadcast Status", "Request status reports from all agents", self.broadcast_status),
            ("▶️ Broadcast Resume", "Tell all agents to resume operations", self.broadcast_resume),
            ("🎯 Broadcast Task", "Assign the same task to all agents", self.broadcast_task)
        ]
        
        row, col = 0, 0
        for text, tooltip, callback in broadcast_controls:
            btn = QPushButton(text)
            btn.setToolTip(tooltip)
            btn.clicked.connect(callback)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #8E44AD;
                    color: white;
                    border-radius: 5px;
                    padding: 12px;
                    font-weight: bold;
                    text-align: left;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #7D3C98;
                }
            """)
            broadcast_grid.addWidget(btn, row, col)
            
            col += 1
            if col > 2:  # 3 columns
                col = 0
                row += 1
        
        broadcast_layout.addLayout(broadcast_grid)
        layout.addWidget(broadcast_group)
        
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
        # Get current mode to determine how many agents are active
        selected_mode = self.mode_combo.currentText()
        if selected_mode == "2 Agents":
            num_agents = 2
        elif selected_mode == "4 Agents":
            num_agents = 4
        else:  # 8 Agents
            num_agents = 8
        
        # Only select agents that are currently active
        self.selected_agents = [f"agent-{i}" for i in range(1, num_agents + 1)]
        self.log_message("Selection", f"Selected all {len(self.selected_agents)} active agents")
    
    def clear_selection(self):
        """Clear agent selection."""
        self.selected_agents = []
        self.log_message("Selection", "Cleared agent selection")
    
    # Individual control methods
    def ping_selected_agents(self):
        """Ping selected agents using PyAutoGUI."""
        if not self.selected_agents:
            self.log_message("Warning", "No agents selected for ping")
            return
        
        for agent_id in self.selected_agents:
            self.log_message("Ping", f"Pinging {agent_id}...")
            try:
                # Get agent coordinates
                coords = self.coordinate_finder.get_coordinates(agent_id)
                if coords:
                    x, y = coords
                    # Click on agent position to activate it
                    pyautogui.click(x, y)
                    time.sleep(0.5)
                    # Type ping command
                    pyautogui.typewrite(f"[PING] {agent_id} - Status check from Dream.OS GUI")
                    pyautogui.press('enter')
                    self.log_message("Ping", f"Ping sent to {agent_id} at coordinates ({x}, {y})")
                else:
                    self.log_message("Error", f"Could not find coordinates for {agent_id}")
            except Exception as e:
                self.log_message("Error", f"Failed to ping {agent_id}: {e}")
    
    def get_status_selected_agents(self):
        """Get status of selected agents by checking their status.json files."""
        if not self.selected_agents:
            self.log_message("Warning", "No agents selected for status check")
            return
        
        for agent_id in self.selected_agents:
            self.log_message("Status", f"Getting status for {agent_id}...")
            try:
                # Check agent's status.json file
                status_file = os.path.join("agent_workspaces", agent_id, "status.json")
                if os.path.exists(status_file):
                    with open(status_file, 'r') as f:
                        status_data = json.load(f)
                    
                    status = status_data.get('status', 'unknown')
                    last_update = status_data.get('last_update', 'unknown')
                    current_task = status_data.get('current_task', 'none')
                    
                    self.log_message("Status", f"{agent_id}: {status} | Task: {current_task} | Updated: {last_update}")
                    
                    # Update the agent widget status
                    if agent_id in self.agent_widgets:
                        self.agent_widgets[agent_id].update_status(status, current_task, last_update)
                else:
                    self.log_message("Status", f"{agent_id}: No status.json found - agent may be offline")
                    if agent_id in self.agent_widgets:
                        self.agent_widgets[agent_id].update_status("offline")
            except Exception as e:
                self.log_message("Error", f"Failed to get status for {agent_id}: {e}")
    
    def resume_selected_agents(self):
        """Resume selected agents using PyAutoGUI."""
        if not self.selected_agents:
            self.log_message("Warning", "No agents selected for resume")
            return
        
        for agent_id in self.selected_agents:
            self.log_message("Resume", f"Resuming {agent_id}...")
            try:
                # Get agent coordinates
                coords = self.coordinate_finder.get_coordinates(agent_id)
                if coords:
                    x, y = coords
                    # Click on agent position to activate it
                    pyautogui.click(x, y)
                    time.sleep(0.5)
                    # Type resume command
                    pyautogui.typewrite(f"[RESUME] {agent_id} - Resume operations from Dream.OS GUI")
                    pyautogui.press('enter')
                    self.log_message("Resume", f"Resume command sent to {agent_id} at coordinates ({x}, {y})")
                else:
                    self.log_message("Error", f"Could not find coordinates for {agent_id}")
            except Exception as e:
                self.log_message("Error", f"Failed to resume {agent_id}: {e}")
    
    def pause_selected_agents(self):
        """Pause selected agents using PyAutoGUI."""
        if not self.selected_agents:
            self.log_message("Warning", "No agents selected for pause")
            return
        
        for agent_id in self.selected_agents:
            self.log_message("Pause", f"Pausing {agent_id}...")
            try:
                # Get agent coordinates
                coords = self.coordinate_finder.get_coordinates(agent_id)
                if coords:
                    x, y = coords
                    # Click on agent position to activate it
                    pyautogui.click(x, y)
                    time.sleep(0.5)
                    # Type pause command
                    pyautogui.typewrite(f"[PAUSE] {agent_id} - Pause operations from Dream.OS GUI")
                    pyautogui.press('enter')
                    self.log_message("Pause", f"Pause command sent to {agent_id} at coordinates ({x}, {y})")
                else:
                    self.log_message("Error", f"Could not find coordinates for {agent_id}")
            except Exception as e:
                self.log_message("Error", f"Failed to pause {agent_id}: {e}")
    
    def sync_selected_agents(self):
        """Sync selected agents using PyAutoGUI."""
        if not self.selected_agents:
            self.log_message("Warning", "No agents selected for sync")
            return
        
        for agent_id in self.selected_agents:
            self.log_message("Sync", f"Syncing {agent_id}...")
            try:
                # Get agent coordinates
                coords = self.coordinate_finder.get_coordinates(agent_id)
                if coords:
                    x, y = coords
                    # Click on agent position to activate it
                    pyautogui.click(x, y)
                    time.sleep(0.5)
                    # Type sync command
                    pyautogui.typewrite(f"[SYNC] {agent_id} - Synchronize with Dream.OS GUI")
                    pyautogui.press('enter')
                    self.log_message("Sync", f"Sync command sent to {agent_id} at coordinates ({x}, {y})")
                else:
                    self.log_message("Error", f"Could not find coordinates for {agent_id}")
            except Exception as e:
                self.log_message("Error", f"Failed to sync {agent_id}: {e}")
    
    def assign_task_selected_agents(self):
        """Assign task to selected agents using PyAutoGUI."""
        if not self.selected_agents:
            self.log_message("Warning", "No agents selected for task assignment")
            return
        
        # Get task from user input
        task, ok = QInputDialog.getText(
            self, 
            "Assign Task", 
            f"Enter task description for {len(self.selected_agents)} selected agent(s):",
            text="Process data analysis"
        )
        
        if not ok or not task.strip():
            self.log_message("Task", "Task assignment cancelled")
            return
        
        for agent_id in self.selected_agents:
            self.log_message("Task", f"Assigning task to {agent_id}...")
            try:
                # Get agent coordinates
                coords = self.coordinate_finder.get_coordinates(agent_id)
                if coords:
                    x, y = coords
                    # Click on agent position to activate it
                    pyautogui.click(x, y)
                    time.sleep(0.5)
                    # Type task assignment command
                    pyautogui.typewrite(f"[TASK] {agent_id} - {task}")
                    pyautogui.press('enter')
                    self.log_message("Task", f"Task assigned to {agent_id} at coordinates ({x}, {y})")
                else:
                    self.log_message("Error", f"Could not find coordinates for {agent_id}")
            except Exception as e:
                self.log_message("Error", f"Failed to assign task to {agent_id}: {e}")
    
    # Broadcast methods
    def broadcast_message(self):
        """Broadcast message to all agents using PyAutoGUI."""
        # Get message from user input
        message, ok = QInputDialog.getText(
            self, 
            "Broadcast Message", 
            "Enter message to send to all agents:",
            text="System broadcast message"
        )
        
        if not ok or not message.strip():
            self.log_message("Broadcast", "Broadcast message cancelled")
            return
        
        self.log_message("Broadcast", "Broadcasting message to all agents...")
        try:
            # Get current mode to determine active agents
            selected_mode = self.mode_combo.currentText()
            if selected_mode == "2 Agents":
                num_agents = 2
            elif selected_mode == "4 Agents":
                num_agents = 4
            else:  # 8 Agents
                num_agents = 8
            
            broadcast_msg = f"[BROADCAST] {message} - {datetime.now().strftime('%H:%M:%S')}"
            
            for i in range(1, num_agents + 1):
                agent_id = f"agent-{i}"
                coords = self.coordinate_finder.get_coordinates(agent_id)
                if coords:
                    x, y = coords
                    pyautogui.click(x, y)
                    time.sleep(0.3)
                    pyautogui.typewrite(broadcast_msg)
                    pyautogui.press('enter')
                    time.sleep(0.2)
            
            self.log_message("Broadcast", f"Broadcast message sent to {num_agents} agents")
        except Exception as e:
            self.log_message("Error", f"Failed to broadcast message: {e}")
    
    def broadcast_ping(self):
        """Broadcast ping to all agents using PyAutoGUI."""
        self.log_message("Broadcast", "Broadcasting ping to all agents...")
        try:
            # Get current mode to determine active agents
            selected_mode = self.mode_combo.currentText()
            if selected_mode == "2 Agents":
                num_agents = 2
            elif selected_mode == "4 Agents":
                num_agents = 4
            else:  # 8 Agents
                num_agents = 8
            
            for i in range(1, num_agents + 1):
                agent_id = f"agent-{i}"
                coords = self.coordinate_finder.get_coordinates(agent_id)
                if coords:
                    x, y = coords
                    pyautogui.click(x, y)
                    time.sleep(0.3)
                    pyautogui.typewrite(f"[BROADCAST_PING] {agent_id} - Status check")
                    pyautogui.press('enter')
                    time.sleep(0.2)
            
            self.log_message("Broadcast", f"Broadcast ping sent to {num_agents} agents")
        except Exception as e:
            self.log_message("Error", f"Failed to broadcast ping: {e}")
    
    def broadcast_status(self):
        """Broadcast status request to all agents using PyAutoGUI."""
        self.log_message("Broadcast", "Broadcasting status request to all agents...")
        try:
            # Get current mode to determine active agents
            selected_mode = self.mode_combo.currentText()
            if selected_mode == "2 Agents":
                num_agents = 2
            elif selected_mode == "4 Agents":
                num_agents = 4
            else:  # 8 Agents
                num_agents = 8
            
            for i in range(1, num_agents + 1):
                agent_id = f"agent-{i}"
                coords = self.coordinate_finder.get_coordinates(agent_id)
                if coords:
                    x, y = coords
                    pyautogui.click(x, y)
                    time.sleep(0.3)
                    pyautogui.typewrite(f"[BROADCAST_STATUS] {agent_id} - Report status")
                    pyautogui.press('enter')
                    time.sleep(0.2)
            
            self.log_message("Broadcast", f"Broadcast status request sent to {num_agents} agents")
        except Exception as e:
            self.log_message("Error", f"Failed to broadcast status request: {e}")
    
    def broadcast_resume(self):
        """Broadcast resume command to all agents using PyAutoGUI."""
        self.log_message("Broadcast", "Broadcasting resume command to all agents...")
        try:
            # Get current mode to determine active agents
            selected_mode = self.mode_combo.currentText()
            if selected_mode == "2 Agents":
                num_agents = 2
            elif selected_mode == "4 Agents":
                num_agents = 4
            else:  # 8 Agents
                num_agents = 8
            
            for i in range(1, num_agents + 1):
                agent_id = f"agent-{i}"
                coords = self.coordinate_finder.get_coordinates(agent_id)
                if coords:
                    x, y = coords
                    pyautogui.click(x, y)
                    time.sleep(0.3)
                    pyautogui.typewrite(f"[BROADCAST_RESUME] {agent_id} - Resume operations")
                    pyautogui.press('enter')
                    time.sleep(0.2)
            
            self.log_message("Broadcast", f"Broadcast resume command sent to {num_agents} agents")
        except Exception as e:
            self.log_message("Error", f"Failed to broadcast resume command: {e}")
    
    def broadcast_task(self):
        """Broadcast task to all agents using PyAutoGUI."""
        # Get task from user input
        task, ok = QInputDialog.getText(
            self, 
            "Broadcast Task", 
            "Enter task to assign to all agents:",
            text="Process data analysis"
        )
        
        if not ok or not task.strip():
            self.log_message("Broadcast", "Broadcast task cancelled")
            return
        
        self.log_message("Broadcast", "Broadcasting task to all agents...")
        try:
            # Get current mode to determine active agents
            selected_mode = self.mode_combo.currentText()
            if selected_mode == "2 Agents":
                num_agents = 2
            elif selected_mode == "4 Agents":
                num_agents = 4
            else:  # 8 Agents
                num_agents = 8
            
            broadcast_task_msg = f"[BROADCAST_TASK] {task} - {datetime.now().strftime('%H:%M:%S')}"
            
            for i in range(1, num_agents + 1):
                agent_id = f"agent-{i}"
                coords = self.coordinate_finder.get_coordinates(agent_id)
                if coords:
                    x, y = coords
                    pyautogui.click(x, y)
                    time.sleep(0.3)
                    pyautogui.typewrite(broadcast_task_msg)
                    pyautogui.press('enter')
                    time.sleep(0.2)
            
            self.log_message("Broadcast", f"Broadcast task sent to {num_agents} agents")
        except Exception as e:
            self.log_message("Error", f"Failed to broadcast task: {e}")
    
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

    def refresh_system_status(self):
        """Refresh system status."""
        self.log_message("System", "Refreshing system status...")
        self.update_agent_statuses()
        self.log_message("System", "System status refreshed")

    def change_agent_mode(self):
        """Change the agent mode."""
        selected_mode = self.mode_combo.currentText()
        self.log_message("System", f"Changing agent mode to {selected_mode}")
        
        # Clear current selection when changing modes
        self.selected_agents = []
        
        # Determine number of agents based on mode
        if selected_mode == "2 Agents":
            num_agents = 2
            grid_cols = 2
        elif selected_mode == "4 Agents":
            num_agents = 4
            grid_cols = 2
        else:  # 8 Agents
            num_agents = 8
            grid_cols = 4
        
        # Show/hide agents based on mode
        for i in range(1, 9):
            agent_id = f"agent-{i}"
            agent_widget = self.agent_widgets[agent_id]
            
            if i <= num_agents:
                agent_widget.setVisible(True)
                agent_widget.setEnabled(True)
            else:
                agent_widget.setVisible(False)
                agent_widget.setEnabled(False)
        
        # Update agent count label
        self.agent_count_label.setText(f"{num_agents} Agents Connected")
        
        # Update mode indicator
        self.mode_indicator_label.setText(f"Mode: {selected_mode}")
        
        # Update grid layout for better spacing
        self.update_grid_layout(num_agents, grid_cols)
        
        self.log_message("System", f"Agent mode changed to {selected_mode} - {num_agents} agents active")
    
    def update_grid_layout(self, num_agents, grid_cols):
        """Update the grid layout for the current number of agents."""
        # Clear the current grid
        while self.agent_grid.count():
            child = self.agent_grid.takeAt(0)
            if child.widget():
                child.widget().setParent(None)
        
        # Re-add agents in the new layout
        row, col = 0, 0
        for i in range(1, num_agents + 1):
            agent_id = f"agent-{i}"
            agent_widget = self.agent_widgets[agent_id]
            self.agent_grid.addWidget(agent_widget, row, col)
            
            col += 1
            if col >= grid_cols:
                col = 0
                row += 1

    def test_coordinates(self):
        """Test if agent coordinates are working."""
        self.log_message("System", "Testing coordinates...")
        for i in range(1, 9):
            agent_id = f"agent-{i}"
            coords = self.coordinate_finder.get_coordinates(agent_id)
            if coords:
                x, y = coords
                self.log_message("System", f"{agent_id}: Coordinates are ({x}, {y})")
            else:
                self.log_message("System", f"{agent_id}: Could not find coordinates")
        self.log_message("System", "Coordinates test completed")

    def view_coordinates(self):
        """View current agent coordinates."""
        self.log_message("System", "Viewing coordinates...")
        for i in range(1, 9):
            agent_id = f"agent-{i}"
            coords = self.coordinate_finder.get_coordinates(agent_id)
            if coords:
                x, y = coords
                self.log_message("System", f"{agent_id}: Coordinates are ({x}, {y})")
            else:
                self.log_message("System", f"{agent_id}: Could not find coordinates")
        self.log_message("System", "Coordinates view completed")

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
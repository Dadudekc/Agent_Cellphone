#!/usr/bin/env python3
"""
PyQt5 Onboarding Components for Dream.OS GUI
Provides reusable onboarding UI components for PyQt5 interface
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, 
                            QPushButton, QGroupBox, QProgressBar, QTextEdit, 
                            QComboBox, QTreeWidget, QTreeWidgetItem, QScrollArea,
                            QSplitter, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from typing import Dict, List, Optional, Callable
import time
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

try:
    from agent_workspaces.onboarding.onboarding_manager import OnboardingManager
except ImportError:
    print("Warning: OnboardingManager not found")

class OnboardingProgressWidget(QWidget):
    """Reusable progress widget for onboarding status"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress_bar = None
        self.progress_label = None
        self.setup_widget()
    
    def setup_widget(self):
        """Setup the progress widget"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        container = QFrame()
        container.setObjectName("progressContainer")
        container.setStyleSheet("""
            #progressContainer {
                background-color: #2C3E50;
                border-radius: 8px;
                border: 2px solid #34495E;
            }
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(8)
        
        # Title
        title_label = QLabel("Onboarding Progress")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: white;
                padding: 5px;
            }
        """)
        container_layout.addWidget(title_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #34495E;
                border-radius: 5px;
                text-align: center;
                background-color: #34495E;
            }
            QProgressBar::chunk {
                background-color: #27AE60;
                border-radius: 3px;
            }
        """)
        container_layout.addWidget(self.progress_bar)
        
        # Progress label
        self.progress_label = QLabel("0% Complete")
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #BDC3C7;
                padding: 3px;
            }
        """)
        container_layout.addWidget(self.progress_label)
        
        layout.addWidget(container)
    
    def update_progress(self, percentage: float):
        """Update progress display"""
        self.progress_bar.setValue(int(percentage))
        self.progress_label.setText(f"{percentage:.1f}% Complete")

class OnboardingStatusWidget(QWidget):
    """Reusable status widget for agent onboarding status"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.status_text = None
        self.setup_widget()
    
    def setup_widget(self):
        """Setup the status widget"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        container = QFrame()
        container.setObjectName("statusContainer")
        container.setStyleSheet("""
            #statusContainer {
                background-color: #2C3E50;
                border-radius: 8px;
                border: 2px solid #34495E;
            }
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(8)
        
        # Title
        title_label = QLabel("Agent Status")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: white;
                padding: 5px;
            }
        """)
        container_layout.addWidget(title_label)
        
        # Status text
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setStyleSheet("""
            QTextEdit {
                background-color: #34495E;
                border: 1px solid #2C3E50;
                border-radius: 5px;
                color: #BDC3C7;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }
        """)
        self.status_text.setMaximumHeight(200)
        container_layout.addWidget(self.status_text)
        
        layout.addWidget(container)
    
    def update_status(self, status_text: str):
        """Update status display"""
        self.status_text.setPlainText(status_text)

class OnboardingLogWidget(QWidget):
    """Reusable log widget for onboarding operations"""
    
    log_cleared = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.log_text = None
        self.setup_widget()
    
    def setup_widget(self):
        """Setup the log widget"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        container = QFrame()
        container.setObjectName("logContainer")
        container.setStyleSheet("""
            #logContainer {
                background-color: #2C3E50;
                border-radius: 8px;
                border: 2px solid #34495E;
            }
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(8)
        
        # Title
        title_label = QLabel("Onboarding Log")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: white;
                padding: 5px;
            }
        """)
        container_layout.addWidget(title_label)
        
        # Log text
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #34495E;
                border: 1px solid #2C3E50;
                border-radius: 5px;
                color: #BDC3C7;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 10px;
            }
        """)
        self.log_text.setMaximumHeight(150)
        container_layout.addWidget(self.log_text)
        
        # Log controls
        log_controls = QHBoxLayout()
        clear_btn = QPushButton("Clear Log")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                border-radius: 5px;
                color: white;
                padding: 5px 10px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        clear_btn.clicked.connect(self.clear_log)
        log_controls.addWidget(clear_btn)
        log_controls.addStretch()
        container_layout.addLayout(log_controls)
        
        layout.addWidget(container)
    
    def log_message(self, message: str, error: bool = False):
        """Add a message to the log"""
        timestamp = time.strftime("%H:%M:%S")
        prefix = "ERROR" if error else "INFO"
        log_entry = f"[{timestamp}] {prefix}: {message}\n"
        
        self.log_text.append(log_entry)
        
        # Auto-scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear_log(self):
        """Clear the log display"""
        self.log_text.clear()
        self.log_cleared.emit()

class OnboardingControlsWidget(QWidget):
    """Reusable controls widget for onboarding operations"""
    
    send_request = pyqtSignal(str, str, str)  # request_type, target, message_type
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.agent_combo = None
        self.message_type_combo = None
        self.setup_widget()
    
    def setup_widget(self):
        """Setup the controls widget"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        container = QFrame()
        container.setObjectName("controlsContainer")
        container.setStyleSheet("""
            #controlsContainer {
                background-color: #2C3E50;
                border-radius: 8px;
                border: 2px solid #34495E;
            }
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(10)
        
        # Title
        title_label = QLabel("Onboarding Controls")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: white;
                padding: 8px;
            }
        """)
        container_layout.addWidget(title_label)
        
        # Agent selection
        agent_group = QGroupBox("Target Agent")
        agent_group.setStyleSheet("""
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
        agent_layout = QHBoxLayout(agent_group)
        
        agent_label = QLabel("Agent:")
        agent_label.setStyleSheet("color: #BDC3C7;")
        agent_layout.addWidget(agent_label)
        
        self.agent_combo = QComboBox()
        self.agent_combo.setStyleSheet("""
            QComboBox {
                background-color: #34495E;
                border: 1px solid #2C3E50;
                border-radius: 4px;
                color: white;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #BDC3C7;
            }
        """)
        agent_layout.addWidget(self.agent_combo)
        container_layout.addWidget(agent_group)
        
        # Message type selection
        message_group = QGroupBox("Message Type")
        message_group.setStyleSheet("""
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
        message_layout = QHBoxLayout(message_group)
        
        message_label = QLabel("Type:")
        message_label.setStyleSheet("color: #BDC3C7;")
        message_layout.addWidget(message_label)
        
        self.message_type_combo = QComboBox()
        self.message_type_combo.setStyleSheet("""
            QComboBox {
                background-color: #34495E;
                border: 1px solid #2C3E50;
                border-radius: 4px;
                color: white;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #BDC3C7;
            }
        """)
        message_layout.addWidget(self.message_type_combo)
        container_layout.addWidget(message_group)
        
        # Quick onboarding buttons
        quick_group = QGroupBox("Quick Onboarding")
        quick_group.setStyleSheet("""
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
        quick_layout = QGridLayout(quick_group)
        
        quick_buttons = [
            ("Send Welcome", "welcome"),
            ("System Overview", "system_overview"),
            ("Communication Protocol", "communication_protocol"),
            ("Roles & Responsibilities", "roles_and_responsibilities"),
            ("Best Practices", "best_practices"),
            ("Getting Started", "getting_started"),
            ("Troubleshooting", "troubleshooting"),
            ("Quick Start", "quick_start")
        ]
        
        for i, (text, msg_type) in enumerate(quick_buttons):
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498DB;
                    border-radius: 5px;
                    color: white;
                    padding: 8px;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #2980B9;
                }
            """)
            btn.clicked.connect(lambda checked, mt=msg_type: self.send_specific_message(mt))
            quick_layout.addWidget(btn, i // 2, i % 2)
        
        container_layout.addWidget(quick_group)
        
        # Bulk operations
        bulk_group = QGroupBox("Bulk Operations")
        bulk_group.setStyleSheet("""
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
        bulk_layout = QVBoxLayout(bulk_group)
        
        onboard_all_btn = QPushButton("Onboard All Agents")
        onboard_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                border-radius: 5px;
                color: white;
                padding: 8px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        onboard_all_btn.clicked.connect(self.onboard_all_agents)
        bulk_layout.addWidget(onboard_all_btn)
        
        send_all_btn = QPushButton("Send All Messages to Agent")
        send_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #F39C12;
                border-radius: 5px;
                color: white;
                padding: 8px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #E67E22;
            }
        """)
        send_all_btn.clicked.connect(self.send_all_messages_to_agent)
        bulk_layout.addWidget(send_all_btn)
        
        container_layout.addWidget(bulk_group)
        layout.addWidget(container)
    
    def send_specific_message(self, message_type: str):
        """Send a specific onboarding message"""
        target = self.agent_combo.currentText()
        self.send_request.emit("specific", target, message_type)
    
    def onboard_all_agents(self):
        """Onboard all agents"""
        self.send_request.emit("bulk", "all", "onboard_all")
    
    def send_all_messages_to_agent(self):
        """Send all messages to a specific agent"""
        target = self.agent_combo.currentText()
        self.send_request.emit("bulk", target, "send_all")
    
    def set_agents(self, agents: List[str]):
        """Set available agents"""
        self.agent_combo.clear()
        self.agent_combo.addItem("all")
        self.agent_combo.addItems(agents)
    
    def set_message_types(self, message_types: List[str]):
        """Set available message types"""
        self.message_type_combo.clear()
        self.message_type_combo.addItems(message_types)

class OnboardingChecklistWidget(QWidget):
    """Reusable checklist widget for onboarding progress tracking"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.checklist_tree = None
        self.setup_widget()
    
    def setup_widget(self):
        """Setup the checklist widget"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        container = QFrame()
        container.setObjectName("checklistContainer")
        container.setStyleSheet("""
            #checklistContainer {
                background-color: #2C3E50;
                border-radius: 8px;
                border: 2px solid #34495E;
            }
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(8)
        
        # Title
        title_label = QLabel("Onboarding Checklist")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: white;
                padding: 5px;
            }
        """)
        container_layout.addWidget(title_label)
        
        # Create treeview for checklist
        self.checklist_tree = QTreeWidget()
        self.checklist_tree.setHeaderLabels(["Status", "Document", "Description"])
        self.checklist_tree.setStyleSheet("""
            QTreeWidget {
                background-color: #34495E;
                border: 1px solid #2C3E50;
                border-radius: 5px;
                color: #BDC3C7;
                font-size: 11px;
            }
            QTreeWidget::item {
                padding: 3px;
            }
            QTreeWidget::item:selected {
                background-color: #3498DB;
            }
        """)
        self.checklist_tree.setMaximumHeight(200)
        container_layout.addWidget(self.checklist_tree)
        
        layout.addWidget(container)
    
    def update_checklist(self, checklist_data: List[Dict]):
        """Update the checklist with new data"""
        self.checklist_tree.clear()
        
        for item_data in checklist_data:
            status = "✓" if item_data.get("completed", False) else "✗"
            document = item_data.get("document", "")
            description = item_data.get("description", "")
            
            item = QTreeWidgetItem([status, document, description])
            self.checklist_tree.addTopLevelItem(item) 
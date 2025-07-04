from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton, QGroupBox, QProgressBar
from PyQt5.QtCore import Qt, QTimer
import json
import os
from pathlib import Path

# Import onboarding integration
try:
    from gui.components.onboarding_integration import onboarding_integration
except ImportError:
    # Fallback if import fails
    onboarding_integration = None

class AgentStatusWidget(QWidget):
    """Individual agent status widget with modern design."""
    def __init__(self, agent_id: str, parent=None):
        super().__init__(parent)
        self.agent_id = agent_id
        self.status = "offline"
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
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
        self.status_label = QLabel("🟢 Online")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #27AE60;
            }
        """)
        container_layout.addWidget(self.status_label)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)
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

class AgentPanel(QWidget):
    """Individual agent panel with status and controls."""
    def __init__(self, agent_id: str, parent=None):
        super().__init__(parent)
        self.agent_id = agent_id
        self.status = "offline"
        self.current_task = "idle"
        self.last_update = "never"
        self.onboarding_progress = 0
        self.onboarding_status = "not_started"
        self.init_ui()
        
        # Set up auto-refresh timer for onboarding status
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.load_onboarding_status)
        self.refresh_timer.start(5000)  # Refresh every 5 seconds
        
        # Load initial onboarding status
        self.load_onboarding_status()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
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
        header_layout = QHBoxLayout()
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
        self.task_label = QLabel("Task: idle")
        self.task_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #BDC3C7;
                padding: 3px;
            }
        """)
        status_layout.addWidget(self.task_label)
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
        
        # Add onboarding status section
        onboarding_group = QGroupBox("Onboarding")
        onboarding_group.setStyleSheet("""
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
        onboarding_layout = QVBoxLayout(onboarding_group)
        
        # Onboarding status label
        self.onboarding_status_label = QLabel("Status: Not Started")
        self.onboarding_status_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #BDC3C7;
                padding: 3px;
            }
        """)
        onboarding_layout.addWidget(self.onboarding_status_label)
        
        # Onboarding progress bar
        self.onboarding_progress_bar = QProgressBar()
        self.onboarding_progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #34495E;
                border-radius: 3px;
                text-align: center;
                background-color: #2C3E50;
                color: white;
                font-size: 10px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #E74C3C, stop:0.5 #F39C12, stop:1 #27AE60);
                border-radius: 2px;
            }
        """)
        self.onboarding_progress_bar.setFixedHeight(15)
        onboarding_layout.addWidget(self.onboarding_progress_bar)
        
        # Onboarding progress percentage
        self.onboarding_progress_label = QLabel("0%")
        self.onboarding_progress_label.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: #BDC3C7;
                padding: 2px;
                text-align: center;
            }
        """)
        onboarding_layout.addWidget(self.onboarding_progress_label)
        
        container_layout.addWidget(onboarding_group)
        
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
        self.status = status
        if task:
            self.current_task = task
        if last_update:
            self.last_update = last_update
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
        if task:
            self.task_label.setText(f"Task: {task[:30]}{'...' if len(task) > 30 else ''}")
        if last_update:
            self.update_label.setText(f"Updated: {last_update}")

    def update_onboarding_status(self, status: str, progress: int):
        """Update the onboarding status display."""
        self.onboarding_status = status
        self.onboarding_progress = progress
        
        # Update status label
        status_text = f"Status: {status.replace('_', ' ').title()}"
        self.onboarding_status_label.setText(status_text)
        
        # Update progress bar
        self.onboarding_progress_bar.setValue(progress)
        
        # Update progress label
        self.onboarding_progress_label.setText(f"{progress}%")
        
        # Update colors based on progress
        if progress == 100:
            self.onboarding_status_label.setStyleSheet("""
                QLabel {
                    font-size: 11px;
                    color: #27AE60;
                    padding: 3px;
                    font-weight: bold;
                }
            """)
        elif progress > 50:
            self.onboarding_status_label.setStyleSheet("""
                QLabel {
                    font-size: 11px;
                    color: #F39C12;
                    padding: 3px;
                }
            """)
        else:
            self.onboarding_status_label.setStyleSheet("""
                QLabel {
                    font-size: 11px;
                    color: #BDC3C7;
                    padding: 3px;
                }
            """)

    def load_onboarding_status(self):
        """Load onboarding status from the agent's status.json file."""
        if onboarding_integration:
            # Use the onboarding integration
            status = onboarding_integration.get_agent_onboarding_status(self.agent_id)
            if "error" not in status:
                self.update_onboarding_status(status["status"], status["progress"])
        else:
            # Fallback to direct file reading
            try:
                status_file = Path(f"agent_workspaces/{self.agent_id}/status.json")
                if status_file.exists():
                    with open(status_file, 'r') as f:
                        status_data = json.load(f)
                    
                    onboarding = status_data.get("onboarding", {})
                    status = onboarding.get("status", "not_started")
                    progress = onboarding.get("progress", 0)
                    
                    self.update_onboarding_status(status, progress)
            except Exception as e:
                print(f"Error loading onboarding status for {self.agent_id}: {e}")

    # Agent control methods (to be connected in main GUI)
    def ping_agent(self):
        pass
    def get_status(self):
        pass
    def resume_agent(self):
        pass
    def pause_agent(self):
        pass
    def assign_task(self):
        pass 
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton, QGroupBox,
    QProgressBar, QLineEdit, QTextEdit, QComboBox
)
from PyQt5.QtCore import Qt, QTimer
import json
import os
from pathlib import Path
import subprocess
import sys

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
        # Contract UI state
        self.contract_task_id_input: QLineEdit | None = None
        self.contract_state_select: QComboBox | None = None
        self.contract_evidence_input: QTextEdit | None = None
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

        # Row 1: quick actions
        row1 = QHBoxLayout()
        for text, tooltip, callback in [
            ("🔍 Ping", "Test if agent is responsive", self.ping_agent),
            ("📊 Status", "Read agent status", self.get_status),
            ("▶️ Resume", "Resume operations", self.resume_agent),
            ("⏸️ Pause", "Pause operations", self.pause_agent),
        ]:
            btn = QPushButton(text)
            btn.setToolTip(tooltip)
            btn.clicked.connect(callback)
            btn.setStyleSheet("""
                QPushButton { background-color: #34495E; color: white; border-radius: 6px; padding: 8px; font-weight: bold; }
                QPushButton:hover { background-color: #2C3E50; }
            """)
            row1.addWidget(btn)
        controls_layout.addLayout(row1)

        # Contract update section
        contract_group = QGroupBox("Contract Update")
        contract_group.setStyleSheet("""
            QGroupBox { color: white; border: 2px solid #34495E; border-radius: 6px; margin-top: 8px; padding-top: 8px; }
        """)
        cg = QVBoxLayout(contract_group)
        # Task ID input
        self.contract_task_id_input = QLineEdit()
        self.contract_task_id_input.setPlaceholderText("task_id (e.g., repo-task-slug)")
        self.contract_task_id_input.setStyleSheet("QLineEdit { background-color: #2C3E50; color: #ECF0F1; border: 1px solid #34495E; border-radius: 4px; padding: 6px; }")
        cg.addWidget(self.contract_task_id_input)
        # State selector
        self.contract_state_select = QComboBox()
        self.contract_state_select.addItems(["ready", "executing", "syncing", "verifying", "done", "blocked"])
        self.contract_state_select.setStyleSheet("QComboBox { background-color: #2C3E50; color: #ECF0F1; border: 1px solid #34495E; border-radius: 4px; padding: 4px; }")
        cg.addWidget(self.contract_state_select)
        # Evidence input
        self.contract_evidence_input = QTextEdit()
        self.contract_evidence_input.setPlaceholderText("evidence (links, notes)")
        self.contract_evidence_input.setFixedHeight(60)
        self.contract_evidence_input.setStyleSheet("QTextEdit { background-color: #2C3E50; color: #ECF0F1; border: 1px solid #34495E; border-radius: 4px; }")
        cg.addWidget(self.contract_evidence_input)
        # Buttons row
        row2 = QHBoxLayout()
        for label, state in [("Start", "executing"), ("Sync", "syncing"), ("Verify", "verifying"), ("Complete", "done")]:
            b = QPushButton(label)
            b.setStyleSheet("QPushButton { background-color: #16A085; color: white; border-radius: 6px; padding: 6px 10px; font-weight: bold; } QPushButton:hover { background-color: #138D75; }")
            b.clicked.connect(lambda _, s=state: self.send_contract_update(s))
            row2.addWidget(b)
        send_btn = QPushButton("Send Update")
        send_btn.setStyleSheet("QPushButton { background-color: #27AE60; color: white; border-radius: 6px; padding: 6px 10px; font-weight: bold; } QPushButton:hover { background-color: #229954; }")
        send_btn.clicked.connect(self.send_selected_update)
        row2.addWidget(send_btn)
        cg.addLayout(row2)
        controls_layout.addWidget(contract_group)
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
        self._send_note("ping", "ping")
    def get_status(self):
        # Read state/status files if present
        try:
            agent_fs_id = self._agent_fs_id()
            state_file = Path(f"agent_workspaces/{agent_fs_id}/state.json")
            status_file = Path(f"agent_workspaces/{agent_fs_id}/status.json")
            state = json.loads(state_file.read_text(encoding="utf-8")) if state_file.exists() else {}
            status = json.loads(status_file.read_text(encoding="utf-8")) if status_file.exists() else {}
            print(f"[STATUS] {self.agent_id}: state={state} status={status}")
        except Exception as e:
            print(f"[STATUS_ERR] {self.agent_id}: {e}")
    def resume_agent(self):
        self._send_note("resume", "resume operations")
    def pause_agent(self):
        self._send_note("note", "pause operations")
    def assign_task(self):
        self._send_note("task", "focus highest leverage task from TASK_LIST.md")

    def send_contract_update(self, state: str) -> None:
        task_id = (self.contract_task_id_input.text().strip() if self.contract_task_id_input else "")
        evidence = (self.contract_evidence_input.toPlainText().strip() if self.contract_evidence_input else "")
        if not task_id:
            print(f"[CONTRACT] {self.agent_id}: missing task_id")
            return
        details = {"task_id": task_id, "state": state, "evidence": [evidence] if evidence else []}
        summary = f"{self.agent_id} contract update: {task_id} -> {state}"
        self._send_sync(to_agent="Agent-5", msg_type="sync", topic="contract_update", summary=summary, details=details)

    def send_selected_update(self) -> None:
        state = self.contract_state_select.currentText() if self.contract_state_select else "executing"
        self.send_contract_update(state)

    def _agent_label(self) -> str:
        # Convert gui id like 'agent-1' to 'Agent-1'
        parts = self.agent_id.split('-')
        return f"{parts[0].capitalize()}-{parts[1]}" if len(parts) == 2 else self.agent_id

    def _agent_fs_id(self) -> str:
        # filesystem uses lowercase 'agent-1'
        return self.agent_id

    def _send_note(self, note_type: str, text: str) -> None:
        summary = f"{self._agent_label()} {text}"
        self._send_sync(to_agent=self._agent_label(), msg_type="note", topic=note_type, summary=summary, details={})

    def _send_sync(self, to_agent: str, msg_type: str, topic: str, summary: str, details: dict) -> None:
        """Use send-sync.ps1 to send a JSON message to an agent inbox."""
        try:
            script = os.path.join("overnight_runner", "tools", "send-sync.ps1")
            payload_path = None
            if details:
                import tempfile
                payload_path = Path(tempfile.gettempdir()) / f"payload_{os.getpid()}_{self.agent_id}.json"
                payload_path.write_text(json.dumps(details, ensure_ascii=False), encoding="utf-8")
            cmd = [
                "pwsh", "-NoLogo", "-NoProfile", "-File", script,
                "-To", to_agent,
                "-Type", msg_type,
                "-Topic", topic,
                "-Summary", summary,
                "-From", self._agent_label(),
            ]
            if payload_path:
                cmd += ["-PayloadPath", str(payload_path)]
            subprocess.run(cmd, check=False, cwd=os.getcwd())
        except Exception as e:
            print(f"[SEND_ERR] {self.agent_id}: {e}")
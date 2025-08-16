#!/usr/bin/env python3
"""
Dream.OS Five-Agent Grid GUI
============================
Modern interface presenting five agent panels in a 2x3 grid (last cell used for shared controls).
Includes ACP new-chat onboarding for all five agents and quick utilities.
"""

from __future__ import annotations

import os
import sys
import threading
import subprocess
import json
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QGroupBox, QFrame, QTextEdit, QFileDialog, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, QTimer

# Import paths
current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))

# Import AgentPanel with fallback path adjustment
try:
    from gui.components.agent_panel import AgentPanel  # type: ignore
except Exception:
    sys.path.insert(0, os.path.join(project_root, 'gui'))
    from components.agent_panel import AgentPanel  # type: ignore


class FiveAgentGridGUI(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.agent_panels = {}
        # Selection state used by panel widgets to target specific agents
        self.selected_agents = []
        self.init_ui()
        self.setup_status_updates()

    def init_ui(self) -> None:
        self.setWindowTitle("Dream.OS Five-Agent Grid GUI")
        self.setGeometry(80, 60, 1600, 900)
        self.setStyleSheet("QMainWindow { background-color: #1A1A1A; }")

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Header
        header = self._build_header()
        main_layout.addWidget(header)

        # Grid of agent panels (2 rows x 3 cols)
        grid = QGridLayout()
        grid.setSpacing(12)

        # Create five agent panels using AgentPanel (expects ids like 'agent-1')
        agent_ids = ["agent-1", "agent-2", "agent-3", "agent-4", "agent-5"]
        positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]
        for agent_id, (r, c) in zip(agent_ids, positions):
            panel = AgentPanel(agent_id, self)
            panel.main_gui = self
            self.agent_panels[agent_id] = panel
            grid.addWidget(panel, r, c)

        # Shared controls in the last cell (1,2)
        controls = self._build_controls()
        grid.addWidget(controls, 1, 2)

        wrapper = QFrame()
        wrapper.setStyleSheet("QFrame { background-color: #2C3E50; border-radius: 10px; }")
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.addLayout(grid)
        main_layout.addWidget(wrapper)

        # Log area
        log = self._build_log_area()
        main_layout.addWidget(log)

        self.statusBar().showMessage("Ready - Five-Agent Grid")

    def _build_header(self) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet(
            "QFrame { background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #2C3E50, stop:1 #3498DB);"
            " border-radius: 10px; padding: 10px; }"
        )
        layout = QHBoxLayout(frame)

        title = QLabel("Dream.OS Five-Agent System")
        title.setStyleSheet("QLabel { font-size: 22px; font-weight: bold; color: white; }")
        subtitle = QLabel("Grid Layout – ACP new-chat onboarding + FSM orchestration")
        subtitle.setStyleSheet("QLabel { font-size: 12px; color: #BDC3C7; }")

        v = QVBoxLayout()
        v.addWidget(title)
        v.addWidget(subtitle)
        layout.addLayout(v)
        layout.addStretch()

        self.system_status_label = QLabel("🟢 Online")
        self.system_status_label.setStyleSheet("QLabel { font-size: 14px; color: #27AE60; font-weight: bold; }")
        layout.addWidget(self.system_status_label)
        return frame

    def _build_controls(self) -> QGroupBox:
        box = QGroupBox("Shared Controls")
        box.setStyleSheet(
            "QGroupBox { color: white; border: 2px solid #34495E; border-radius: 8px; margin-top: 10px; }"
            "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 4px 8px; }"
        )
        layout = QVBoxLayout(box)

        onboard_btn = QPushButton("🚀 Onboard (New Chat)")
        onboard_btn.setToolTip("Open new chat in each agent and send onboarding prompt")
        onboard_btn.setStyleSheet("QPushButton { background-color: #27AE60; color: white; border-radius: 8px; padding: 10px; font-weight: bold; }")
        onboard_btn.clicked.connect(self.onboard_agents_new_chat)

        start_listener_btn = QPushButton("🛰️ Start Agent-5 Listener")
        start_listener_btn.setStyleSheet("QPushButton { background-color: #3498DB; color: white; border-radius: 8px; padding: 10px; font-weight: bold; }")
        start_listener_btn.clicked.connect(self.start_fsm_listener)

        start_runner_btn = QPushButton("📡 Start FSM 5-Agent Run")
        start_runner_btn.setStyleSheet("QPushButton { background-color: #8E44AD; color: white; border-radius: 8px; padding: 10px; font-weight: bold; }")
        start_runner_btn.clicked.connect(self.start_fsm_runner)

        seed_tasks_btn = QPushButton("🌱 Seed Sample Tasks")
        seed_tasks_btn.setStyleSheet("QPushButton { background-color: #F39C12; color: white; border-radius: 8px; padding: 10px; font-weight: bold; }")
        seed_tasks_btn.clicked.connect(self.seed_sample_tasks)

        fsm_request_btn = QPushButton("📨 Send FSM Request Now")
        fsm_request_btn.setStyleSheet("QPushButton { background-color: #16A085; color: white; border-radius: 8px; padding: 10px; font-weight: bold; }")
        fsm_request_btn.clicked.connect(self.send_fsm_request)

        stop_btn = QPushButton("🛑 Stop Overnight/Listener")
        stop_btn.setStyleSheet("QPushButton { background-color: #E74C3C; color: white; border-radius: 8px; padding: 10px; font-weight: bold; }")
        stop_btn.clicked.connect(self.stop_processes)

        status_btn = QPushButton("📊 Refresh Status")
        status_btn.setStyleSheet("QPushButton { background-color: #34495E; color: white; border-radius: 8px; padding: 10px; font-weight: bold; }")
        status_btn.clicked.connect(self.update_agent_statuses)

        layout.addWidget(onboard_btn)
        layout.addWidget(start_listener_btn)
        layout.addWidget(start_runner_btn)
        layout.addWidget(seed_tasks_btn)
        layout.addWidget(fsm_request_btn)
        layout.addWidget(stop_btn)
        layout.addWidget(status_btn)
        return box

    def _build_log_area(self) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: #2C3E50; border-radius: 10px; border: 2px solid #34495E; }")
        v = QVBoxLayout(frame)
        title = QLabel("System Activity Log")
        title.setStyleSheet("QLabel { font-size: 14px; font-weight: bold; color: white; padding: 5px; }")
        v.addWidget(title)
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setStyleSheet("QTextEdit { background-color: #1A1A1A; color: #ECF0F1; border: 1px solid #34495E; border-radius: 5px; font-family: 'Consolas','Monaco', monospace; font-size: 11px; }")
        self.log_display.setMaximumHeight(220)
        v.addWidget(self.log_display)

        # Lightweight tasks summary
        tasks_title = QLabel("FSM Tasks Summary")
        tasks_title.setStyleSheet("QLabel { font-size: 12px; font-weight: bold; color: #ECF0F1; padding: 5px; }")
        v.addWidget(tasks_title)
        self.tasks_list = QListWidget()
        self.tasks_list.setStyleSheet("QListWidget { background-color: #1A1A1A; color: #BDC3C7; border: 1px solid #34495E; border-radius: 5px; font-size: 11px; }")
        self.tasks_list.setMaximumHeight(180)
        v.addWidget(self.tasks_list)

        # Add Clear Log button
        clear_btn = QPushButton("🧹 Clear Log")
        clear_btn.clicked.connect(self.clear_log)
        clear_btn.setStyleSheet("QPushButton { background-color: #7F8C8D; color: white; border-radius: 5px; padding: 8px; font-weight: bold; font-size: 10px; }")
        v.addWidget(clear_btn)

        save_btn = QPushButton("💾 Save Log")
        save_btn.clicked.connect(self.save_log)
        save_btn.setStyleSheet("QPushButton { background-color: #27AE60; color: white; border-radius: 5px; padding: 8px; font-weight: bold; font-size: 10px; }")
        v.addWidget(save_btn)
        return frame

    def log_message(self, sender: str, message: str) -> None:
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_display.append(f"[{ts}] {sender}: {message}")
        sb = self.log_display.verticalScrollBar()
        sb.setValue(sb.maximum())

    def setup_status_updates(self) -> None:
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_agent_statuses)
        self.status_timer.start(5000)
        self.log_message("System", "Five-Agent Grid GUI initialized")
        # Also refresh tasks summary periodically
        self.tasks_timer = QTimer()
        self.tasks_timer.timeout.connect(self.refresh_tasks_summary)
        self.tasks_timer.start(7000)

    def update_agent_statuses(self) -> None:
        # Lightweight placeholder – integrate OnboardingIntegration as needed
        workspace_root = os.environ.get("AGENT_FILE_ROOT", "D:\\repos\\Dadudekc")
        for agent_id in ["agent-1", "agent-2", "agent-3", "agent-4", "agent-5"]:
            try:
                status_file = os.path.join(workspace_root, agent_id, "status.json")
                if os.path.exists(status_file):
                    data = json.load(open(status_file, 'r'))
                    status = data.get('status', 'unknown')
                    task = data.get('current_task', 'idle')
                    self.log_message("Status", f"{agent_id}: {status} - {task}")
            except Exception as e:
                self.log_message("Error", f"status for {agent_id}: {e}")

    def refresh_tasks_summary(self) -> None:
        try:
            tasks_dir = os.path.join(os.getcwd(), "fsm_data", "tasks")
            items = []
            if os.path.isdir(tasks_dir):
                for name in sorted(os.listdir(tasks_dir)):
                    if not name.endswith('.json'):
                        continue
                    p = os.path.join(tasks_dir, name)
                    try:
                        data = json.load(open(p, 'r', encoding='utf-8'))
                    except Exception:
                        continue
                    task_id = data.get('task_id') or os.path.splitext(name)[0]
                    state = data.get('state', 'new')
                    owner = data.get('owner') or '-'
                    intent = (data.get('intent') or '').strip()
                    items.append(f"[{state}] {task_id} → {owner} — {intent}")
            self.tasks_list.clear()
            for s in items[:100]:
                self.tasks_list.addItem(QListWidgetItem(s))
        except Exception:
            # silent guard for GUI stability
            pass

    def onboard_agents_new_chat(self) -> None:
        self.log_message("System", "Starting ACP new-chat onboarding for five agents...")
        def run_tool():
            try:
                tool = os.path.join(os.getcwd(), "overnight_runner", "tools", "onboard_via_acp.py")
                if not os.path.exists(tool):
                    self.log_message("Error", f"Onboarding tool not found: {tool}")
                    return
                result = subprocess.run([sys.executable, tool, "--layout", "5-agent"], capture_output=True, text=True, cwd=os.getcwd())
                if result.returncode == 0:
                    self.log_message("System", "ACP onboarding prompts sent.")
                else:
                    self.log_message("Error", f"ACP onboarding failed: {result.stderr}")
            except Exception as e:
                self.log_message("Error", f"ACP onboarding error: {e}")
        t = threading.Thread(target=run_tool)
        t.daemon = True
        t.start()

    def start_fsm_listener(self) -> None:
        self.log_message("System", "Starting Agent-5 inbox listener...")
        def run_listener():
            try:
                result = subprocess.run([sys.executable, os.path.join("overnight_runner", "listener.py"), "--agent", "Agent-5"], capture_output=True, text=True, cwd=os.getcwd())
                if result.returncode == 0:
                    self.log_message("System", "Agent-5 listener exited.")
                else:
                    self.log_message("Error", f"Listener error: {result.stderr}")
            except Exception as e:
                self.log_message("Error", f"Listener failed: {e}")
        t = threading.Thread(target=run_listener)
        t.daemon = True
        t.start()

    def start_fsm_runner(self) -> None:
        self.log_message("System", "Starting FSM 5-agent run (Agent-5 captain)...")
        def run_runner():
            try:
                # Ensure comms root exists
                today = datetime.now().strftime("%Y%m%d")
                comms_base = os.path.join(os.getcwd(), "communications")
                comm_root = os.path.join(comms_base, f"overnight_{today}")
                os.makedirs(comm_root, exist_ok=True)

                args = [
                    sys.executable, os.path.join("overnight_runner", "runner.py"),
                    "--layout", "5-agent",
                    "--captain", "Agent-5",
                    "--resume-agents", "Agent-1,Agent-2,Agent-3,Agent-4",
                    "--sender", "Agent-3",
                    "--plan", "contracts",
                    "--fsm-enabled", "--fsm-agent", "Agent-5", "--fsm-workflow", "default",
                    "--interval-sec", "300", "--initial-wait-sec", "30", "--phase-wait-sec", "10",
                    "--stagger-ms", "2000", "--jitter-ms", "600",
                    "--comm-root", comm_root, "--create-comm-folders",
                ]
                subprocess.Popen(args, cwd=os.getcwd())
            except Exception as e:
                self.log_message("Error", f"Runner failed: {e}")
        t = threading.Thread(target=run_runner)
        t.daemon = True
        t.start()

    def seed_sample_tasks(self) -> None:
        self.log_message("System", "Seeding sample FSM tasks...")
        try:
            tasks_dir = os.path.join(os.getcwd(), "fsm_data", "tasks")
            os.makedirs(tasks_dir, exist_ok=True)
            seed = [
                {"task_id":"task-001","repo":"unified-workspace","intent":"add unit tests for APIClient retry/backoff","state":"new"},
                {"task_id":"task-002","repo":"trading-platform","intent":"add pre-commit (flake8/black) and fix top lint errors","state":"new"},
            ]
            for t in seed:
                with open(os.path.join(tasks_dir, f"{t['task_id']}.json"), 'w', encoding='utf-8') as f:
                    json.dump(t, f, indent=2)
            self.log_message("System", "Seeded task-001, task-002")
        except Exception as e:
            self.log_message("Error", f"Seed tasks failed: {e}")

    def send_fsm_request(self) -> None:
        self.log_message("System", "Sending FSM request to Agent-5...")
        try:
            workspace_root = os.environ.get("AGENT_FILE_ROOT", "D:\\repos\\Dadudekc")
            inbox = os.path.join(workspace_root, "Agent-5", "inbox")
            os.makedirs(inbox, exist_ok=True)
            payload = {
                "type": "fsm_request",
                "from": "Agent-3",
                "to": "Agent-5",
                "workflow": "default",
                "agents": ["Agent-1","Agent-2","Agent-3","Agent-4"],
            }
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fn = os.path.join(inbox, f"fsm_request_{ts}.json")
            with open(fn, 'w', encoding='utf-8') as f:
                json.dump(payload, f, indent=2)
            self.log_message("System", f"Dropped {os.path.basename(fn)}")
        except Exception as e:
            self.log_message("Error", f"FSM request failed: {e}")

    def stop_processes(self) -> None:
        self.log_message("System", "Stopping runner/listener processes...")
        try:
            script = os.path.join(os.getcwd(), "overnight_runner", "tools", "stop_overnight.ps1")
            if os.path.exists(script):
                subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script], cwd=os.getcwd())
                self.log_message("System", "Stop command issued.")
            else:
                self.log_message("Error", f"Stop script not found: {script}")
        except Exception as e:
            self.log_message("Error", f"Stop failed: {e}")

    def save_log(self) -> None:
        fn, _ = QFileDialog.getSaveFileName(self, "Save Log", "", "Text Files (*.txt);;All Files (*)")
        if fn:
            try:
                with open(fn, 'w', encoding='utf-8') as f:
                    f.write(self.log_display.toPlainText())
                self.log_message("System", f"Log saved to {fn}")
            except Exception as e:
                self.log_message("Error", f"Failed to save log: {e}")

    def clear_log(self) -> None:
        try:
            self.log_display.clear()
            self.log_message("System", "Log cleared")
        except Exception as e:
            self.log_message("Error", f"Failed to clear log: {e}")

    # --- Minimal agent control handlers used by panel widgets ---
    def _selected_or_all(self) -> list[str]:
        try:
            if getattr(self, "selected_agents", None):
                return list(self.selected_agents)
        except Exception:
            pass
        return list(self.agent_panels.keys())

    def ping_selected_agents(self) -> None:
        for agent_id in self._selected_or_all():
            self.log_message("Ping", f"Pinging {agent_id}...")

    def get_status_selected_agents(self) -> None:
        for agent_id in self._selected_or_all():
            # Lightweight file-based status probe consistent with update_agent_statuses
            try:
                workspace_root = os.environ.get("AGENT_FILE_ROOT", "D:\\repos\\Dadudekc")
                status_file = os.path.join(workspace_root, agent_id, "status.json")
                if os.path.exists(status_file):
                    data = json.load(open(status_file, 'r', encoding='utf-8'))
                    status = data.get('status', 'unknown')
                    task = data.get('current_task', 'idle')
                    self.log_message("Status", f"{agent_id}: {status} - {task}")
                else:
                    self.log_message("Status", f"{agent_id}: no status.json")
            except Exception as e:
                self.log_message("Error", f"status for {agent_id}: {e}")

    def resume_selected_agents(self) -> None:
        for agent_id in self._selected_or_all():
            self.log_message("Resume", f"Resuming {agent_id}...")


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    win = FiveAgentGridGUI()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()



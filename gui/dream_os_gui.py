#!/usr/bin/env python3
"""
Dream.OS Cell Phone GUI
Modern PyQt interface for managing agent communication functionality
"""

import sys
import threading
import time
from datetime import datetime
import os  # EDIT START: Added for path handling
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QGridLayout, QLabel, QPushButton, 
                            QComboBox, QTextEdit, QLineEdit, QGroupBox, 
                            QTabWidget, QSplitter, QFrame, QScrollArea)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QPixmap  # EDIT END: Added QPixmap import

# Import our agent cell phone system
from agent_cell_phone import AgentCellPhone, MsgTag

class StatusThread(QThread):
    """Thread for updating agent status."""
    status_updated = pyqtSignal(str)
    
    def __init__(self, acp):
        super().__init__()
        self.acp = acp
        self.running = True
    
    def run(self):
        while self.running:
            try:
                agents = self.acp.get_available_agents()
                status = f"Connected to {len(agents)} agents: {', '.join(agents)}"
                self.status_updated.emit(status)
                time.sleep(5)  # Update every 5 seconds
            except Exception as e:
                self.status_updated.emit(f"Status error: {e}")
                time.sleep(10)
    
    def stop(self):
        self.running = False

class DreamOSCellPhoneGUI(QMainWindow):
    """Modern PyQt GUI for Dream.OS Cell Phone."""
    
    def __init__(self):
        super().__init__()
        self.acp = AgentCellPhone(layout_mode="8-agent")
        self.agents = self.acp.get_available_agents()
        
        self.init_ui()
        self.setup_status_thread()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Dream.OS Cell Phone")
        # EDIT START: Set application window icon using logo.png if available
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))
        # EDIT END
        self.setGeometry(100, 100, 1000, 700)
        
        # Set modern styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #4CAF50;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton[type="secondary"] {
                background-color: #2196F3;
            }
            QPushButton[type="secondary"]:hover {
                background-color: #1976D2;
            }
            QPushButton[type="warning"] {
                background-color: #FF9800;
            }
            QPushButton[type="warning"]:hover {
                background-color: #F57C00;
            }
            QPushButton[type="danger"] {
                background-color: #F44336;
            }
            QPushButton[type="danger"]:hover {
                background-color: #D32F2F;
            }
            QComboBox {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 5px;
                color: white;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ffffff;
            }
            QTextEdit {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 4px;
                color: white;
                padding: 5px;
            }
            QLineEdit {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 5px;
                color: white;
            }
            QTabWidget::pane {
                border: 1px solid #555555;
                background-color: #2b2b2b;
            }
            QTabBar::tab {
                background-color: #3c3c3c;
                color: white;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Add tabs
        self.tab_widget.addTab(self.create_control_tab(), "🎮 Controls")
        self.tab_widget.addTab(self.create_messaging_tab(), "💬 Messaging")
        self.tab_widget.addTab(self.create_scripts_tab(), "🔧 Scripts")
        self.tab_widget.addTab(self.create_status_tab(), "📊 Status")
        
        # Status bar
        self.statusBar().showMessage("Dream.OS Cell Phone Ready")
        
    def create_header(self):
        """Create the header section."""
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        
        # EDIT START: Display logo image if available then title
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        if os.path.exists(logo_path):
            logo_pix = QPixmap(logo_path)
            if not logo_pix.isNull():
                logo_pix = logo_pix.scaledToHeight(40, Qt.SmoothTransformation)
                logo_label = QLabel()
                logo_label.setPixmap(logo_pix)
                header_layout.addWidget(logo_label)

        # Logo and title
        title_label = QLabel("📱 Dream.OS Cell Phone")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #4CAF50;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Agent selector
        agent_group = QGroupBox("Select Agent")
        agent_layout = QHBoxLayout(agent_group)
        
        self.agent_combo = QComboBox()
        self.agent_combo.addItems(self.agents)
        self.agent_combo.setCurrentText(self.agents[0] if self.agents else "")
        
        agent_layout.addWidget(QLabel("Agent:"))
        agent_layout.addWidget(self.agent_combo)
        
        header_layout.addWidget(agent_group)
        
        return header_frame
    
    def create_control_tab(self):
        """Create the control tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Individual controls
        individual_group = QGroupBox("Individual Agent Controls")
        individual_layout = QGridLayout(individual_group)
        
        # Row 1
        individual_layout.addWidget(QPushButton("📤 Send Resume", clicked=self.send_resume), 0, 0)
        individual_layout.addWidget(QPushButton("🔄 Sync Status", clicked=self.sync_status), 0, 1)
        individual_layout.addWidget(QPushButton("⏸️ Pause Agent", clicked=self.pause_agent), 0, 2)
        individual_layout.addWidget(QPushButton("▶️ Resume Agent", clicked=self.resume_agent), 0, 3)
        
        # Row 2
        individual_layout.addWidget(QPushButton("📋 Get Status", clicked=self.get_agent_status), 1, 0)
        individual_layout.addWidget(QPushButton("🔍 Ping Agent", clicked=self.ping_agent), 1, 1)
        individual_layout.addWidget(QPushButton("🎯 Assign Task", clicked=self.assign_task), 1, 2)
        individual_layout.addWidget(QPushButton("⚡ Emergency Stop", clicked=self.emergency_stop), 1, 3)
        
        layout.addWidget(individual_group)
        
        # Broadcast controls
        broadcast_group = QGroupBox("Broadcast Controls")
        broadcast_layout = QGridLayout(broadcast_group)
        
        # Row 1
        broadcast_layout.addWidget(QPushButton("📢 Broadcast Resume", clicked=self.broadcast_resume), 0, 0)
        broadcast_layout.addWidget(QPushButton("🔄 Broadcast Sync", clicked=self.broadcast_sync), 0, 1)
        broadcast_layout.addWidget(QPushButton("⏸️ Broadcast Pause", clicked=self.broadcast_pause), 0, 2)
        
        # Row 2
        broadcast_layout.addWidget(QPushButton("🎯 Broadcast Task", clicked=self.broadcast_task), 1, 0)
        broadcast_layout.addWidget(QPushButton("🔍 Broadcast Ping", clicked=self.broadcast_ping), 1, 1)
        broadcast_layout.addWidget(QPushButton("⚡ Emergency Broadcast", clicked=self.emergency_broadcast), 1, 2)
        
        layout.addWidget(broadcast_group)
        
        # Quick actions
        quick_group = QGroupBox("Quick Actions")
        quick_layout = QHBoxLayout(quick_group)
        
        quick_layout.addWidget(QPushButton("🚀 Start All Agents", clicked=self.start_all_agents))
        quick_layout.addWidget(QPushButton("🛑 Stop All Agents", clicked=self.stop_all_agents))
        quick_layout.addWidget(QPushButton("🔄 Restart All", clicked=self.restart_all_agents))
        
        layout.addWidget(quick_group)
        layout.addStretch()
        
        return widget
    
    def create_messaging_tab(self):
        """Create the enhanced messaging tab with advanced features."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Create splitter for better organization
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Message sending
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Message input group
        message_group = QGroupBox("Send Message")
        message_layout = QVBoxLayout(message_group)
        
        # Target selection
        target_layout = QHBoxLayout()
        target_layout.addWidget(QLabel("Target:"))
        self.target_combo = QComboBox()
        self.target_combo.addItems(["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8", "all"])
        target_layout.addWidget(self.target_combo)
        target_layout.addStretch()
        message_layout.addLayout(target_layout)
        
        # Message type selector
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Message Type:"))
        self.message_type_combo = QComboBox()
        self.message_type_combo.addItems(["Normal", "Task", "Resume", "Sync", "Emergency", "Command"])
        self.message_type_combo.currentTextChanged.connect(self.on_message_type_changed)
        type_layout.addWidget(self.message_type_combo)
        type_layout.addStretch()
        message_layout.addLayout(type_layout)
        
        # Command selector (shown when Command type is selected)
        self.command_layout = QHBoxLayout()
        self.command_layout.addWidget(QLabel("Command:"))
        self.command_combo = QComboBox()
        self.command_combo.addItems(["ping", "status", "resume", "sync", "verify", "task", "captain"])
        self.command_layout.addWidget(self.command_combo)
        self.command_layout.addStretch()
        message_layout.addLayout(self.command_layout)
        
        # Message input
        input_layout = QHBoxLayout()
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Enter your message here...")
        self.message_input.returnPressed.connect(self.send_custom_message)
        input_layout.addWidget(self.message_input)
        
        send_btn = QPushButton("📤 Send")
        send_btn.clicked.connect(self.send_custom_message)
        input_layout.addWidget(send_btn)
        message_layout.addLayout(input_layout)
        
        left_layout.addWidget(message_group)
        
        # Quick commands group
        quick_group = QGroupBox("Quick Commands")
        quick_layout = QGridLayout(quick_group)
        
        # Row 1
        quick_layout.addWidget(QPushButton("🔍 Ping", clicked=self.quick_ping), 0, 0)
        quick_layout.addWidget(QPushButton("📋 Status", clicked=self.quick_status), 0, 1)
        quick_layout.addWidget(QPushButton("▶️ Resume", clicked=self.quick_resume), 0, 2)
        quick_layout.addWidget(QPushButton("🔄 Sync", clicked=self.quick_sync), 0, 3)
        
        # Row 2
        quick_layout.addWidget(QPushButton("🎯 Task", clicked=self.quick_task), 1, 0)
        quick_layout.addWidget(QPushButton("⚡ Emergency", clicked=self.quick_emergency), 1, 1)
        quick_layout.addWidget(QPushButton("🔧 Verify", clicked=self.quick_verify), 1, 2)
        quick_layout.addWidget(QPushButton("👑 Captain", clicked=self.quick_captain), 1, 3)
        
        left_layout.addWidget(quick_group)
        
        # Broadcast controls
        broadcast_group = QGroupBox("Broadcast Controls")
        broadcast_layout = QGridLayout(broadcast_group)
        
        broadcast_layout.addWidget(QPushButton("📢 Broadcast Message", clicked=self.broadcast_message), 0, 0)
        broadcast_layout.addWidget(QPushButton("🔍 Broadcast Ping", clicked=self.broadcast_ping), 0, 1)
        broadcast_layout.addWidget(QPushButton("📋 Broadcast Status", clicked=self.broadcast_status), 0, 2)
        broadcast_layout.addWidget(QPushButton("🎯 Broadcast Task", clicked=self.broadcast_task), 0, 3)
        
        left_layout.addWidget(broadcast_group)
        
        # Interactive mode toggle
        interactive_group = QGroupBox("Interactive Mode")
        interactive_layout = QHBoxLayout(interactive_group)
        
        self.interactive_btn = QPushButton("🎮 Start Interactive Mode")
        self.interactive_btn.clicked.connect(self.toggle_interactive_mode)
        interactive_layout.addWidget(self.interactive_btn)
        
        self.interactive_status = QLabel("Interactive mode: OFF")
        self.interactive_status.setStyleSheet("color: #FF9800;")
        interactive_layout.addWidget(self.interactive_status)
        
        left_layout.addWidget(interactive_group)
        
        left_layout.addStretch()
        
        # Right panel - Message history and console
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Message history
        history_group = QGroupBox("Message History & Console")
        history_layout = QVBoxLayout(history_group)
        
        self.message_history = QTextEdit()
        self.message_history.setReadOnly(True)
        self.message_history.setMinimumHeight(300)
        history_layout.addWidget(self.message_history)
        
        # History controls
        history_controls = QHBoxLayout()
        history_controls.addWidget(QPushButton("🔄 Refresh", clicked=self.refresh_messages))
        history_controls.addWidget(QPushButton("🗑️ Clear", clicked=self.clear_messages))
        history_controls.addWidget(QPushButton("💾 Save Log", clicked=self.save_message_log))
        history_controls.addStretch()
        history_layout.addLayout(history_controls)
        
        right_layout.addWidget(history_group)
        
        # Interactive console (hidden by default)
        self.console_group = QGroupBox("Interactive Console")
        console_layout = QVBoxLayout(self.console_group)
        
        self.console_input = QLineEdit()
        self.console_input.setPlaceholderText("Enter command (send <target> <message>, command <target> <cmd> [args], status, quit)")
        self.console_input.returnPressed.connect(self.execute_console_command)
        console_layout.addWidget(self.console_input)
        
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setMaximumHeight(150)
        console_layout.addWidget(self.console_output)
        
        self.console_group.setVisible(False)
        right_layout.addWidget(self.console_group)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 600])  # Set initial split sizes
        
        layout.addWidget(splitter)
        
        return widget
    
    def create_scripts_tab(self):
        """Create the scripts tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Scripts group
        scripts_group = QGroupBox("Scripts")
        scripts_layout = QVBoxLayout(scripts_group)
        
        # Scripts buttons
        scripts_layout.addWidget(QPushButton("🚀 Run All Scripts", clicked=self.run_all_scripts))
        scripts_layout.addWidget(QPushButton("🛑 Stop All Scripts", clicked=self.stop_all_scripts))
        scripts_layout.addWidget(QPushButton("🔄 Restart All Scripts", clicked=self.restart_all_scripts))
        
        layout.addWidget(scripts_group)
        
        return widget
    
    def create_status_tab(self):
        """Create the status tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # System status
        system_group = QGroupBox("System Status")
        system_layout = QVBoxLayout(system_group)
        
        self.system_status = QTextEdit()
        self.system_status.setReadOnly(True)
        system_layout.addWidget(self.system_status)
        
        # Status controls
        status_controls = QHBoxLayout()
        status_controls.addWidget(QPushButton("🔄 Refresh Status", clicked=self.refresh_system_status))
        status_controls.addWidget(QPushButton("📊 Detailed Report", clicked=self.generate_report))
        status_controls.addStretch()
        system_layout.addLayout(status_controls)
        
        layout.addWidget(system_group)
        
        # Agent grid
        agent_group = QGroupBox("Agent Status Grid")
        agent_layout = QGridLayout(agent_group)
        
        # Create agent status buttons
        self.agent_buttons = {}
        row, col = 0, 0
        for agent in self.agents:
            btn = QPushButton(f"{agent}\n🟢 Online")
            btn.setMinimumSize(120, 80)
            btn.clicked.connect(lambda checked, a=agent: self.select_agent(a))
            self.agent_buttons[agent] = btn
            agent_layout.addWidget(btn, row, col)
            col += 1
            if col > 3:  # 4 columns
                col = 0
                row += 1
        
        layout.addWidget(agent_group)
        layout.addStretch()
        
        return widget
    
    def setup_status_thread(self):
        """Setup the status update thread."""
        self.status_thread = StatusThread(self.acp)
        self.status_thread.status_updated.connect(self.update_status_display)
        self.status_thread.start()
    
    def log_message(self, message):
        """Log a message to the history."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.message_history.append(log_entry)
        self.system_status.append(log_entry)
    
    def select_agent(self, agent):
        """Select an agent from the grid."""
        self.agent_combo.setCurrentText(agent)
        self.log_message(f"Selected agent: {agent}")
    
    # Individual control methods
    def send_resume(self):
        agent = self.agent_combo.currentText()
        try:
            self.acp.send(agent, "Resume operation", MsgTag.RESUME)
            self.log_message(f"📤 Sent resume command to {agent}")
        except Exception as e:
            self.log_message(f"❌ Failed to send resume to {agent}: {e}")
    
    def sync_status(self):
        agent = self.agent_combo.currentText()
        try:
            self.acp.send(agent, "Sync status", MsgTag.SYNC)
            self.log_message(f"🔄 Sent sync command to {agent}")
        except Exception as e:
            self.log_message(f"❌ Failed to send sync to {agent}: {e}")
    
    def pause_agent(self):
        agent = self.agent_combo.currentText()
        try:
            self.acp.send(agent, "Pause operation", MsgTag.NORMAL)
            self.log_message(f"⏸️ Sent pause command to {agent}")
        except Exception as e:
            self.log_message(f"❌ Failed to send pause to {agent}: {e}")
    
    def resume_agent(self):
        agent = self.agent_combo.currentText()
        try:
            self.acp.send(agent, "Resume operation", MsgTag.RESUME)
            self.log_message(f"▶️ Sent resume command to {agent}")
        except Exception as e:
            self.log_message(f"❌ Failed to send resume to {agent}: {e}")
    
    def get_agent_status(self):
        agent = self.agent_combo.currentText()
        try:
            self.acp.send(agent, "Get status", MsgTag.SYNC)
            self.log_message(f"📋 Requested status from {agent}")
        except Exception as e:
            self.log_message(f"❌ Failed to get status from {agent}: {e}")
    
    def ping_agent(self):
        agent = self.agent_combo.currentText()
        try:
            self.acp.send(agent, "Ping", MsgTag.NORMAL)
            self.log_message(f"🔍 Pinging {agent}")
        except Exception as e:
            self.log_message(f"❌ Failed to ping {agent}: {e}")
    
    def assign_task(self):
        agent = self.agent_combo.currentText()
        try:
            self.acp.send(agent, "Assign new task", MsgTag.TASK)
            self.log_message(f"🎯 Assigned task to {agent}")
        except Exception as e:
            self.log_message(f"❌ Failed to assign task to {agent}: {e}")
    
    def emergency_stop(self):
        agent = self.agent_combo.currentText()
        try:
            self.acp.send(agent, "Emergency stop", MsgTag.EMERGENCY)
            self.log_message(f"⚡ Emergency stop sent to {agent}")
        except Exception as e:
            self.log_message(f"❌ Failed to emergency stop {agent}: {e}")
    
    # Broadcast control methods
    def broadcast_resume(self):
        try:
            self.acp.broadcast("Resume all operations", MsgTag.RESUME)
            self.log_message("📢 Broadcasted resume command to all agents")
        except Exception as e:
            self.log_message(f"❌ Broadcast resume failed: {e}")
    
    def broadcast_sync(self):
        try:
            self.acp.broadcast("Sync all status", MsgTag.SYNC)
            self.log_message("🔄 Broadcasted sync command to all agents")
        except Exception as e:
            self.log_message(f"❌ Broadcast sync failed: {e}")
    
    def broadcast_pause(self):
        try:
            self.acp.broadcast("Pause all operations", MsgTag.NORMAL)
            self.log_message("⏸️ Broadcasted pause command to all agents")
        except Exception as e:
            self.log_message(f"❌ Broadcast pause failed: {e}")
    
    def broadcast_task(self):
        try:
            self.acp.broadcast("New task assignment", MsgTag.TASK)
            self.log_message("🎯 Broadcasted task to all agents")
        except Exception as e:
            self.log_message(f"❌ Broadcast task failed: {e}")
    
    def broadcast_ping(self):
        try:
            self.acp.broadcast("Ping all agents", MsgTag.NORMAL)
            self.log_message("🔍 Broadcasted ping to all agents")
        except Exception as e:
            self.log_message(f"❌ Broadcast ping failed: {e}")
    
    def emergency_broadcast(self):
        try:
            self.acp.broadcast("Emergency broadcast", MsgTag.EMERGENCY)
            self.log_message("⚡ Emergency broadcast sent to all agents")
        except Exception as e:
            self.log_message(f"❌ Emergency broadcast failed: {e}")
    
    # Quick action methods
    def start_all_agents(self):
        try:
            self.acp.broadcast("Start all agents", MsgTag.RESUME)
            self.log_message("🚀 Started all agents")
        except Exception as e:
            self.log_message(f"❌ Failed to start all agents: {e}")
    
    def stop_all_agents(self):
        try:
            self.acp.broadcast("Stop all agents", MsgTag.NORMAL)
            self.log_message("🛑 Stopped all agents")
        except Exception as e:
            self.log_message(f"❌ Failed to stop all agents: {e}")
    
    def restart_all_agents(self):
        try:
            self.acp.broadcast("Restart all agents", MsgTag.RESUME)
            self.log_message("🔄 Restarted all agents")
        except Exception as e:
            self.log_message(f"❌ Failed to restart all agents: {e}")
    
    # Messaging methods
    def on_message_type_changed(self, message_type):
        """Handle message type change to show/hide command selector."""
        if message_type == "Command":
            self.command_layout.setVisible(True)
            self.message_input.setPlaceholderText("Enter command arguments (optional)...")
        else:
            self.command_layout.setVisible(False)
            self.message_input.setPlaceholderText("Enter your message here...")
    
    def quick_ping(self):
        """Send ping command to selected target."""
        target = self.target_combo.currentText()
        try:
            if target == "all":
                self.acp.broadcast("Ping", MsgTag.NORMAL)
                self.log_message("🔍 Broadcasted ping to all agents")
            else:
                self.acp.send(target, "Ping", MsgTag.NORMAL)
                self.log_message(f"🔍 Pinging {target}")
        except Exception as e:
            self.log_message(f"❌ Failed to ping {target}: {e}")
    
    def quick_status(self):
        """Send status command to selected target."""
        target = self.target_combo.currentText()
        try:
            if target == "all":
                self.acp.broadcast("Get status", MsgTag.SYNC)
                self.log_message("📋 Broadcasted status request to all agents")
            else:
                self.acp.send(target, "Get status", MsgTag.SYNC)
                self.log_message(f"📋 Requested status from {target}")
        except Exception as e:
            self.log_message(f"❌ Failed to get status from {target}: {e}")
    
    def quick_resume(self):
        """Send resume command to selected target."""
        target = self.target_combo.currentText()
        try:
            if target == "all":
                self.acp.broadcast("Resume operation", MsgTag.RESUME)
                self.log_message("▶️ Broadcasted resume command to all agents")
            else:
                self.acp.send(target, "Resume operation", MsgTag.RESUME)
                self.log_message(f"▶️ Sent resume command to {target}")
        except Exception as e:
            self.log_message(f"❌ Failed to send resume to {target}: {e}")
    
    def quick_sync(self):
        """Send sync command to selected target."""
        target = self.target_combo.currentText()
        try:
            if target == "all":
                self.acp.broadcast("Sync status", MsgTag.SYNC)
                self.log_message("🔄 Broadcasted sync command to all agents")
            else:
                self.acp.send(target, "Sync status", MsgTag.SYNC)
                self.log_message(f"🔄 Sent sync command to {target}")
        except Exception as e:
            self.log_message(f"❌ Failed to send sync to {target}: {e}")
    
    def quick_task(self):
        """Send task command to selected target."""
        target = self.target_combo.currentText()
        try:
            if target == "all":
                self.acp.broadcast("Assign new task", MsgTag.TASK)
                self.log_message("🎯 Broadcasted task assignment to all agents")
            else:
                self.acp.send(target, "Assign new task", MsgTag.TASK)
                self.log_message(f"🎯 Assigned task to {target}")
        except Exception as e:
            self.log_message(f"❌ Failed to assign task to {target}: {e}")
    
    def quick_emergency(self):
        """Send emergency command to selected target."""
        target = self.target_combo.currentText()
        try:
            if target == "all":
                self.acp.broadcast("Emergency stop", MsgTag.EMERGENCY)
                self.log_message("⚡ Broadcasted emergency command to all agents")
            else:
                self.acp.send(target, "Emergency stop", MsgTag.EMERGENCY)
                self.log_message(f"⚡ Sent emergency command to {target}")
        except Exception as e:
            self.log_message(f"❌ Failed to send emergency command to {target}: {e}")
    
    def quick_verify(self):
        """Send verify command to selected target."""
        target = self.target_combo.currentText()
        try:
            if target == "all":
                self.acp.broadcast("Verify system", MsgTag.SYNC)
                self.log_message("🔧 Broadcasted verify command to all agents")
            else:
                self.acp.send(target, "Verify system", MsgTag.SYNC)
                self.log_message(f"🔧 Sent verify command to {target}")
        except Exception as e:
            self.log_message(f"❌ Failed to send verify command to {target}: {e}")
    
    def quick_captain(self):
        """Send captain command to selected target."""
        target = self.target_combo.currentText()
        try:
            if target == "all":
                self.acp.broadcast("Captain report", MsgTag.NORMAL)
                self.log_message("👑 Broadcasted captain command to all agents")
            else:
                self.acp.send(target, "Captain report", MsgTag.NORMAL)
                self.log_message(f"👑 Sent captain command to {target}")
        except Exception as e:
            self.log_message(f"❌ Failed to send captain command to {target}: {e}")
    
    def broadcast_message(self):
        """Broadcast a custom message to all agents."""
        message = self.message_input.text()
        if not message:
            self.log_message("❌ No message to broadcast")
            return
        
        try:
            self.acp.broadcast(message, MsgTag.NORMAL)
            self.log_message(f"📢 Broadcasted message to all agents: {message}")
            self.message_input.clear()
        except Exception as e:
            self.log_message(f"❌ Failed to broadcast message: {e}")
    
    def broadcast_status(self):
        """Broadcast status request to all agents."""
        try:
            self.acp.broadcast("Get status", MsgTag.SYNC)
            self.log_message("📋 Broadcasted status request to all agents")
        except Exception as e:
            self.log_message(f"❌ Failed to broadcast status request: {e}")
    
    def toggle_interactive_mode(self):
        """Toggle interactive mode on/off."""
        if not hasattr(self, 'interactive_mode') or not self.interactive_mode:
            self.interactive_mode = True
            self.interactive_btn.setText("🛑 Stop Interactive Mode")
            self.interactive_btn.setStyleSheet("background-color: #F44336;")
            self.interactive_status.setText("Interactive mode: ON")
            self.interactive_status.setStyleSheet("color: #4CAF50;")
            self.console_group.setVisible(True)
            self.log_message("🎮 Interactive mode started")
            self.console_output.append("🎮 Interactive Agent Messenger Started\n")
            self.console_output.append("Available commands:\n")
            self.console_output.append("- send <target> <message>\n")
            self.console_output.append("- command <target> <cmd> [args]\n")
            self.console_output.append("- status\n")
            self.console_output.append("- quit\n")
        else:
            self.interactive_mode = False
            self.interactive_btn.setText("🎮 Start Interactive Mode")
            self.interactive_btn.setStyleSheet("")
            self.interactive_status.setText("Interactive mode: OFF")
            self.interactive_status.setStyleSheet("color: #FF9800;")
            self.console_group.setVisible(False)
            self.log_message("🛑 Interactive mode stopped")
    
    def execute_console_command(self):
        """Execute a command from the interactive console."""
        if not hasattr(self, 'interactive_mode') or not self.interactive_mode:
            return
        
        cmd = self.console_input.text().strip()
        if not cmd:
            return
        
        self.console_output.append(f"$ {cmd}\n")
        self.console_input.clear()
        
        try:
            parts = cmd.split()
            if len(parts) < 2:
                self.console_output.append("Usage: send <target> <message>, command <target> <cmd> [args], status, or quit\n")
                return
            
            if parts[0].lower() == 'send':
                if len(parts) < 3:
                    self.console_output.append("Usage: send <target> <message>\n")
                    return
                
                target = parts[1]
                message_text = ' '.join(parts[2:])
                
                if target == "all":
                    self.acp.broadcast(message_text, MsgTag.NORMAL)
                    self.console_output.append(f"✅ Message broadcast to all agents\n")
                else:
                    self.acp.send(target, message_text, MsgTag.NORMAL)
                    self.console_output.append(f"✅ Message sent to {target}\n")
            
            elif parts[0].lower() == 'command':
                if len(parts) < 3:
                    self.console_output.append("Usage: command <target> <cmd> [args]\n")
                    return
                
                target = parts[1]
                command = parts[2]
                args = parts[3:] if len(parts) > 3 else []
                
                if target == "all":
                    self.acp.broadcast(f"Command: {command} {' '.join(args)}", MsgTag.NORMAL)
                    self.console_output.append(f"✅ Command '{command}' broadcast to all agents\n")
                else:
                    self.acp.send(target, f"Command: {command} {' '.join(args)}", MsgTag.NORMAL)
                    self.console_output.append(f"✅ Command '{command}' sent to {target}\n")
            
            elif parts[0].lower() == 'status':
                status = f"Connected to {len(self.agents)} agents: {', '.join(self.agents)}"
                self.console_output.append(f"📊 {status}\n")
            
            elif parts[0].lower() in ['quit', 'exit', 'q']:
                self.toggle_interactive_mode()
            
            else:
                self.console_output.append("Unknown command. Use: send, command, status, or quit\n")
                
        except Exception as e:
            self.console_output.append(f"❌ Error: {e}\n")
    
    def save_message_log(self):
        """Save the message history to a file."""
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"message_log_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.message_history.toPlainText())
            
            self.log_message(f"💾 Message log saved to {filename}")
        except Exception as e:
            self.log_message(f"❌ Failed to save message log: {e}")
    
    def send_custom_message(self):
        """Send a custom message with enhanced functionality."""
        target = self.target_combo.currentText()
        message = self.message_input.text()
        message_type = self.message_type_combo.currentText()
        
        if not message and message_type != "Command":
            return
        
        try:
            if message_type == "Command":
                command = self.command_combo.currentText()
                if target == "all":
                    self.acp.broadcast(f"Command: {command} {message}", MsgTag.NORMAL)
                    self.log_message(f"📤 Broadcasted command '{command}' to all agents: {message}")
                else:
                    self.acp.send(target, f"Command: {command} {message}", MsgTag.NORMAL)
                    self.log_message(f"📤 Sent command '{command}' to {target}: {message}")
            else:
                # Map message type to MsgTag
                tag_map = {
                    "Normal": MsgTag.NORMAL,
                    "Task": MsgTag.TASK,
                    "Resume": MsgTag.RESUME,
                    "Sync": MsgTag.SYNC,
                    "Emergency": MsgTag.EMERGENCY
                }
                
                tag = tag_map.get(message_type, MsgTag.NORMAL)
                
                if target == "all":
                    self.acp.broadcast(message, tag)
                    self.log_message(f"📤 Broadcasted {message_type} message to all agents: {message}")
                else:
                    self.acp.send(target, message, tag)
                    self.log_message(f"📤 Sent {message_type} message to {target}: {message}")
            
            self.message_input.clear()
        except Exception as e:
            self.log_message(f"❌ Failed to send message: {e}")
    
    def refresh_messages(self):
        self.log_message("🔄 Message history refreshed")
    
    def clear_messages(self):
        self.message_history.clear()
        self.system_status.clear()
        self.log_message("🗑️ Message history cleared")
    
    def refresh_system_status(self):
        self.log_message("🔄 System status refreshed")
        self.log_message(f"📊 Connected to {len(self.agents)} agents: {', '.join(self.agents)}")
    
    def generate_report(self):
        self.log_message("📊 Generating detailed system report...")
        self.log_message(f"📋 Total agents: {len(self.agents)}")
        self.log_message(f"📋 Agent list: {', '.join(self.agents)}")
        self.log_message("📋 System operational and ready")
    
    def update_status_display(self, status):
        """Update the status display."""
        self.statusBar().showMessage(status)
    
    # Script execution methods
    def run_all_scripts(self):
        """Run all available scripts."""
        try:
            import subprocess
            import os
            
            # Set PYTHONPATH to include src directory
            env = os.environ.copy()
            env['PYTHONPATH'] = os.path.join(os.getcwd(), 'src') + os.pathsep + env.get('PYTHONPATH', '')
            
            # Run agent messenger
            subprocess.Popen([sys.executable, "scripts/agent_messenger.py"], env=env)
            self.log_message("🚀 Started agent_messenger.py")
            
            # Run onboarding sequence
            subprocess.Popen([sys.executable, "scripts/agent_onboarding_sequence.py"], env=env)
            self.log_message("🚀 Started agent_onboarding_sequence.py")
            
            # Run send to agents
            subprocess.Popen([sys.executable, "scripts/send_to_agents.py"], env=env)
            self.log_message("🚀 Started send_to_agents.py")
            
            self.log_message("✅ All scripts started successfully")
            
        except Exception as e:
            self.log_message(f"❌ Error running scripts: {e}")
    
    def stop_all_scripts(self):
        """Stop all running scripts."""
        try:
            import subprocess
            import os
            
            # Kill Python processes running our scripts
            if os.name == 'nt':  # Windows
                subprocess.run(["taskkill", "/f", "/im", "python.exe"], 
                             capture_output=True, text=True)
            else:  # Unix/Linux
                subprocess.run(["pkill", "-f", "scripts/"], 
                             capture_output=True, text=True)
            
            self.log_message("🛑 All scripts stopped")
            
        except Exception as e:
            self.log_message(f"❌ Error stopping scripts: {e}")
    
    def restart_all_scripts(self):
        """Restart all scripts."""
        self.stop_all_scripts()
        self.log_message("🔄 Restarting all scripts...")
        self.run_all_scripts()
    
    def closeEvent(self, event):
        """Handle window close event."""
        if hasattr(self, 'status_thread'):
            self.status_thread.stop()
            self.status_thread.wait()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Dream.OS Cell Phone")
    app.setApplicationVersion("1.0")
    
    window = DreamOSCellPhoneGUI()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 
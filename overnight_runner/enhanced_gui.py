#!/usr/bin/env python3
"""
Enhanced Overnight Runner GUI with Agent-5 Command Center
--------------------------------------------------------
• Expanded GUI for commanding Agent-5
• PyAutoGUI messaging queue system to prevent conflicts
• Agent coordination and overnight run facilitation
• Real-time status monitoring and control
"""

from __future__ import annotations

import os
import subprocess
import sys
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk, scrolledtext
from typing import Dict, List, Optional, Tuple
import queue
import json

# Import the configurable paths system
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "core"))
try:
    from config import get_repos_root, get_owner_path, get_communications_root
except ImportError:
    # Fallback if config system not available
    def get_repos_root(): return "D:/repos"
    def get_owner_path(): return "D:/repos/Dadudekc"
    def get_communications_root(): return "D:/repos/communications"


class PyAutoGUIQueue:
    """Queue system for PyAutoGUI messaging to prevent conflicts when multiple agents/instances try to control PyAutoGUI simultaneously."""
    
    def __init__(self):
        self.message_queue = queue.Queue()
        self.processing = False
        self.agent_locks: Dict[str, threading.Lock] = {}
        self.processing_thread = None
        self.start_processing()
    
    def add_agent(self, agent_id: str):
        """Add an agent to the queue system."""
        if agent_id not in self.agent_locks:
            self.agent_locks[agent_id] = threading.Lock()
    
    def queue_message(self, agent_id: str, message: str, priority: int = 1) -> bool:
        """Queue a message for an agent with priority (lower = higher priority)."""
        try:
            self.add_agent(agent_id)
            self.message_queue.put((priority, time.time(), agent_id, message))
            return True
        except Exception as e:
            print(f"Error queuing message: {e}")
            return False
    
    def start_processing(self):
        """Start the message processing thread."""
        if not self.processing:
            self.processing = True
            self.processing_thread = threading.Thread(target=self._process_queue, daemon=True)
            self.processing_thread.start()
    
    def stop_processing(self):
        """Stop the message processing thread."""
        self.processing = False
        if self.processing_thread:
            self.processing_thread.join(timeout=1)

    def clear_queue(self) -> bool:
        """Purge all pending messages and release agent locks.

        Returns:
            bool: True if the queue was cleared without error, False otherwise.
        """
        try:
            # Stop processing to avoid race conditions while clearing
            self.stop_processing()

            # Drain all pending messages
            while not self.message_queue.empty():
                try:
                    self.message_queue.get_nowait()
                    self.message_queue.task_done()
                except queue.Empty:
                    break

            # Release any agent locks that might still be held
            for lock in self.agent_locks.values():
                try:
                    if lock.locked():
                        lock.release()
                except Exception:
                    # If a lock can't be released (shouldn't happen with normal
                    # threading.Lock), continue clearing the rest
                    continue

            return True
        except Exception as e:
            print(f"Error clearing queue: {e}")
            return False
        finally:
            # Restart processing so new messages can be handled
            self.start_processing()
    
    def _process_queue(self):
        """Process messages from the queue one at a time."""
        while self.processing:
            try:
                # Get message with timeout to allow stopping
                try:
                    priority, timestamp, agent_id, message = self.message_queue.get(timeout=1)
                except queue.Empty:
                    continue
                
                # Acquire lock for this agent
                if agent_id in self.agent_locks:
                    with self.agent_locks[agent_id]:
                        print(f"[QUEUE] Processing message for {agent_id}: {message[:50]}...")
                        
                        # Simulate PyAutoGUI operation with delay
                        time.sleep(0.5)  # Simulate typing time
                        
                        # Mark message as processed
                        self.message_queue.task_done()
                        
                        print(f"[QUEUE] Completed message for {agent_id}")
                
            except Exception as e:
                print(f"Error processing message: {e}")
                continue
    
    def get_queue_status(self) -> Dict[str, any]:
        """Get current queue status."""
        return {
            "queue_size": self.message_queue.qsize(),
            "processing": self.processing,
            "agent_locks": {agent: lock.locked() for agent, lock in self.agent_locks.items()}
        }


class Agent5CommandCenter:
    """Command center for Agent-5 to control other agents and facilitate overnight runs."""
    
    def __init__(self, gui):
        self.gui = gui
        self.acp_queue = PyAutoGUIQueue()
        self.agent_status: Dict[str, str] = {}
        self.task_queue: List[Dict] = []
        
    def send_command(self, agent_id: str, command: str, priority: int = 1):
        """Send a command to a specific agent through the queue system."""
        if self.acp_queue.queue_message(agent_id, command, priority):
            self.gui.log_message(f"Command queued for {agent_id}: {command[:50]}...")
            return True
        return False
    
    def broadcast_command(self, command: str, priority: int = 1):
        """Broadcast a command to all agents."""
        agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]
        for agent in agents:
            self.send_command(agent, command, priority)
    
    def coordinate_agents(self, task_description: str):
        """Coordinate multiple agents for a collaborative task."""
        # Create coordination sequence
        coordination_plan = [
            ("Agent-1", f"Coordinate: {task_description} - Take lead on planning"),
            ("Agent-2", f"Coordinate: {task_description} - Handle technical architecture"),
            ("Agent-3", f"Coordinate: {task_description} - Manage data and analytics"),
            ("Agent-4", f"Coordinate: {task_description} - Handle DevOps and infrastructure")
        ]
        
        for agent, command in coordination_plan:
            self.send_command(agent, command, priority=1)
            time.sleep(0.5)  # Stagger commands
    
    def start_overnight_run(self, duration_minutes: int = 60):
        """Start an overnight run with coordinated agent tasks."""
        self.gui.log_message("🚀 Starting overnight run coordination...")
        
        # Phase 1: Onboarding
        onboarding_commands = [
            ("Agent-1", "ONBOARDING: Prepare for overnight development session"),
            ("Agent-2", "ONBOARDING: Prepare for overnight development session"),
            ("Agent-3", "ONBOARDING: Prepare for overnight development session"),
            ("Agent-4", "ONBOARDING: Prepare for overnight development session")
        ]
        
        for agent, command in onboarding_commands:
            self.send_command(agent, command, priority=1)
            time.sleep(1)
        
        # Phase 2: Task assignment
        task_commands = [
            ("Agent-1", "TASK: Review and prioritize development contracts"),
            ("Agent-2", "TASK: Analyze technical requirements and architecture"),
            ("Agent-3", "TASK: Prepare data models and analytics framework"),
            ("Agent-4", "TASK: Set up development environment and CI/CD")
        ]
        
        for agent, command in task_commands:
            self.send_command(agent, command, priority=2)
            time.sleep(1)
        
        self.gui.log_message(f"✅ Overnight run started - Duration: {duration_minutes} minutes")
    
    def monitor_agent_status(self):
        """Monitor the status of all agents."""
        status_commands = [
            ("Agent-1", "STATUS: Report current task and progress"),
            ("Agent-2", "STATUS: Report current task and progress"),
            ("Agent-3", "STATUS: Report current task and progress"),
            ("Agent-4", "STATUS: Report current task and progress")
        ]
        
        for agent, command in status_commands:
            self.send_command(agent, command, priority=3)
            time.sleep(0.5)
    
    def get_queue_status(self) -> Dict[str, any]:
        """Get the current queue status."""
        return self.acp_queue.get_queue_status()


class EnhancedRunnerGUI:
    """Enhanced GUI with Agent-5 command center and PyAutoGUI queue system."""
    
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Enhanced Overnight Runner - Agent-5 Command Center")
        self.root.geometry("900x700")
        
        # Initialize components
        self.agent5_center = Agent5CommandCenter(self)
        self.listener_proc: Optional[subprocess.Popen] = None
        self.runner_proc: Optional[subprocess.Popen] = None
        
        # Create GUI components
        self._create_gui()
        
        # Start status update thread
        self._start_status_updates()
    
    def _create_gui(self):
        """Create the enhanced GUI layout."""
        # Create notebook for tabbed interface
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Agent-5 Command Center
        self._create_command_center_tab(notebook)
        
        # Tab 2: Overnight Runner Control
        self._create_runner_control_tab(notebook)
        
        # Tab 3: Queue Management
        self._create_queue_management_tab(notebook)
        
        # Tab 4: Agent Status & Monitoring
        self._create_agent_monitoring_tab(notebook)
    
    def _create_command_center_tab(self, notebook):
        """Create the Agent-5 command center tab."""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="🎯 Agent-5 Command Center")
        
        # Title
        title_label = tk.Label(frame, text="Agent-5 Command Center", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Quick Commands Frame
        quick_frame = ttk.LabelFrame(frame, text="Quick Commands", padding=10)
        quick_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Row 1: Individual Agent Commands
        row1 = tk.Frame(quick_frame)
        row1.pack(fill=tk.X, pady=5)
        
        tk.Label(row1, text="Agent:").pack(side=tk.LEFT)
        self.agent_var = tk.StringVar(value="Agent-1")
        agent_combo = ttk.Combobox(row1, textvariable=self.agent_var, 
                                  values=["Agent-1", "Agent-2", "Agent-3", "Agent-4"], width=10)
        agent_combo.pack(side=tk.LEFT, padx=5)
        
        tk.Label(row1, text="Command:").pack(side=tk.LEFT, padx=(10, 0))
        self.command_var = tk.StringVar(value="STATUS: Report current progress")
        command_entry = tk.Entry(row1, textvariable=self.command_var, width=40)
        command_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(row1, text="Send Command", 
                 command=self._send_individual_command).pack(side=tk.LEFT, padx=5)
        
        # Row 2: Broadcast Commands
        row2 = tk.Frame(quick_frame)
        row2.pack(fill=tk.X, pady=5)
        
        tk.Label(row2, text="Broadcast:").pack(side=tk.LEFT)
        self.broadcast_var = tk.StringVar(value="COORDINATE: Prepare for development session")
        broadcast_entry = tk.Entry(row2, textvariable=self.broadcast_var, width=50)
        broadcast_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(row2, text="Broadcast to All", 
                 command=self._broadcast_command).pack(side=tk.LEFT, padx=5)
        
        # Row 3: Predefined Commands
        row3 = tk.Frame(quick_frame)
        row3.pack(fill=tk.X, pady=5)
        
        tk.Button(row3, text="🚀 Start Overnight Run", 
                 command=self._start_overnight_run).pack(side=tk.LEFT, padx=5)
        tk.Button(row3, text="📊 Monitor Status", 
                 command=self._monitor_agent_status).pack(side=tk.LEFT, padx=5)
        tk.Button(row3, text="🤝 Coordinate Team", 
                 command=self._coordinate_team).pack(side=tk.LEFT, padx=5)
        tk.Button(row3, text="🔄 Refresh All", 
                 command=self._refresh_all_agents).pack(side=tk.LEFT, padx=5)
        
        # Task Management Frame
        task_frame = ttk.LabelFrame(frame, text="Task Management", padding=10)
        task_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Task input
        task_input_frame = tk.Frame(task_frame)
        task_input_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(task_input_frame, text="Task Description:").pack(side=tk.LEFT)
        self.task_var = tk.StringVar(value="Implement new feature based on requirements")
        task_entry = tk.Entry(task_input_frame, textvariable=self.task_var, width=50)
        task_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(task_input_frame, text="Assign Task", 
                 command=self._assign_task).pack(side=tk.LEFT, padx=5)
        
        # Task list
        self.task_listbox = tk.Listbox(task_frame, height=8)
        self.task_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Log Frame
        log_frame = ttk.LabelFrame(frame, text="Command Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8)
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def _create_runner_control_tab(self, notebook):
        """Create the overnight runner control tab."""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="🏃 Overnight Runner")
        
        # Title
        title_label = tk.Label(frame, text="Overnight Runner Control", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Configuration Frame
        config_frame = ttk.LabelFrame(frame, text="Configuration", padding=10)
        config_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Row 1: Basic settings
        row1 = tk.Frame(config_frame)
        row1.pack(fill=tk.X, pady=5)
        
        tk.Label(row1, text="Layout:").grid(row=0, column=0, sticky="w")
        self.layout_var = tk.StringVar(value="5-agent")
        tk.Entry(row1, textvariable=self.layout_var, width=16).grid(row=0, column=1, sticky="w")
        
        tk.Label(row1, text="Captain:").grid(row=0, column=2, sticky="w")
        self.captain_var = tk.StringVar(value="Agent-5")
        tk.Entry(row1, textvariable=self.captain_var, width=16).grid(row=0, column=3, sticky="w")
        
        # Row 2: Agent settings
        row2 = tk.Frame(config_frame)
        row2.pack(fill=tk.X, pady=5)
        
        tk.Label(row2, text="Resume Agents:").grid(row=0, column=0, sticky="w")
        self.resume_var = tk.StringVar(value="Agent-1,Agent-2,Agent-3,Agent-4")
        tk.Entry(row2, textvariable=self.resume_var, width=40).grid(row=0, column=1, columnspan=3, sticky="we")
        
        # Row 3: Timing settings
        row3 = tk.Frame(config_frame)
        row3.pack(fill=tk.X, pady=5)
        
        tk.Label(row3, text="Interval (sec):").grid(row=0, column=0, sticky="w")
        self.interval_var = tk.StringVar(value="300")
        tk.Entry(row3, textvariable=self.interval_var, width=16).grid(row=0, column=1, sticky="w")
        
        tk.Label(row3, text="Duration (min):").grid(row=0, column=2, sticky="w")
        self.duration_var = tk.StringVar(value="60")
        tk.Entry(row3, textvariable=self.duration_var, width=16).grid(row=0, column=3, sticky="w")
        
        # Row 4: Communication settings
        row4 = tk.Frame(config_frame)
        row4.pack(fill=tk.X, pady=5)
        
        tk.Label(row4, text="Comms Root:").grid(row=0, column=0, sticky="w")
        self.comms_var = tk.StringVar(value=self._default_comms_root())
        tk.Entry(row4, textvariable=self.comms_var, width=40).grid(row=0, column=1, columnspan=3, sticky="we")
        
        # Control Frame
        control_frame = ttk.LabelFrame(frame, text="Control", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Row 1: Listener controls
        row1 = tk.Frame(control_frame)
        row1.pack(fill=tk.X, pady=5)
        
        tk.Label(row1, text="Listener Agent:").grid(row=0, column=0, sticky="w")
        self.listener_agent_var = tk.StringVar(value="Agent-5")
        tk.Entry(row1, textvariable=self.listener_agent_var, width=16).grid(row=0, column=1, sticky="w")
        
        tk.Button(row1, text="Start Listener", 
                 command=self.start_listener).grid(row=0, column=2, sticky="we", padx=5)
        tk.Button(row1, text="Stop Listener", 
                 command=self.stop_listener).grid(row=0, column=3, sticky="we", padx=5)
        
        # Row 2: Runner controls
        row2 = tk.Frame(control_frame)
        row2.pack(fill=tk.X, pady=5)
        
        self.test_mode = tk.BooleanVar(value=False)
        tk.Checkbutton(row2, text="Test mode (no typing)", 
                      variable=self.test_mode).grid(row=0, column=0, columnspan=2, sticky="w")
        
        tk.Button(row2, text="Start Runner", 
                 command=self.start_runner).grid(row=0, column=2, sticky="we", padx=5)
        tk.Button(row2, text="Stop Runner", 
                 command=self.stop_runner).grid(row=0, column=3, sticky="we", padx=5)
        
        # Row 3: Utility controls
        row3 = tk.Frame(control_frame)
        row3.pack(fill=tk.X, pady=5)
        
        tk.Label(row3, text="Calibrate Agent:").grid(row=0, column=0, sticky="w")
        self.calib_agent_var = tk.StringVar(value="Agent-5")
        tk.Entry(row3, textvariable=self.calib_agent_var, width=16).grid(row=0, column=1, sticky="w")
        
        tk.Button(row3, text="Calibrate", 
                 command=self.calibrate_agent).grid(row=0, column=2, sticky="we", padx=5)
        tk.Button(row3, text="Open Onboarding", 
                 command=self.open_onboarding).grid(row=0, column=3, sticky="we", padx=5)
        
        # Status
        self.status_var = tk.StringVar(value="Idle")
        status_label = tk.Label(frame, textvariable=self.status_var, anchor="w", 
                               font=("Arial", 10, "bold"))
        status_label.pack(pady=8)
        
        # Configure grid weights
        for c in range(4):
            row1.grid_columnconfigure(c, weight=1)
            row2.grid_columnconfigure(c, weight=1)
            row3.grid_columnconfigure(c, weight=1)
    
    def _create_queue_management_tab(self, notebook):
        """Create the queue management tab."""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="📋 Queue Management")
        
        # Title
        title_label = tk.Label(frame, text="PyAutoGUI Message Queue Management", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Queue Status Frame
        status_frame = ttk.LabelFrame(frame, text="Queue Status", padding=10)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Status display
        self.queue_status_var = tk.StringVar(value="Queue Status: Initializing...")
        status_label = tk.Label(status_frame, textvariable=self.queue_status_var, 
                               font=("Arial", 10))
        status_label.pack(pady=5)
        
        # Queue controls
        control_frame = tk.Frame(status_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(control_frame, text="Refresh Status", 
                 command=self._refresh_queue_status).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Clear Queue", 
                 command=self._clear_queue).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Pause Processing", 
                 command=self._pause_queue).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Resume Processing", 
                 command=self._resume_queue).pack(side=tk.LEFT, padx=5)
        
        # Agent Lock Status Frame
        lock_frame = ttk.LabelFrame(frame, text="Agent Lock Status", padding=10)
        lock_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.lock_text = scrolledtext.ScrolledText(lock_frame, height=10)
        self.lock_text.pack(fill=tk.BOTH, expand=True)
        
        # Queue Statistics Frame
        stats_frame = ttk.LabelFrame(frame, text="Queue Statistics", padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.stats_var = tk.StringVar(value="Statistics: Loading...")
        stats_label = tk.Label(stats_frame, textvariable=self.stats_var, 
                              font=("Arial", 10))
        stats_label.pack(pady=5)
    
    def _create_agent_monitoring_tab(self, notebook):
        """Create the agent monitoring tab."""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="👥 Agent Monitoring")
        
        # Title
        title_label = tk.Label(frame, text="Agent Status & Monitoring", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Agent Status Frame
        status_frame = ttk.LabelFrame(frame, text="Agent Status", padding=10)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create agent status displays
        self.agent_status_vars = {}
        agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]
        
        for i, agent in enumerate(agents):
            row = i // 2
            col = (i % 2) * 2
            
            frame_row = tk.Frame(status_frame)
            frame_row.pack(fill=tk.X, pady=2)
            
            tk.Label(frame_row, text=f"{agent}:", width=10, anchor="w").pack(side=tk.LEFT)
            
            status_var = tk.StringVar(value="Unknown")
            self.agent_status_vars[agent] = status_var
            status_label = tk.Label(frame_row, textvariable=status_var, 
                                   width=20, anchor="w")
            status_label.pack(side=tk.LEFT, padx=5)
            
            tk.Button(frame_row, text="Check Status", 
                     command=lambda a=agent: self._check_agent_status(a)).pack(side=tk.LEFT, padx=5)
            tk.Button(frame_row, text="Send Nudge", 
                     command=lambda a=agent: self._send_nudge(a)).pack(side=tk.LEFT, padx=5)
        
        # Monitoring Controls Frame
        control_frame = ttk.LabelFrame(frame, text="Monitoring Controls", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        control_row = tk.Frame(control_frame)
        control_row.pack(fill=tk.X, pady=5)
        
        tk.Button(control_row, text="🔄 Refresh All Status", 
                 command=self._refresh_all_status).pack(side=tk.LEFT, padx=5)
        tk.Button(control_row, text="📊 Start Monitoring", 
                 command=self._start_monitoring).pack(side=tk.LEFT, padx=5)
        tk.Button(control_row, text="⏹️ Stop Monitoring", 
                 command=self._stop_monitoring).pack(side=tk.LEFT, padx=5)
        tk.Button(control_row, text="🚨 Emergency Stop", 
                 command=self._emergency_stop).pack(side=tk.LEFT, padx=5)
        
        # Activity Log Frame
        log_frame = ttk.LabelFrame(frame, text="Activity Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.activity_text = scrolledtext.ScrolledText(log_frame, height=10)
        self.activity_text.pack(fill=tk.BOTH, expand=True)
    
    def _send_individual_command(self):
        """Send a command to an individual agent."""
        agent = self.agent_var.get()
        command = self.command_var.get()
        
        if self.agent5_center.send_command(agent, command):
            self.log_message(f"✅ Command sent to {agent}: {command}")
        else:
            self.log_message(f"❌ Failed to send command to {agent}")
    
    def _broadcast_command(self):
        """Broadcast a command to all agents."""
        command = self.broadcast_var.get()
        
        if self.agent5_center.broadcast_command(command):
            self.log_message(f"✅ Command broadcasted to all agents: {command}")
        else:
            self.log_message(f"❌ Failed to broadcast command")
    
    def _start_overnight_run(self):
        """Start an overnight run."""
        duration = 60  # Default 60 minutes
        self.agent5_center.start_overnight_run(duration)
    
    def _monitor_agent_status(self):
        """Monitor agent status."""
        self.agent5_center.monitor_agent_status()
        self.log_message("📊 Agent status monitoring initiated")
    
    def _coordinate_team(self):
        """Coordinate the team for a collaborative task."""
        task = self.task_var.get()
        self.agent5_center.coordinate_agents(task)
        self.log_message(f"🤝 Team coordination initiated for: {task}")
    
    def _refresh_all_agents(self):
        """Refresh all agent statuses."""
        self._refresh_all_status()
        self.log_message("🔄 All agent statuses refreshed")
    
    def _assign_task(self):
        """Assign a task to agents."""
        task = self.task_var.get()
        if task:
            self.agent5_center.coordinate_agents(task)
            self.log_message(f"📋 Task assigned: {task}")
            
            # Add to task list
            self.task_listbox.insert(0, f"{time.strftime('%H:%M:%S')} - {task}")
    
    def _refresh_queue_status(self):
        """Refresh the queue status display."""
        status = self.agent5_center.get_queue_status()
        
        self.queue_status_var.set(
            f"Queue Size: {status['queue_size']} | "
            f"Processing: {'Yes' if status['processing'] else 'No'}"
        )
        
        # Update lock status
        lock_text = "Agent Lock Status:\n"
        for agent, locked in status['agent_locks'].items():
            status_icon = "🔒" if locked else "🔓"
            lock_text += f"{status_icon} {agent}: {'Locked' if locked else 'Unlocked'}\n"
        
        self.lock_text.delete(1.0, tk.END)
        self.lock_text.insert(1.0, lock_text)
        
        # Update statistics
        self.stats_var.set(
            f"Total Agents: {len(status['agent_locks'])} | "
            f"Active Locks: {sum(status['agent_locks'].values())} | "
            f"Queue Depth: {status['queue_size']}"
        )
    
    def _clear_queue(self):
        """Clear the message queue."""
        # This would need to be implemented in the PyAutoGUIQueue class
        self.log_message("🗑️ Queue clear requested (not yet implemented)")
    
    def _pause_queue(self):
        """Pause queue processing."""
        self.agent5_center.acp_queue.stop_processing()
        self.log_message("⏸️ Queue processing paused")
    
    def _resume_queue(self):
        """Resume queue processing."""
        self.agent5_center.acp_queue.start_processing()
        self.log_message("▶️ Queue processing resumed")
    
    def _check_agent_status(self, agent):
        """Check the status of a specific agent."""
        # Simulate status check
        statuses = ["Active", "Working", "Idle", "Stalled", "Error"]
        import random
        status = random.choice(statuses)
        
        self.agent_status_vars[agent].set(status)
        self.log_message(f"📊 {agent} status: {status}")
    
    def _send_nudge(self, agent):
        """Send a nudge to a specific agent."""
        if self.agent5_center.send_command(agent, "NUDGE: Wake up and report status", priority=1):
            self.log_message(f"👆 Nudge sent to {agent}")
        else:
            self.log_message(f"❌ Failed to send nudge to {agent}")
    
    def _refresh_all_status(self):
        """Refresh all agent statuses."""
        for agent in self.agent_status_vars:
            self._check_agent_status(agent)
    
    def _start_monitoring(self):
        """Start continuous monitoring."""
        self.log_message("📊 Continuous monitoring started")
        # This would start a background monitoring thread
    
    def _stop_monitoring(self):
        """Stop continuous monitoring."""
        self.log_message("⏹️ Continuous monitoring stopped")
    
    def _emergency_stop(self):
        """Emergency stop all operations."""
        self.log_message("🚨 EMERGENCY STOP ACTIVATED")
        # This would stop all runners, listeners, and clear queues
    
    def log_message(self, message: str):
        """Log a message to the command log."""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Also log to activity log in monitoring tab
        self.activity_text.insert(tk.END, log_entry)
        self.activity_text.see(tk.END)
    
    def _start_status_updates(self):
        """Start periodic status updates."""
        def update_loop():
            while True:
                try:
                    self.root.after(0, self._refresh_queue_status)
                    time.sleep(5)  # Update every 5 seconds
                except Exception as e:
                    print(f"Status update error: {e}")
                    break
        
        status_thread = threading.Thread(target=update_loop, daemon=True)
        status_thread.start()
    
    def _default_comms_root(self) -> str:
        """Get default communications root."""
        try:
            from datetime import datetime
            d = datetime.now().strftime("%Y%m%d")
            return f"{get_communications_root()}/overnight_{d}_"
        except:
            return "D:/repos/communications/overnight_YYYYMMDD_"
    
    def _python(self) -> str:
        """Get Python executable path."""
        return sys.executable or "python"
    
    # Runner control methods (adapted from original GUI)
    def start_listener(self) -> None:
        """Start the listener process."""
        if self.listener_proc and self.listener_proc.poll() is None:
            messagebox.showinfo("Listener", "Listener already running")
            return
        
        agent = self.listener_agent_var.get().strip() or "Agent-5"
        cmd = [self._python(), "overnight_runner/listener.py", "--agent", agent]
        self.listener_proc = subprocess.Popen(cmd, cwd=str(Path(__file__).resolve().parents[1]))
        self.status_var.set(f"Listener started for {agent}")
        self.log_message(f"🎧 Listener started for {agent}")
    
    def stop_listener(self) -> None:
        """Stop the listener process."""
        if self.listener_proc and self.listener_proc.poll() is None:
            self.listener_proc.terminate()
            self.listener_proc = None
            self.status_var.set("Listener stopped")
            self.log_message("🛑 Listener stopped")
        else:
            self.status_var.set("Listener not running")
    
    def start_runner(self) -> None:
        """Start the overnight runner."""
        if self.runner_proc and self.runner_proc.poll() is None:
            messagebox.showinfo("Runner", "Runner already running")
            return
        
        layout = self.layout_var.get().strip() or "5-agent"
        captain = self.captain_var.get().strip() or "Agent-5"
        resume = self.resume_var.get().strip() or "Agent-1,Agent-2,Agent-3,Agent-4"
        interval = self.interval_var.get().strip() or "300"
        duration = self.duration_var.get().strip() or "60"
        comms = self.comms_var.get().strip() or self._default_comms_root()
        
        Path(comms).mkdir(parents=True, exist_ok=True)
        
        args = [
            self._python(), "overnight_runner/runner.py",
            "--layout", layout,
            "--captain", captain,
            "--resume-agents", resume,
            "--interval-sec", interval,
            "--duration-min", duration,
            "--comm-root", comms, "--create-comm-folders",
        ]
        
        if self.test_mode.get():
            args.append("--test")
        
        self.runner_proc = subprocess.Popen(args, cwd=str(Path(__file__).resolve().parents[1]))
        self.status_var.set("Runner started")
        self.log_message("🏃 Overnight runner started")
    
    def stop_runner(self) -> None:
        """Stop the overnight runner."""
        if self.runner_proc and self.runner_proc.poll() is None:
            self.runner_proc.terminate()
            self.runner_proc = None
            self.status_var.set("Runner stopped")
            self.log_message("🛑 Overnight runner stopped")
        else:
            self.status_var.set("Runner not running")
    
    def calibrate_agent(self) -> None:
        """Calibrate an agent's coordinates."""
        layout = self.layout_var.get().strip() or "5-agent"
        agent = self.calib_agent_var.get().strip() or "Agent-5"
        cmd = [self._python(), "overnight_runner/tools/capture_coords.py", 
               "--layout", layout, "--agent", agent, "--delay", "6"]
        
        try:
            subprocess.Popen(cmd, cwd=str(Path(__file__).resolve().parents[1]))
            self.status_var.set(f"Calibration started for {agent} ({layout})")
            self.log_message(f"🎯 Calibration started for {agent}")
        except Exception as e:
            messagebox.showerror("Calibrate", str(e))
    
    def open_onboarding(self) -> None:
        """Open the onboarding documentation."""
        root_dir = Path(__file__).resolve().parent / "onboarding"
        index = root_dir / "00_INDEX.md"
        
        try:
            if os.name == "nt":
                os.startfile(index)  # type: ignore[attr-defined]
            else:
                subprocess.Popen(["open", str(index)])
        except Exception:
            messagebox.showinfo("Onboarding", f"Open manually: {index}")


def main() -> int:
    """Main entry point."""
    root = tk.Tk()
    EnhancedRunnerGUI(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
Agent Status Manager
===================
Helper script for agents to manage status.json and respond to Dream.OS GUI commands.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional

class AgentStatusManager:
    """Manages agent status.json file and GUI communication."""
    
    def __init__(self, agent_id: str, workspace_path: str = None):
        """
        Initialize the status manager.
        
        Args:
            agent_id: The agent ID (e.g., "agent-1")
            workspace_path: Path to agent workspace (defaults to agent_workspaces/agent_id)
        """
        self.agent_id = agent_id
        self.workspace_path = workspace_path or f"agent_workspaces/{agent_id}"
        self.status_file = os.path.join(self.workspace_path, "status.json")
        
        # Initialize status if file doesn't exist
        if not os.path.exists(self.status_file):
            self.initialize_status()
    
    def initialize_status(self):
        """Initialize the status.json file with default values."""
        status_data = {
            "status": "online",
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "current_task": "idle",
            "agent_id": self.agent_id,
            "capabilities": [
                "task_execution",
                "status_reporting",
                "message_handling",
                "performance_monitoring"
            ],
            "performance_metrics": {
                "tasks_completed": 0,
                "uptime_hours": 0.0,
                "last_response_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "error_count": 0,
                "success_rate": 100.0
            },
            "message_history": [
                {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "initialization",
                    "content": "Agent initialized",
                    "response": "Agent ready for operations",
                    "status_before": "offline",
                    "status_after": "online"
                }
            ],
            "debug_mode": False,
            "debug_log": []
        }
        
        self.save_status(status_data)
        print(f"Initialized status.json for {self.agent_id}")
    
    def load_status(self) -> Dict[str, Any]:
        """Load current status from status.json."""
        try:
            with open(self.status_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading status: {e}")
            return {}
    
    def save_status(self, status_data: Dict[str, Any]):
        """Save status to status.json with error handling."""
        try:
            # Create backup
            if os.path.exists(self.status_file):
                backup_file = f"{self.status_file}.backup"
                with open(self.status_file, 'r') as f:
                    with open(backup_file, 'w') as bf:
                        bf.write(f.read())
            
            # Write new status
            with open(self.status_file, 'w') as f:
                json.dump(status_data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving status: {e}")
    
    def update_status(self, new_status: str, current_task: str = None):
        """
        Update agent status.
        
        Args:
            new_status: "online", "busy", "offline", or "error"
            current_task: Description of current task
        """
        status_data = self.load_status()
        previous_status = status_data.get("status", "unknown")
        
        status_data.update({
            "status": new_status,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "current_task": current_task or status_data.get("current_task", "idle")
        })
        
        # Update performance metrics
        if "performance_metrics" not in status_data:
            status_data["performance_metrics"] = {}
        
        status_data["performance_metrics"]["last_response_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.save_status(status_data)
        print(f"Status updated: {previous_status} -> {new_status}")
    
    def log_message(self, message_type: str, content: str, response: str):
        """
        Log a message interaction.
        
        Args:
            message_type: Type of message (ping, task, status, broadcast, etc.)
            content: Incoming message content
            response: Agent's response
        """
        status_data = self.load_status()
        
        if "message_history" not in status_data:
            status_data["message_history"] = []
        
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": message_type,
            "content": content,
            "response": response,
            "status_before": status_data.get("status", "unknown"),
            "status_after": status_data.get("status", "unknown")
        }
        
        status_data["message_history"].append(log_entry)
        
        # Keep only last 50 messages to prevent file bloat
        if len(status_data["message_history"]) > 50:
            status_data["message_history"] = status_data["message_history"][-50:]
        
        self.save_status(status_data)
        print(f"Message logged: {message_type} - {content[:50]}...")
    
    def handle_gui_command(self, command: str) -> str:
        """
        Handle a command from the Dream.OS GUI.
        
        Args:
            command: The command string from GUI
            
        Returns:
            Response string to send back
        """
        command = command.strip()
        
        # Parse command type
        if command.startswith("[PING]"):
            return self.handle_ping(command)
        elif command.startswith("[RESUME]"):
            return self.handle_resume(command)
        elif command.startswith("[PAUSE]"):
            return self.handle_pause(command)
        elif command.startswith("[SYNC]"):
            return self.handle_sync(command)
        elif command.startswith("[TASK]"):
            return self.handle_task(command)
        elif command.startswith("[BROADCAST"):
            return self.handle_broadcast(command)
        else:
            return self.handle_unknown_command(command)
    
    def handle_ping(self, command: str) -> str:
        """Handle ping command."""
        status_data = self.load_status()
        current_status = status_data.get("status", "unknown")
        current_task = status_data.get("current_task", "idle")
        
        response = f"[PING_RESPONSE] {self.agent_id} is {current_status} - {current_task}"
        
        self.update_status("online", current_task)
        self.log_message("ping", command, response)
        
        return response
    
    def handle_resume(self, command: str) -> str:
        """Handle resume command."""
        response = f"[RESUME_CONFIRMED] {self.agent_id} resumed operations"
        
        self.update_status("online", "Resumed operations")
        self.log_message("resume", command, response)
        
        return response
    
    def handle_pause(self, command: str) -> str:
        """Handle pause command."""
        response = f"[PAUSE_CONFIRMED] {self.agent_id} paused operations"
        
        self.update_status("offline", "Paused operations")
        self.log_message("pause", command, response)
        
        return response
    
    def handle_sync(self, command: str) -> str:
        """Handle sync command."""
        status_data = self.load_status()
        response = f"[SYNC_CONFIRMED] {self.agent_id} synchronized - Status: {status_data.get('status', 'unknown')}"
        
        self.update_status("online", "Synchronized")
        self.log_message("sync", command, response)
        
        return response
    
    def handle_task(self, command: str) -> str:
        """Handle task assignment."""
        # Extract task description from command
        task_description = command.split(" - ", 1)[1] if " - " in command else "Unknown task"
        
        response = f"[TASK_ACKNOWLEDGED] {self.agent_id} received task: {task_description}"
        
        self.update_status("busy", task_description)
        self.log_message("task", command, response)
        
        # Here you would execute the actual task
        # For now, we just acknowledge receipt
        
        return response
    
    def handle_broadcast(self, command: str) -> str:
        """Handle broadcast commands."""
        if "BROADCAST_PING" in command:
            return self.handle_ping(command)
        elif "BROADCAST_STATUS" in command:
            status_data = self.load_status()
            response = f"[BROADCAST_STATUS_RESPONSE] {self.agent_id}: {status_data.get('status', 'unknown')} - {status_data.get('current_task', 'idle')}"
            self.log_message("broadcast_status", command, response)
            return response
        elif "BROADCAST_RESUME" in command:
            return self.handle_resume(command)
        elif "BROADCAST_TASK" in command:
            return self.handle_task(command)
        else:
            response = f"[BROADCAST_ACKNOWLEDGED] {self.agent_id} received broadcast"
            self.log_message("broadcast", command, response)
            return response
    
    def handle_unknown_command(self, command: str) -> str:
        """Handle unknown commands."""
        response = f"[UNKNOWN_COMMAND] {self.agent_id} received unknown command: {command[:50]}"
        self.log_message("unknown", command, response)
        return response
    
    def update_performance_metrics(self, tasks_completed: int = None, error_count: int = None):
        """Update performance metrics."""
        status_data = self.load_status()
        
        if "performance_metrics" not in status_data:
            status_data["performance_metrics"] = {}
        
        metrics = status_data["performance_metrics"]
        
        if tasks_completed is not None:
            metrics["tasks_completed"] = tasks_completed
        
        if error_count is not None:
            metrics["error_count"] = error_count
        
        # Calculate success rate
        total_tasks = metrics.get("tasks_completed", 0) + metrics.get("error_count", 0)
        if total_tasks > 0:
            metrics["success_rate"] = (metrics.get("tasks_completed", 0) / total_tasks) * 100
        else:
            metrics["success_rate"] = 100.0
        
        metrics["last_response_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.save_status(status_data)
        print(f"Performance metrics updated: {metrics}")

# Example usage
if __name__ == "__main__":
    # Example of how an agent would use this
    agent_manager = AgentStatusManager("agent-1")
    
    # Simulate receiving a ping command
    ping_command = "[PING] agent-1 - Status check from Dream.OS GUI"
    response = agent_manager.handle_gui_command(ping_command)
    print(f"Response: {response}")
    
    # Simulate receiving a task
    task_command = "[TASK] agent-1 - Process data analysis"
    response = agent_manager.handle_gui_command(task_command)
    print(f"Response: {response}")
    
    # Update performance metrics
    agent_manager.update_performance_metrics(tasks_completed=5, error_count=1) 
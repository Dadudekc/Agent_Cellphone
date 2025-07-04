#!/usr/bin/env python3
"""
Base GUI Controller
==================
Shared GUI functionality and utilities to eliminate code duplication
across different GUI implementations.
"""

import os
import json
import threading
import time
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any
from abc import ABC, abstractmethod

try:
    from PyQt5.QtWidgets import (QTextEdit, QFileDialog, QMessageBox, 
                                QInputDialog, QApplication)
    from PyQt5.QtCore import QTimer
    from PyQt5.QtGui import QFont
except ImportError:
    print("PyQt5 not available. Please install: pip install PyQt5")
    raise

class BaseGUIController(ABC):
    """
    Base class for GUI controllers that provides shared functionality
    to eliminate code duplication across different GUI implementations.
    """
    
    def __init__(self, coordinate_finder=None, framework=None):
        """
        Initialize the base GUI controller.
        
        Args:
            coordinate_finder: Coordinate finder instance
            framework: Agent autonomy framework instance
        """
        self.coordinate_finder = coordinate_finder
        self.framework = framework
        self.selected_agents = []
        self.log_display = None
        self.status_timer = None
        self.agent_widgets = {}
        
    # ============================================================================
    # LOGGING METHODS (Shared across all GUIs)
    # ============================================================================
    
    def log_message(self, sender: str, message: str):
        """Add a message to the log display."""
        if not self.log_display:
            return
            
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {sender}: {message}"
        self.log_display.append(log_entry)
        
        # Auto-scroll to bottom
        scrollbar = self.log_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear_log(self):
        """Clear the log display."""
        if not self.log_display:
            return
            
        self.log_display.clear()
        self.log_message("System", "Log cleared")
    
    def save_log(self):
        """Save the log to a file."""
        if not self.log_display:
            return
            
        filename, _ = QFileDialog.getSaveFileName(
            None, "Save Log", "", "Text Files (*.txt);;All Files (*)"
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.log_display.toPlainText())
                self.log_message("System", f"Log saved to {filename}")
            except Exception as e:
                self.log_message("Error", f"Failed to save log: {e}")
    
    # ============================================================================
    # AGENT SELECTION METHODS (Shared across all GUIs)
    # ============================================================================
    
    def select_all_agents(self):
        """Select all available agents."""
        self.selected_agents = list(self.agent_widgets.keys())
        self.log_message("Selection", f"Selected all {len(self.selected_agents)} agents")
    
    def clear_selection(self):
        """Clear agent selection."""
        self.selected_agents = []
        self.log_message("Selection", "Cleared agent selection")
    
    def get_available_agents(self) -> List[str]:
        """Get list of available agent IDs."""
        return list(self.agent_widgets.keys())
    
    # ============================================================================
    # GENERIC ACTION METHODS (Consolidates duplicate patterns)
    # ============================================================================
    
    def execute_selected_agents_action(self, action_type: str, action_name: str, 
                                     action_func: callable = None):
        """
        Generic method to execute actions on selected agents.
        Replaces the 6 duplicate methods in dream_os_gui_v2.py.
        
        Args:
            action_type: Type of action (e.g., "ping", "status", "resume")
            action_name: Display name for the action
            action_func: Optional custom function to execute for each agent
        """
        if not self.selected_agents:
            self.log_message("Warning", f"No agents selected for {action_name}")
            return
        
        for agent_id in self.selected_agents:
            self.log_message(action_name.title(), f"{action_name.title()}ing {agent_id}...")
            
            if action_func:
                try:
                    action_func(agent_id)
                except Exception as e:
                    self.log_message("Error", f"Failed to {action_name} {agent_id}: {e}")
            else:
                # Default implementation - can be overridden
                self._default_agent_action(agent_id, action_type)
    
    def _default_agent_action(self, agent_id: str, action_type: str):
        """Default implementation for agent actions."""
        # This can be overridden by subclasses for specific behavior
        pass
    
    # Convenience methods that use the generic action method
    def ping_selected_agents(self):
        """Ping selected agents."""
        self.execute_selected_agents_action("ping", "ping")
    
    def get_status_selected_agents(self):
        """Get status of selected agents."""
        self.execute_selected_agents_action("status", "status check")
    
    def resume_selected_agents(self):
        """Resume selected agents."""
        self.execute_selected_agents_action("resume", "resume")
    
    def pause_selected_agents(self):
        """Pause selected agents."""
        self.execute_selected_agents_action("pause", "pause")
    
    def sync_selected_agents(self):
        """Sync selected agents."""
        self.execute_selected_agents_action("sync", "sync")
    
    def assign_task_selected_agents(self):
        """Assign task to selected agents."""
        self.execute_selected_agents_action("task", "task assignment")
    
    # ============================================================================
    # BROADCAST METHODS (Consolidates duplicate patterns)
    # ============================================================================
    
    def broadcast_action(self, action_type: str, action_name: str, 
                        default_command: str = None, action_func: callable = None):
        """
        Generic method to broadcast actions to all agents.
        Replaces the 5 duplicate broadcast methods in dream_os_gui_v2.py.
        
        Args:
            action_type: Type of broadcast action
            action_name: Display name for the action
            default_command: Default command to use if no custom function
            action_func: Optional custom function to execute
        """
        if action_func:
            try:
                action_func()
            except Exception as e:
                self.log_message("Error", f"Broadcast {action_name} failed: {e}")
        else:
            self.log_message("Broadcast", f"Broadcasting {action_name} to all agents...")
            # Default implementation - can be overridden
            self._default_broadcast_action(action_type, default_command)
    
    def _default_broadcast_action(self, action_type: str, default_command: str = None):
        """Default implementation for broadcast actions."""
        # This can be overridden by subclasses for specific behavior
        pass
    
    # Convenience methods that use the generic broadcast method
    def broadcast_message(self):
        """Broadcast message to all agents."""
        self.broadcast_action("message", "message")
    
    def broadcast_ping(self):
        """Broadcast ping to all agents."""
        self.broadcast_action("ping", "ping", "ping")
    
    def broadcast_status(self):
        """Broadcast status request to all agents."""
        self.broadcast_action("status", "status request", "status")
    
    def broadcast_resume(self):
        """Broadcast resume command to all agents."""
        self.broadcast_action("resume", "resume command", "resume")
    
    def broadcast_task(self):
        """Broadcast task to all agents."""
        self.broadcast_action("task", "task", "task")
    
    # ============================================================================
    # STATUS UPDATE METHODS (Shared across all GUIs)
    # ============================================================================
    
    def setup_status_updates(self, update_interval: int = 5000):
        """Setup periodic status updates."""
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_agent_statuses)
        self.status_timer.start(update_interval)  # Update every 5 seconds by default
        
        # Initial log message
        self.log_message("System", "GUI Controller initialized")
    
    def update_agent_statuses(self):
        """Update agent statuses periodically."""
        # This should be implemented by subclasses based on their specific needs
        pass
    
    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get status for a specific agent."""
        try:
            status_file = os.path.join("agent_workspaces", agent_id, "status.json")
            if os.path.exists(status_file):
                with open(status_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.log_message("Error", f"Failed to get {agent_id} status: {e}")
        return {"status": "unknown", "current_task": "idle", "last_update": "unknown"}
    
    # ============================================================================
    # UTILITY METHODS (Shared across all GUIs)
    # ============================================================================
    
    def send_message_to_agents(self, message: str, agent_ids: List[str] = None):
        """
        Send a message to specified agents or all agents if none specified.
        
        Args:
            message: Message to send
            agent_ids: List of agent IDs to send to (None for all)
        """
        if agent_ids is None:
            agent_ids = self.get_available_agents()
        
        if not message.strip():
            self.log_message("Message", "Empty message, not sending")
            return
        
        self.log_message("Message", f"Sending message: {message}")
        
        for agent_id in agent_ids:
            try:
                if self.coordinate_finder:
                    coords = self.coordinate_finder.get_coordinates(agent_id)
                    if coords:
                        x, y = coords
                        # Note: This requires pyautogui - subclasses should implement
                        self._send_message_via_coordinates(agent_id, message, x, y)
                    else:
                        self.log_message("Error", f"No coordinates found for {agent_id}")
                else:
                    self._send_message_via_framework(agent_id, message)
            except Exception as e:
                self.log_message("Error", f"Failed to send message to {agent_id}: {e}")
    
    def _send_message_via_coordinates(self, agent_id: str, message: str, x: int, y: int):
        """Send message using coordinates (requires pyautogui)."""
        # This should be implemented by subclasses that use coordinate-based messaging
        pass
    
    def _send_message_via_framework(self, agent_id: str, message: str):
        """Send message using the framework."""
        # This should be implemented by subclasses that use framework-based messaging
        pass
    
    def test_coordinates(self):
        """Test agent coordinates."""
        if not self.coordinate_finder:
            self.log_message("Error", "Coordinate finder not available")
            return
            
        self.log_message("System", "Testing coordinates...")
        for agent_id in self.get_available_agents():
            coords = self.coordinate_finder.get_coordinates(agent_id)
            if coords:
                x, y = coords
                self.log_message("System", f"{agent_id}: Coordinates ({x}, {y})")
            else:
                self.log_message("System", f"{agent_id}: No coordinates found")
        self.log_message("System", "Coordinate test completed")
    
    # ============================================================================
    # ABSTRACT METHODS (Must be implemented by subclasses)
    # ============================================================================
    
    @abstractmethod
    def init_ui(self):
        """Initialize the user interface."""
        pass
    
    @abstractmethod
    def create_agent_widgets(self):
        """Create agent-specific widgets."""
        pass 
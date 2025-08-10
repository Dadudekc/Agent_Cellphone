#!/usr/bin/env python3
"""Messaging utilities used by the GUI.

This module previously talked directly to :mod:`agent_cell_phone` but has
been refactored to use service abstractions.  A service instance is
injected into :class:`MessagingUtils` allowing different implementations
to be swapped (e.g. local in‑process or remote API backed).
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from services.agent_service import AgentService, LocalAgentService


class MessagingUtils:
    """Utility class for agent messaging operations."""

    def __init__(
        self,
        service: Optional[AgentService] = None,
        layout_mode: str = "8-agent",
        test_mode: bool = True,
    ) -> None:
        """Initialize messaging utilities."""

        self.layout_mode = layout_mode
        self.test_mode = test_mode
        # Allow dependency injection of a service implementation
        self.service: AgentService = service or LocalAgentService(
            layout_mode=layout_mode, test_mode=test_mode
        )
    
    def get_available_agents(self) -> List[str]:
        """Get list of available agents"""
        return self.service.get_available_agents()
    
    def get_available_commands(self) -> List[str]:
        """Get list of available commands"""
        return [
            "ping", "status", "resume", "sync", "verify", 
            "task", "captain", "repair", "backup", "restore"
        ]
    
    def get_available_tags(self) -> List[str]:
        """Get list of available message tags"""
        return [
            "NORMAL",
            "RESUME",
            "SYNC",
            "VERIFY",
            "REPAIR",
            "BACKUP",
            "RESTORE",
            "CLEANUP",
            "CAPTAIN",
            "TASK",
            "INTEGRATE",
            "REPLY",
            "COORDINATE",
            "ONBOARDING",
            "COMMAND",
        ]
    
    def send_message(self, target: str, message: str, tag: str = "NORMAL") -> Tuple[bool, str]:
        """Send a message to a specific agent"""
        try:
            available = self.get_available_agents()
            if target not in available and target != "all":
                return False, f"Invalid target: {target}"
            return self.service.send_message(target, message, tag)
        except Exception as e:
            return False, f"Error sending message: {e}"
    
    def send_command(self, target: str, command: str, args: List[str] = None) -> Tuple[bool, str]:
        """Send a command to a specific agent"""
        try:
            available = self.get_available_agents()
            if target not in available and target != "all":
                return False, f"Invalid target: {target}"
            if command not in self.get_available_commands():
                return False, f"Invalid command: {command}"
            return self.service.send_command(target, command, args)
        except Exception as e:
            return False, f"Error sending command: {e}"
    
    def ping_agent(self, target: str) -> Tuple[bool, str]:
        """Ping a specific agent"""
        return self.send_command(target, "ping")
    
    def get_agent_status(self, target: str) -> Tuple[bool, str]:
        """Get status of a specific agent"""
        return self.send_command(target, "status")
    
    def resume_agent(self, target: str) -> Tuple[bool, str]:
        """Resume operations for a specific agent"""
        return self.send_command(target, "resume")
    
    def sync_agent(self, target: str) -> Tuple[bool, str]:
        """Sync data for a specific agent"""
        return self.send_command(target, "sync")
    
    def verify_agent(self, target: str) -> Tuple[bool, str]:
        """Verify a specific agent"""
        return self.send_command(target, "verify")
    
    def assign_task(self, target: str, task_description: str) -> Tuple[bool, str]:
        """Assign a task to a specific agent"""
        return self.send_command(target, "task", ["assign", task_description])
    
    def broadcast_captain_message(self, message: str) -> Tuple[bool, str]:
        """Send a captain message to all agents"""
        return self.send_message("all", message, "CAPTAIN")
    
    def get_system_status(self) -> Dict:
        """Get overall system status"""
        try:
            status = self.service.get_system_status()
            status["timestamp"] = datetime.now().isoformat()
            return status
        except Exception as e:
            return {"error": f"Error getting system status: {e}"}
    
    def test_connectivity(self) -> Dict:
        """Test connectivity to all agents"""
        results = {}
        agents = self.get_available_agents()
        
        for agent in agents:
            success, message = self.ping_agent(agent)
            results[agent] = {
                "success": success,
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
        
        return results
    
    def get_message_history(self) -> List[Dict]:
        """Get message history (placeholder for future implementation)"""
        # This would integrate with a logging system
        return []
    
    def validate_message(self, message: str) -> Tuple[bool, str]:
        """Validate message format and content"""
        if not message or not message.strip():
            return False, "Message cannot be empty"
        
        if len(message) > 1000:
            return False, "Message too long (max 1000 characters)"
        
        return True, "Message is valid"
    
    def validate_target(self, target: str) -> Tuple[bool, str]:
        """Validate target agent"""
        available_agents = self.get_available_agents()

        if target == "all":
            return True, "Valid target"

        if target in available_agents:
            return True, "Valid target"

        return False, f"Invalid target. Available: {', '.join(available_agents)}"
    
    # Legacy helper functions that required direct access to AgentCellPhone
    # have been removed to keep this utility focused on service-driven
    # messaging.  Additional functionality can be implemented via the
    # injected service as needed.
#!/usr/bin/env python3
"""
Messaging Utilities for Dream.OS GUI
Provides messaging functionality extracted from agent_messenger.py
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

try:
    from agent_cell_phone import AgentCellPhone, MsgTag
except ImportError:
    print("Warning: agent_cell_phone module not found")

class MessagingUtils:
    """Utility class for agent messaging operations"""
    
    def __init__(self, layout_mode: str = "8-agent", test_mode: bool = True):
        """Initialize messaging utilities"""
        self.layout_mode = layout_mode
        self.test_mode = test_mode
        self.acp = None
        self.initialize_agent_cell_phone()
    
    def initialize_agent_cell_phone(self):
        """Initialize the AgentCellPhone instance"""
        try:
            self.acp = AgentCellPhone(layout_mode=self.layout_mode, test=self.test_mode)
            return True
        except Exception as e:
            print(f"Error initializing AgentCellPhone: {e}")
            return False
    
    def get_available_agents(self) -> List[str]:
        """Get list of available agents"""
        if self.acp:
            return self.acp.get_available_agents()
        return []
    
    def get_available_commands(self) -> List[str]:
        """Get list of available commands"""
        return [
            "ping", "status", "resume", "sync", "verify", 
            "task", "captain", "repair", "backup", "restore"
        ]
    
    def get_available_tags(self) -> List[str]:
        """Get list of available message tags"""
        return [tag.name for tag in MsgTag]
    
    def send_message(self, target: str, message: str, tag: str = "NORMAL") -> Tuple[bool, str]:
        """Send a message to a specific agent"""
        try:
            if not self.acp:
                return False, "AgentCellPhone not initialized"
            
            # Validate target
            if target not in self.get_available_agents() and target != "all":
                return False, f"Invalid target: {target}"
            
            # Get message tag
            try:
                msg_tag = MsgTag[tag.upper()]
            except KeyError:
                msg_tag = MsgTag.NORMAL
            
            # Send message
            if target == "all":
                self.acp.broadcast(message, msg_tag)
                return True, f"Message broadcast to all agents"
            else:
                self.acp.send(target, message, msg_tag)
                return True, f"Message sent to {target}"
                
        except Exception as e:
            return False, f"Error sending message: {e}"
    
    def send_command(self, target: str, command: str, args: List[str] = None) -> Tuple[bool, str]:
        """Send a command to a specific agent"""
        try:
            if not self.acp:
                return False, "AgentCellPhone not initialized"
            
            # Validate target
            if target not in self.get_available_agents() and target != "all":
                return False, f"Invalid target: {target}"
            
            # Validate command
            if command not in self.get_available_commands():
                return False, f"Invalid command: {command}"
            
            # Format command message
            command_text = command
            if args:
                command_text += " " + " ".join(args)
            
            # Send command
            if target == "all":
                self.acp.broadcast(command_text, MsgTag.COMMAND)
                return True, f"Command '{command}' broadcast to all agents"
            else:
                self.acp.send(target, command_text, MsgTag.COMMAND)
                return True, f"Command '{command}' sent to {target}"
                
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
            if not self.acp:
                return {"error": "AgentCellPhone not initialized"}
            
            status = {
                "layout_mode": self.acp.get_layout_mode(),
                "available_agents": self.acp.get_available_agents(),
                "available_layouts": self.acp.get_available_layouts(),
                "timestamp": datetime.now().isoformat()
            }
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
    
    def get_agent_info(self, agent_name: str) -> Dict:
        """Get information about a specific agent"""
        try:
            if not self.acp:
                return {"error": "AgentCellPhone not initialized"}
            
            agents = self.get_available_agents()
            if agent_name not in agents:
                return {"error": f"Agent {agent_name} not found"}
            
            # Get agent coordinates
            coords = self.acp._coords.get(agent_name, {})
            
            info = {
                "name": agent_name,
                "layout_mode": self.acp.get_layout_mode(),
                "coordinates": coords,
                "available": True,
                "last_seen": datetime.now().isoformat()
            }
            
            return info
        except Exception as e:
            return {"error": f"Error getting agent info: {e}"}
    
    def switch_layout_mode(self, new_layout: str) -> Tuple[bool, str]:
        """Switch to a different layout mode"""
        try:
            available_layouts = self.acp.get_available_layouts() if self.acp else []
            
            if new_layout not in available_layouts:
                return False, f"Invalid layout mode. Available: {', '.join(available_layouts)}"
            
            # Reinitialize with new layout
            self.layout_mode = new_layout
            success = self.initialize_agent_cell_phone()
            
            if success:
                return True, f"Switched to {new_layout} layout"
            else:
                return False, "Failed to initialize new layout"
                
        except Exception as e:
            return False, f"Error switching layout: {e}"
    
    def toggle_test_mode(self) -> Tuple[bool, str]:
        """Toggle between test and live mode"""
        try:
            self.test_mode = not self.test_mode
            success = self.initialize_agent_cell_phone()
            
            mode = "test" if self.test_mode else "live"
            if success:
                return True, f"Switched to {mode} mode"
            else:
                return False, f"Failed to initialize {mode} mode"
                
        except Exception as e:
            return False, f"Error toggling mode: {e}"

# Convenience functions for direct use
def create_messaging_utils(layout_mode: str = "8-agent", test_mode: bool = True) -> MessagingUtils:
    """Create a messaging utils instance"""
    return MessagingUtils(layout_mode, test_mode)

def send_quick_message(target: str, message: str, layout_mode: str = "8-agent") -> Tuple[bool, str]:
    """Quick function to send a message"""
    utils = MessagingUtils(layout_mode, test_mode=True)
    return utils.send_message(target, message)

def send_quick_command(target: str, command: str, layout_mode: str = "8-agent") -> Tuple[bool, str]:
    """Quick function to send a command"""
    utils = MessagingUtils(layout_mode, test_mode=True)
    return utils.send_command(target, command) 
#!/usr/bin/env python3
"""
Shared Classes for GUI
=====================
Extracted duplicate classes to eliminate code duplication across GUI files.
"""

import os
import json
from typing import Dict, Tuple, Optional, Any

class CoordinateFinder:
    """
    Shared coordinate finder class to eliminate duplication across GUI files.
    Provides fallback functionality when the main coordinate finder is not available.
    """
    
    def __init__(self):
        """Initialize the coordinate finder."""
        self.coordinates = {}
        self._load_coordinates()
    
    def _load_coordinates(self):
        """Load coordinates from configuration files."""
        try:
            # Try to load from runtime config
            config_path = os.path.join("runtime", "config", "cursor_agent_coords.json")
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    self.coordinates = json.load(f)
            else:
                # Fallback to default coordinates
                self.coordinates = self._get_default_coordinates()
        except Exception:
            # Fallback to default coordinates on any error
            self.coordinates = self._get_default_coordinates()
    
    def _get_default_coordinates(self) -> Dict[str, Tuple[int, int]]:
        """Get default coordinates for agents."""
        return {f"agent-{i}": (100 + i*50, 100 + i*50) for i in range(1, 9)}
    
    def get_all_coordinates(self) -> Dict[str, Tuple[int, int]]:
        """Get coordinates for all agents."""
        return self.coordinates.copy()
    
    def get_coordinates(self, agent_id: str) -> Optional[Tuple[int, int]]:
        """Get coordinates for a specific agent."""
        return self.coordinates.get(agent_id, (100, 100))
    
    def update_coordinates(self, agent_id: str, x: int, y: int):
        """Update coordinates for a specific agent."""
        self.coordinates[agent_id] = (x, y)
    
    def save_coordinates(self):
        """Save coordinates to configuration file."""
        try:
            config_dir = os.path.join("runtime", "config")
            os.makedirs(config_dir, exist_ok=True)
            config_path = os.path.join(config_dir, "cursor_agent_coords.json")
            
            with open(config_path, 'w') as f:
                json.dump(self.coordinates, f, indent=2)
        except Exception as e:
            print(f"Failed to save coordinates: {e}")


class AgentAutonomyFramework:
    """
    Shared agent autonomy framework class to eliminate duplication across GUI files.
    Provides fallback functionality when the main framework is not available.
    """
    
    def __init__(self):
        """Initialize the agent autonomy framework."""
        self.agents = {}
        self._load_agents()
    
    def _load_agents(self):
        """Load agent configurations."""
        try:
            # Try to load from agent workspaces
            agent_dir = "agent_workspaces"
            if os.path.exists(agent_dir):
                for item in os.listdir(agent_dir):
                    if item.startswith("agent-") and os.path.isdir(os.path.join(agent_dir, item)):
                        self.agents[item] = {
                            "status": "unknown",
                            "current_task": "idle",
                            "last_update": "unknown"
                        }
        except Exception:
            # Fallback to default agents
            self.agents = {f"agent-{i}": {"status": "unknown", "current_task": "idle", "last_update": "unknown"} 
                          for i in range(1, 9)}
    
    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get status for a specific agent."""
        return self.agents.get(agent_id, {"status": "unknown", "current_task": "idle", "last_update": "unknown"})
    
    def update_agent_status(self, agent_id: str, status: str, task: str = None):
        """Update status for a specific agent."""
        if agent_id in self.agents:
            self.agents[agent_id]["status"] = status
            if task:
                self.agents[agent_id]["current_task"] = task
            self.agents[agent_id]["last_update"] = self._get_timestamp()
    
    def get_all_agents(self) -> Dict[str, Dict[str, Any]]:
        """Get status for all agents."""
        return self.agents.copy()
    
    def _get_timestamp(self) -> str:
        """Get current timestamp string."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def broadcast_message(self, message: str) -> bool:
        """Broadcast a message to all agents."""
        # This is a placeholder - actual implementation would depend on the framework
        print(f"Broadcasting message: {message}")
        return True
    
    def send_message(self, agent_id: str, message: str) -> bool:
        """Send a message to a specific agent."""
        # This is a placeholder - actual implementation would depend on the framework
        print(f"Sending message to {agent_id}: {message}")
        return True


# Convenience function to get shared instances
def get_shared_coordinate_finder() -> CoordinateFinder:
    """Get a shared coordinate finder instance."""
    return CoordinateFinder()


def get_shared_agent_framework() -> AgentAutonomyFramework:
    """Get a shared agent autonomy framework instance."""
    return AgentAutonomyFramework() 
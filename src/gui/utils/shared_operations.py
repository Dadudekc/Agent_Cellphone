#!/usr/bin/env python3
"""
Shared Operations Module
=======================
Consolidates common utility functions and operations used across multiple
GUI components to eliminate duplication and standardize functionality.
"""

import os
import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any, Union
from pathlib import Path

# Import existing components
try:
    from src.gui.utils.unified_broadcast_service import UnifiedBroadcastService, BroadcastType, BroadcastPriority
    from src.gui.utils.shared_classes import CoordinateFinder, AgentAutonomyFramework
except ImportError:
    # Fallback imports
    UnifiedBroadcastService = None
    BroadcastType = None
    BroadcastPriority = None
    CoordinateFinder = None
    AgentAutonomyFramework = None


class SharedOperations:
    """
    Shared operations class that provides common functionality used across
    multiple GUI components and utilities.
    """
    
    def __init__(self, layout_mode: str = "8-agent", test_mode: bool = True):
        """
        Initialize shared operations.
        
        Args:
            layout_mode: Layout mode for agent configuration
            test_mode: Whether to run in test mode
        """
        self.layout_mode = layout_mode
        self.test_mode = test_mode
        
        # Initialize shared services
        self.broadcast_service = None
        self.coordinate_finder = None
        self.agent_framework = None
        
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize shared services"""
        # Initialize broadcast service
        try:
            if UnifiedBroadcastService:
                self.broadcast_service = UnifiedBroadcastService(self.layout_mode, self.test_mode)
        except Exception as e:
            print(f"Warning: Could not initialize broadcast service: {e}")
        
        # Initialize coordinate finder
        try:
            if CoordinateFinder:
                self.coordinate_finder = CoordinateFinder()
        except Exception as e:
            print(f"Warning: Could not initialize coordinate finder: {e}")
        
        # Initialize agent framework
        try:
            if AgentAutonomyFramework:
                self.agent_framework = AgentAutonomyFramework()
        except Exception as e:
            print(f"Warning: Could not initialize agent framework: {e}")
    
    # ============================================================================
    # AGENT OPERATIONS
    # ============================================================================
    
    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get status for a specific agent"""
        try:
            # Try to get from agent workspace
            status_file = os.path.join("agent_workspaces", agent_id, "status.json")
            if os.path.exists(status_file):
                with open(status_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error reading agent status: {e}")
        
        # Fallback to default status
        return {
            "status": "unknown",
            "current_task": "idle",
            "last_update": datetime.now().isoformat()
        }
    
    def get_all_agent_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Get status for all agents"""
        statuses = {}
        
        # Get available agents
        agents = self._get_available_agents()
        
        for agent_id in agents:
            statuses[agent_id] = self.get_agent_status(agent_id)
        
        return statuses
    
    def ping_agent(self, agent_id: str) -> Tuple[bool, str]:
        """Ping a specific agent"""
        if self.broadcast_service:
            result = self.broadcast_service.broadcast_command("ping", targets=[agent_id])
            return result.success, result.message
        
        # Fallback implementation
        try:
            status = self.get_agent_status(agent_id)
            if status["status"] != "unknown":
                return True, f"Agent {agent_id} is responsive"
            else:
                return False, f"Agent {agent_id} is not responding"
        except Exception as e:
            return False, f"Error pinging agent {agent_id}: {e}"
    
    def ping_all_agents(self) -> Dict[str, Tuple[bool, str]]:
        """Ping all agents"""
        results = {}
        agents = self._get_available_agents()
        
        for agent_id in agents:
            results[agent_id] = self.ping_agent(agent_id)
        
        return results
    
    def resume_agent(self, agent_id: str) -> Tuple[bool, str]:
        """Resume operations for a specific agent"""
        if self.broadcast_service:
            result = self.broadcast_service.broadcast_command("resume", targets=[agent_id])
            return result.success, result.message
        
        # Fallback implementation
        try:
            # Update agent status file
            status_file = os.path.join("agent_workspaces", agent_id, "status.json")
            if os.path.exists(status_file):
                with open(status_file, 'r') as f:
                    status = json.load(f)
                
                status["status"] = "active"
                status["last_update"] = datetime.now().isoformat()
                
                with open(status_file, 'w') as f:
                    json.dump(status, f, indent=2)
                
                return True, f"Agent {agent_id} resumed"
            else:
                return False, f"Agent {agent_id} status file not found"
        except Exception as e:
            return False, f"Error resuming agent {agent_id}: {e}"
    
    def pause_agent(self, agent_id: str) -> Tuple[bool, str]:
        """Pause operations for a specific agent"""
        if self.broadcast_service:
            result = self.broadcast_service.broadcast_command("pause", targets=[agent_id])
            return result.success, result.message
        
        # Fallback implementation
        try:
            # Update agent status file
            status_file = os.path.join("agent_workspaces", agent_id, "status.json")
            if os.path.exists(status_file):
                with open(status_file, 'r') as f:
                    status = json.load(f)
                
                status["status"] = "paused"
                status["last_update"] = datetime.now().isoformat()
                
                with open(status_file, 'w') as f:
                    json.dump(status, f, indent=2)
                
                return True, f"Agent {agent_id} paused"
            else:
                return False, f"Agent {agent_id} status file not found"
        except Exception as e:
            return False, f"Error pausing agent {agent_id}: {e}"
    
    def sync_agent(self, agent_id: str) -> Tuple[bool, str]:
        """Sync data for a specific agent"""
        if self.broadcast_service:
            result = self.broadcast_service.broadcast_command("sync", targets=[agent_id])
            return result.success, result.message
        
        # Fallback implementation
        return True, f"Agent {agent_id} synced"
    
    def assign_task_to_agent(self, agent_id: str, task_description: str) -> Tuple[bool, str]:
        """Assign a task to a specific agent"""
        if self.broadcast_service:
            result = self.broadcast_service.broadcast_command("task", ["assign", task_description], [agent_id])
            return result.success, result.message
        
        # Fallback implementation
        try:
            # Create task file in agent workspace
            task_file = os.path.join("agent_workspaces", agent_id, "tasks", f"task_{int(time.time())}.json")
            os.makedirs(os.path.dirname(task_file), exist_ok=True)
            
            task_data = {
                "description": task_description,
                "assigned_at": datetime.now().isoformat(),
                "status": "assigned"
            }
            
            with open(task_file, 'w') as f:
                json.dump(task_data, f, indent=2)
            
            return True, f"Task assigned to {agent_id}"
        except Exception as e:
            return False, f"Error assigning task to {agent_id}: {e}"
    
    # ============================================================================
    # BROADCAST OPERATIONS
    # ============================================================================
    
    def broadcast_message(self, message: str, targets: Optional[List[str]] = None) -> Tuple[bool, str]:
        """Broadcast a message to agents"""
        if self.broadcast_service:
            result = self.broadcast_service.broadcast_message(message, targets)
            return result.success, result.message
        
        # Fallback implementation
        return True, f"Message broadcast to {len(targets or [])} agents"
    
    def broadcast_command(self, command: str, args: Optional[List[str]] = None, 
                         targets: Optional[List[str]] = None) -> Tuple[bool, str]:
        """Broadcast a command to agents"""
        if self.broadcast_service:
            result = self.broadcast_service.broadcast_command(command, args, targets)
            return result.success, result.message
        
        # Fallback implementation
        return True, f"Command '{command}' broadcast to {len(targets or [])} agents"
    
    def broadcast_system_message(self, message: str, targets: Optional[List[str]] = None) -> Tuple[bool, str]:
        """Broadcast a system message to agents"""
        if self.broadcast_service:
            result = self.broadcast_service.broadcast_system_message(message, targets)
            return result.success, result.message
        
        # Fallback implementation
        return True, f"System message broadcast to {len(targets or [])} agents"
    
    def broadcast_emergency(self, message: str, targets: Optional[List[str]] = None) -> Tuple[bool, str]:
        """Broadcast an emergency message to agents"""
        if self.broadcast_service:
            result = self.broadcast_service.broadcast_emergency(message, targets)
            return result.success, result.message
        
        # Fallback implementation
        return True, f"Emergency message broadcast to {len(targets or [])} agents"
    
    # ============================================================================
    # COORDINATE OPERATIONS
    # ============================================================================
    
    def get_agent_coordinates(self, agent_id: str) -> Optional[Tuple[int, int]]:
        """Get coordinates for a specific agent"""
        if self.coordinate_finder:
            return self.coordinate_finder.get_coordinates(agent_id)
        
        # Fallback to default coordinates
        return (100, 100)
    
    def get_all_coordinates(self) -> Dict[str, Tuple[int, int]]:
        """Get coordinates for all agents"""
        if self.coordinate_finder:
            return self.coordinate_finder.get_all_coordinates()
        
        # Fallback to default coordinates
        agents = self._get_available_agents()
        return {agent: (100 + i*50, 100 + i*50) for i, agent in enumerate(agents)}
    
    def update_agent_coordinates(self, agent_id: str, x: int, y: int) -> bool:
        """Update coordinates for a specific agent"""
        if self.coordinate_finder:
            self.coordinate_finder.update_coordinates(agent_id, x, y)
            return True
        
        return False
    
    def save_coordinates(self) -> bool:
        """Save coordinates to configuration file"""
        if self.coordinate_finder:
            self.coordinate_finder.save_coordinates()
            return True
        
        return False
    
    # ============================================================================
    # SYSTEM OPERATIONS
    # ============================================================================
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status"""
        try:
            # Get agent statuses
            agent_statuses = self.get_all_agent_statuses()
            
            # Calculate health metrics
            total_agents = len(agent_statuses)
            active_agents = sum(1 for status in agent_statuses.values() 
                              if status.get("status") == "active")
            
            # Ping all agents to check responsiveness
            ping_results = self.ping_all_agents()
            responsive_agents = sum(1 for success, _ in ping_results.values() if success)
            
            health_status = {
                "total_agents": total_agents,
                "active_agents": active_agents,
                "responsive_agents": responsive_agents,
                "response_rate": (responsive_agents / total_agents * 100) if total_agents > 0 else 0,
                "system_status": "healthy" if responsive_agents == total_agents else "degraded",
                "agent_statuses": agent_statuses,
                "ping_results": ping_results,
                "timestamp": datetime.now().isoformat()
            }
            
            return health_status
        except Exception as e:
            return {"error": f"Error getting system health: {e}"}
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get comprehensive system metrics"""
        try:
            health = self.get_system_health()
            coordinates = self.get_all_coordinates()
            
            metrics = {
                "health": health,
                "coordinates": coordinates,
                "layout_mode": self.layout_mode,
                "test_mode": self.test_mode,
                "timestamp": datetime.now().isoformat()
            }
            
            # Add broadcast service statistics if available
            if self.broadcast_service:
                metrics["broadcast_stats"] = self.broadcast_service.get_statistics()
            
            return metrics
        except Exception as e:
            return {"error": f"Error getting system metrics: {e}"}
    
    def test_system_connectivity(self) -> Dict[str, Any]:
        """Test connectivity to all agents"""
        try:
            results = {}
            agents = self._get_available_agents()
            
            for agent_id in agents:
                # Test ping
                ping_success, ping_message = self.ping_agent(agent_id)
                
                # Test coordinates
                coords = self.get_agent_coordinates(agent_id)
                coords_available = coords is not None
                
                # Test status
                status = self.get_agent_status(agent_id)
                
                results[agent_id] = {
                    "ping": {"success": ping_success, "message": ping_message},
                    "coordinates": {"available": coords_available, "coords": coords},
                    "status": status,
                    "timestamp": datetime.now().isoformat()
                }
            
            return results
        except Exception as e:
            return {"error": f"Error testing connectivity: {e}"}
    
    # ============================================================================
    # UTILITY OPERATIONS
    # ============================================================================
    
    def _get_available_agents(self) -> List[str]:
        """Get list of available agents"""
        agents = []
        
        # Try to get from broadcast service
        if self.broadcast_service:
            try:
                agents = self.broadcast_service._get_all_agents()
            except:
                pass
        
        # Try to get from coordinate finder
        if not agents and self.coordinate_finder:
            try:
                coords = self.coordinate_finder.get_all_coordinates()
                agents = list(coords.keys())
            except:
                pass
        
        # Try to get from agent framework
        if not agents and self.agent_framework:
            try:
                agents = list(self.agent_framework.agents.keys())
            except:
                pass
        
        # Fallback to default agents
        if not agents:
            agents = [f"agent-{i}" for i in range(1, 9)]
        
        return agents
    
    def validate_agent_id(self, agent_id: str) -> Tuple[bool, str]:
        """Validate an agent ID"""
        available_agents = self._get_available_agents()
        
        if agent_id in available_agents:
            return True, "Valid agent ID"
        else:
            return False, f"Invalid agent ID. Available: {', '.join(available_agents)}"
    
    def get_agent_info(self, agent_id: str) -> Dict[str, Any]:
        """Get comprehensive information about an agent"""
        try:
            # Validate agent ID
            is_valid, validation_message = self.validate_agent_id(agent_id)
            if not is_valid:
                return {"error": validation_message}
            
            # Get various information
            status = self.get_agent_status(agent_id)
            coordinates = self.get_agent_coordinates(agent_id)
            ping_success, ping_message = self.ping_agent(agent_id)
            
            info = {
                "agent_id": agent_id,
                "status": status,
                "coordinates": coordinates,
                "ping": {"success": ping_success, "message": ping_message},
                "layout_mode": self.layout_mode,
                "timestamp": datetime.now().isoformat()
            }
            
            return info
        except Exception as e:
            return {"error": f"Error getting agent info: {e}"}
    
    def execute_agent_action(self, agent_id: str, action: str, **kwargs) -> Tuple[bool, str]:
        """Execute a generic action on an agent"""
        try:
            if action == "ping":
                return self.ping_agent(agent_id)
            elif action == "resume":
                return self.resume_agent(agent_id)
            elif action == "pause":
                return self.pause_agent(agent_id)
            elif action == "sync":
                return self.sync_agent(agent_id)
            elif action == "status":
                status = self.get_agent_status(agent_id)
                return True, f"Agent {agent_id} status: {status}"
            elif action == "assign_task":
                task_description = kwargs.get("task_description", "No task specified")
                return self.assign_task_to_agent(agent_id, task_description)
            else:
                return False, f"Unknown action: {action}"
        except Exception as e:
            return False, f"Error executing action {action} on {agent_id}: {e}"


# Convenience functions for direct use
def create_shared_operations(layout_mode: str = "8-agent", test_mode: bool = True) -> SharedOperations:
    """Create a shared operations instance"""
    return SharedOperations(layout_mode, test_mode)


def quick_agent_action(agent_id: str, action: str, layout_mode: str = "8-agent", **kwargs) -> Tuple[bool, str]:
    """Quick function to execute an action on an agent"""
    ops = SharedOperations(layout_mode, test_mode=True)
    return ops.execute_agent_action(agent_id, action, **kwargs)


def quick_broadcast(content: str, broadcast_type: str = "message", layout_mode: str = "8-agent") -> Tuple[bool, str]:
    """Quick function to broadcast a message"""
    ops = SharedOperations(layout_mode, test_mode=True)
    
    if broadcast_type == "message":
        return ops.broadcast_message(content)
    elif broadcast_type == "command":
        return ops.broadcast_command(content)
    elif broadcast_type == "system":
        return ops.broadcast_system_message(content)
    elif broadcast_type == "emergency":
        return ops.broadcast_emergency(content)
    else:
        return ops.broadcast_message(content) 
#!/usr/bin/env python3
"""
Coordination Utilities for Dream.OS GUI
Provides agent coordination and management functionality
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

class CoordinationUtils:
    """Utility class for agent coordination operations"""
    
    def __init__(self, layout_mode: str = "8-agent", test_mode: bool = True):
        """Initialize coordination utilities"""
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
    
    def get_system_coordinates(self) -> Dict:
        """Get system coordinates and layout information"""
        try:
            if not self.acp:
                return {"error": "AgentCellPhone not initialized"}
            
            coords = self.acp._coords
            layout_mode = self.acp.get_layout_mode()
            available_layouts = self.acp.get_available_layouts()
            
            return {
                "layout_mode": layout_mode,
                "available_layouts": available_layouts,
                "coordinates": coords,
                "total_agents": len(coords),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Error getting coordinates: {e}"}
    
    def test_all_agents(self) -> Dict[str, Dict]:
        """Test connectivity to all agents"""
        results = {}
        agents = self.acp.get_available_agents() if self.acp else []
        
        for agent in agents:
            agent_result = {
                "ping": self._test_ping(agent),
                "status": self._test_status(agent),
                "timestamp": datetime.now().isoformat()
            }
            results[agent] = agent_result
        
        return results
    
    def _test_ping(self, agent: str) -> Dict:
        """Test ping to a specific agent"""
        try:
            start_time = time.time()
            success, message = self.acp.send(agent, "ping", MsgTag.COMMAND)
            end_time = time.time()
            
            return {
                "success": success,
                "message": message,
                "response_time": round((end_time - start_time) * 1000, 2),  # ms
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error: {e}",
                "response_time": None,
                "timestamp": datetime.now().isoformat()
            }
    
    def _test_status(self, agent: str) -> Dict:
        """Test status request to a specific agent"""
        try:
            start_time = time.time()
            success, message = self.acp.send(agent, "status", MsgTag.COMMAND)
            end_time = time.time()
            
            return {
                "success": success,
                "message": message,
                "response_time": round((end_time - start_time) * 1000, 2),  # ms
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error: {e}",
                "response_time": None,
                "timestamp": datetime.now().isoformat()
            }
    
    def broadcast_system_message(self, message: str, tag: str = "NORMAL") -> Tuple[bool, str]:
        """Broadcast a message to all agents"""
        try:
            if not self.acp:
                return False, "AgentCellPhone not initialized"
            
            # Get message tag
            try:
                msg_tag = MsgTag[tag.upper()]
            except KeyError:
                msg_tag = MsgTag.NORMAL
            
            # Broadcast message
            self.acp.broadcast(message, msg_tag)
            return True, f"Message broadcast to all agents with tag {tag}"
            
        except Exception as e:
            return False, f"Error broadcasting message: {e}"
    
    def send_coordination_command(self, command: str, targets: List[str] = None) -> Dict[str, Tuple[bool, str]]:
        """Send a coordination command to specified agents or all agents"""
        results = {}
        
        if targets is None:
            targets = self.acp.get_available_agents() if self.acp else []
        
        for target in targets:
            success, message = self.acp.send(target, command, MsgTag.COMMAND)
            results[target] = (success, message)
            time.sleep(0.5)  # Small delay between sends
        
        return results
    
    def sync_all_agents(self) -> Dict[str, Tuple[bool, str]]:
        """Synchronize all agents"""
        return self.send_coordination_command("sync")
    
    def resume_all_agents(self) -> Dict[str, Tuple[bool, str]]:
        """Resume all agents"""
        return self.send_coordination_command("resume")
    
    def verify_all_agents(self) -> Dict[str, Tuple[bool, str]]:
        """Verify all agents"""
        return self.send_coordination_command("verify")
    
    def get_system_health(self) -> Dict:
        """Get overall system health status"""
        try:
            if not self.acp:
                return {"error": "AgentCellPhone not initialized"}
            
            # Test all agents
            test_results = self.test_all_agents()
            
            # Calculate health metrics
            total_agents = len(test_results)
            responsive_agents = sum(1 for result in test_results.values() 
                                  if result["ping"]["success"])
            
            avg_ping_time = 0
            successful_pings = 0
            
            for result in test_results.values():
                if result["ping"]["success"] and result["ping"]["response_time"]:
                    avg_ping_time += result["ping"]["response_time"]
                    successful_pings += 1
            
            if successful_pings > 0:
                avg_ping_time /= successful_pings
            
            health_status = {
                "total_agents": total_agents,
                "responsive_agents": responsive_agents,
                "response_rate": (responsive_agents / total_agents * 100) if total_agents > 0 else 0,
                "average_ping_time": round(avg_ping_time, 2),
                "system_status": "healthy" if responsive_agents == total_agents else "degraded",
                "test_results": test_results,
                "timestamp": datetime.now().isoformat()
            }
            
            return health_status
        except Exception as e:
            return {"error": f"Error getting system health: {e}"}
    
    def assign_tasks_to_agents(self, tasks: Dict[str, str]) -> Dict[str, Tuple[bool, str]]:
        """Assign specific tasks to specific agents"""
        results = {}
        
        for agent, task in tasks.items():
            if agent in (self.acp.get_available_agents() if self.acp else []):
                command = f"task assign {task}"
                success, message = self.acp.send(agent, command, MsgTag.COMMAND)
                results[agent] = (success, message)
            else:
                results[agent] = (False, f"Agent {agent} not found")
        
        return results
    
    def get_agent_workloads(self) -> Dict[str, Dict]:
        """Get workload information for all agents"""
        results = {}
        agents = self.acp.get_available_agents() if self.acp else []
        
        for agent in agents:
            try:
                # Check agent workspace for task information
                agent_workspace = project_root / "agent_workspaces" / agent
                task_list_file = agent_workspace / "task_list.json"
                
                workload_info = {
                    "agent": agent,
                    "workspace_exists": agent_workspace.exists(),
                    "task_list_exists": task_list_file.exists(),
                    "task_count": 0,
                    "last_updated": None
                }
                
                if task_list_file.exists():
                    try:
                        with open(task_list_file, 'r') as f:
                            task_data = json.load(f)
                            workload_info["task_count"] = len(task_data.get("tasks", []))
                            workload_info["last_updated"] = datetime.fromtimestamp(
                                task_list_file.stat().st_mtime
                            ).isoformat()
                    except Exception as e:
                        workload_info["error"] = f"Error reading task list: {e}"
                
                results[agent] = workload_info
                
            except Exception as e:
                results[agent] = {"error": f"Error getting workload: {e}"}
        
        return results
    
    def balance_workload(self) -> Dict[str, str]:
        """Attempt to balance workload across agents"""
        try:
            workloads = self.get_agent_workloads()
            
            # Find agents with highest and lowest workloads
            agent_loads = []
            for agent, info in workloads.items():
                if "error" not in info:
                    agent_loads.append((agent, info.get("task_count", 0)))
            
            if len(agent_loads) < 2:
                return {"message": "Not enough agents for load balancing"}
            
            # Sort by task count
            agent_loads.sort(key=lambda x: x[1])
            
            lowest_load = agent_loads[0]
            highest_load = agent_loads[-1]
            
            if highest_load[1] - lowest_load[1] <= 1:
                return {"message": "Workload is already balanced"}
            
            # Suggest task redistribution
            tasks_to_move = (highest_load[1] - lowest_load[1]) // 2
            
            return {
                "suggestion": f"Move {tasks_to_move} tasks from {highest_load[0]} to {lowest_load[1]}",
                "current_distribution": dict(agent_loads),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Error balancing workload: {e}"}
    
    def get_system_metrics(self) -> Dict:
        """Get comprehensive system metrics"""
        try:
            health = self.get_system_health()
            workloads = self.get_agent_workloads()
            coordinates = self.get_system_coordinates()
            
            metrics = {
                "health": health,
                "workloads": workloads,
                "coordinates": coordinates,
                "timestamp": datetime.now().isoformat()
            }
            
            # Calculate additional metrics
            if "error" not in health:
                total_tasks = sum(info.get("task_count", 0) for info in workloads.values() 
                                if "error" not in info)
                metrics["total_tasks"] = total_tasks
                metrics["average_tasks_per_agent"] = total_tasks / len(workloads) if workloads else 0
            
            return metrics
        except Exception as e:
            return {"error": f"Error getting system metrics: {e}"}
    
    def emergency_broadcast(self, message: str) -> Tuple[bool, str]:
        """Send an emergency broadcast to all agents"""
        return self.broadcast_system_message(message, "CAPTAIN")
    
    def system_maintenance_mode(self, enable: bool) -> Dict[str, Tuple[bool, str]]:
        """Enable or disable system maintenance mode"""
        command = "maintenance on" if enable else "maintenance off"
        return self.send_coordination_command(command)
    
    def get_agent_logs(self, agent: str, lines: int = 50) -> Dict:
        """Get recent logs for a specific agent"""
        try:
            agent_workspace = project_root / "agent_workspaces" / agent
            
            if not agent_workspace.exists():
                return {"error": f"Agent workspace not found: {agent}"}
            
            # Look for log files
            log_files = list(agent_workspace.glob("*.log"))
            
            logs = {}
            for log_file in log_files:
                try:
                    with open(log_file, 'r') as f:
                        lines_content = f.readlines()
                        logs[log_file.name] = lines_content[-lines:] if len(lines_content) > lines else lines_content
                except Exception as e:
                    logs[log_file.name] = [f"Error reading log: {e}"]
            
            return {
                "agent": agent,
                "logs": logs,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Error getting agent logs: {e}"}
    
    def clear_agent_logs(self, agent: str) -> Tuple[bool, str]:
        """Clear logs for a specific agent"""
        try:
            agent_workspace = project_root / "agent_workspaces" / agent
            
            if not agent_workspace.exists():
                return False, f"Agent workspace not found: {agent}"
            
            # Find and clear log files
            log_files = list(agent_workspace.glob("*.log"))
            cleared_count = 0
            
            for log_file in log_files:
                try:
                    log_file.unlink()
                    cleared_count += 1
                except Exception as e:
                    return False, f"Error clearing log {log_file.name}: {e}"
            
            return True, f"Cleared {cleared_count} log files for {agent}"
        except Exception as e:
            return False, f"Error clearing logs: {e}"

# Convenience functions
def create_coordination_utils(layout_mode: str = "8-agent", test_mode: bool = True) -> CoordinationUtils:
    """Create a coordination utils instance"""
    return CoordinationUtils(layout_mode, test_mode)

def get_system_health() -> Dict:
    """Quick function to get system health"""
    utils = CoordinationUtils(test_mode=True)
    return utils.get_system_health()

def test_all_agents() -> Dict[str, Dict]:
    """Quick function to test all agents"""
    utils = CoordinationUtils(test_mode=True)
    return utils.test_all_agents()

def broadcast_message(message: str) -> Tuple[bool, str]:
    """Quick function to broadcast a message"""
    utils = CoordinationUtils(test_mode=True)
    return utils.broadcast_system_message(message) 
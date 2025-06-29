#!/usr/bin/env python3
"""
Dream.OS Agent Autonomy Framework
=================================
Core framework for autonomous agent development and coordination.
"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class AgentAutonomyFramework:
    """
    Core framework for autonomous agent development and coordination.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the Agent Autonomy Framework.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.agents = {}
        self.tasks = {}
        self.communication_channels = {}
        self.logger = logger
        
        logger.info("Agent Autonomy Framework initialized")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load config from {config_path}: {e}")
        
        # Default configuration
        return {
            "max_agents": 10,
            "communication_timeout": 30,
            "task_timeout": 300,
            "log_level": "INFO",
            "workspace_path": "agent_workspaces"
        }
    
    def register_agent(self, agent_id: str, capabilities: List[str], 
                      workspace_path: Optional[str] = None) -> bool:
        """
        Register a new agent in the framework.
        
        Args:
            agent_id: Unique identifier for the agent
            capabilities: List of agent capabilities
            workspace_path: Path to agent workspace
            
        Returns:
            True if registration successful, False otherwise
        """
        if agent_id in self.agents:
            logger.warning(f"Agent {agent_id} already registered")
            return False
        
        if len(self.agents) >= self.config["max_agents"]:
            logger.error("Maximum number of agents reached")
            return False
        
        # Create agent workspace
        if not workspace_path:
            workspace_path = os.path.join(self.config["workspace_path"], agent_id)
        
        try:
            os.makedirs(workspace_path, exist_ok=True)
            
            self.agents[agent_id] = {
                "id": agent_id,
                "capabilities": capabilities,
                "workspace_path": workspace_path,
                "status": "idle",
                "current_task": None,
                "registered_at": datetime.now().isoformat(),
                "last_heartbeat": datetime.now().isoformat()
            }
            
            logger.info(f"Agent {agent_id} registered successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register agent {agent_id}: {e}")
            return False
    
    def unregister_agent(self, agent_id: str) -> bool:
        """
        Unregister an agent from the framework.
        
        Args:
            agent_id: ID of agent to unregister
            
        Returns:
            True if unregistration successful, False otherwise
        """
        if agent_id not in self.agents:
            logger.warning(f"Agent {agent_id} not found")
            return False
        
        # Clean up agent resources
        try:
            agent = self.agents[agent_id]
            if agent["current_task"]:
                self._release_task(agent_id, agent["current_task"])
            
            del self.agents[agent_id]
            logger.info(f"Agent {agent_id} unregistered successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unregister agent {agent_id}: {e}")
            return False
    
    def create_task(self, task_id: str, description: str, requirements: List[str],
                   priority: str = "medium", timeout: Optional[int] = None) -> bool:
        """
        Create a new task in the framework.
        
        Args:
            task_id: Unique identifier for the task
            description: Task description
            requirements: List of required capabilities
            priority: Task priority (low, medium, high, critical)
            timeout: Task timeout in seconds
            
        Returns:
            True if task creation successful, False otherwise
        """
        if task_id in self.tasks:
            logger.warning(f"Task {task_id} already exists")
            return False
        
        if not timeout:
            timeout = self.config["task_timeout"]
        
        self.tasks[task_id] = {
            "id": task_id,
            "description": description,
            "requirements": requirements,
            "priority": priority,
            "status": "pending",
            "assigned_to": None,
            "created_at": datetime.now().isoformat(),
            "timeout": timeout,
            "result": None
        }
        
        logger.info(f"Task {task_id} created successfully")
        return True
    
    def assign_task(self, task_id: str, agent_id: str) -> bool:
        """
        Assign a task to an agent.
        
        Args:
            task_id: ID of task to assign
            agent_id: ID of agent to assign task to
            
        Returns:
            True if assignment successful, False otherwise
        """
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found")
            return False
        
        if agent_id not in self.agents:
            logger.error(f"Agent {agent_id} not found")
            return False
        
        task = self.tasks[task_id]
        agent = self.agents[agent_id]
        
        # Check if agent has required capabilities
        if not all(req in agent["capabilities"] for req in task["requirements"]):
            logger.error(f"Agent {agent_id} lacks required capabilities for task {task_id}")
            return False
        
        # Check if agent is available
        if agent["status"] != "idle":
            logger.error(f"Agent {agent_id} is not available (status: {agent['status']})")
            return False
        
        # Assign task
        task["status"] = "assigned"
        task["assigned_to"] = agent_id
        agent["status"] = "busy"
        agent["current_task"] = task_id
        
        logger.info(f"Task {task_id} assigned to agent {agent_id}")
        return True
    
    def complete_task(self, task_id: str, result: Any) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: ID of task to complete
            result: Task result
            
        Returns:
            True if completion successful, False otherwise
        """
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found")
            return False
        
        task = self.tasks[task_id]
        if task["status"] != "assigned":
            logger.error(f"Task {task_id} is not assigned")
            return False
        
        # Update task
        task["status"] = "completed"
        task["result"] = result
        task["completed_at"] = datetime.now().isoformat()
        
        # Update agent
        agent_id = task["assigned_to"]
        if agent_id in self.agents:
            self.agents[agent_id]["status"] = "idle"
            self.agents[agent_id]["current_task"] = None
        
        logger.info(f"Task {task_id} completed successfully")
        return True
    
    def _release_task(self, agent_id: str, task_id: str):
        """Release a task from an agent."""
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = "pending"
            self.tasks[task_id]["assigned_to"] = None
    
    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific agent."""
        return self.agents.get(agent_id)
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific task."""
        return self.tasks.get(task_id)
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """Get list of all registered agents."""
        return list(self.agents.values())
    
    def list_tasks(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get list of tasks, optionally filtered by status."""
        tasks = list(self.tasks.values())
        if status:
            tasks = [task for task in tasks if task["status"] == status]
        return tasks
    
    def send_message(self, from_agent: str, to_agent: str, message: str, 
                    message_type: str = "info") -> bool:
        """
        Send a message between agents.
        
        Args:
            from_agent: Source agent ID
            to_agent: Target agent ID
            message: Message content
            message_type: Type of message (info, task, error, etc.)
            
        Returns:
            True if message sent successfully, False otherwise
        """
        if from_agent not in self.agents or to_agent not in self.agents:
            logger.error("Invalid agent IDs for message")
            return False
        
        message_data = {
            "from": from_agent,
            "to": to_agent,
            "message": message,
            "type": message_type,
            "timestamp": datetime.now().isoformat()
        }
        
        # Store message in target agent's workspace
        target_workspace = self.agents[to_agent]["workspace_path"]
        messages_dir = os.path.join(target_workspace, "messages")
        os.makedirs(messages_dir, exist_ok=True)
        
        message_file = os.path.join(messages_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{from_agent}.json")
        
        try:
            with open(message_file, 'w') as f:
                json.dump(message_data, f, indent=2)
            
            logger.info(f"Message sent from {from_agent} to {to_agent}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False
    
    def broadcast_message(self, from_agent: str, message: str, 
                         message_type: str = "info") -> int:
        """
        Broadcast a message to all agents.
        
        Args:
            from_agent: Source agent ID
            message: Message content
            message_type: Type of message
            
        Returns:
            Number of agents that received the message
        """
        if from_agent not in self.agents:
            logger.error("Invalid source agent ID for broadcast")
            return 0
        
        success_count = 0
        for agent_id in self.agents:
            if agent_id != from_agent:
                if self.send_message(from_agent, agent_id, message, message_type):
                    success_count += 1
        
        logger.info(f"Broadcast message sent to {success_count} agents")
        return success_count
    
    def get_framework_status(self) -> Dict[str, Any]:
        """Get overall framework status."""
        return {
            "total_agents": len(self.agents),
            "total_tasks": len(self.tasks),
            "pending_tasks": len([t for t in self.tasks.values() if t["status"] == "pending"]),
            "assigned_tasks": len([t for t in self.tasks.values() if t["status"] == "assigned"]),
            "completed_tasks": len([t for t in self.tasks.values() if t["status"] == "completed"]),
            "idle_agents": len([a for a in self.agents.values() if a["status"] == "idle"]),
            "busy_agents": len([a for a in self.agents.values() if a["status"] == "busy"])
        }

def main():
    """Main function for testing the framework."""
    framework = AgentAutonomyFramework()
    
    # Example usage
    framework.register_agent("agent-1", ["development", "testing"])
    framework.register_agent("agent-2", ["documentation", "analysis"])
    
    framework.create_task("task-1", "Develop new feature", ["development"])
    framework.assign_task("task-1", "agent-1")
    
    framework.send_message("agent-1", "agent-2", "Hello from agent-1!")
    
    status = framework.get_framework_status()
    print("Framework Status:", json.dumps(status, indent=2))

if __name__ == "__main__":
    main() 
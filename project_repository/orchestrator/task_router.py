import asyncio, logging, json, time
from pathlib import Path
from typing import Dict, List, Any, Optional

log = logging.getLogger("router")

class TaskRouter:
    """Routes tasks to agents and manages task lifecycle."""
    
    def __init__(self):
        self.tasks = {}  # task_id -> task_data
        self.assigned_tasks = {}  # agent_id -> task_id
        self.completed_tasks = {}  # task_id -> completion_data
        self.agent_status = {}  # agent_id -> status
        self.task_counter = 0
    
    def ingest_prd(self, prd_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Convert PRD to tasks and add to queue."""
        project_name = prd_data["name"]
        requirements = prd_data.get("requirements", [])
        
        tasks = []
        for i, requirement in enumerate(requirements):
            task_id = f"task_{project_name}_{i+1}"
            
            task = {
                "id": task_id,
                "title": f"Implement {requirement}",
                "description": f"Develop functionality for: {requirement}",
                "project": project_name,
                "requirement": requirement,
                "status": "pending",
                "priority": prd_data.get("priority", "medium"),
                "estimated_hours": 8.0,
                "created_at": time.strftime('%Y-%m-%d %H:%M:%S'),
                "progress": 0,
                "assigned_to": None
            }
            
            self.tasks[task_id] = task
            tasks.append(task)
            self.task_counter += 1
        
        log.info("📋 Ingested PRD '%s' into %d tasks", project_name, len(tasks))
        return tasks
    
    async def get_next_task(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get next available task for an agent."""
        # Check if agent is already working on a task
        if agent_id in self.assigned_tasks:
            task_id = self.assigned_tasks[agent_id]
            if task_id in self.tasks:
                return self.tasks[task_id]
        
        # Find available task
        for task_id, task in self.tasks.items():
            if (task["status"] == "pending" and 
                task["assigned_to"] is None):
                
                # Assign task to agent
                task["status"] = "assigned"
                task["assigned_to"] = agent_id
                task["assigned_at"] = time.strftime('%Y-%m-%d %H:%M:%S')
                self.assigned_tasks[agent_id] = task_id
                
                log.info("📝 Assigned task '%s' to %s", task["title"], agent_id)
                return task
        
        return None
    
    async def complete_task(self, agent_id: str, task_data: Dict[str, Any]):
        """Mark a task as completed."""
        task_id = task_data.get("id")
        if not task_id:
            return
        
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task["status"] = "completed"
            task["completed_at"] = time.strftime('%Y-%m-%d %H:%M:%S')
            task["progress"] = 100
            
            # Move to completed tasks
            self.completed_tasks[task_id] = task.copy()
            
            # Remove from assigned tasks
            if agent_id in self.assigned_tasks:
                del self.assigned_tasks[agent_id]
            
            log.info("✅ Task '%s' completed by %s", task["title"], agent_id)
    
    def get_task_status(self) -> Dict[str, Any]:
        """Get overall task status."""
        total_tasks = len(self.tasks)
        pending_tasks = len([t for t in self.tasks.values() if t["status"] == "pending"])
        assigned_tasks = len([t for t in self.tasks.values() if t["status"] == "assigned"])
        completed_tasks = len(self.completed_tasks)
        
        return {
            "total": total_tasks,
            "pending": pending_tasks,
            "assigned": assigned_tasks,
            "completed": completed_tasks,
            "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        }
    
    def get_agent_tasks(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get all tasks for a specific agent."""
        agent_tasks = []
        for task in self.tasks.values():
            if task.get("assigned_to") == agent_id:
                agent_tasks.append(task)
        return agent_tasks
    
    def dispatch_tasks(self, tasks: List[Dict[str, Any]]):
        """Dispatch tasks to available agents."""
        log.info("📤 Dispatching %d tasks to agents", len(tasks))
        
        # For now, just log the dispatch
        # In a real implementation, this would assign tasks to specific agents
        for task in tasks:
            log.info("   📋 Task: %s", task["title"])
    
    def update_agent_status(self, agent_id: str, status: str, **kwargs):
        """Update agent status."""
        self.agent_status[agent_id] = {
            "status": status,
            "updated_at": time.strftime('%Y-%m-%d %H:%M:%S'),
            **kwargs
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status."""
        task_status = self.get_task_status()
        
        active_agents = [agent_id for agent_id, status in self.agent_status.items() 
                        if status.get("status") == "working"]
        
        return {
            "tasks": task_status,
            "agents": {
                "total": len(self.agent_status),
                "active": len(active_agents),
                "active_list": active_agents
            },
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        } 
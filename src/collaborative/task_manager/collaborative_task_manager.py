"""
📋 Collaborative Task Manager

**Agent-2 Responsibility**: Task breakdown and resource allocation
**Purpose**: Multi-agent task coordination and progress tracking
**Features**: Task assignment, progress monitoring, dependency management

This module provides comprehensive task management for multi-agent collaboration,
enabling efficient resource allocation and workflow optimization.
"""

import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import logging
from dataclasses import dataclass, asdict
from enum import Enum

class TaskStatus(Enum):
    """Task status enumeration."""
    CREATED = "created"
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    REVIEW = "review"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    """Task priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class TaskDependency:
    """Task dependency structure."""
    task_id: str
    dependency_type: str  # "blocks", "requires", "suggests"
    critical: bool = False
    estimated_delay_hours: float = 0.0

@dataclass
class AgentCapability:
    """Agent capability structure."""
    agent_id: str
    expertise_areas: List[str]
    skill_levels: Dict[str, int]  # 1-10 scale
    availability_hours: float
    current_workload: float
    collaboration_preferences: List[str]

@dataclass
class CollaborativeTask:
    """Collaborative task structure."""
    task_id: str
    title: str
    description: str
    task_type: str
    priority: TaskPriority
    status: TaskStatus
    agents: List[str]
    estimated_hours: float
    actual_hours: float = 0.0
    progress: float = 0.0
    dependencies: List[TaskDependency] = None
    subtasks: List[str] = None
    created_at: str = None
    updated_at: str = None
    deadline: str = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = datetime.now().isoformat()
        if self.dependencies is None:
            self.dependencies = []
        if self.subtasks is None:
            self.subtasks = []
        if self.tags is None:
            self.tags = []

class CollaborativeTaskManager:
    """
    Comprehensive task management system for multi-agent collaboration.
    
    **Agent-2 leads this system** to manage task breakdown, resource allocation,
    and workflow optimization across all agents.
    """
    
    def __init__(self, data_path: str = "src/collaborative/task_manager/data"):
        self.data_path = Path(data_path)
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # Core task management
        self.tasks: Dict[str, CollaborativeTask] = {}
        self.agent_capabilities: Dict[str, AgentCapability] = {}
        self.workflows: Dict[str, Dict] = {}
        self.resource_allocation: Dict[str, Dict] = {}
        
        # Task optimization
        self.task_dependencies: Dict[str, List[str]] = {}
        self.critical_paths: List[List[str]] = []
        self.resource_conflicts: List[Dict] = []
        
        # Performance tracking
        self.completion_metrics: Dict[str, Any] = {}
        self.efficiency_scores: Dict[str, float] = {}
        self.collaboration_patterns: Dict[str, List] = []
        
        # Threading for real-time updates
        self._lock = threading.RLock()
        self._optimization_active = False
        self._optimization_thread = None
        
        # Initialize logging
        self._setup_logging()
        
        # Load existing data
        self._load_existing_data()
        
        logging.info("📋 Collaborative Task Manager initialized - Agent-2 resource allocation active")
    
    def _setup_logging(self):
        """Setup logging for task management."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - 📋 %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.data_path / 'task_management.log'),
                logging.StreamHandler()
            ]
        )
    
    def _load_existing_data(self):
        """Load existing task management data."""
        try:
            # Load tasks
            tasks_file = self.data_path / 'tasks.json'
            if tasks_file.exists():
                with open(tasks_file, 'r') as f:
                    tasks_data = json.load(f)
                    for task_id, task_data in tasks_data.items():
                        # Convert back to CollaborativeTask object
                        task = CollaborativeTask(**task_data)
                        task.priority = TaskPriority(task_data['priority'])
                        task.status = TaskStatus(task_data['status'])
                        self.tasks[task_id] = task
            
            # Load agent capabilities
            capabilities_file = self.data_path / 'agent_capabilities.json'
            if capabilities_file.exists():
                with open(capabilities_file, 'r') as f:
                    capabilities_data = json.load(f)
                    for agent_id, cap_data in capabilities_data.items():
                        self.agent_capabilities[agent_id] = AgentCapability(**cap_data)
            
            # Load workflows
            workflows_file = self.data_path / 'workflows.json'
            if workflows_file.exists():
                with open(workflows_file, 'r') as f:
                    self.workflows = json.load(f)
                    
            logging.info(f"📚 Loaded existing data: {len(self.tasks)} tasks, {len(self.agent_capabilities)} agents")
            
        except Exception as e:
            logging.warning(f"⚠️ Could not load existing data: {e}")
    
    def create_task(self, title: str, description: str, task_type: str,
                   priority: TaskPriority, agents: List[str], 
                   estimated_hours: float, deadline: str = None,
                   dependencies: List[TaskDependency] = None,
                   subtasks: List[str] = None, tags: List[str] = None) -> str:
        """
        Create a new collaborative task (Agent-2 task breakdown).
        
        Args:
            title: Task title
            description: Task description
            task_type: Type of task
            priority: Task priority
            agents: List of assigned agents
            estimated_hours: Estimated completion time
            deadline: Optional deadline
            dependencies: Task dependencies
            subtasks: Subtask list
            tags: Task tags
        
        Returns:
            Created task ID
        """
        with self._lock:
            # Generate unique task ID
            task_id = f"task_{int(time.time())}_{len(self.tasks)}"
            
            # Create task
            task = CollaborativeTask(
                task_id=task_id,
                title=title,
                description=description,
                task_type=task_type,
                priority=priority,
                status=TaskStatus.CREATED,
                agents=agents,
                estimated_hours=estimated_hours,
                deadline=deadline,
                dependencies=dependencies or [],
                subtasks=subtasks or [],
                tags=tags or []
            )
            
            self.tasks[task_id] = task
            
            # Update dependencies
            for dep in task.dependencies:
                if dep.task_id not in self.task_dependencies:
                    self.task_dependencies[dep.task_id] = []
                self.task_dependencies[dep.task_id].append(task_id)
            
            # Initialize agent workloads
            for agent in agents:
                if agent in self.agent_capabilities:
                    self.agent_capabilities[agent].current_workload += estimated_hours
            
            logging.info(f"📋 Agent-2: Created task '{title}' with {len(agents)} agents, priority: {priority.value}")
            return task_id
    
    def break_down_task(self, task_id: str, subtasks: List[Dict[str, Any]]) -> bool:
        """
        Break down a task into subtasks (Agent-2 task decomposition).
        
        Args:
            task_id: Parent task ID
            subtasks: List of subtask definitions
        
        Returns:
            Success status
        """
        with self._lock:
            if task_id not in self.tasks:
                logging.warning(f"⚠️ Task '{task_id}' not found")
                return False
            
            task = self.tasks[task_id]
            
            # Create subtasks
            for subtask_def in subtasks:
                subtask_id = f"subtask_{int(time.time())}_{len(task.subtasks)}"
                
                # Create subtask
                subtask = CollaborativeTask(
                    task_id=subtask_id,
                    title=subtask_def['title'],
                    description=subtask_def['description'],
                    task_type=subtask_def.get('type', 'subtask'),
                    priority=TaskPriority(subtask_def.get('priority', 'medium')),
                    status=TaskStatus.CREATED,
                    agents=subtask_def.get('agents', task.agents),
                    estimated_hours=subtask_def.get('estimated_hours', 0.0),
                    tags=subtask_def.get('tags', []) + ['subtask']
                )
                
                self.tasks[subtask_id] = subtask
                task.subtasks.append(subtask_id)
                
                # Add dependency relationship
                dep = TaskDependency(
                    task_id=subtask_id,
                    dependency_type="blocks",
                    critical=subtask_def.get('critical', False)
                )
                task.dependencies.append(dep)
            
            task.status = TaskStatus.PLANNED
            task.updated_at = datetime.now().isoformat()
            
            logging.info(f"📋 Agent-2: Broke down task '{task.title}' into {len(subtasks)} subtasks")
            return True
    
    def allocate_resources(self, task_id: str, resource_plan: Dict[str, Any]) -> bool:
        """
        Allocate resources for a task (Agent-2 resource allocation).
        
        Args:
            task_id: Task identifier
            resource_plan: Resource allocation plan
        
        Returns:
            Success status
        """
        with self._lock:
            if task_id not in self.tasks:
                logging.warning(f"⚠️ Task '{task_id}' not found")
                return False
            
            task = self.tasks[task_id]
            
            # Store resource allocation
            self.resource_allocation[task_id] = {
                "allocated_at": datetime.now().isoformat(),
                "agents": resource_plan.get("agents", {}),
                "tools": resource_plan.get("tools", []),
                "budget": resource_plan.get("budget", 0.0),
                "timeline": resource_plan.get("timeline", {}),
                "constraints": resource_plan.get("constraints", [])
            }
            
            # Update agent availability
            for agent_id, allocation in resource_plan.get("agents", {}).items():
                if agent_id in self.agent_capabilities:
                    agent = self.agent_capabilities[agent_id]
                    agent.current_workload += allocation.get("hours", 0.0)
            
            task.status = TaskStatus.PLANNED
            task.updated_at = datetime.now().isoformat()
            
            logging.info(f"📋 Agent-2: Allocated resources for task '{task.title}'")
            return True
    
    def update_task_progress(self, task_id: str, agent: str, 
                           progress: float, actual_hours: float = 0.0,
                           notes: str = None) -> bool:
        """
        Update task progress for a specific agent.
        
        Args:
            task_id: Task identifier
            agent: Agent updating progress
            progress: Progress percentage (0.0 to 1.0)
            actual_hours: Actual hours worked
            notes: Progress notes
        
        Returns:
            Success status
        """
        with self._lock:
            if task_id not in self.tasks:
                logging.warning(f"⚠️ Task '{task_id}' not found")
                return False
            
            task = self.tasks[task_id]
            if agent not in task.agents:
                logging.warning(f"⚠️ Agent '{agent}' not assigned to task '{task_id}'")
                return False
            
            # Update progress
            old_progress = task.progress
            task.progress = progress
            task.actual_hours += actual_hours
            task.updated_at = datetime.now().isoformat()
            
            # Update status based on progress
            if progress >= 1.0:
                task.status = TaskStatus.COMPLETED
                logging.info(f"🎉 Task '{task.title}' completed by {agent}!")
            elif progress > 0.0 and task.status == TaskStatus.CREATED:
                task.status = TaskStatus.IN_PROGRESS
            
            # Update completion metrics
            if task_id not in self.completion_metrics:
                self.completion_metrics[task_id] = {
                    "started_at": datetime.now().isoformat(),
                    "agent_progress": {},
                    "milestones": []
                }
            
            self.completion_metrics[task_id]["agent_progress"][agent] = {
                "progress": progress,
                "hours": actual_hours,
                "notes": notes,
                "updated_at": datetime.now().isoformat()
            }
            
            logging.info(f"📊 Agent-2: Updated progress for task '{task.title}' - {agent}: {progress:.1%}")
            return True
    
    def optimize_workflow(self, workflow_id: str = None) -> Dict[str, Any]:
        """
        Optimize workflow efficiency (Agent-2 workflow optimization).
        
        Args:
            workflow_id: Specific workflow to optimize, or None for all
        
        Returns:
            Optimization results
        """
        with self._lock:
            optimization_results = {
                "workflows_optimized": 0,
                "efficiency_improvements": [],
                "resource_reallocations": [],
                "timeline_optimizations": []
            }
            
            # Analyze current workflows
            workflows_to_optimize = [workflow_id] if workflow_id else list(self.workflows.keys())
            
            for wf_id in workflows_to_optimize:
                if wf_id not in self.workflows:
                    continue
                
                workflow = self.workflows[wf_id]
                
                # Identify bottlenecks
                bottlenecks = self._identify_bottlenecks(wf_id)
                
                # Optimize resource allocation
                resource_optimizations = self._optimize_resource_allocation(wf_id)
                
                # Optimize timeline
                timeline_optimizations = self._optimize_timeline(wf_id)
                
                if bottlenecks or resource_optimizations or timeline_optimizations:
                    optimization_results["workflows_optimized"] += 1
                    optimization_results["efficiency_improvements"].extend(bottlenecks)
                    optimization_results["resource_reallocations"].extend(resource_optimizations)
                    optimization_results["timeline_optimizations"].extend(timeline_optimizations)
            
            logging.info(f"📋 Agent-2: Optimized {optimization_results['workflows_optimized']} workflows")
            return optimization_results
    
    def _identify_bottlenecks(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Identify workflow bottlenecks."""
        bottlenecks = []
        
        # Analyze task dependencies and critical paths
        workflow_tasks = [t for t in self.tasks.values() if t.tags and 'workflow' in t.tags]
        
        for task in workflow_tasks:
            # Check for blocked tasks
            if task.status == TaskStatus.BLOCKED:
                bottlenecks.append({
                    "type": "blocked_task",
                    "task_id": task.task_id,
                    "description": f"Task '{task.title}' is blocked",
                    "severity": "high" if task.priority in [TaskPriority.HIGH, TaskPriority.CRITICAL] else "medium"
                })
            
            # Check for resource conflicts
            if task.agents:
                for agent in task.agents:
                    if agent in self.agent_capabilities:
                        agent_cap = self.agent_capabilities[agent]
                        if agent_cap.current_workload > agent_cap.availability_hours * 0.8:
                            bottlenecks.append({
                                "type": "resource_overload",
                                "agent_id": agent,
                                "description": f"Agent {agent} is overloaded",
                                "severity": "high"
                            })
        
        return bottlenecks
    
    def _optimize_resource_allocation(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Optimize resource allocation for a workflow."""
        optimizations = []
        
        # Rebalance agent workloads
        for agent_id, capability in self.agent_capabilities.items():
            if capability.current_workload > capability.availability_hours * 0.9:
                # Find tasks that can be reassigned
                reassignable_tasks = [
                    t for t in self.tasks.values()
                    if agent_id in t.agents and t.status in [TaskStatus.CREATED, TaskStatus.PLANNED]
                ]
                
                for task in reassignable_tasks:
                    # Find alternative agents
                    alternative_agents = [
                        a for a in self.agent_capabilities.keys()
                        if a != agent_id and a not in task.agents
                        and self.agent_capabilities[a].current_workload < self.agent_capabilities[a].availability_hours * 0.7
                    ]
                    
                    if alternative_agents:
                        optimizations.append({
                            "type": "workload_rebalancing",
                            "task_id": task.task_id,
                            "from_agent": agent_id,
                            "to_agent": alternative_agents[0],
                            "reason": "Overload prevention"
                        })
        
        return optimizations
    
    def _optimize_timeline(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Optimize workflow timeline."""
        optimizations = []
        
        # Identify critical path delays
        critical_tasks = [t for t in self.tasks.values() 
                         if t.priority in [TaskPriority.HIGH, TaskPriority.CRITICAL]
                         and t.status in [TaskStatus.CREATED, TaskStatus.PLANNED]]
        
        for task in critical_tasks:
            if task.deadline:
                deadline = datetime.fromisoformat(task.deadline)
                estimated_completion = datetime.now() + timedelta(hours=task.estimated_hours)
                
                if estimated_completion > deadline:
                    optimizations.append({
                        "type": "timeline_optimization",
                        "task_id": task.task_id,
                        "description": f"Task '{task.title}' may miss deadline",
                        "suggestion": "Increase priority or add resources"
                    })
        
        return optimizations
    
    def get_workflow_summary(self) -> Dict[str, Any]:
        """Get comprehensive workflow summary (Agent-2 reporting)."""
        with self._lock:
            total_tasks = len(self.tasks)
            completed_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED])
            in_progress_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS])
            blocked_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.BLOCKED])
            
            # Calculate efficiency metrics
            total_estimated_hours = sum(t.estimated_hours for t in self.tasks.values())
            total_actual_hours = sum(t.actual_hours for t in self.tasks.values())
            efficiency = (total_estimated_hours / max(total_actual_hours, 1)) if total_actual_hours > 0 else 1.0
            
            # Resource utilization
            agent_utilization = {}
            for agent_id, capability in self.agent_capabilities.items():
                utilization = capability.current_workload / max(capability.availability_hours, 1)
                agent_utilization[agent_id] = min(utilization, 1.0)
            
            avg_utilization = sum(agent_utilization.values()) / max(len(agent_utilization), 1)
            
            summary = {
                "workflow_status": "ACTIVE",
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "in_progress_tasks": in_progress_tasks,
                "blocked_tasks": blocked_tasks,
                "completion_rate": completed_tasks / max(total_tasks, 1),
                "efficiency_score": efficiency,
                "average_resource_utilization": avg_utilization,
                "active_workflows": len(self.workflows),
                "resource_conflicts": len(self.resource_conflicts),
                "last_optimized": datetime.now().isoformat()
            }
            
            return summary
    
    def _save_data(self):
        """Save task management data to persistent storage."""
        try:
            # Save tasks
            tasks_data = {tid: asdict(task) for tid, task in self.tasks.items()}
            with open(self.data_path / 'tasks.json', 'w') as f:
                json.dump(tasks_data, f, indent=2)
            
            # Save agent capabilities
            capabilities_data = {aid: asdict(cap) for aid, cap in self.agent_capabilities.items()}
            with open(self.data_path / 'agent_capabilities.json', 'w') as f:
                json.dump(capabilities_data, f, indent=2)
            
            # Save workflows
            with open(self.data_path / 'workflows.json', 'w') as f:
                json.dump(self.workflows, f, indent=2)
                
        except Exception as e:
            logging.error(f"❌ Failed to save task management data: {e}")
    
    def __str__(self):
        """String representation of task management status."""
        summary = self.get_workflow_summary()
        return (f"📋 Collaborative Task Manager - "
                f"Status: {summary['workflow_status']}, "
                f"Tasks: {summary['completed_tasks']}/{summary['total_tasks']} completed, "
                f"Efficiency: {summary['efficiency_score']:.2f}")


# Global instance for system-wide access
collaborative_task_manager = CollaborativeTaskManager()




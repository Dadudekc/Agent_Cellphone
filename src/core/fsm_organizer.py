#!/usr/bin/env python3
"""
FSM Organizer - Finite State Machine based workflow and task management
Manages agentic workflows, project states, and task tracking for Jarvis
"""

import time
import logging
import threading
import json
import os
from typing import Dict, List, Optional, Callable, Any
from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import uuid

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ProjectStatus(Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class WorkflowType(Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"
    RESEARCH = "research"
    DEBUGGING = "debugging"
    OPTIMIZATION = "optimization"

@dataclass
class Task:
    id: str
    name: str
    description: str
    priority: TaskPriority
    status: TaskStatus
    project_id: str
    workflow_id: str
    assigned_agent: Optional[str] = None
    dependencies: List[str] = None
    estimated_duration: Optional[int] = None  # minutes
    actual_duration: Optional[int] = None
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    tags: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class Project:
    id: str
    name: str
    description: str
    status: ProjectStatus
    tasks: List[str] = None  # Task IDs
    workflows: List[str] = None  # Workflow IDs
    created_at: datetime = None
    updated_at: datetime = None
    deadline: Optional[datetime] = None
    tags: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.tasks is None:
            self.tasks = []
        if self.workflows is None:
            self.workflows = []
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

@dataclass
class Workflow:
    id: str
    name: str
    description: str
    workflow_type: WorkflowType
    project_id: str
    tasks: List[str] = None  # Task IDs
    current_task_index: int = 0
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.tasks is None:
            self.tasks = []
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.now()

class FSMOrganizer:
    """
    Finite State Machine based organizer for managing workflows, projects, and tasks
    """
    
    def __init__(self, storage_path: str = "fsm_data"):
        self.logger = logging.getLogger("FSMOrganizer")
        self.storage_path = storage_path
        
        # Initialize storage
        self._init_storage()
        
        # State containers
        self.projects: Dict[str, Project] = {}
        self.tasks: Dict[str, Task] = {}
        self.workflows: Dict[str, Workflow] = {}
        
        # Load existing data
        self._load_data()
        
        # Event callbacks
        self.event_callbacks: Dict[str, List[Callable]] = {
            'task_created': [],
            'task_started': [],
            'task_completed': [],
            'task_failed': [],
            'project_created': [],
            'project_updated': [],
            'workflow_started': [],
            'workflow_completed': []
        }
        
        # Auto-save thread
        self.auto_save_thread = threading.Thread(target=self._auto_save_loop, daemon=True)
        self.auto_save_thread.start()
        
        self.logger.info("FSM Organizer initialized")
    
    def _init_storage(self):
        """Initialize storage directories"""
        os.makedirs(self.storage_path, exist_ok=True)
        os.makedirs(os.path.join(self.storage_path, "projects"), exist_ok=True)
        os.makedirs(os.path.join(self.storage_path, "tasks"), exist_ok=True)
        os.makedirs(os.path.join(self.storage_path, "workflows"), exist_ok=True)
    
    def _load_data(self):
        """Load existing data from storage"""
        try:
            # Load projects
            projects_dir = os.path.join(self.storage_path, "projects")
            for filename in os.listdir(projects_dir):
                if filename.endswith('.json'):
                    with open(os.path.join(projects_dir, filename), 'r') as f:
                        data = json.load(f)
                        project = Project(**data)
                        self.projects[project.id] = project
            
            # Load tasks
            tasks_dir = os.path.join(self.storage_path, "tasks")
            for filename in os.listdir(tasks_dir):
                if filename.endswith('.json'):
                    with open(os.path.join(tasks_dir, filename), 'r') as f:
                        data = json.load(f)
                        task = Task(**data)
                        self.tasks[task.id] = task
            
            # Load workflows
            workflows_dir = os.path.join(self.storage_path, "workflows")
            for filename in os.listdir(workflows_dir):
                if filename.endswith('.json'):
                    with open(os.path.join(workflows_dir, filename), 'r') as f:
                        data = json.load(f)
                        workflow = Workflow(**data)
                        self.workflows[workflow.id] = workflow
            
            self.logger.info(f"Loaded {len(self.projects)} projects, {len(self.tasks)} tasks, {len(self.workflows)} workflows")
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
    
    def _save_data(self):
        """Save data to storage"""
        try:
            # Save projects
            for project in self.projects.values():
                filename = os.path.join(self.storage_path, "projects", f"{project.id}.json")
                with open(filename, 'w') as f:
                    json.dump(asdict(project), f, indent=2, default=str)
            
            # Save tasks
            for task in self.tasks.values():
                filename = os.path.join(self.storage_path, "tasks", f"{task.id}.json")
                with open(filename, 'w') as f:
                    json.dump(asdict(task), f, indent=2, default=str)
            
            # Save workflows
            for workflow in self.workflows.values():
                filename = os.path.join(self.storage_path, "workflows", f"{workflow.id}.json")
                with open(filename, 'w') as f:
                    json.dump(asdict(workflow), f, indent=2, default=str)
            
            self.logger.debug("Data saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving data: {e}")
    
    def _auto_save_loop(self):
        """Auto-save loop"""
        while True:
            time.sleep(30)  # Save every 30 seconds
            self._save_data()
    
    def add_event_callback(self, event_type: str, callback: Callable):
        """Add event callback"""
        if event_type in self.event_callbacks:
            self.event_callbacks[event_type].append(callback)
    
    def _trigger_event(self, event_type: str, data: Dict[str, Any]):
        """Trigger event callbacks"""
        if event_type in self.event_callbacks:
            for callback in self.event_callbacks[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    self.logger.error(f"Event callback error: {e}")
    
    # Project Management
    def create_project(self, name: str, description: str, tags: List[str] = None, deadline: Optional[datetime] = None) -> str:
        """Create a new project"""
        project_id = str(uuid.uuid4())
        project = Project(
            id=project_id,
            name=name,
            description=description,
            status=ProjectStatus.PLANNING,
            tags=tags or [],
            deadline=deadline
        )
        
        self.projects[project_id] = project
        self._trigger_event('project_created', {'project_id': project_id, 'project': project})
        self.logger.info(f"Created project: {name} ({project_id})")
        return project_id
    
    def update_project_status(self, project_id: str, status: ProjectStatus):
        """Update project status"""
        if project_id in self.projects:
            project = self.projects[project_id]
            project.status = status
            project.updated_at = datetime.now()
            self._trigger_event('project_updated', {'project_id': project_id, 'project': project})
            self.logger.info(f"Updated project {project_id} status to {status.value}")
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """Get project by ID"""
        return self.projects.get(project_id)
    
    def get_projects_by_status(self, status: ProjectStatus) -> List[Project]:
        """Get projects by status"""
        return [p for p in self.projects.values() if p.status == status]
    
    # Task Management
    def create_task(self, name: str, description: str, project_id: str, workflow_id: str,
                   priority: TaskPriority = TaskPriority.MEDIUM, estimated_duration: Optional[int] = None,
                   dependencies: List[str] = None, tags: List[str] = None) -> str:
        """Create a new task"""
        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            name=name,
            description=description,
            priority=priority,
            status=TaskStatus.PENDING,
            project_id=project_id,
            workflow_id=workflow_id,
            dependencies=dependencies or [],
            estimated_duration=estimated_duration,
            tags=tags or []
        )
        
        self.tasks[task_id] = task
        
        # Add to project
        if project_id in self.projects:
            self.projects[project_id].tasks.append(task_id)
        
        # Add to workflow
        if workflow_id in self.workflows:
            self.workflows[workflow_id].tasks.append(task_id)
        
        self._trigger_event('task_created', {'task_id': task_id, 'task': task})
        self.logger.info(f"Created task: {name} ({task_id})")
        return task_id
    
    def start_task(self, task_id: str, assigned_agent: Optional[str] = None):
        """Start a task"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = TaskStatus.IN_PROGRESS
            task.started_at = datetime.now()
            if assigned_agent:
                task.assigned_agent = assigned_agent
            
            self._trigger_event('task_started', {'task_id': task_id, 'task': task})
            self.logger.info(f"Started task: {task.name} ({task_id})")
    
    def complete_task(self, task_id: str):
        """Complete a task"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            
            if task.started_at:
                duration = (task.completed_at - task.started_at).total_seconds() / 60
                task.actual_duration = int(duration)
            
            self._trigger_event('task_completed', {'task_id': task_id, 'task': task})
            self.logger.info(f"Completed task: {task.name} ({task_id})")
    
    def fail_task(self, task_id: str, reason: str = None):
        """Mark task as failed"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = TaskStatus.FAILED
            if reason:
                task.metadata['failure_reason'] = reason
            
            self._trigger_event('task_failed', {'task_id': task_id, 'task': task})
            self.logger.info(f"Failed task: {task.name} ({task_id}) - {reason}")
    
    def get_ready_tasks(self) -> List[Task]:
        """Get tasks that are ready to start (dependencies met)"""
        ready_tasks = []
        for task in self.tasks.values():
            if task.status == TaskStatus.PENDING:
                # Check if all dependencies are completed
                dependencies_met = True
                for dep_id in task.dependencies:
                    if dep_id in self.tasks:
                        dep_task = self.tasks[dep_id]
                        if dep_task.status != TaskStatus.COMPLETED:
                            dependencies_met = False
                            break
                
                if dependencies_met:
                    ready_tasks.append(task)
        
        return sorted(ready_tasks, key=lambda t: t.priority.value, reverse=True)
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Get tasks by status"""
        return [t for t in self.tasks.values() if t.status == status]
    
    def get_tasks_by_priority(self, priority: TaskPriority) -> List[Task]:
        """Get tasks by priority"""
        return [t for t in self.tasks.values() if t.priority == priority]
    
    # Workflow Management
    def create_workflow(self, name: str, description: str, workflow_type: WorkflowType, project_id: str) -> str:
        """Create a new workflow"""
        workflow_id = str(uuid.uuid4())
        workflow = Workflow(
            id=workflow_id,
            name=name,
            description=description,
            workflow_type=workflow_type,
            project_id=project_id
        )
        
        self.workflows[workflow_id] = workflow
        
        # Add to project
        if project_id in self.projects:
            self.projects[project_id].workflows.append(workflow_id)
        
        self.logger.info(f"Created workflow: {name} ({workflow_id})")
        return workflow_id
    
    def start_workflow(self, workflow_id: str):
        """Start a workflow"""
        if workflow_id in self.workflows:
            workflow = self.workflows[workflow_id]
            workflow.status = TaskStatus.IN_PROGRESS
            workflow.started_at = datetime.now()
            
            # Start the first task if available
            if workflow.tasks:
                first_task_id = workflow.tasks[0]
                if first_task_id in self.tasks:
                    self.start_task(first_task_id)
            
            self._trigger_event('workflow_started', {'workflow_id': workflow_id, 'workflow': workflow})
            self.logger.info(f"Started workflow: {workflow.name} ({workflow_id})")
    
    def advance_workflow(self, workflow_id: str):
        """Advance to next task in workflow"""
        if workflow_id in self.workflows:
            workflow = self.workflows[workflow_id]
            
            # Complete current task
            if workflow.current_task_index < len(workflow.tasks):
                current_task_id = workflow.tasks[workflow.current_task_index]
                if current_task_id in self.tasks:
                    self.complete_task(current_task_id)
            
            # Move to next task
            workflow.current_task_index += 1
            
            if workflow.current_task_index < len(workflow.tasks):
                # Start next task
                next_task_id = workflow.tasks[workflow.current_task_index]
                if next_task_id in self.tasks:
                    self.start_task(next_task_id)
            else:
                # Workflow completed
                workflow.status = TaskStatus.COMPLETED
                workflow.completed_at = datetime.now()
                self._trigger_event('workflow_completed', {'workflow_id': workflow_id, 'workflow': workflow})
                self.logger.info(f"Completed workflow: {workflow.name} ({workflow_id})")
    
    def get_active_workflows(self) -> List[Workflow]:
        """Get active workflows"""
        return [w for w in self.workflows.values() if w.status == TaskStatus.IN_PROGRESS]
    
    # Reporting and Analytics
    def get_project_progress(self, project_id: str) -> Dict[str, Any]:
        """Get project progress report"""
        if project_id not in self.projects:
            return {}
        
        project = self.projects[project_id]
        project_tasks = [t for t in self.tasks.values() if t.project_id == project_id]
        
        total_tasks = len(project_tasks)
        completed_tasks = len([t for t in project_tasks if t.status == TaskStatus.COMPLETED])
        in_progress_tasks = len([t for t in project_tasks if t.status == TaskStatus.IN_PROGRESS])
        failed_tasks = len([t for t in project_tasks if t.status == TaskStatus.FAILED])
        
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            'project_id': project_id,
            'project_name': project.name,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'in_progress_tasks': in_progress_tasks,
            'failed_tasks': failed_tasks,
            'progress_percentage': progress,
            'status': project.status.value
        }
    
    def get_system_overview(self) -> Dict[str, Any]:
        """Get system overview"""
        total_projects = len(self.projects)
        total_tasks = len(self.tasks)
        total_workflows = len(self.workflows)
        
        active_projects = len([p for p in self.projects.values() if p.status == ProjectStatus.ACTIVE])
        pending_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.PENDING])
        in_progress_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS])
        completed_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED])
        
        return {
            'total_projects': total_projects,
            'active_projects': active_projects,
            'total_tasks': total_tasks,
            'pending_tasks': pending_tasks,
            'in_progress_tasks': in_progress_tasks,
            'completed_tasks': completed_tasks,
            'total_workflows': total_workflows,
            'active_workflows': len(self.get_active_workflows())
        }
    
    def get_high_priority_tasks(self) -> List[Task]:
        """Get high priority tasks"""
        return [t for t in self.tasks.values() 
                if t.priority in [TaskPriority.HIGH, TaskPriority.CRITICAL] 
                and t.status in [TaskStatus.PENDING, TaskStatus.IN_PROGRESS]]
    
    def get_overdue_tasks(self) -> List[Task]:
        """Get overdue tasks (estimated duration exceeded)"""
        overdue_tasks = []
        for task in self.tasks.values():
            if task.status == TaskStatus.IN_PROGRESS and task.started_at and task.estimated_duration:
                elapsed_minutes = (datetime.now() - task.started_at).total_seconds() / 60
                if elapsed_minutes > task.estimated_duration:
                    overdue_tasks.append(task)
        return overdue_tasks
    
    def cleanup_completed_projects(self, days_old: int = 30):
        """Archive completed projects older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        archived_count = 0
        
        for project in self.projects.values():
            if (project.status == ProjectStatus.COMPLETED and 
                project.updated_at and project.updated_at < cutoff_date):
                project.status = ProjectStatus.ARCHIVED
                archived_count += 1
        
        if archived_count > 0:
            self.logger.info(f"Archived {archived_count} old completed projects")
    
    def close(self):
        """Close the organizer and save data"""
        self._save_data()
        self.logger.info("FSM Organizer closed")

# Example usage and testing
if __name__ == "__main__":
    # Create organizer
    organizer = FSMOrganizer()
    
    # Create a project
    project_id = organizer.create_project(
        name="Jarvis Enhancement",
        description="Enhance Jarvis with FSM-based workflow management",
        tags=["jarvis", "enhancement", "workflow"]
    )
    
    # Create a workflow
    workflow_id = organizer.create_workflow(
        name="Development Workflow",
        description="Standard development workflow",
        workflow_type=WorkflowType.DEVELOPMENT,
        project_id=project_id
    )
    
    # Create tasks
    task1_id = organizer.create_task(
        name="Design FSM Structure",
        description="Design the FSM structure for workflow management",
        project_id=project_id,
        workflow_id=workflow_id,
        priority=TaskPriority.HIGH,
        estimated_duration=120
    )
    
    task2_id = organizer.create_task(
        name="Implement FSM Logic",
        description="Implement the FSM logic and state transitions",
        project_id=project_id,
        workflow_id=workflow_id,
        priority=TaskPriority.HIGH,
        estimated_duration=180,
        dependencies=[task1_id]
    )
    
    task3_id = organizer.create_task(
        name="Test FSM System",
        description="Test the FSM system with various scenarios",
        project_id=project_id,
        workflow_id=workflow_id,
        priority=TaskPriority.MEDIUM,
        estimated_duration=90,
        dependencies=[task2_id]
    )
    
    # Start workflow
    organizer.start_workflow(workflow_id)
    
    # Get system overview
    overview = organizer.get_system_overview()
    print("System Overview:", overview)
    
    # Get project progress
    progress = organizer.get_project_progress(project_id)
    print("Project Progress:", progress)
    
    # Close organizer
    organizer.close() 
#!/usr/bin/env python3
"""
🤝 ENHANCED AGENT COORDINATION FRAMEWORK v2.0
==============================================
Advanced agent coordination with improved collaboration, task management,
and coordination protocols for seamless multi-agent operations.
"""

import os
import sys
import json
import time
import threading
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import queue
import uuid
import asyncio

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.services.agent_cell_phone import AgentCellPhone, MsgTag
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)

class TaskPriority(Enum):
    """Task priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"
    PRESIDENTIAL = "presidential"

class TaskStatus(Enum):
    """Task status states"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    REVIEW = "review"
    COMPLETED = "completed"
    FAILED = "failed"

class CoordinationMode(Enum):
    """Coordination modes for different scenarios"""
    HIERARCHICAL = "hierarchical"      # Top-down coordination
    COLLABORATIVE = "collaborative"    # Peer-to-peer collaboration
    DEMOCRATIC = "democratic"          # Voting-based decisions
    EMERGENCY = "emergency"            # Crisis response mode
    INNOVATION = "innovation"          # Creative problem solving

class AgentRole(Enum):
    """Agent roles in coordination"""
    COORDINATOR = "coordinator"        # Leads coordination
    EXECUTOR = "executor"              # Executes tasks
    REVIEWER = "reviewer"              # Reviews work
    SUPPORT = "support"                # Provides assistance
    OBSERVER = "observer"              # Monitors progress

@dataclass
class CoordinationTask:
    """Task structure for coordination"""
    task_id: str
    title: str
    description: str
    priority: TaskPriority
    status: TaskStatus
    assigned_agents: List[str]
    dependencies: List[str]
    created_at: datetime
    due_date: Optional[datetime]
    estimated_hours: float
    actual_hours: float
    progress_percentage: float
    tags: List[str]
    metadata: Dict[str, Any]

@dataclass
class CollaborationSession:
    """Collaboration session for agents working together"""
    session_id: str
    title: str
    objective: str
    participating_agents: List[str]
    session_type: str
    start_time: datetime
    end_time: Optional[datetime]
    status: str
    achievements: List[str]
    challenges: List[str]
    next_steps: List[str]
    session_notes: str

@dataclass
class CoordinationProtocol:
    """Coordination protocol definition"""
    protocol_id: str
    name: str
    description: str
    coordination_mode: CoordinationMode
    required_agents: List[str]
    steps: List[Dict[str, Any]]
    success_criteria: List[str]
    fallback_protocols: List[str]
    is_active: bool

class TaskManager:
    """Manages task assignment, tracking, and completion"""
    
    def __init__(self, agent_cellphone: AgentCellPhone):
        self.acp = agent_cellphone
        self.logger = logging.getLogger(__name__)
        
        # Task storage
        self.tasks: Dict[str, CoordinationTask] = {}
        self.task_queue = queue.PriorityQueue()
        self.completed_tasks: List[CoordinationTask] = []
        
        # Agent workload tracking
        self.agent_workloads: Dict[str, Dict[str, Any]] = {}
        
        # Task dependencies
        self.task_dependencies: Dict[str, List[str]] = {}
        self.blocked_tasks: List[str] = []
    
    def create_task(self, task_data: Dict[str, Any]) -> str:
        """Create a new coordination task"""
        try:
            task_id = str(uuid.uuid4())
            
            task = CoordinationTask(
                task_id=task_id,
                title=task_data["title"],
                description=task_data["description"],
                priority=TaskPriority(task_data["priority"]),
                status=TaskStatus.PENDING,
                assigned_agents=task_data.get("assigned_agents", []),
                dependencies=task_data.get("dependencies", []),
                created_at=datetime.now(),
                due_date=datetime.fromisoformat(task_data["due_date"]) if task_data.get("due_date") else None,
                estimated_hours=task_data.get("estimated_hours", 1.0),
                actual_hours=0.0,
                progress_percentage=0.0,
                tags=task_data.get("tags", []),
                metadata=task_data.get("metadata", {})
            )
            
            self.tasks[task_id] = task
            
            # Add to priority queue
            priority_value = self._get_priority_value(task.priority)
            self.task_queue.put((priority_value, task_id))
            
            # Check dependencies
            if task.dependencies:
                self._check_task_dependencies(task_id)
            
            self.logger.info(f"✅ Task created: {task.title} (ID: {task_id})")
            return task_id
            
        except Exception as e:
            self.logger.error(f"Failed to create task: {e}")
            return None
    
    def _get_priority_value(self, priority: TaskPriority) -> int:
        """Convert priority to numeric value for queue ordering"""
        priority_map = {
            TaskPriority.LOW: 1,
            TaskPriority.NORMAL: 2,
            TaskPriority.HIGH: 3,
            TaskPriority.CRITICAL: 4,
            TaskPriority.PRESIDENTIAL: 5
        }
        return priority_map.get(priority, 2)
    
    def _check_task_dependencies(self, task_id: str):
        """Check if task dependencies are satisfied"""
        task = self.tasks[task_id]
        
        if not task.dependencies:
            return
        
        # Check if all dependencies are completed
        dependencies_completed = all(
            dep_id in [t.task_id for t in self.completed_tasks]
            for dep_id in task.dependencies
        )
        
        if not dependencies_completed:
            # Task is blocked
            task.status = TaskStatus.BLOCKED
            self.blocked_tasks.append(task_id)
            self.logger.info(f"⚠️ Task {task.title} is blocked by dependencies")
        else:
            # Dependencies satisfied, task can proceed
            task.status = TaskStatus.PENDING
            if task_id in self.blocked_tasks:
                self.blocked_tasks.remove(task_id)
            self.logger.info(f"✅ Task {task.title} dependencies satisfied")
    
    def assign_task(self, task_id: str, agent_id: str) -> bool:
        """Assign a task to an agent"""
        try:
            if task_id not in self.tasks:
                self.logger.warning(f"Task {task_id} not found")
                return False
            
            task = self.tasks[task_id]
            
            if task.status != TaskStatus.PENDING:
                self.logger.warning(f"Task {task_id} is not in pending status")
                return False
            
            # Add agent to assigned agents
            if agent_id not in task.assigned_agents:
                task.assigned_agents.append(agent_id)
            
            # Update task status
            task.status = TaskStatus.ASSIGNED
            
            # Update agent workload
            self._update_agent_workload(agent_id, task_id, "assigned")
            
            # Notify agent
            self._notify_task_assignment(task, agent_id)
            
            self.logger.info(f"✅ Task {task.title} assigned to {agent_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to assign task: {e}")
            return False
    
    def _update_agent_workload(self, agent_id: str, task_id: str, action: str):
        """Update agent workload tracking"""
        if agent_id not in self.agent_workloads:
            self.agent_workloads[agent_id] = {
                "assigned_tasks": [],
                "active_tasks": [],
                "completed_tasks": [],
                "total_hours": 0.0,
                "current_capacity": 100.0
            }
        
        workload = self.agent_workloads[agent_id]
        
        if action == "assigned":
            if task_id not in workload["assigned_tasks"]:
                workload["assigned_tasks"].append(task_id)
        elif action == "started":
            if task_id in workload["assigned_tasks"]:
                workload["assigned_tasks"].remove(task_id)
            if task_id not in workload["active_tasks"]:
                workload["active_tasks"].append(task_id)
        elif action == "completed":
            if task_id in workload["active_tasks"]:
                workload["active_tasks"].remove(task_id)
            if task_id not in workload["completed_tasks"]:
                workload["completed_tasks"].append(task_id)
    
    def _notify_task_assignment(self, task: CoordinationTask, agent_id: str):
        """Notify agent of task assignment"""
        try:
            message = f"📋 TASK ASSIGNED: {task.title}\n\n{task.description}\n\nPriority: {task.priority.value.upper()}\nDue: {task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else 'No due date'}"
            
            self.acp.send_message(
                agent_id,
                message,
                MsgTag.INFO
            )
        except Exception as e:
            self.logger.error(f"Failed to notify task assignment: {e}")
    
    def update_task_progress(self, task_id: str, progress_percentage: float, notes: str = "") -> bool:
        """Update task progress"""
        try:
            if task_id not in self.tasks:
                return False
            
            task = self.tasks[task_id]
            old_progress = task.progress_percentage
            task.progress_percentage = min(progress_percentage, 100.0)
            
            # Update status based on progress
            if task.progress_percentage == 100.0:
                task.status = TaskStatus.COMPLETED
                self._complete_task(task_id)
            elif task.progress_percentage > 0 and task.status == TaskStatus.ASSIGNED:
                task.status = TaskStatus.IN_PROGRESS
            
            # Log progress update
            self.logger.info(f"📈 Task {task.title} progress: {old_progress}% → {task.progress_percentage}%")
            
            # Notify stakeholders
            self._notify_progress_update(task, old_progress, task.progress_percentage)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update task progress: {e}")
            return False
    
    def _complete_task(self, task_id: str):
        """Mark task as completed"""
        task = self.tasks[task_id]
        
        # Move to completed tasks
        self.completed_tasks.append(task)
        del self.tasks[task_id]
        
        # Update agent workloads
        for agent_id in task.assigned_agents:
            self._update_agent_workload(agent_id, task_id, "completed")
        
        # Check blocked tasks for dependency resolution
        self._check_blocked_tasks()
        
        self.logger.info(f"🎉 Task completed: {task.title}")
    
    def _check_blocked_tasks(self):
        """Check if any blocked tasks can now proceed"""
        for task_id in self.blocked_tasks[:]:  # Copy list to avoid modification during iteration
            self._check_task_dependencies(task_id)
    
    def _notify_progress_update(self, task: CoordinationTask, old_progress: float, new_progress: float):
        """Notify stakeholders of progress update"""
        try:
            message = f"📈 PROGRESS UPDATE: {task.title}\n\nProgress: {old_progress}% → {new_progress}%\nStatus: {task.status.value}"
            
            # Notify assigned agents
            for agent_id in task.assigned_agents:
                self.acp.send_message(
                    agent_id,
                    message,
                    MsgTag.INFO
                )
            
            # Notify coordinators if significant progress
            if new_progress - old_progress >= 25:
                self.acp.send_message(
                    "ALL",
                    f"🎯 Significant progress on {task.title}: {new_progress}% complete",
                    MsgTag.INFO
                )
                
        except Exception as e:
            self.logger.error(f"Failed to notify progress update: {e}")
    
    def get_agent_tasks(self, agent_id: str) -> List[CoordinationTask]:
        """Get all tasks assigned to an agent"""
        return [
            task for task in self.tasks.values()
            if agent_id in task.assigned_agents
        ]
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive task status"""
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        return {
            "task_id": task.task_id,
            "title": task.title,
            "status": task.status.value,
            "progress": task.progress_percentage,
            "assigned_agents": task.assigned_agents,
            "dependencies": task.dependencies,
            "is_blocked": task_id in self.blocked_tasks
        }

class CollaborationManager:
    """Manages collaboration sessions between agents"""
    
    def __init__(self, agent_cellphone: AgentCellPhone):
        self.acp = agent_cellphone
        self.logger = logging.getLogger(__name__)
        
        # Active collaboration sessions
        self.active_sessions: Dict[str, CollaborationSession] = {}
        self.session_history: List[CollaborationSession] = []
        
        # Collaboration templates
        self.collaboration_templates = {
            "brainstorming": {
                "duration": timedelta(hours=1),
                "max_participants": 5,
                "structure": ["introduction", "idea_generation", "discussion", "consolidation"]
            },
            "problem_solving": {
                "duration": timedelta(hours=2),
                "max_participants": 4,
                "structure": ["problem_definition", "analysis", "solution_generation", "evaluation"]
            },
            "code_review": {
                "duration": timedelta(hours=1.5),
                "max_participants": 3,
                "structure": ["code_overview", "review", "feedback", "action_items"]
            },
            "planning": {
                "duration": timedelta(hours=1.5),
                "max_participants": 6,
                "structure": ["objective_setting", "planning", "resource_allocation", "timeline"]
            }
        }
    
    def create_collaboration_session(self, session_data: Dict[str, Any]) -> str:
        """Create a new collaboration session"""
        try:
            session_id = str(uuid.uuid4())
            
            session = CollaborationSession(
                session_id=session_id,
                title=session_data["title"],
                objective=session_data["objective"],
                participating_agents=session_data["participating_agents"],
                session_type=session_data["session_type"],
                start_time=datetime.now(),
                end_time=None,
                status="active",
                achievements=[],
                challenges=[],
                next_steps=[],
                session_notes=""
            )
            
            self.active_sessions[session_id] = session
            
            # Notify participants
            self._notify_session_creation(session)
            
            self.logger.info(f"🤝 Collaboration session created: {session.title}")
            return session_id
            
        except Exception as e:
            self.logger.error(f"Failed to create collaboration session: {e}")
            return None
    
    def _notify_session_creation(self, session: CollaborationSession):
        """Notify all participants of session creation"""
        try:
            message = f"🤝 COLLABORATION SESSION: {session.title}\n\nObjective: {session.objective}\n\nParticipants: {', '.join(session.participating_agents)}\n\nSession starting now!"
            
            for agent_id in session.participating_agents:
                self.acp.send_message(
                    agent_id,
                    message,
                    MsgTag.INFO
                )
            
            # Notify other agents
            other_agents = [a for a in ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"] if a not in session.participating_agents]
            if other_agents:
                self.acp.send_message(
                    "ALL",
                    f"🤝 New collaboration session: {session.title} with {len(session.participating_agents)} participants",
                    MsgTag.INFO
                )
                
        except Exception as e:
            self.logger.error(f"Failed to notify session creation: {e}")
    
    def update_session_progress(self, session_id: str, achievement: str, challenge: str = "", next_step: str = ""):
        """Update collaboration session progress"""
        try:
            if session_id not in self.active_sessions:
                return False
            
            session = self.active_sessions[session_id]
            
            if achievement:
                session.achievements.append(achievement)
            
            if challenge:
                session.challenges.append(challenge)
            
            if next_step:
                session.next_steps.append(next_step)
            
            # Notify participants of progress
            self._notify_session_progress(session, achievement, challenge, next_step)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update session progress: {e}")
            return False
    
    def _notify_session_progress(self, session: CollaborationSession, achievement: str, challenge: str, next_step: str):
        """Notify participants of session progress"""
        try:
            message = f"📈 SESSION PROGRESS: {session.title}\n\n"
            
            if achievement:
                message += f"✅ Achievement: {achievement}\n\n"
            
            if challenge:
                message += f"⚠️ Challenge: {challenge}\n\n"
            
            if next_step:
                message += f"🎯 Next Step: {next_step}\n\n"
            
            message += f"Session Status: {session.status}"
            
            for agent_id in session.participating_agents:
                self.acp.send_message(
                    agent_id,
                    message,
                    MsgTag.INFO
                )
                
        except Exception as e:
            self.logger.error(f"Failed to notify session progress: {e}")
    
    def end_collaboration_session(self, session_id: str, summary: str = "") -> bool:
        """End a collaboration session"""
        try:
            if session_id not in self.active_sessions:
                return False
            
            session = self.active_sessions[session_id]
            session.end_time = datetime.now()
            session.status = "completed"
            session.session_notes = summary
            
            # Move to history
            self.session_history.append(session)
            del self.active_sessions[session_id]
            
            # Notify participants of completion
            self._notify_session_completion(session)
            
            self.logger.info(f"🏁 Collaboration session ended: {session.title}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to end collaboration session: {e}")
            return False
    
    def _notify_session_completion(self, session: CollaborationSession):
        """Notify participants of session completion"""
        try:
            duration = session.end_time - session.start_time
            duration_str = str(duration).split('.')[0]  # Remove microseconds
            
            message = f"🏁 SESSION COMPLETED: {session.title}\n\n"
            message += f"Duration: {duration_str}\n"
            message += f"Achievements: {len(session.achievements)}\n"
            message += f"Challenges: {len(session.challenges)}\n"
            message += f"Next Steps: {len(session.next_steps)}\n\n"
            
            if session.session_notes:
                message += f"Summary: {session.session_notes}"
            
            for agent_id in session.participating_agents:
                self.acp.send_message(
                    agent_id,
                    message,
                    MsgTag.INFO
                )
                
        except Exception as e:
            self.logger.error(f"Failed to notify session completion: {e}")

class CoordinationProtocolManager:
    """Manages coordination protocols for different scenarios"""
    
    def __init__(self, agent_cellphone: AgentCellPhone):
        self.acp = agent_cellphone
        self.logger = logging.getLogger(__name__)
        
        # Available protocols
        self.protocols: Dict[str, CoordinationProtocol] = {}
        
        # Active protocol executions
        self.active_executions: Dict[str, Dict[str, Any]] = {}
        
        # Initialize default protocols
        self._initialize_default_protocols()
    
    def _initialize_default_protocols(self):
        """Initialize default coordination protocols"""
        default_protocols = [
            {
                "protocol_id": "emergency_response",
                "name": "Emergency Response Protocol",
                "description": "Rapid response coordination for critical situations",
                "coordination_mode": CoordinationMode.EMERGENCY,
                "required_agents": ["Agent-1", "Agent-5"],
                "steps": [
                    {"step": 1, "action": "Assess situation", "agent": "Agent-1"},
                    {"step": 2, "action": "Mobilize resources", "agent": "Agent-5"},
                    {"step": 3, "action": "Execute response", "agent": "ALL"},
                    {"step": 4, "action": "Monitor and adjust", "agent": "Agent-1"}
                ],
                "success_criteria": ["Situation contained", "Resources deployed", "Response executed"],
                "fallback_protocols": ["hierarchical_override"],
                "is_active": True
            },
            {
                "protocol_id": "innovation_session",
                "name": "Innovation Session Protocol",
                "description": "Creative problem-solving coordination",
                "coordination_mode": CoordinationMode.INNOVATION,
                "required_agents": ["Agent-2", "Agent-3", "Agent-4"],
                "steps": [
                    {"step": 1, "action": "Define challenge", "agent": "Agent-2"},
                    {"step": 2, "action": "Generate ideas", "agent": "ALL"},
                    {"step": 3, "action": "Evaluate solutions", "agent": "Agent-3"},
                    {"step": 4, "action": "Plan implementation", "agent": "Agent-4"}
                ],
                "success_criteria": ["Challenge defined", "Ideas generated", "Solution selected"],
                "fallback_protocols": ["collaborative_fallback"],
                "is_active": True
            }
        ]
        
        for protocol_data in default_protocols:
            protocol = CoordinationProtocol(**protocol_data)
            self.protocols[protocol.protocol_id] = protocol
        
        self.logger.info(f"✅ Initialized {len(self.protocols)} default protocols")
    
    def execute_protocol(self, protocol_id: str, context: Dict[str, Any]) -> str:
        """Execute a coordination protocol"""
        try:
            if protocol_id not in self.protocols:
                self.logger.warning(f"Protocol {protocol_id} not found")
                return None
            
            protocol = self.protocols[protocol_id]
            execution_id = str(uuid.uuid4())
            
            # Initialize execution
            self.active_executions[execution_id] = {
                "protocol_id": protocol_id,
                "context": context,
                "current_step": 0,
                "status": "executing",
                "start_time": datetime.now(),
                "step_results": [],
                "participating_agents": protocol.required_agents.copy()
            }
            
            # Notify agents of protocol execution
            self._notify_protocol_execution(protocol, execution_id, context)
            
            # Execute first step
            self._execute_protocol_step(execution_id, 0)
            
            self.logger.info(f"🚀 Protocol {protocol.name} execution started")
            return execution_id
            
        except Exception as e:
            self.logger.error(f"Failed to execute protocol: {e}")
            return None
    
    def _notify_protocol_execution(self, protocol: CoordinationProtocol, execution_id: str, context: Dict[str, Any]):
        """Notify agents of protocol execution"""
        try:
            message = f"🚀 PROTOCOL EXECUTION: {protocol.name}\n\n"
            message += f"Description: {protocol.description}\n"
            message += f"Mode: {protocol.coordination_mode.value}\n"
            message += f"Context: {json.dumps(context, indent=2)}"
            
            for agent_id in protocol.required_agents:
                self.acp.send_message(
                    agent_id,
                    message,
                    MsgTag.IMPORTANT
                )
                
        except Exception as e:
            self.logger.error(f"Failed to notify protocol execution: {e}")
    
    def _execute_protocol_step(self, execution_id: str, step_index: int):
        """Execute a specific protocol step"""
        try:
            execution = self.active_executions[execution_id]
            protocol = self.protocols[execution["protocol_id"]]
            
            if step_index >= len(protocol.steps):
                # Protocol completed
                self._complete_protocol_execution(execution_id)
                return
            
            step = protocol.steps[step_index]
            execution["current_step"] = step_index
            
            # Execute step
            step_result = self._execute_step_action(step, execution)
            execution["step_results"].append(step_result)
            
            # Move to next step
            self._execute_protocol_step(execution_id, step_index + 1)
            
        except Exception as e:
            self.logger.error(f"Failed to execute protocol step: {e}")
            self._handle_protocol_error(execution_id, e)
    
    def _execute_step_action(self, step: Dict[str, Any], execution: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific step action"""
        try:
            action = step["action"]
            agent = step["agent"]
            
            # Notify agents of step execution
            if agent == "ALL":
                for agent_id in execution["participating_agents"]:
                    self.acp.send_message(
                        agent_id,
                        f"🎯 EXECUTING STEP {step['step']}: {action}",
                        MsgTag.INFO
                    )
            else:
                self.acp.send_message(
                    agent,
                    f"🎯 EXECUTING STEP {step['step']}: {action}",
                    MsgTag.INFO
                )
            
            # Simulate step execution
            time.sleep(2)  # Simulate processing time
            
            return {
                "step": step["step"],
                "action": action,
                "agent": agent,
                "status": "completed",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to execute step action: {e}")
            return {
                "step": step["step"],
                "action": step["action"],
                "agent": step["agent"],
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _complete_protocol_execution(self, execution_id: str):
        """Complete protocol execution"""
        try:
            execution = self.active_executions[execution_id]
            protocol = self.protocols[execution["protocol_id"]]
            
            execution["status"] = "completed"
            execution["end_time"] = datetime.now()
            
            # Notify completion
            message = f"🏁 PROTOCOL COMPLETED: {protocol.name}\n\n"
            message += f"Execution Time: {execution['end_time'] - execution['start_time']}\n"
            message += f"Steps Completed: {len(execution['step_results'])}"
            
            for agent_id in execution["participating_agents"]:
                self.acp.send_message(
                    agent_id,
                    message,
                    MsgTag.INFO
                )
            
            self.logger.info(f"🏁 Protocol {protocol.name} execution completed")
            
        except Exception as e:
            self.logger.error(f"Failed to complete protocol execution: {e}")
    
    def _handle_protocol_error(self, execution_id: str, error: Exception):
        """Handle protocol execution errors"""
        try:
            execution = self.active_executions[execution_id]
            protocol = self.protocols[execution["protocol_id"]]
            
            execution["status"] = "failed"
            execution["error"] = str(error)
            
            # Notify agents of failure
            message = f"❌ PROTOCOL FAILED: {protocol.name}\n\nError: {str(error)}\n\nFallback protocols available: {', '.join(protocol.fallback_protocols)}"
            
            for agent_id in execution["participating_agents"]:
                self.acp.send_message(
                    agent_id,
                    message,
                    MsgTag.IMPORTANT
                )
            
            self.logger.error(f"❌ Protocol {protocol.name} execution failed: {error}")
            
        except Exception as e:
            self.logger.error(f"Failed to handle protocol error: {e}")

class EnhancedAgentCoordinationFramework:
    """
    🤝 ENHANCED AGENT COORDINATION FRAMEWORK
    Advanced coordination with task management, collaboration, and protocols
    """
    
    def __init__(self, layout_mode: str = "5-agent"):
        # Initialize agent cellphone
        self.acp = AgentCellPhone(agent_id="Coordination-Framework", layout_mode=layout_mode)
        
        # Initialize components
        self.task_manager = TaskManager(self.acp)
        self.collaboration_manager = CollaborationManager(self.acp)
        self.protocol_manager = CoordinationProtocolManager(self.acp)
        
        # System state
        self.is_active = False
        self.coordination_thread = None
        
        # Setup logging
        self.setup_logging()
        
        # Start coordination system
        self.start_coordination()
    
    def setup_logging(self):
        """Setup logging for the coordination framework"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)s | %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "coordination_framework.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def start_coordination(self):
        """Start the coordination framework"""
        if self.is_active:
            self.logger.warning("⚠️ Coordination already active")
            return
        
        self.is_active = True
        self.coordination_thread = threading.Thread(target=self._coordination_loop, daemon=True)
        self.coordination_thread.start()
        
        self.logger.info("🚀 Enhanced coordination framework started")
    
    def stop_coordination(self):
        """Stop the coordination framework"""
        self.is_active = False
        
        if self.coordination_thread:
            self.coordination_thread.join(timeout=5)
        
        self.logger.info("🛑 Enhanced coordination framework stopped")
    
    def _coordination_loop(self):
        """Main coordination loop"""
        while self.is_active:
            try:
                # Monitor active tasks
                self._monitor_active_tasks()
                
                # Monitor collaboration sessions
                self._monitor_collaboration_sessions()
                
                # Monitor protocol executions
                self._monitor_protocol_executions()
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Coordination loop error: {e}")
                time.sleep(10)
    
    def _monitor_active_tasks(self):
        """Monitor active tasks for updates"""
        active_tasks = [task for task in self.task_manager.tasks.values() if task.status in [TaskStatus.IN_PROGRESS, TaskStatus.ASSIGNED]]
        
        for task in active_tasks:
            # Check for stalled tasks
            if task.status == TaskStatus.ASSIGNED:
                time_since_assignment = (datetime.now() - task.created_at).total_seconds()
                if time_since_assignment > 3600:  # 1 hour
                    self.logger.warning(f"⚠️ Task {task.title} has been assigned for over 1 hour")
    
    def _monitor_collaboration_sessions(self):
        """Monitor active collaboration sessions"""
        for session_id, session in self.collaboration_manager.active_sessions.items():
            # Check session duration
            session_duration = datetime.now() - session.start_time
            if session_duration > timedelta(hours=3):  # 3 hours max
                self.logger.warning(f"⚠️ Collaboration session {session.title} has been running for over 3 hours")
    
    def _monitor_protocol_executions(self):
        """Monitor active protocol executions"""
        for execution_id, execution in self.protocol_manager.active_executions.items():
            if execution["status"] == "executing":
                execution_time = datetime.now() - execution["start_time"]
                if execution_time > timedelta(hours=2):  # 2 hours max
                    self.logger.warning(f"⚠️ Protocol execution {execution_id} has been running for over 2 hours")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        active_tasks = len([t for t in self.task_manager.tasks.values() if t.status in [TaskStatus.IN_PROGRESS, TaskStatus.ASSIGNED]])
        active_sessions = len(self.collaboration_manager.active_sessions)
        active_protocols = len([e for e in self.protocol_manager.active_executions.values() if e["status"] == "executing"])
        
        return {
            "coordination_active": self.is_active,
            "active_tasks": active_tasks,
            "total_tasks": len(self.task_manager.tasks),
            "completed_tasks": len(self.task_manager.completed_tasks),
            "active_collaboration_sessions": active_sessions,
            "active_protocol_executions": active_protocols,
            "total_protocols": len(self.protocol_manager.protocols),
            "system_health": "healthy" if active_tasks < 10 and active_sessions < 5 else "busy" if active_tasks < 20 else "overloaded"
        }
    
    def create_coordination_task(self, task_data: Dict[str, Any]) -> str:
        """Create a new coordination task"""
        return self.task_manager.create_task(task_data)
    
    def start_collaboration_session(self, session_data: Dict[str, Any]) -> str:
        """Start a new collaboration session"""
        return self.collaboration_manager.create_collaboration_session(session_data)
    
    def execute_coordination_protocol(self, protocol_id: str, context: Dict[str, Any]) -> str:
        """Execute a coordination protocol"""
        return self.protocol_manager.execute_protocol(protocol_id, context)

def main():
    """Main function to demonstrate the enhanced coordination framework"""
    print("🤝 ENHANCED AGENT COORDINATION FRAMEWORK")
    print("=" * 60)
    
    # Initialize the framework
    framework = EnhancedAgentCoordinationFramework()
    
    # Display system status
    status = framework.get_system_status()
    print(f"\n📊 SYSTEM STATUS:")
    print(f"Coordination: {'✅ Active' if status['coordination_active'] else '❌ Inactive'}")
    print(f"Active Tasks: {status['active_tasks']}")
    print(f"Total Tasks: {status['total_tasks']}")
    print(f"Completed Tasks: {status['completed_tasks']}")
    print(f"Active Sessions: {status['active_collaboration_sessions']}")
    print(f"Active Protocols: {status['active_protocol_executions']}")
    print(f"System Health: {status['system_health'].upper()}")
    
    print(f"\n🎯 FEATURES:")
    print("• Advanced Task Management")
    print("• Collaboration Session Management")
    print("• Coordination Protocol Execution")
    print("• Real-time Monitoring")
    print("• Adaptive Coordination")
    print("• Multi-mode Operations")
    
    print(f"\n✅ Framework initialized successfully!")
    print("Press Ctrl+C to stop...")
    
    try:
        # Keep framework running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down coordination framework...")
        framework.stop_coordination()

if __name__ == "__main__":
    main()



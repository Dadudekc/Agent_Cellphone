"""
FSM Orchestrator - Core component for managing task states and agent coordination

This module implements the Finite State Machine orchestrator that:
- Manages task states (NEW → IN_PROGRESS → COMPLETED)
- Processes agent reports and updates
- Emits verification messages for completed tasks
- Handles error conditions gracefully
- Provides background monitoring capabilities
"""

import json
import logging
import threading
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum


class TaskState(Enum):
    """Task state enumeration"""
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    """Task data structure"""
    id: str
    title: str
    description: str
    state: TaskState
    created_at: str
    updated_at: str
    assigned_agent: Optional[str] = None
    evidence: List[Dict[str, Any]] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.evidence is None:
            self.evidence = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class AgentReport:
    """Agent report data structure"""
    agent_id: str
    task_id: str
    report_type: str  # "update", "completion", "error"
    content: str
    evidence: List[Dict[str, Any]]
    timestamp: str
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class FSMOrchestrator:
    """FSM Orchestrator for managing task states and agent coordination"""
    
    def __init__(self, fsm_root: Path, inbox_root: Path, outbox_root: Path):
        """
        Initialize FSM Orchestrator
        
        Args:
            fsm_root: Root directory for FSM data
            inbox_root: Root directory for agent inboxes
            outbox_root: Root directory for agent outboxes
        """
        self.fsm_root = Path(fsm_root)
        self.inbox_root = Path(inbox_root)
        self.outbox_root = Path(outbox_root)
        
        # Create necessary directories
        self.tasks_dir = self.fsm_root / "tasks"
        self.workflows_dir = self.fsm_root / "workflows"
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.workflows_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Background monitoring
        self._monitoring = False
        self._monitor_thread = None
        self._stop_event = threading.Event()
        
        # Task cache for performance
        self._task_cache: Dict[str, Task] = {}
        self._cache_lock = threading.Lock()
        
        self.logger.info(f"FSM Orchestrator initialized with root: {self.fsm_root}")
    
    def create_task(self, task_id: str, title: str, description: str, 
                   assigned_agent: Optional[str] = None) -> Task:
        """Create a new task"""
        now = datetime.utcnow().isoformat()
        task = Task(
            id=task_id,
            title=title,
            description=description,
            state=TaskState.NEW,
            created_at=now,
            updated_at=now,
            assigned_agent=assigned_agent
        )
        
        self._save_task(task)
        self.logger.info(f"Created task: {task_id} - {title}")
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID"""
        # Check cache first
        with self._cache_lock:
            if task_id in self._task_cache:
                return self._task_cache[task_id]
        
        # Load from disk
        task_file = self.tasks_dir / f"{task_id}.json"
        if not task_file.exists():
            return None
        
        try:
            with open(task_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                task = Task(**data)
                # Update cache
                with self._cache_lock:
                    self._task_cache[task_id] = task
                return task
        except Exception as e:
            self.logger.error(f"Error loading task {task_id}: {e}")
            return None
    
    def update_task_state(self, task_id: str, new_state: TaskState, 
                         agent_id: Optional[str] = None) -> bool:
        """Update task state"""
        task = self.get_task(task_id)
        if not task:
            self.logger.error(f"Task not found: {task_id}")
            return False
        
        task.state = new_state
        task.updated_at = datetime.utcnow().isoformat()
        if agent_id:
            task.assigned_agent = agent_id
        
        self._save_task(task)
        self.logger.info(f"Updated task {task_id} state to: {new_state}")
        return True
    
    def add_evidence(self, task_id: str, evidence: Dict[str, Any]) -> bool:
        """Add evidence to a task"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        evidence['timestamp'] = datetime.utcnow().isoformat()
        task.evidence.append(evidence)
        task.updated_at = datetime.utcnow().isoformat()
        
        self._save_task(task)
        return True
    
    def process_agent_report(self, report: AgentReport) -> bool:
        """Process an agent report and update task state accordingly"""
        try:
            task = self.get_task(report.task_id)
            if not task:
                self.logger.error(f"Task not found for report: {report.task_id}")
                return False
            
            # Add evidence from report
            self.add_evidence(report.task_id, {
                'agent_id': report.agent_id,
                'report_type': report.report_type,
                'content': report.content,
                'evidence': report.evidence,
                'timestamp': report.timestamp
            })
            
            # Update task state based on report type
            if report.report_type == "completion":
                success = self.update_task_state(report.task_id, TaskState.COMPLETED, report.agent_id)
                if success:
                    self._emit_verification_message(report.task_id, "completed")
            elif report.report_type == "update":
                if task.state == TaskState.NEW:
                    self.update_task_state(report.task_id, TaskState.IN_PROGRESS, report.agent_id)
            elif report.report_type == "error":
                self.update_task_state(report.task_id, TaskState.FAILED, report.agent_id)
            
            self.logger.info(f"Processed {report.report_type} report from {report.agent_id} for task {report.task_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing agent report: {e}")
            return False
    
    def _emit_verification_message(self, task_id: str, status: str):
        """Emit verification message for task completion"""
        try:
            task = self.get_task(task_id)
            if not task or not task.assigned_agent:
                return
            
            verification_msg = {
                "type": "verification",
                "task_id": task_id,
                "status": status,
                "timestamp": datetime.utcnow().isoformat(),
                "evidence_count": len(task.evidence),
                "metadata": task.metadata or {}
            }
            
            # Write to agent's inbox
            agent_inbox = self.inbox_root / task.assigned_agent / "inbox"
            agent_inbox.mkdir(parents=True, exist_ok=True)
            
            verification_file = agent_inbox / f"verify_{task_id}_{int(time.time())}.json"
            with open(verification_file, 'w', encoding='utf-8') as f:
                json.dump(verification_msg, f, indent=2)
            
            self.logger.info(f"Emitted verification message for task {task_id}")
            
        except Exception as e:
            self.logger.error(f"Error emitting verification message: {e}")
    
    def _save_task(self, task: Task):
        """Save task to disk"""
        try:
            task_file = self.tasks_dir / f"{task.id}.json"
            with open(task_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(task), f, indent=2, default=str)
            
            # Update cache
            with self._cache_lock:
                self._task_cache[task.id] = task
                
        except Exception as e:
            self.logger.error(f"Error saving task {task.id}: {e}")
    
    def start_monitoring(self):
        """Start background monitoring of inboxes"""
        if self._monitoring:
            return
        
        self._monitoring = True
        self._stop_event.clear()
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
        self.logger.info("Started FSM monitoring")
    
    def stop_monitoring(self):
        """Stop background monitoring"""
        if not self._monitoring:
            return
        
        self._monitoring = False
        self._stop_event.set()
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5.0)
        self.logger.info("Stopped FSM monitoring")
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        while not self._stop_event.is_set():
            try:
                self._check_inboxes()
                time.sleep(1.0)  # Check every second
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(5.0)  # Wait longer on error
    
    def _check_inboxes(self):
        """Check agent inboxes for new reports"""
        try:
            for agent_dir in self.inbox_root.iterdir():
                if not agent_dir.is_dir():
                    continue
                
                inbox_dir = agent_dir / "inbox"
                if not inbox_dir.exists():
                    continue
                
                # Look for new report files
                for report_file in inbox_dir.glob("report_*.json"):
                    try:
                        with open(report_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            report = AgentReport(**data)
                            
                        # Process the report
                        if self.process_agent_report(report):
                            # Move to processed folder or delete
                            processed_dir = inbox_dir / "processed"
                            processed_dir.mkdir(exist_ok=True)
                            report_file.rename(processed_dir / report_file.name)
                            
                    except Exception as e:
                        self.logger.error(f"Error processing report file {report_file}: {e}")
                        
        except Exception as e:
            self.logger.error(f"Error checking inboxes: {e}")
    
    def get_status_summary(self) -> Dict[str, Any]:
        """Get current status summary for monitoring"""
        try:
            task_files = list(self.tasks_dir.glob("*.json"))
            total_tasks = len(task_files)
            
            state_counts = {state.value: 0 for state in TaskState}
            for task_file in task_files:
                try:
                    with open(task_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        state = data.get('state', 'unknown')
                        if state in state_counts:
                            state_counts[state] += 1
                except:
                    pass
            
            return {
                "total_tasks": total_tasks,
                "state_counts": state_counts,
                "monitoring_active": self._monitoring,
                "cache_size": len(self._task_cache),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting status summary: {e}")
            return {"error": str(e)}
    
    def cleanup(self):
        """Cleanup resources"""
        self.stop_monitoring()
        with self._cache_lock:
            self._task_cache.clear()
        self.logger.info("FSM Orchestrator cleaned up")


# Utility functions for external use
def create_fsm_orchestrator(fsm_root: str, inbox_root: str, outbox_root: str) -> FSMOrchestrator:
    """Factory function to create FSM Orchestrator"""
    return FSMOrchestrator(
        fsm_root=Path(fsm_root),
        inbox_root=Path(inbox_root),
        outbox_root=Path(outbox_root)
    )


if __name__ == "__main__":
    # Example usage
    import tempfile
    
    with tempfile.TemporaryDirectory() as temp_dir:
        fsm = FSMOrchestrator(
            fsm_root=Path(temp_dir) / "fsm_data",
            inbox_root=Path(temp_dir) / "inboxes",
            outbox_root=Path(temp_dir) / "outboxes"
        )
        
        # Create a test task
        task = fsm.create_task("TEST_001", "Test Task", "A test task for validation")
        print(f"Created task: {task.id} - {task.title}")
        
        # Get status
        status = fsm.get_status_summary()
        print(f"Status: {status}")
        
        fsm.cleanup()


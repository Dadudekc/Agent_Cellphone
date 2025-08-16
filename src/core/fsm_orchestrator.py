#!/usr/bin/env python3
"""
FSM Orchestrator
================
Consumes FSM updates from the inbox consumer and updates central task state,
emitting verification messages for completed tasks.
"""

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import time
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class FSMUpdate:
    """Represents an FSM update from an agent"""
    event: str
    agent: str
    task: Optional[str] = None
    actions: List[str] = field(default_factory=list)
    commit_message: Optional[str] = None
    status: Optional[str] = None
    raw: Optional[str] = None
    timestamp: Optional[str] = None
    ts: Optional[int] = None

@dataclass
class TaskState:
    """Represents the current state of a task"""
    task_id: str
    repo: str
    intent: str
    state: str
    owner: Optional[str] = None
    assigned_at: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    last_update: Optional[str] = None

class FSMOrchestrator:
    """Orchestrates FSM state transitions and task management"""
    
    def __init__(self, fsm_root: Path, inbox_root: Path, outbox_root: Path):
        self.fsm_root = Path(fsm_root)
        self.inbox_root = Path(inbox_root)
        self.outbox_root = Path(outbox_root)
        self.tasks_dir = self.fsm_root / "tasks"
        self.workflows_dir = self.fsm_root / "workflows"
        
        # Ensure directories exist
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.workflows_dir.mkdir(parents=True, exist_ok=True)
        self.outbox_root.mkdir(parents=True, exist_ok=True)
        
        # State tracking
        self.processed_updates = set()
        self.task_cache: Dict[str, TaskState] = {}
        self._monitoring = False
        self._stop_event = threading.Event()
        self._task_counter = 0  # Add counter for unique task IDs
        
        logger.info(f"FSM Orchestrator initialized: {self.fsm_root}")
    
    def load_task(self, task_id: str) -> Optional[TaskState]:
        """Load a task from the FSM data directory"""
        task_file = self.tasks_dir / f"{task_id}.json"
        if not task_file.exists():
            return None
        
        try:
            data = json.loads(task_file.read_text(encoding="utf-8"))
            return TaskState(
                task_id=data.get("id", task_id),
                repo=data.get("project_id", "unknown"),
                intent=data.get("name", "Unknown task"),
                state=data.get("status", "unknown"),
                owner=data.get("assigned_agent"),
                assigned_at=data.get("created_at"),
                started_at=data.get("started_at"),
                completed_at=data.get("completed_at"),
                evidence=data.get("evidence", []),
                last_update=data.get("updated_at")
            )
        except Exception as e:
            logger.error(f"Error loading task {task_id}: {e}")
            return None
    
    def save_task(self, task: TaskState) -> bool:
        """Save a task to the FSM data directory"""
        try:
            task_file = self.tasks_dir / f"{task.task_id}.json"
            data = {
                "id": task.task_id,
                "name": task.intent,
                "description": task.intent,
                "priority": "TaskPriority.HIGH",
                "status": task.state,
                "project_id": task.repo,
                "workflow_id": "default",
                "assigned_agent": task.owner,
                "dependencies": [],
                "estimated_duration": 180,
                "actual_duration": None,
                "created_at": task.assigned_at or datetime.now().isoformat(),
                "started_at": task.started_at,
                "completed_at": task.completed_at,
                "updated_at": datetime.now().isoformat(),
                "tags": [],
                "evidence": task.evidence,
                "metadata": {
                    "evidence_count": len(task.evidence),
                    "last_update": task.last_update
                }
            }
            
            task_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            logger.info(f"Task {task.task_id} saved with state: {task.state}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving task {task.task_id}: {e}")
            return False
    
    def process_fsm_update(self, update: FSMUpdate) -> bool:
        """Process an FSM update and update task state accordingly"""
        try:
            logger.info(f"Processing FSM update: {update.event} from {update.agent}")
            
            if update.event == "AGENT_REPORT":
                return self._handle_agent_report(update)
            elif update.event == "AGENT_FREEFORM":
                return self._handle_agent_freeform(update)
            else:
                logger.warning(f"Unknown event type: {update.event}")
                return False
                
        except Exception as e:
            logger.error(f"Error processing FSM update: {e}")
            return False
    
    def _handle_agent_report(self, update: FSMUpdate) -> bool:
        """Handle structured agent reports"""
        if not update.task:
            logger.warning("Agent report missing task information")
            return False
        
        # Try to find existing task or create new one
        task = self._find_or_create_task(update)
        if not task:
            return False
        
        # Update task state based on status
        if "completed" in update.status.lower() or "done" in update.status.lower():
            task.state = "completed"
            task.completed_at = datetime.now().isoformat()
        elif "in progress" in update.status.lower() or "working" in update.status.lower():
            task.state = "in_progress"
            if not task.started_at:
                task.started_at = datetime.now().isoformat()
        elif "assigned" in update.status.lower():
            task.state = "assigned"
            task.assigned_at = datetime.now().isoformat()
        
        # Add evidence if provided
        if update.raw:
            evidence = {
                "kind": "agent_report",
                "agent": update.agent,
                "timestamp": update.timestamp or datetime.now().isoformat(),
                "summary": update.status,
                "raw": update.raw,
                "commit_message": update.commit_message
            }
            task.evidence.append(evidence)
        
        task.last_update = datetime.now().isoformat()
        
        # Save updated task
        if self.save_task(task):
            # Emit verification if task completed
            if task.state == "completed":
                self._emit_verification(task, update)
            return True
        
        return False
    
    def _handle_agent_freeform(self, update: FSMUpdate) -> bool:
        """Handle freeform agent messages"""
        logger.info(f"Agent {update.agent} freeform message: {update.raw}")
        # For now, just log freeform messages
        # Could be extended to track agent activity
        return True
    
    def _find_or_create_task(self, update: FSMUpdate) -> Optional[TaskState]:
        """Find existing task or create new one based on agent report"""
        # Try to extract task ID from various fields
        task_id = None
        
        # Check if task field contains a task ID (must start with "task-")
        if update.task and update.task.startswith("task-"):
            task_id = update.task
            # Try to load existing task
            task = self.load_task(task_id)
            if task:
                return task
        
        # Create new task if none exists
        if update.task:
            self._task_counter += 1
            task = TaskState(
                task_id=f"task-{int(time.time())}-{self._task_counter}",
                repo="unknown",
                intent=update.task,
                state="new",
                owner=update.agent,
                assigned_at=datetime.now().isoformat(),
                evidence=[]
            )
            return task
        
        return None
    
    def _emit_verification(self, task: TaskState, update: FSMUpdate) -> None:
        """Emit verification message for completed task"""
        try:
            verification = {
                "type": "verification",
                "task_id": task.task_id,
                "agent": update.agent,
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
                "evidence_count": len(task.evidence),
                "summary": f"Task {task.task_id} completed by {update.agent}",
                "details": {
                    "intent": task.intent,
                    "completion_time": task.completed_at,
                    "evidence": task.evidence
                }
            }
            
            # Write verification to outbox
            ver_file = self.outbox_root / f"verification_{task.task_id}_{int(time.time())}.json"
            ver_file.write_text(
                json.dumps(verification, indent=2, ensure_ascii=False), 
                encoding="utf-8"
            )
            
            logger.info(f"Verification emitted for task {task.task_id}")
            
        except Exception as e:
            logger.error(f"Error emitting verification for task {task.task_id}: {e}")
    
    def stop_monitoring(self) -> None:
        """Stop the inbox monitoring loop"""
        logger.info("Stopping FSM Orchestrator monitoring...")
        self._monitoring = False
        self._stop_event.set()
    
    def is_monitoring(self) -> bool:
        """Check if monitoring is currently active"""
        return self._monitoring
    
    def get_status_summary(self) -> Dict[str, Any]:
        """Get a summary of orchestrator status for reporting"""
        try:
            total_tasks = len(list(self.tasks_dir.glob("*.json")))
            completed_tasks = 0
            in_progress_tasks = 0
            
            for task_file in self.tasks_dir.glob("*.json"):
                try:
                    data = json.loads(task_file.read_text(encoding="utf-8"))
                    status = data.get("status", "unknown")
                    if status == "completed":
                        completed_tasks += 1
                    elif status in ["in_progress", "assigned"]:
                        in_progress_tasks += 1
                except Exception:
                    continue
            
            return {
                "monitoring": self._monitoring,
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "in_progress_tasks": in_progress_tasks,
                "processed_updates": len(self.processed_updates),
                "inbox_path": str(self.inbox_root),
                "outbox_path": str(self.outbox_root)
            }
        except Exception as e:
            logger.error(f"Error generating status summary: {e}")
            return {"error": str(e)}

    def monitor_inbox(self, poll_interval: int = 5) -> None:
        """Monitor the inbox for new FSM updates"""
        logger.info(f"Starting inbox monitoring: {self.inbox_root}")
        self._monitoring = True
        
        while self._monitoring and not self._stop_event.is_set():
            try:
                # Process any new JSON files in the inbox
                for f in sorted(self.inbox_root.glob("*.json")):
                    if f.name in self.processed_updates:
                        continue
                    
                    try:
                        # Read and parse the update
                        data = json.loads(f.read_text(encoding="utf-8"))
                        logger.info(f"Processing update: {f.name}")
                        
                        # Convert to FSMUpdate
                        update = FSMUpdate(
                            event=data.get("event", "UNKNOWN"),
                            agent=data.get("agent", "unknown"),
                            task=data.get("task"),
                            actions=data.get("actions", []),
                            commit_message=data.get("commit_message"),
                            status=data.get("status"),
                            raw=data.get("raw"),
                            timestamp=data.get("timestamp"),
                            ts=data.get("ts")
                        )
                        
                        # Process the update
                        if self.process_fsm_update(update):
                            self.processed_updates.add(f.name)
                            # Move to processed folder
                            processed_dir = self.inbox_root / "processed"
                            processed_dir.mkdir(exist_ok=True)
                            f.rename(processed_dir / f.name)
                            logger.info(f"Update {f.name} processed successfully")
                        else:
                            logger.warning(f"Failed to process update {f.name}")
                            
                    except Exception as e:
                        logger.error(f"Error processing {f.name}: {e}")
                        # Move to error folder
                        error_dir = self.inbox_root / "errors"
                        error_dir.mkdir(exist_ok=True)
                        try:
                            f.rename(error_dir / f.name)
                        except:
                            pass
                
                # Clean up old processed file names
                if len(self.processed_updates) > 1000:
                    self.processed_updates = set(list(self.processed_updates)[-1000:])
                    
                # Check stop event with shorter intervals
                for _ in range(poll_interval):
                    if self._stop_event.is_set():
                        break
                    time.sleep(1)
                    
            except Exception as e:
                logger.error(f"Error in inbox monitoring: {e}")
                if not self._stop_event.is_set():
                    time.sleep(poll_interval)
        
        logger.info("FSM Orchestrator monitoring stopped")
        self._monitoring = False

def main():
    """Main entry point for FSM Orchestrator"""
    import argparse
    
    parser = argparse.ArgumentParser(description="FSM Orchestrator")
    parser.add_argument("--fsm-root", default="fsm_data", help="FSM data root directory")
    parser.add_argument("--inbox-root", default="runtime/fsm_bridge/outbox", help="FSM inbox directory")
    parser.add_argument("--outbox-root", default="communications/overnight_YYYYMMDD_/Agent-5/verifications", help="Verification outbox directory")
    parser.add_argument("--poll-interval", type=int, default=5, help="Polling interval in seconds")
    
    args = parser.parse_args()
    
    orchestrator = FSMOrchestrator(
        fsm_root=args.fsm_root,
        inbox_root=args.inbox_root,
        outbox_root=args.outbox_root
    )
    
    try:
        orchestrator.monitor_inbox(poll_interval=args.poll_interval)
    except KeyboardInterrupt:
        logger.info("FSM Orchestrator stopped by user")
    except Exception as e:
        logger.error(f"FSM Orchestrator error: {e}")
        raise

if __name__ == "__main__":
    main()

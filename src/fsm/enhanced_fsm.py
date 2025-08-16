#!/usr/bin/env python3
"""
Enhanced FSM with Repository Intelligence
========================================
Provides personalized, contextual guidance based on actual agent work.
"""

import time
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

from .repository_activity_monitor import RepositoryActivityMonitor, RepositoryContext

@dataclass
class AgentState:
    """Enhanced agent state with work context"""
    agent: str
    timestamp: float
    current_repo: Optional[str] = None
    last_activity: Optional[float] = None
    status: str = "unknown"
    progress: Dict[str, any] = None
    blockers: List[str] = None
    last_message: Optional[str] = None
    message_count: int = 0
    
    def __post_init__(self):
        if self.progress is None:
            self.progress = {}
        if self.blockers is None:
            self.blockers = []

class EnhancedFSM:
    """Enhanced FSM with repository intelligence"""
    
    def __init__(self, repos_root: str = "D:/repos/Dadudekc"):
        self.repo_monitor = RepositoryActivityMonitor(repos_root)
        self.agent_states: Dict[str, AgentState] = {}
        self.message_history: List[Dict] = []
        self.state_file = Path("runtime/fsm/enhanced_fsm_state.json")
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing state
        self._load_state()
    
    def update_agent_state(self, agent: str) -> AgentState:
        """Update agent state based on actual repository work"""
        work_context = self.repo_monitor.get_agent_work_context(agent)
        
        # Determine status based on activity
        status = self._determine_agent_status(work_context)
        
        # Calculate progress metrics
        progress = self._calculate_progress(agent, work_context)
        
        # Create or update agent state
        if agent not in self.agent_states:
            self.agent_states[agent] = AgentState(
                agent=agent,
                timestamp=time.time(),
                message_count=0
            )
        
        state = self.agent_states[agent]
        state.timestamp = time.time()
        state.current_repo = work_context.current_repo
        state.last_activity = work_context.last_modified
        state.status = status
        state.progress = progress
        state.blockers = work_context.blockers
        
        return state
    
    def _determine_agent_status(self, context: RepositoryContext) -> str:
        """Determine agent status based on work context"""
        if not context.current_repo:
            return "idle"
        
        if not context.last_modified:
            return "assigned"
        
        # Check if agent has been active recently (within last 30 minutes)
        time_since_activity = time.time() - context.last_modified
        if time_since_activity < 1800:  # 30 minutes
            return "working"
        elif time_since_activity < 3600:  # 1 hour
            return "idle"
        else:
            return "stalled"
    
    def _calculate_progress(self, agent: str, context: RepositoryContext) -> Dict[str, any]:
        """Calculate progress metrics for an agent"""
        if not context.current_repo:
            return {"repos_assigned": 0, "repos_completed": 0, "current_task": None}
        
        # Count completed vs assigned repos
        assigned_repos = self.repo_monitor.agent_repos.get(agent, [])
        completed_repos = 0
        
        for repo in assigned_repos:
            repo_path = self.repo_monitor.repos_root / repo
            if repo_path.exists():
                # Check if repo has substantial work
                if self._has_substantial_work(repo_path):
                    completed_repos += 1
        
        return {
            "repos_assigned": len(assigned_repos),
            "repos_completed": completed_repos,
            "current_repo": context.current_repo,
            "has_recent_commits": bool(context.recent_commits),
            "has_file_changes": bool(context.file_changes),
            "task_files": list(context.task_progress.keys())
        }
    
    def _has_substantial_work(self, repo_path: Path) -> bool:
        """Check if repository has substantial work"""
        try:
            # Check for key files that indicate work
            key_files = ["README.md", "requirements.txt", "main.py", "index.html", "package.json"]
            has_key_files = any((repo_path / f).exists() for f in key_files)
            
            # Check for git history
            has_git_history = (repo_path / ".git").exists()
            
            return has_key_files or has_git_history
        except Exception:
            return False
    
    def generate_personalized_message(self, agent: str, message_type: str) -> str:
        """Generate personalized message based on agent's current work"""
        # Update agent state first
        state = self.update_agent_state(agent)
        
        if message_type == "RESUME":
            return self._generate_resume_message(agent, state)
        elif message_type == "TASK":
            return self._generate_task_message(agent, state)
        elif message_type == "COORDINATE":
            return self._generate_coordinate_message(agent, state)
        elif message_type == "RESCUE":
            return self._generate_rescue_message(agent, state)
        else:
            return self._generate_generic_message(agent, state)
    
    def _generate_resume_message(self, agent: str, state: AgentState) -> str:
        """Generate personalized resume message"""
        if not state.current_repo:
            return f"[RESUME] {agent}, start working on your first assigned repository. Check your TASK_LIST.md for assignments."
        
        if state.status == "working":
            repo = state.current_repo
            progress = state.progress
            completed = progress.get("repos_completed", 0)
            total = progress.get("repos_assigned", 0)
            
            return f"[RESUME] {agent}, continue working on {repo}. Progress: {completed}/{total} repos completed. Update your TASK_LIST.md with current status."
        
        elif state.status == "stalled":
            repo = state.current_repo
            return f"[RESUME] {agent}, you were working on {repo} but appear stalled. Continue with your current task or move to the next repository."
        
        else:
            return f"[RESUME] {agent}, review your assigned contracts in inbox and update your TASK_LIST.md with next verification steps."
    
    def _generate_task_message(self, agent: str, state: AgentState) -> str:
        """Generate personalized task message"""
        if not state.current_repo:
            return f"[TASK] {agent}, complete one contract to acceptance criteria. Commit small, verifiable edits and attach evidence."
        
        repo = state.current_repo
        blockers = state.blockers
        
        if blockers:
            blocker_msg = f" Address blockers: {', '.join(blockers[:2])}."
        else:
            blocker_msg = ""
        
        return f"[TASK] {agent}, complete one contract in {repo} to acceptance criteria.{blocker_msg} Commit small, verifiable edits and attach evidence."
    
    def _generate_coordinate_message(self, agent: str, state: AgentState) -> str:
        """Generate personalized coordinate message"""
        if not state.current_repo:
            return f"[COORDINATE] {agent}, post a contract update to Agent-5: task_id, current state, next action, evidence links."
        
        repo = state.current_repo
        progress = state.progress
        
        return f"[COORDINATE] {agent}, post a contract update for {repo} to Agent-5: task_id, current state, next action, evidence links. Progress: {progress.get('repos_completed', 0)}/{progress.get('repos_assigned', 0)} repos."
    
    def _generate_rescue_message(self, agent: str, state: AgentState) -> str:
        """Generate personalized rescue message"""
        if not state.current_repo:
            return f"[RESCUE] {agent}, you appear stalled. Start working on your assigned repositories."
        
        repo = state.current_repo
        blockers = state.blockers
        
        if blockers:
            blocker_msg = f" Address blockers: {', '.join(blockers[:2])}."
        else:
            blocker_msg = ""
        
        return f"[RESCUE] {agent}, you appear stalled on {repo}.{blocker_msg} Continue with your current task or move to the next repository."
    
    def _generate_generic_message(self, agent: str, state: AgentState) -> str:
        """Generate generic message when type is unknown"""
        return f"[MESSAGE] {agent}, continue with your assigned work. Current status: {state.status}."
    
    def get_coordination_summary(self) -> Dict[str, any]:
        """Get comprehensive coordination summary"""
        # Update all agent states
        for agent in self.repo_monitor.agent_repos.keys():
            self.update_agent_state(agent)
        
        # Get repository-level summary
        repo_summary = self.repo_monitor.get_coordination_summary()
        
        # Add FSM-specific data
        fsm_summary = {
            "fsm_timestamp": time.time(),
            "agent_states": {},
            "message_history": self.message_history[-10:],  # Last 10 messages
            "overall_status": "operational"
        }
        
        for agent, state in self.agent_states.items():
            fsm_summary["agent_states"][agent] = asdict(state)
        
        # Combine summaries
        combined_summary = {**repo_summary, **fsm_summary}
        
        return combined_summary
    
    def record_message(self, agent: str, message_type: str, content: str):
        """Record message for history tracking"""
        message_record = {
            "timestamp": time.time(),
            "agent": agent,
            "type": message_type,
            "content": content,
            "state_snapshot": asdict(self.agent_states.get(agent, {}))
        }
        
        self.message_history.append(message_record)
        
        # Update message count for agent
        if agent in self.agent_states:
            self.agent_states[agent].message_count += 1
            self.agent_states[agent].last_message = content
        
        # Keep only last 100 messages
        if len(self.message_history) > 100:
            self.message_history = self.message_history[-100:]
        
        # Save state
        self._save_state()
    
    def _save_state(self):
        """Save FSM state to disk"""
        try:
            state_data = {
                "timestamp": time.time(),
                "agent_states": {agent: asdict(state) for agent, state in self.agent_states.items()},
                "message_history": self.message_history[-50:]  # Keep last 50 for persistence
            }
            
            with self.state_file.open("w", encoding="utf-8") as f:
                json.dump(state_data, f, indent=2, default=str)
        except Exception as e:
            print(f"Failed to save FSM state: {e}")
    
    def _load_state(self):
        """Load FSM state from disk"""
        try:
            if self.state_file.exists():
                with self.state_file.open("r", encoding="utf-8") as f:
                    state_data = json.load(f)
                
                # Restore agent states
                for agent, state_dict in state_data.get("agent_states", {}).items():
                    self.agent_states[agent] = AgentState(**state_dict)
                
                # Restore message history
                self.message_history = state_data.get("message_history", [])
        except Exception as e:
            print(f"Failed to load FSM state: {e}")
    
    def get_agent_recommendations(self, agent: str) -> List[str]:
        """Get personalized recommendations for an agent"""
        state = self.update_agent_state(agent)
        recommendations = []
        
        if not state.current_repo:
            recommendations.append("Start working on your first assigned repository")
            recommendations.append("Create a TASK_LIST.md to track progress")
        
        elif state.status == "stalled":
            recommendations.append(f"Continue work on {state.current_repo}")
            recommendations.append("Address any blockers before moving to next repo")
        
        elif state.status == "working":
            progress = state.progress
            completed = progress.get("repos_completed", 0)
            total = progress.get("repos_assigned", 0)
            
            if completed < total:
                recommendations.append(f"Complete current work on {state.current_repo}")
                recommendations.append(f"Move to next repository ({completed + 1}/{total})")
            else:
                recommendations.append("All repositories completed - report to Agent-5")
        
        if state.blockers:
            recommendations.append(f"Address blockers: {', '.join(state.blockers[:2])}")
        
        return recommendations

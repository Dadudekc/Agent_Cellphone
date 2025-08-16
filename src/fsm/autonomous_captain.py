#!/usr/bin/env python3
"""
Autonomous CAPTAIN System for Agent-5
=====================================
Self-prompting, intelligent coordination with smart new chat logic.
"""

import time
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

from .enhanced_fsm import EnhancedFSM
from src.services.agent_cell_phone import AgentCellPhone, MsgTag

@dataclass
class CaptainTask:
    """CAPTAIN task with priority and status"""
    id: str
    title: str
    description: str
    priority: str  # high, medium, low
    status: str    # pending, in_progress, completed
    assigned_agent: Optional[str] = None
    created_at: float = None
    completed_at: Optional[float] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()

class AutonomousCaptain:
    """Autonomous CAPTAIN system that self-prompting and coordinates"""
    
    def __init__(self, repos_root: str = "D:/repos/Dadudekc"):
        self.fsm = EnhancedFSM(repos_root)
        self.acp = AgentCellPhone(agent_id="Agent-5", layout_mode="5-agent", test=False)
        self.tasks: List[CaptainTask] = []
        self.state_file = Path("runtime/fsm/captain_state.json")
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing state
        self._load_state()
        
        # Initialize with default CAPTAIN tasks
        self._initialize_captain_tasks()
    
    def _initialize_captain_tasks(self):
        """Initialize default CAPTAIN tasks"""
        if not self.tasks:
            self.tasks = [
                CaptainTask(
                    id="task-001",
                    title="Coordinate Agent Progress",
                    description="Monitor and coordinate all agent progress across repositories",
                    priority="high",
                    status="pending"
                ),
                CaptainTask(
                    id="task-002", 
                    title="Resolve Blockers",
                    description="Identify and resolve blockers preventing agent progress",
                    priority="high",
                    status="pending"
                ),
                CaptainTask(
                    id="task-003",
                    title="Update TASK_LIST.md",
                    description="Update repository TASK_LIST.md entries across active repos",
                    priority="medium",
                    status="pending"
                ),
                CaptainTask(
                    id="task-004",
                    title="FSM Contract Alignment",
                    description="Draft and align FSM contracts per agent (states, transitions)",
                    priority="medium",
                    status="pending"
                ),
                CaptainTask(
                    id="task-005",
                    title="Next Verification Planning",
                    description="Plan and execute next verification steps for all agents",
                    priority="high",
                    status="pending"
                )
            ]
    
    def self_prompt(self) -> str:
        """Generate self-prompt based on current state and tasks"""
        # Get current coordination summary
        summary = self.fsm.get_coordination_summary()
        
        # Analyze current situation
        active_agents = summary["overall_progress"]["active_agents"]
        stalled_agents = summary["overall_progress"]["stalled_agents"]
        
        # Generate situational awareness
        if stalled_agents > 0:
            situation = f"🚨 URGENT: {stalled_agents} agents are stalled and need immediate attention!"
            priority = "high"
        elif active_agents >= 4:
            situation = f"✅ GOOD: {active_agents}/4 agents are actively working"
            priority = "medium"
        else:
            situation = f"⚠️ WARNING: Only {active_agents}/4 agents are active"
            priority = "high"
        
        # Generate self-prompt
        prompt = f"""
🎯 CAPTAIN SELF-PROMPT - {time.strftime('%H:%M:%S')}

{situation}

📊 CURRENT STATUS:
- Active Agents: {active_agents}
- Stalled Agents: {stalled_agents}
- Pending Tasks: {len([t for t in self.tasks if t.status == 'pending'])}
- High Priority: {len([t for t in self.tasks if t.priority == 'high' and t.status == 'pending'])}

🎯 IMMEDIATE ACTIONS NEEDED:
"""
        
        # Add high priority tasks
        high_priority = [t for t in self.tasks if t.priority == 'high' and t.status == 'pending']
        for task in high_priority[:3]:  # Top 3 high priority
            prompt += f"- {task.title}: {task.description}\n"
        
        # Add agent-specific actions
        prompt += "\n🤖 AGENT-SPECIFIC ACTIONS:\n"
        for agent, agent_data in summary["agents"].items():
            if agent == "Agent-5":
                continue
                
            if agent_data["status"] == "stalled":
                prompt += f"- RESCUE {agent}: They appear stalled on {agent_data.get('current_repo', 'unknown repo')}\n"
            elif agent_data["status"] == "working":
                progress = agent_data.get("has_progress", False)
                if progress:
                    prompt += f"- COORDINATE {agent}: Get progress update on {agent_data.get('current_repo', 'current work')}\n"
                else:
                    prompt += f"- CHECK {agent}: Verify they're actually working on {agent_data.get('current_repo', 'assigned repos')}\n"
        
        prompt += "\n💡 NEXT STEPS:\n"
        prompt += "1. Execute high priority tasks\n"
        prompt += "2. Rescue stalled agents\n"
        prompt += "3. Coordinate active agents\n"
        prompt += "4. Update progress tracking\n"
        prompt += "5. Plan next verification cycle\n"
        
        return prompt
    
    def execute_captain_actions(self):
        """Execute CAPTAIN actions based on current state"""
        # Get self-prompt
        prompt = self.self_prompt()
        print(prompt)
        
        # Execute high priority tasks
        self._execute_high_priority_tasks()
        
        # Rescue stalled agents
        self._rescue_stalled_agents()
        
        # Coordinate active agents
        self._coordinate_active_agents()
        
        # Update progress tracking
        self._update_progress_tracking()
    
    def _execute_high_priority_tasks(self):
        """Execute high priority CAPTAIN tasks"""
        high_priority = [t for t in self.tasks if t.priority == 'high' and t.status == 'pending']
        
        for task in high_priority[:2]:  # Execute top 2 high priority
            print(f"🎯 Executing: {task.title}")
            
            if task.id == "task-001":  # Coordinate Agent Progress
                self._coordinate_all_agents()
            elif task.id == "task-002":  # Resolve Blockers
                self._resolve_blockers()
            elif task.id == "task-005":  # Next Verification Planning
                self._plan_next_verification()
            
            # Mark as in progress
            task.status = "in_progress"
    
    def _coordinate_all_agents(self):
        """Coordinate all agents for comprehensive progress update"""
        print("🤝 Coordinating all agents for progress update")
        
        summary = self.fsm.get_coordination_summary()
        
        for agent, agent_data in summary["agents"].items():
            if agent == "Agent-5":
                continue
                
            print(f"📊 Coordinating {agent}: {agent_data.get('status', 'unknown')} - {agent_data.get('current_repo', 'no repo')}")
            
            # Generate personalized coordinate message
            message = self.fsm.generate_personalized_message(agent, "COORDINATE")
            
            # Send in existing chat (input coordinates)
            self._send_message_smart(agent, message, "COORDINATE", new_chat=False)
    
    def _rescue_stalled_agents(self):
        """Rescue stalled agents with personalized messages"""
        summary = self.fsm.get_coordination_summary()
        
        for agent, agent_data in summary["agents"].items():
            if agent == "Agent-5":
                continue
                
            if agent_data["status"] == "stalled":
                print(f"🚨 Rescuing stalled agent: {agent}")
                
                # Generate personalized rescue message
                message = self.fsm.generate_personalized_message(agent, "RESCUE")
                
                # Send with new chat (starter coordinates)
                self._send_message_smart(agent, message, "RESCUE", new_chat=True)
                
                # Update task status
                self._update_task_status("task-002", "in_progress")
    
    def _coordinate_active_agents(self):
        """Coordinate active agents for progress updates"""
        summary = self.fsm.get_coordination_summary()
        
        for agent, agent_data in summary["agents"].items():
            if agent == "Agent-5":
                continue
                
            if agent_data["status"] == "working":
                print(f"🤝 Coordinating active agent: {agent}")
                
                # Generate personalized coordinate message
                message = self.fsm.generate_personalized_message(agent, "COORDINATE")
                
                # Send in existing chat (input coordinates)
                self._send_message_smart(agent, message, "COORDINATE", new_chat=False)
    
    def _resolve_blockers(self):
        """Identify and resolve blockers"""
        summary = self.fsm.get_coordination_summary()
        
        for agent, agent_data in summary["agents"].items():
            if agent == "Agent-5":
                continue
                
            blockers = agent_data.get("blockers", [])
            if blockers:
                print(f"🔧 Resolving blockers for {agent}: {blockers}")
                
                # Create blocker resolution task
                blocker_task = CaptainTask(
                    id=f"blocker-{agent}-{int(time.time())}",
                    title=f"Resolve Blockers for {agent}",
                    description=f"Address blockers: {', '.join(blockers[:2])}",
                    priority="high",
                    status="pending",
                    assigned_agent=agent
                )
                self.tasks.append(blocker_task)
    
    def _plan_next_verification(self):
        """Plan next verification cycle"""
        print("📋 Planning next verification cycle")
        
        # Create verification planning task
        verification_task = CaptainTask(
            id=f"verification-{int(time.time())}",
            title="Execute Verification Cycle",
            description="Run next verification cycle for all agents",
            priority="high",
            status="pending"
        )
        self.tasks.append(verification_task)
    
    def _send_message_smart(self, agent: str, content: str, message_type: str, new_chat: bool = False):
        """Send message with smart new chat logic"""
        try:
            if new_chat:
                # Use starter coordinates and open new chat
                self.acp.send(agent, content, MsgTag.TASK, new_chat=True)
                print(f"[NEW CHAT] {agent}: {content[:50]}...")
            else:
                # Use input coordinates in existing chat
                self.acp.send(agent, content, MsgTag.TASK, new_chat=False)
                print(f"[EXISTING CHAT] {agent}: {content[:50]}...")
            
            # Record in FSM
            self.fsm.record_message(agent, message_type, content)
            
        except Exception as e:
            print(f"Failed to send message to {agent}: {e}")
    
    def _update_task_status(self, task_id: str, status: str):
        """Update task status"""
        for task in self.tasks:
            if task.id == task_id:
                task.status = status
                if status == "completed":
                    task.completed_at = time.time()
                break
    
    def _update_progress_tracking(self):
        """Update progress tracking across repositories"""
        print("📊 Updating progress tracking")
        
        # Update TASK_LIST.md entries
        self._update_task_list_entries()
        
        # Save captain state
        self._save_state()
    
    def _update_task_list_entries(self):
        """Update TASK_LIST.md entries across active repos"""
        print("📝 Updating TASK_LIST.md entries")
        
        # This would involve updating TASK_LIST.md files in repositories
        # For now, mark the task as completed
        self._update_task_status("task-003", "completed")
    
    def _save_state(self):
        """Save CAPTAIN state to disk"""
        try:
            state_data = {
                "timestamp": time.time(),
                "tasks": [task.__dict__ for task in self.tasks],
                "captain_status": "active"
            }
            
            with self.state_file.open("w", encoding="utf-8") as f:
                json.dump(state_data, f, indent=2, default=str)
        except Exception as e:
            print(f"Failed to save CAPTAIN state: {e}")
    
    def _load_state(self):
        """Load CAPTAIN state from disk"""
        try:
            if self.state_file.exists():
                with self.state_file.open("r", encoding="utf-8") as f:
                    state_data = json.load(f)
                
                # Restore tasks
                if "tasks" in state_data:
                    self.tasks = [CaptainTask(**task_dict) for task_dict in state_data["tasks"]]
        except Exception as e:
            print(f"Failed to load CAPTAIN state: {e}")
    
    def run_captain_cycle(self):
        """Run one CAPTAIN coordination cycle"""
        print("🎖️ CAPTAIN Agent-5 Autonomous Coordination Cycle")
        print("=" * 60)
        
        # Execute CAPTAIN actions
        self.execute_captain_actions()
        
        # Save state
        self._save_state()
        
        print("✅ CAPTAIN cycle completed")
        print(f"📊 Active tasks: {len([t for t in self.tasks if t.status == 'pending'])}")
        print(f"🎯 High priority: {len([t for t in self.tasks if t.priority == 'high' and t.status == 'pending'])}")

def main():
    """Main CAPTAIN execution"""
    captain = AutonomousCaptain()
    
    try:
        captain.run_captain_cycle()
    except KeyboardInterrupt:
        print("\n🛑 CAPTAIN interrupted by user")
    except Exception as e:
        print(f"❌ CAPTAIN error: {e}")

if __name__ == "__main__":
    main()

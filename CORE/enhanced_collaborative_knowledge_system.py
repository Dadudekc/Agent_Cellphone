#!/usr/bin/env python3
"""
🚀 ENHANCED COLLABORATIVE KNOWLEDGE MANAGEMENT SYSTEM v2.0
=========================================================
Advanced knowledge management with presidential captaincy terms and agent cellphone integration
"""

import os
import sys
import json
import time
import threading
import asyncio
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import uuid
import logging

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.services.agent_cell_phone import AgentCellPhone, MsgTag
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)

class KnowledgeType(Enum):
    """Enhanced types of knowledge that can be stored and shared"""
    TASK = "task"
    PROTOCOL = "protocol"
    SOLUTION = "solution"
    ANALYSIS = "analysis"
    COORDINATION = "coordination"
    LEARNING = "learning"
    SECURITY = "security"
    PRESIDENTIAL_DECISION = "presidential_decision"
    EXECUTIVE_ORDER = "executive_order"
    POLICY_FRAMEWORK = "policy_framework"
    STRATEGIC_INITIATIVE = "strategic_initiative"

class KnowledgePriority(Enum):
    """Enhanced priority levels for knowledge items"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    PRESIDENTIAL = "presidential"  # Highest priority for presidential decisions

class CaptaincyTerm(Enum):
    """Presidential captaincy terms for agent coordination"""
    CAMPAIGN_TERM = "campaign_term"      # Task-list based term
    ELECTION_PHASE = "election_phase"    # Election and voting phase
    TRANSITION_PHASE = "transition_phase" # Handoff between captains

@dataclass
class CampaignTask:
    """Individual task within a captain's campaign"""
    task_id: str
    title: str
    description: str
    priority: str
    estimated_duration: str
    dependencies: List[str]
    assigned_agent: Optional[str] = None
    status: str = "pending"
    progress: float = 0.0
    created_at: datetime = None
    completed_at: Optional[datetime] = None

@dataclass
class CampaignTaskList:
    """A captain's proposed task list for their campaign"""
    campaign_id: str
    captain_agent: str
    title: str
    description: str
    vision_statement: str
    tasks: List[CampaignTask]
    expected_outcomes: List[str]
    success_metrics: List[str]
    created_at: datetime
    status: str = "proposed"
    total_votes: int = 0
    approval_votes: Dict[str, bool] = None
    adopted_tasks: List[str] = None  # Tasks adopted from other campaigns

@dataclass
class PresidentialDecision:
    """Presidential decision structure for agent coordination"""
    decision_id: str
    president_agent: str
    term: CaptaincyTerm
    decision_type: str
    title: str
    description: str
    rationale: str
    affected_agents: List[str]
    implementation_timeline: str
    success_metrics: List[str]
    created_at: datetime
    effective_date: datetime
    status: str
    approval_votes: Dict[str, bool]
    execution_progress: float

@dataclass
class KnowledgeItem:
    """Enhanced knowledge item structure with presidential integration"""
    id: str
    type: KnowledgeType
    title: str
    content: str
    agent_id: str
    priority: KnowledgePriority
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    version: int
    dependencies: List[str]
    status: str
    metadata: Dict[str, Any]
    presidential_approval: Optional[str] = None
    term_affiliation: Optional[CaptaincyTerm] = None

@dataclass
class CollaborationSession:
    """Enhanced collaboration session with presidential oversight"""
    session_id: str
    agents: List[str]
    president_agent: str
    objective: str
    start_time: datetime
    status: str
    knowledge_shared: List[str]
    decisions_made: List[str]
    next_actions: List[str]
    term_phase: CaptaincyTerm
    session_type: str

class PresidentialCaptaincySystem:
    """Presidential captaincy system based on task list completion and campaign elections"""
    
    def __init__(self):
        self.current_term = CaptaincyTerm.ELECTION_PHASE
        self.current_captain = None
        self.captain_history = []
        
        # Available agents for captaincy
        self.available_agents = [
            "Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"
        ]
        
        # Campaign and election state
        self.active_campaigns: Dict[str, CampaignTaskList] = {}
        self.election_results: Dict[str, Dict[str, int]] = {}
        self.current_campaign: Optional[CampaignTaskList] = None
        
        # Campaign tracking
        self.campaign_start_date: Optional[datetime] = None
        self.campaign_start_threshold = 0.8  # 80% completion allows new campaign to start
        self.captain_handoff_threshold = 0.95  # 95% completion triggers captain handoff
        
        # Voting state
        self.voting_open = False
        self.votes_cast: Dict[str, str] = {}  # agent_id -> campaign_id
        
        # Task adoption tracking
        self.adopted_tasks: List[CampaignTask] = []
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current captaincy system state"""
        if self.current_campaign:
            completed_tasks = sum(1 for task in self.current_campaign.tasks if task.status == "completed")
            total_tasks = len(self.current_campaign.tasks)
            completion_percentage = (completed_tasks / total_tasks) if total_tasks > 0 else 0.0
            
            return {
                "current_term": self.current_term.value,
                "current_captain": self.current_captain,
                "campaign_title": self.current_campaign.title,
                "campaign_progress": completion_percentage,
                "tasks_completed": completed_tasks,
                "total_tasks": total_tasks,
                "campaign_start_date": self.campaign_start_date.isoformat() if self.campaign_start_date else None,
                "voting_open": self.voting_open,
                "active_campaigns": len(self.active_campaigns)
            }
        else:
            return {
                "current_term": self.current_term.value,
                "current_captain": None,
                "campaign_title": None,
                "campaign_progress": 0.0,
                "tasks_completed": 0,
                "total_tasks": 0,
                "campaign_start_date": None,
                "voting_open": self.voting_open,
                "active_campaigns": len(self.active_campaigns)
            }
    
    def start_election_phase(self) -> bool:
        """Start the election phase for new captain selection"""
        if self.current_term != CaptaincyTerm.ELECTION_PHASE:
            return False
        
        # Check if current campaign allows new election
        if not self.can_start_new_campaign():
            return False
        
        self.voting_open = True
        self.votes_cast.clear()
        self.active_campaigns.clear()
        
        # Notify all agents to submit campaign proposals
        return True
    
    def submit_campaign_proposal(self, campaign: CampaignTaskList) -> bool:
        """Submit a campaign proposal for voting"""
        if not self.voting_open:
            return False
        
        campaign.campaign_id = str(uuid.uuid4())
        campaign.created_at = datetime.now()
        campaign.status = "proposed"
        campaign.approval_votes = {}
        campaign.adopted_tasks = []
        
        self.active_campaigns[campaign.campaign_id] = campaign
        return True
    
    def vote_on_campaign(self, agent_id: str, campaign_id: str, approve: bool) -> bool:
        """Vote on a campaign proposal"""
        if not self.voting_open or agent_id in self.votes_cast:
            return False
        
        if campaign_id not in self.active_campaigns:
            return False
        
        campaign = self.active_campaigns[campaign_id]
        campaign.approval_votes[agent_id] = approve
        
        if approve:
            campaign.total_votes += 1
        
        self.votes_cast[agent_id] = campaign_id
        return True
    
    def close_voting_and_select_captain(self) -> Optional[str]:
        """Close voting and select the winning captain"""
        if not self.voting_open:
            return None
        
        self.voting_open = False
        
        # Find campaign with most votes
        winning_campaign = None
        max_votes = 0
        
        for campaign in self.active_campaigns.values():
            if campaign.total_votes > max_votes:
                max_votes = campaign.total_votes
                winning_campaign = campaign
        
        if winning_campaign:
            # Transition to campaign term
            self.current_term = CaptaincyTerm.CAMPAIGN_TERM
            self.current_captain = winning_campaign.captain_agent
            self.current_campaign = winning_campaign
            self.campaign_start_date = datetime.now()
            
            # Record captain history
            self.captain_history.append({
                "captain": self.current_captain,
                "campaign_id": winning_campaign.campaign_id,
                "campaign_title": winning_campaign.title,
                "start_date": self.campaign_start_date.isoformat(),
                "status": "active"
            })
            
            return winning_campaign.campaign_id
        
        return None
    
    def adopt_task_from_other_campaign(self, task: CampaignTask, source_campaign_id: str) -> bool:
        """Allow current captain to adopt tasks from other campaigns"""
        if self.current_term != CaptaincyTerm.CAMPAIGN_TERM or not self.current_campaign:
            return False
        
        # Create adopted task
        adopted_task = CampaignTask(
            task_id=str(uuid.uuid4()),
            title=f"Adopted: {task.title}",
            description=f"Adopted from {source_campaign_id}: {task.description}",
            priority=task.priority,
            estimated_duration=task.estimated_duration,
            dependencies=task.dependencies.copy(),
            created_at=datetime.now()
        )
        
        self.current_campaign.tasks.append(adopted_task)
        self.adopted_tasks.append(adopted_task)
        
        if self.current_campaign.adopted_tasks is None:
            self.current_campaign.adopted_tasks = []
        self.current_campaign.adopted_tasks.append(adopted_task.task_id)
        
        return True
    
    def update_task_progress(self, task_id: str, progress: float, status: str = None) -> bool:
        """Update progress of a campaign task"""
        if not self.current_campaign:
            return False
        
        for task in self.current_campaign.tasks:
            if task.task_id == task_id:
                task.progress = progress
                if status:
                    task.status = status
                if progress >= 100.0:
                    task.status = "completed"
                    task.completed_at = datetime.now()
                return True
        
        return False
    
    def check_campaign_completion(self) -> Dict[str, Any]:
        """Check campaign completion status and return appropriate actions"""
        if not self.current_campaign:
            return {"action": "none", "completion_percentage": 0.0}
        
        completed_tasks = sum(1 for task in self.current_campaign.tasks if task.status == "completed")
        total_tasks = len(self.current_campaign.tasks)
        
        if total_tasks == 0:
            return {"action": "none", "completion_percentage": 0.0}
        
        completion_percentage = completed_tasks / total_tasks
        
        if completion_percentage >= self.captain_handoff_threshold:
            # Campaign fully complete - trigger captain handoff
            return {"action": "handoff", "completion_percentage": completion_percentage}
        elif completion_percentage >= self.campaign_start_threshold:
            # Campaign ready for new election - allow new campaign to start
            return {"action": "start_new", "completion_percentage": completion_percentage}
        else:
            # Campaign still in progress
            return {"action": "continue", "completion_percentage": completion_percentage}
    
    def can_start_new_campaign(self) -> bool:
        """Check if a new campaign can start (80% completion reached)"""
        if not self.current_campaign:
            return True  # No current campaign, can start new one
        
        completion_status = self.check_campaign_completion()
        return completion_status["action"] in ["start_new", "handoff"]
    
    def should_handoff_captain(self) -> bool:
        """Check if captain should handoff (95% completion reached)"""
        if not self.current_campaign:
            return False
        
        completion_status = self.check_campaign_completion()
        return completion_status["action"] == "handoff"
    
    def _complete_campaign(self):
        """Complete current campaign and prepare for new election"""
        if not self.current_campaign:
            return
        
        # Update captain history
        for record in self.captain_history:
            if record["captain"] == self.current_captain and record["status"] == "active":
                record["status"] = "completed"
                record["end_date"] = datetime.now().isoformat()
                record["completion_percentage"] = self._calculate_campaign_completion()
                break
        
        # Transition to election phase
        self.current_term = CaptaincyTerm.ELECTION_PHASE
        self.current_captain = None
        self.current_campaign = None
        self.campaign_start_date = None
        
        # Clear adopted tasks
        self.adopted_tasks.clear()
    
    def _calculate_campaign_completion(self) -> float:
        """Calculate current campaign completion percentage"""
        if not self.current_campaign:
            return 0.0
        
        completed_tasks = sum(1 for task in self.current_campaign.tasks if task.status == "completed")
        total_tasks = len(self.current_campaign.tasks)
        
        return (completed_tasks / total_tasks) if total_tasks > 0 else 0.0
    
    def make_presidential_decision(self, decision: PresidentialDecision) -> bool:
        """Make a presidential decision (captain decision)"""
        if decision.president_agent != self.current_captain:
            return False
        
        decision.term = self.current_term
        decision.created_at = datetime.now()
        decision.status = "pending_approval"
        
        # Add to presidential decisions
        if not hasattr(self, 'presidential_decisions'):
            self.presidential_decisions = []
        self.presidential_decisions.append(decision)
        
        return True

class EnhancedCollaborativeKnowledgeManager:
    """
    🚀 ENHANCED COLLABORATIVE KNOWLEDGE MANAGEMENT SYSTEM
    Advanced knowledge management with presidential captaincy and agent cellphone integration
    """
    
    def __init__(self, data_dir: str = "enhanced_collaborative_knowledge"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize presidential captaincy system
        self.captaincy_system = PresidentialCaptaincySystem()
        
        # Initialize agent cellphone integration
        self.acp = AgentCellPhone(agent_id="Enhanced-Knowledge-Manager", layout_mode="5-agent")
        
        # Core knowledge storage
        self.knowledge_base: Dict[str, KnowledgeItem] = {}
        self.knowledge_index: Dict[str, List[str]] = {}
        
        # Collaboration tracking
        self.active_sessions: Dict[str, CollaborationSession] = {}
        self.collaboration_history: List[Dict[str, Any]] = []
        
        # Agent coordination state
        self.agent_states: Dict[str, Dict[str, Any]] = {}
        self.coordination_protocols: Dict[str, Dict[str, Any]] = {}
        
        # Presidential decisions tracking
        self.presidential_decisions: List[PresidentialDecision] = []
        
        # Campaign management
        self.campaign_tasks: Dict[str, CampaignTask] = {}
        self.campaign_progress: Dict[str, float] = {}
        
        # Campaign submission directory
        self.campaign_submissions_dir = Path("captain_submissions")
        self.campaign_submissions_dir.mkdir(exist_ok=True)
        
        # Automated campaign workflow
        self.campaign_workflow_state = "idle"  # idle, collecting_proposals, voting, execution
        self.campaign_deadlines = {}
        
        # Setup logging
        self.setup_logging()
        
        # Load existing knowledge
        self._load_knowledge_base()
        self._initialize_coordination_protocols()
        
        # Start background coordination monitoring
        self._start_coordination_monitor()
        
        # Start campaign monitoring
        self._start_campaign_monitor()
        
        # Start automated campaign workflow
        self._start_automated_campaign_workflow()
    
    def setup_logging(self):
        """Setup logging for the enhanced system"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)s | %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "enhanced_knowledge_system.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _initialize_coordination_protocols(self):
        """Initialize enhanced coordination protocols"""
        self.coordination_protocols = {
            "campaign_coordination": {
                "description": "Campaign-based captaincy coordination protocols",
                "protocols": [
                    "Campaign proposal submission",
                    "Agent voting and election",
                    "Task list execution",
                    "Campaign completion monitoring"
                ]
            },
            "knowledge_sharing": {
                "description": "Enhanced knowledge sharing protocols",
                "protocols": [
                    "Cross-campaign knowledge preservation",
                    "Captain decision documentation",
                    "Strategic knowledge classification",
                    "Legacy knowledge management"
                ]
            },
            "agent_collaboration": {
                "description": "Multi-agent collaboration protocols",
                "protocols": [
                    "Captain oversight",
                    "Campaign-based objectives",
                    "Collaborative decision making",
                    "Performance tracking"
                ]
            }
        }
    
    def _start_campaign_monitor(self):
        """Start campaign monitoring for completion and election triggers"""
        def monitor_campaigns():
            while True:
                try:
                    # Check campaign completion status
                    completion_status = self.captaincy_system.check_campaign_completion()
                    current_state = self.captaincy_system.get_current_state()
                    
                    if completion_status["action"] == "handoff":
                        # Campaign fully complete - trigger captain handoff
                        self.logger.info(f"🎯 Campaign fully completed: {current_state['campaign_title']}")
                        self.logger.info(f"🎯 Captain {current_state['current_captain']} handoff triggered")
                        
                        # Notify all agents of campaign completion and handoff
                        self._notify_campaign_handoff(
                            current_state['current_captain'], 
                            completion_status['completion_percentage']
                        )
                        
                        # Complete the campaign and start new election
                        self.captaincy_system._complete_campaign()
                        self.captaincy_system.start_election_phase()
                        self._notify_campaign_election_start()
                        
                        # Create campaign completion knowledge
                        self._create_campaign_completion_knowledge(current_state)
                        
                    elif completion_status["action"] == "start_new":
                        # Campaign ready for new election - allow new campaign to start
                        if self.captaincy_system.current_term == CaptaincyTerm.CAMPAIGN_TERM:
                            self.logger.info(f"🎯 Campaign ready for new election: {current_state['campaign_title']}")
                            self.logger.info(f"🎯 Current completion: {completion_status['completion_percentage']:.1%}")
                            
                            # Notify agents that new campaign can start
                            self._notify_campaign_ready_for_new_election(
                                current_state['current_captain'],
                                completion_status['completion_percentage']
                            )
                    
                    time.sleep(1800)  # Check every 30 minutes
                    
                except Exception as e:
                    self.logger.error(f"Campaign monitoring error: {e}")
                    time.sleep(300)
        
        campaign_thread = threading.Thread(target=monitor_campaigns, daemon=True)
        campaign_thread.start()
    
    def _start_automated_campaign_workflow(self):
        """Start automated campaign workflow management"""
        def manage_campaign_workflow():
            while True:
                try:
                    # Check current workflow state and take appropriate actions
                    if self.campaign_workflow_state == "idle":
                        # Check if we should start collecting proposals
                        if self.captaincy_system.current_term == CaptaincyTerm.ELECTION_PHASE:
                            self._automated_start_campaign_collection()
                    
                    elif self.campaign_workflow_state == "collecting_proposals":
                        # Check if deadline reached or all agents submitted
                        if self._check_campaign_submission_deadline():
                            self._automated_close_submissions_and_start_voting()
                    
                    elif self.campaign_workflow_state == "voting":
                        # Check if voting deadline reached
                        if self._check_voting_deadline():
                            self._automated_close_voting_and_select_captain()
                    
                    elif self.campaign_workflow_state == "execution":
                        # Monitor campaign execution
                        self._automated_monitor_campaign_execution()
                    
                    time.sleep(300)  # Check every 5 minutes
                    
                except Exception as e:
                    self.logger.error(f"Automated campaign workflow error: {e}")
                    time.sleep(60)
        
        workflow_thread = threading.Thread(target=manage_campaign_workflow, daemon=True)
        workflow_thread.start()
    
    def _automated_start_campaign_collection(self):
        """Automatically start collecting campaign proposals from all agents"""
        try:
            self.campaign_workflow_state = "collecting_proposals"
            
            # Set submission deadline (24 hours from now)
            submission_deadline = datetime.now() + timedelta(hours=24)
            self.campaign_deadlines["submission"] = submission_deadline
            
            # Create campaign submission prompt
            submission_prompt = self._create_campaign_submission_prompt()
            
            # Send to all agents via agent cellphone
            for agent_id in self.captaincy_system.available_agents:
                try:
                    self.acp.send_message(
                        to_agent=agent_id,
                        message=submission_prompt,
                        msg_tag=MsgTag.COORDINATION
                    )
                    self.logger.info(f"Campaign submission prompt sent to {agent_id}")
                except Exception as e:
                    self.logger.error(f"Failed to send submission prompt to {agent_id}: {e}")
            
            # Create submission directory structure
            self._setup_campaign_submission_directory()
            
            self.logger.info("🗳️ Automated campaign collection started")
            
        except Exception as e:
            self.logger.error(f"Failed to start automated campaign collection: {e}")
    
    def _create_campaign_submission_prompt(self) -> str:
        """Create a comprehensive prompt for campaign submissions"""
        prompt = """🎯 CAMPAIGN SUBMISSION REQUEST

You are invited to submit a campaign proposal for captaincy. Your campaign should outline a comprehensive task list that will advance our projects.

📋 CAMPAIGN REQUIREMENTS:
1. Campaign Title: Clear, descriptive name
2. Vision Statement: Your strategic vision
3. Task List: 3-5 specific, actionable tasks
4. Expected Outcomes: What will be achieved
5. Success Metrics: How success will be measured
6. Timeline: Estimated duration for each task

📁 SUBMISSION INSTRUCTIONS:
- Save your campaign as: captain_submissions/Agent-[YOUR_ID]_campaign.md
- Include all required sections above
- Be specific and actionable
- Focus on project advancement

⏰ DEADLINE: 24 hours from now

🗳️ VOTING PROCESS:
- All agents will vote on submitted campaigns
- Highest-voted campaign becomes active
- Captain can adopt ideas from other campaigns

Submit your campaign proposal to demonstrate your leadership vision!"""
        
        return prompt
    
    def _setup_campaign_submission_directory(self):
        """Setup directory structure for campaign submissions"""
        try:
            # Create main submissions directory
            submissions_dir = self.campaign_submissions_dir
            
            # Create template file
            template_content = """# Campaign Proposal Template

## Campaign Title
[Your campaign title here]

## Vision Statement
[Your strategic vision for advancing our projects]

## Task List

### Task 1: [Task Title]
- **Description**: [Detailed description]
- **Priority**: [High/Medium/Low]
- **Estimated Duration**: [Time estimate]
- **Dependencies**: [Any dependencies]
- **Expected Outcome**: [What this task will achieve]

### Task 2: [Task Title]
- **Description**: [Detailed description]
- **Priority**: [High/Medium/Low]
- **Estimated Duration**: [Time estimate]
- **Dependencies**: [Any dependencies]
- **Expected Outcome**: [What this task will achieve]

### Task 3: [Task Title]
- **Description**: [Detailed description]
- **Priority**: [High/Medium/Low]
- **Estimated Duration**: [Time estimate]
- **Dependencies**: [Any dependencies]
- **Expected Outcome**: [What this task will achieve]

## Expected Outcomes
- [Outcome 1]
- [Outcome 2]
- [Outcome 3]

## Success Metrics
- [Metric 1]
- [Metric 2]
- [Metric 3]

## Timeline
- **Total Campaign Duration**: [Overall timeline]
- **Phase 1**: [First phase details]
- **Phase 2**: [Second phase details]
- **Phase 3**: [Final phase details]

---
*Submitted by: [Your Agent ID]*
*Date: [Submission Date]*
"""
            
            template_file = submissions_dir / "campaign_template.md"
            with open(template_file, 'w') as f:
                f.write(template_content)
            
            # Create README for submissions
            readme_content = """# Campaign Submissions Directory

This directory contains campaign proposals for captaincy elections.

## Current Status
- **Workflow State**: {workflow_state}
- **Submission Deadline**: {submission_deadline}
- **Voting Deadline**: {voting_deadline}

## Submission Files
- `campaign_template.md` - Template for campaign proposals
- `Agent-[ID]_campaign.md` - Individual agent submissions

## How to Submit
1. Copy the template file
2. Rename it to `Agent-[YOUR_ID]_campaign.md`
3. Fill in your campaign details
4. Save in this directory

## Voting Process
- All agents review submitted campaigns
- Vote via the system interface
- Highest-voted campaign becomes active
- Captain can adopt ideas from other campaigns

## Current Submissions
{submission_list}
"""
            
            readme_file = submissions_dir / "README.md"
            with open(readme_file, 'w') as f:
                f.write(readme_content)
            
            self.logger.info("✅ Campaign submission directory setup completed")
            
        except Exception as e:
            self.logger.error(f"Failed to setup campaign submission directory: {e}")
    
    def _check_campaign_submission_deadline(self) -> bool:
        """Check if campaign submission deadline has been reached"""
        if "submission" not in self.campaign_deadlines:
            return False
        
        return datetime.now() >= self.campaign_deadlines["submission"]
    
    def _check_voting_deadline(self) -> bool:
        """Check if voting deadline has been reached"""
        if "voting" not in self.campaign_deadlines:
            return False
        
        return datetime.now() >= self.campaign_deadlines["voting"]
    
    def _automated_close_submissions_and_start_voting(self):
        """Automatically close submissions and start voting phase"""
        try:
            self.campaign_workflow_state = "voting"
            
            # Set voting deadline (48 hours from now)
            voting_deadline = datetime.now() + timedelta(hours=48)
            self.campaign_deadlines["voting"] = voting_deadline
            
            # Collect all submitted campaigns
            submitted_campaigns = self._collect_submitted_campaigns()
            
            if not submitted_campaigns:
                self.logger.warning("No campaign submissions found - extending deadline")
                # Extend deadline by 12 hours
                self.campaign_deadlines["submission"] = datetime.now() + timedelta(hours=12)
                return
            
            # Start voting phase
            self.captaincy_system.start_election_phase()
            
            # Create voting prompt
            voting_prompt = self._create_voting_prompt(submitted_campaigns)
            
            # Send voting prompt to all agents
            for agent_id in self.captaincy_system.available_agents:
                try:
                    self.acp.send_message(
                        to_agent=agent_id,
                        message=voting_prompt,
                        msg_tag=MsgTag.COORDINATION
                    )
                    self.logger.info(f"Voting prompt sent to {agent_id}")
                except Exception as e:
                    self.logger.error(f"Failed to send voting prompt to {agent_id}: {e}")
            
            # Update submission directory README
            self._update_submission_directory_status()
            
            self.logger.info("🗳️ Automated voting phase started")
            
        except Exception as e:
            self.logger.error(f"Failed to start automated voting: {e}")
    
    def _collect_submitted_campaigns(self) -> List[Dict[str, Any]]:
        """Collect all submitted campaign files from the submissions directory"""
        try:
            submitted_campaigns = []
            submissions_dir = self.campaign_submissions_dir
            
            for campaign_file in submissions_dir.glob("Agent-*_campaign.md"):
                try:
                    with open(campaign_file, 'r') as f:
                        content = f.read()
                    
                    # Parse campaign content (basic parsing - could be enhanced)
                    campaign_data = self._parse_campaign_submission(content, campaign_file.name)
                    submitted_campaigns.append(campaign_data)
                    
                except Exception as e:
                    self.logger.error(f"Failed to parse campaign file {campaign_file}: {e}")
            
            return submitted_campaigns
            
        except Exception as e:
            self.logger.error(f"Failed to collect submitted campaigns: {e}")
            return []
    
    def _parse_campaign_submission(self, content: str, filename: str) -> Dict[str, Any]:
        """Parse campaign submission markdown content"""
        try:
            # Extract agent ID from filename
            agent_id = filename.replace("_campaign.md", "")
            
            # Basic parsing - extract key sections
            lines = content.split('\n')
            campaign_data = {
                "agent_id": agent_id,
                "filename": filename,
                "content": content,
                "title": "Unknown",
                "vision": "Unknown",
                "tasks": [],
                "outcomes": [],
                "metrics": []
            }
            
            current_section = None
            for line in lines:
                line = line.strip()
                
                if line.startswith('# Campaign Title'):
                    current_section = "title"
                elif line.startswith('# Vision Statement'):
                    current_section = "vision"
                elif line.startswith('# Task List'):
                    current_section = "tasks"
                elif line.startswith('# Expected Outcomes'):
                    current_section = "outcomes"
                elif line.startswith('# Success Metrics'):
                    current_section = "metrics"
                elif line.startswith('### Task'):
                    current_section = "task_detail"
                elif line.startswith('- **') and current_section == "task_detail":
                    # Parse task details
                    pass
                elif line.startswith('- ') and current_section in ["outcomes", "metrics"]:
                    if current_section == "outcomes":
                        campaign_data["outcomes"].append(line[2:])
                    elif current_section == "metrics":
                        campaign_data["metrics"].append(line[2:])
                elif current_section == "title" and line and not line.startswith('#'):
                    campaign_data["title"] = line
                elif current_section == "vision" and line and not line.startswith('#'):
                    campaign_data["vision"] = line
            
            return campaign_data
            
        except Exception as e:
            self.logger.error(f"Failed to parse campaign submission: {e}")
            return {"agent_id": "Unknown", "filename": filename, "content": content}
    
    def _create_voting_prompt(self, submitted_campaigns: List[Dict[str, Any]]) -> str:
        """Create a comprehensive voting prompt for all agents"""
        prompt = f"""🗳️ CAMPAIGN VOTING PHASE

{len(submitted_campaigns)} campaign proposals have been submitted. Please review and vote for the campaign you believe will advance our projects the most.

📋 SUBMITTED CAMPAIGNS:

"""
        
        for i, campaign in enumerate(submitted_campaigns, 1):
            prompt += f"""**Campaign {i}: {campaign['title']}**
- **Agent**: {campaign['agent_id']}
- **Vision**: {campaign['vision']}
- **Tasks**: {len(campaign['tasks'])} proposed tasks
- **Expected Outcomes**: {', '.join(campaign['outcomes'][:3])}

"""
        
        prompt += """🗳️ VOTING INSTRUCTIONS:
1. Review all campaign proposals in: captain_submissions/
2. Consider which campaign will advance our projects most effectively
3. Vote via the system interface or respond to this message
4. You can only vote once per election cycle

⏰ VOTING DEADLINE: 48 hours from now

🎯 VOTING CRITERIA:
- Strategic vision and clarity
- Feasibility of proposed tasks
- Potential impact on project advancement
- Innovation and creativity

Submit your vote to help select our next captain!"""
        
        return prompt
    
    def _automated_close_voting_and_select_captain(self):
        """Automatically close voting and select the winning captain"""
        try:
            # Close voting
            winning_campaign_id = self.captaincy_system.close_voting_and_select_captain()
            
            if winning_campaign_id:
                self.campaign_workflow_state = "execution"
                
                # Get winning campaign details
                winning_campaign = self.captaincy_system.active_campaigns.get(winning_campaign_id)
                
                if winning_campaign:
                    # Create campaign execution prompt
                    execution_prompt = self._create_campaign_execution_prompt(winning_campaign)
                    
                    # Send to all agents
                    for agent_id in self.captaincy_system.available_agents:
                        try:
                            self.acp.send_message(
                                to_agent=agent_id,
                                message=execution_prompt,
                                msg_tag=MsgTag.COORDINATION
                            )
                            self.logger.info(f"Campaign execution prompt sent to {agent_id}")
                        except Exception as e:
                            self.logger.error(f"Failed to send execution prompt to {agent_id}: {e}")
                    
                    # Update submission directory
                    self._update_submission_directory_status()
                    
                    self.logger.info(f"👑 Automated captain selection completed: {winning_campaign.captain_agent}")
                else:
                    self.logger.error("Winning campaign not found after selection")
            else:
                self.logger.warning("No winning campaign selected - restarting election")
                self.campaign_workflow_state = "idle"
                
        except Exception as e:
            self.logger.error(f"Failed to close voting and select captain: {e}")
    
    def _create_campaign_execution_prompt(self, winning_campaign: CampaignTaskList) -> str:
        """Create a prompt for campaign execution"""
        prompt = f"""👑 NEW CAPTAIN SELECTED: {winning_campaign.captain_agent}

🎯 CAMPAIGN: {winning_campaign.title}
📋 VISION: {winning_campaign.vision_statement}

📊 CAMPAIGN TASKS:
"""
        
        for i, task in enumerate(winning_campaign.tasks, 1):
            prompt += f"""**Task {i}: {task.title}**
- Description: {task.description}
- Priority: {task.priority}
- Duration: {task.estimated_duration}
- Dependencies: {', '.join(task.dependencies) if task.dependencies else 'None'}

"""
        
        prompt += """🚀 EXECUTION PHASE:
- All agents should support the captain's campaign
- Contribute to task completion
- Report progress regularly
- Collaborate on dependencies

📁 CAMPAIGN FILES:
- Campaign details: captain_submissions/
- Progress tracking: System interface
- Task updates: Via system methods

Let's execute this campaign successfully!"""
        
        return prompt
    
    def _automated_monitor_campaign_execution(self):
        """Monitor campaign execution and trigger transitions"""
        try:
            # Check campaign completion status
            completion_status = self.captaincy_system.check_campaign_completion()
            
            if completion_status["action"] == "start_new":
                # Campaign ready for new election
                self.logger.info("🎯 Campaign ready for new election - transitioning to idle state")
                self.campaign_workflow_state = "idle"
                
            elif completion_status["action"] == "handoff":
                # Campaign handoff triggered
                self.logger.info("🎯 Campaign handoff triggered - transitioning to idle state")
                self.campaign_workflow_state = "idle"
                
        except Exception as e:
            self.logger.error(f"Failed to monitor campaign execution: {e}")
    
    def _update_submission_directory_status(self):
        """Update the README file with current workflow status"""
        try:
            readme_file = self.campaign_submissions_dir / "README.md"
            
            if readme_file.exists():
                with open(readme_file, 'r') as f:
                    content = f.read()
                
                # Update status information
                workflow_state = self.campaign_workflow_state
                submission_deadline = self.campaign_deadlines.get("submission", "Not set")
                voting_deadline = self.campaign_deadlines.get("voting", "Not set")
                
                # Format deadlines
                if isinstance(submission_deadline, datetime):
                    submission_deadline = submission_deadline.strftime("%Y-%m-%d %H:%M")
                if isinstance(voting_deadline, datetime):
                    voting_deadline = voting_deadline.strftime("%Y-%m-%d %H:%M")
                
                # Get submission list
                submitted_campaigns = self._collect_submitted_campaigns()
                submission_list = "\n".join([f"- {campaign['agent_id']}: {campaign['title']}" for campaign in submitted_campaigns])
                
                # Update content
                content = content.replace("{workflow_state}", workflow_state)
                content = content.replace("{submission_deadline}", str(submission_deadline))
                content = content.replace("{voting_deadline}", str(voting_deadline))
                content = content.replace("{submission_list}", submission_list)
                
                with open(readme_file, 'w') as f:
                    f.write(content)
                
        except Exception as e:
            self.logger.error(f"Failed to update submission directory status: {e}")
    
    def _notify_term_change(self):
        """Notify all agents of presidential term change"""
        term_info = self.captaincy_system.get_current_term_info()
        
        notification = {
            "type": "presidential_term_change",
            "new_term": term_info["current_term"],
            "new_president": term_info["current_president"],
            "term_objectives": term_info["current_objectives"],
            "timestamp": datetime.now().isoformat()
        }
        
        # Send notification via agent cellphone
        try:
            self.acp.send_message(
                "ALL",
                f"🎖️ PRESIDENTIAL TERM CHANGE: {term_info['current_term'].upper()}",
                MsgTag.IMPORTANT,
                json.dumps(notification, indent=2)
            )
        except Exception as e:
            self.logger.error(f"Failed to send term change notification: {e}")
    
    def _create_term_transition_knowledge(self):
        """Create knowledge item for term transition"""
        current_state = self.captaincy_system.get_current_state()
        
        transition_knowledge = KnowledgeItem(
            id=str(uuid.uuid4()),
            type=KnowledgeType.STRATEGIC_INITIATIVE,
            title=f"Campaign Transition: {current_state['current_term']}",
            content=f"Transition to {current_state['current_term']} with Captain {current_state['current_captain']}",
            agent_id="System",
            priority=KnowledgePriority.PRESIDENTIAL,
            tags=["campaign", "transition", current_state["current_term"]],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            version=1,
            dependencies=[],
            status="active",
            metadata={
                "term": current_state["current_term"],
                "captain": current_state["current_captain"],
                "campaign_title": current_state.get("campaign_title", "N/A")
            },
            presidential_approval=current_state["current_captain"],
            term_affiliation=self.captaincy_system.current_term
        )
        
        self.add_knowledge_item(transition_knowledge)
    
    def _notify_campaign_election_start(self):
        """Notify all agents that campaign election phase has started"""
        message = "🗳️ CAMPAIGN ELECTION PHASE: Submit your campaign proposals for captaincy!"
        message += "\n\nAll agents should submit their task list proposals."
        message += "\nVoting will begin once all proposals are submitted."
        
        # Send to all agents
        for agent_id in ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]:
            try:
                self.acp.send_message(
                    to_agent=agent_id,
                    message=message,
                    msg_tag=MsgTag.COORDINATION
                )
                self.logger.info(f"Campaign election notification sent to {agent_id}")
            except Exception as e:
                self.logger.error(f"Failed to send campaign election notification to {agent_id}: {e}")
    
    def _notify_captain_selected(self, captain_agent: str, campaign_title: str):
        """Notify all agents of new captain selection"""
        message = f"👑 NEW CAPTAIN SELECTED: {captain_agent} has been elected captain!"
        message += f"\n\nCampaign: {campaign_title}"
        message += "\n\nAll agents should support the captain's campaign and contribute to task completion."
        
        # Send to all agents
        for agent_id in ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]:
            try:
                self.acp.send_message(
                    to_agent=agent_id,
                    message=message,
                    msg_tag=MsgTag.COORDINATION
                )
                self.logger.info(f"Captain selection notification sent to {agent_id}")
            except Exception as e:
                self.logger.error(f"Failed to send captain selection notification to {agent_id}: {e}")
    
    def _notify_campaign_ready_for_new_election(self, captain_agent: str, completion_percentage: float):
        """Notify all agents that campaign is ready for new election (80% completion)"""
        message = f"🎯 CAMPAIGN READY FOR NEW ELECTION: {captain_agent}'s campaign has reached {completion_percentage:.1f}% completion!"
        message += "\n\nNew campaign proposals can now be submitted while current campaign finishes remaining tasks."
        message += "\nCurrent captain will continue until 95% completion for handoff."
        
        # Send to all agents
        for agent_id in ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]:
            try:
                self.acp.send_message(
                    to_agent=agent_id,
                    message=message,
                    msg_tag=MsgTag.COORDINATION
                )
                self.logger.info(f"Campaign ready for new election notification sent to {agent_id}")
            except Exception as e:
                self.logger.error(f"Failed to send campaign ready notification to {agent_id}: {e}")
    
    def _notify_campaign_handoff(self, captain_agent: str, completion_percentage: float):
        """Notify all agents that campaign handoff is triggered (95% completion)"""
        message = f"🎯 CAMPAIGN HANDOFF: {captain_agent}'s campaign has reached {completion_percentage:.1f}% completion!"
        message += "\n\nCaptain handoff triggered. Current campaign will be completed and new captain will take over."
        message += "\nNew election cycle will begin immediately."
        
        # Send to all agents
        for agent_id in ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]:
            try:
                self.acp.send_message(
                    to_agent=agent_id,
                    message=message,
                    msg_tag=MsgTag.COORDINATION
                )
                self.logger.info(f"Campaign handoff notification sent to {agent_id}")
            except Exception as e:
                self.logger.error(f"Failed to send campaign handoff notification to {agent_id}: {e}")
    
    def _notify_campaign_completion(self, captain_agent: str, completion_percentage: float):
        """Notify all agents that campaign is complete and new election is needed"""
        message = f"🎯 CAMPAIGN COMPLETE: {captain_agent}'s campaign has reached {completion_percentage:.1f}% completion!"
        message += "\n\nNew election cycle will begin. All agents should prepare new campaign proposals."
        
        # Send to all agents
        for agent_id in ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]:
            try:
                self.acp.send_message(
                    to_agent=agent_id,
                    message=message,
                    msg_tag=MsgTag.COORDINATION
                )
                self.logger.info(f"Campaign completion notification sent to {agent_id}")
            except Exception as e:
                self.logger.error(f"Failed to send campaign completion notification to {agent_id}: {e}")
    
    def _create_campaign_completion_knowledge(self, campaign_state: Dict[str, Any]):
        """Create knowledge item for campaign completion"""
        completion_knowledge = KnowledgeItem(
            id=str(uuid.uuid4()),
            type=KnowledgeType.STRATEGIC_INITIATIVE,
            title=f"Campaign Completion: {campaign_state['campaign_title']}",
            content=f"Campaign under {campaign_state['current_captain']} has been completed successfully",
            agent_id="System",
            priority=KnowledgePriority.PRESIDENTIAL,
            tags=["campaign", "completion", "captaincy", "election"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            version=1,
            dependencies=[],
            status="completed",
            metadata={
                "campaign_title": campaign_state['campaign_title'],
                "captain": campaign_state['current_captain'],
                "completion_percentage": campaign_state['campaign_progress'],
                "tasks_completed": campaign_state['tasks_completed'],
                "total_tasks": campaign_state['total_tasks']
            },
            presidential_approval=campaign_state['current_captain'],
            term_affiliation=CaptaincyTerm.ELECTION_PHASE
        )
        
        self.add_knowledge_item(completion_knowledge)
    
    def add_knowledge_item(self, item: KnowledgeItem) -> bool:
        """Add a new knowledge item to the system"""
        try:
            # Validate presidential approval if required
            if item.priority == KnowledgePriority.PRESIDENTIAL:
                if not item.presidential_approval:
                    item.presidential_approval = self.captaincy_system.current_president
            
            # Set term affiliation if not specified
            if not item.term_affiliation:
                item.term_affiliation = self.captaincy_system.current_term
            
            # Add to knowledge base
            self.knowledge_base[item.id] = item
            
            # Update index
            for tag in item.tags:
                if tag not in self.knowledge_index:
                    self.knowledge_index[tag] = []
                self.knowledge_index[tag].append(item.id)
            
            # Save to disk
            self._save_knowledge_item(item)
            
            # Notify agents of new knowledge
            self._notify_new_knowledge(item)
            
            self.logger.info(f"✅ Added knowledge item: {item.title}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add knowledge item: {e}")
            return False
    
    def _save_knowledge_item(self, item: KnowledgeItem):
        """Save knowledge item to disk"""
        item_file = self.data_dir / f"{item.id}.json"
        
        # Convert datetime objects to ISO strings for JSON serialization
        item_dict = asdict(item)
        item_dict["created_at"] = item.created_at.isoformat()
        item_dict["updated_at"] = item.updated_at.isoformat()
        if item.term_affiliation:
            item_dict["term_affiliation"] = item.term_affiliation.value
        
        with open(item_file, 'w') as f:
            json.dump(item_dict, f, indent=2)
    
    def _notify_new_knowledge(self, item: KnowledgeItem):
        """Notify agents of new knowledge via agent cellphone"""
        try:
            priority_emoji = "🚨" if item.priority == KnowledgePriority.PRESIDENTIAL else "📚"
            term_info = f" (Term: {item.term_affiliation.value})" if item.term_affiliation else ""
            
            message = f"{priority_emoji} NEW KNOWLEDGE: {item.title}{term_info}\n\n{item.content[:200]}..."
            
            self.acp.send_message(
                "ALL",
                message,
                MsgTag.INFO if item.priority != KnowledgePriority.PRESIDENTIAL else MsgTag.IMPORTANT
            )
        except Exception as e:
            self.logger.error(f"Failed to notify agents of new knowledge: {e}")
    
    def get_knowledge_by_term(self, term: CaptaincyTerm) -> List[KnowledgeItem]:
        """Get all knowledge items for a specific presidential term"""
        return [
            item for item in self.knowledge_base.values()
            if item.term_affiliation == term
        ]
    
    def get_presidential_decisions(self, term: Optional[CaptaincyTerm] = None) -> List[PresidentialDecision]:
        """Get presidential decisions for a specific term or all terms"""
        if term:
            return [
                decision for decision in self.presidential_decisions
                if decision.term == term
            ]
        return self.presidential_decisions
    
    def get_current_term_status(self) -> Dict[str, Any]:
        """Get comprehensive current term status (legacy method - use get_campaign_status instead)"""
        campaign_status = self.get_campaign_status()
        term_knowledge = self.get_knowledge_by_term(self.captaincy_system.current_term)
        term_decisions = self.get_presidential_decisions(self.captaincy_system.current_term)
        
        return {
            **campaign_status,
            "knowledge_items_count": len(term_knowledge),
            "presidential_decisions_count": len(term_decisions),
            "knowledge_by_type": self._categorize_knowledge(term_knowledge),
            "recent_decisions": term_decisions[-5:] if term_decisions else []
        }
    
    def _categorize_knowledge(self, knowledge_items: List[KnowledgeItem]) -> Dict[str, int]:
        """Categorize knowledge items by type"""
        categories = {}
        for item in knowledge_items:
            category = item.type.value
            categories[category] = categories.get(category, 0) + 1
        return categories
    
    def _start_coordination_monitor(self):
        """Start background coordination monitoring"""
        def monitor_coordination():
            while True:
                try:
                    # Check campaign status
                    campaign_status = self.get_campaign_status()
                    
                    # Log current status
                    self.logger.info(f"Current term: {campaign_status['current_term']}")
                    if campaign_status.get('current_captain'):
                        self.logger.info(f"Current captain: {campaign_status['current_captain']}")
                        self.logger.info(f"Campaign: {campaign_status.get('campaign_title', 'N/A')}")
                        self.logger.info(f"Campaign progress: {campaign_status.get('campaign_progress', 0):.1%}")
                    else:
                        self.logger.info("No active captain - election phase")
                    
                    time.sleep(300)  # Check every 5 minutes
                    
                except Exception as e:
                    self.logger.error(f"Coordination monitoring error: {e}")
                    time.sleep(60)
        
        monitor_thread = threading.Thread(target=monitor_coordination, daemon=True)
        monitor_thread.start()
    
    def _load_knowledge_base(self):
        """Load existing knowledge base from disk"""
        try:
            for item_file in self.data_dir.glob("*.json"):
                try:
                    with open(item_file, 'r') as f:
                        item_data = json.load(f)
                    
                    # Convert ISO strings back to datetime objects
                    item_data["created_at"] = datetime.fromisoformat(item_data["created_at"])
                    item_data["updated_at"] = datetime.fromisoformat(item_data["updated_at"])
                    
                    # Convert term string back to enum
                    if "term_affiliation" in item_data:
                        item_data["term_affiliation"] = CaptaincyTerm(item_data["term_affiliation"])
                    
                    # Create KnowledgeItem object
                    item = KnowledgeItem(**item_data)
                    self.knowledge_base[item.id] = item
                    
                    # Update index
                    for tag in item.tags:
                        if tag not in self.knowledge_index:
                            self.knowledge_index[tag] = []
                        self.knowledge_index[tag].append(item.id)
                    
                except Exception as e:
                    self.logger.error(f"Failed to load knowledge item from {item_file}: {e}")
            
            self.logger.info(f"✅ Loaded {len(self.knowledge_base)} knowledge items")
            
        except Exception as e:
            self.logger.error(f"Failed to load knowledge base: {e}")
    
    # Campaign Management Methods
    def start_campaign_election(self) -> bool:
        """Start a new campaign election phase"""
        try:
            if self.captaincy_system.start_election_phase():
                self._notify_campaign_election_start()
                self.logger.info("🗳️ Campaign election phase started")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to start campaign election: {e}")
            return False
    
    def submit_campaign_proposal(self, campaign: CampaignTaskList) -> bool:
        """Submit a campaign proposal for voting"""
        try:
            if self.captaincy_system.submit_campaign_proposal(campaign):
                self.logger.info(f"📋 Campaign proposal submitted by {campaign.captain_agent}: {campaign.title}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to submit campaign proposal: {e}")
            return False
    
    def vote_on_campaign(self, agent_id: str, campaign_id: str, approve: bool) -> bool:
        """Vote on a campaign proposal"""
        try:
            if self.captaincy_system.vote_on_campaign(agent_id, campaign_id, approve):
                vote_text = "approved" if approve else "rejected"
                self.logger.info(f"🗳️ {agent_id} {vote_text} campaign {campaign_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to vote on campaign: {e}")
            return False
    
    def close_voting_and_select_captain(self) -> Optional[str]:
        """Close voting and select the winning captain"""
        try:
            winning_campaign_id = self.captaincy_system.close_voting_and_select_captain()
            if winning_campaign_id:
                winning_campaign = self.captaincy_system.active_campaigns.get(winning_campaign_id)
                if winning_campaign:
                    self._notify_captain_selected(winning_campaign.captain_agent, winning_campaign.title)
                    self._create_campaign_transition_knowledge(winning_campaign_id, winning_campaign.captain_agent, winning_campaign.title)
                    self.logger.info(f"👑 Captain selected: {winning_campaign.captain_agent} with campaign: {winning_campaign.title}")
                return winning_campaign_id
            return None
        except Exception as e:
            self.logger.error(f"Failed to close voting and select captain: {e}")
            return None
    
    def adopt_task_from_other_campaign(self, task: CampaignTask, source_campaign_id: str) -> bool:
        """Allow current captain to adopt tasks from other campaigns"""
        try:
            if self.captaincy_system.adopt_task_from_other_campaign(task, source_campaign_id):
                self.logger.info(f"📋 Task adopted: {task.title} from campaign {source_campaign_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to adopt task: {e}")
            return False
    
    def update_campaign_task_progress(self, task_id: str, progress: float, status: str = None) -> bool:
        """Update progress of a campaign task"""
        try:
            if self.captaincy_system.update_task_progress(task_id, progress, status):
                self.logger.info(f"📊 Task progress updated: {task_id} - {progress:.1f}%")
                
                # Check campaign completion status
                completion_status = self.captaincy_system.check_campaign_completion()
                
                if completion_status["action"] == "start_new":
                    self.logger.info("🎯 Campaign ready for new election (80% completion reached)")
                elif completion_status["action"] == "handoff":
                    self.logger.info("🎯 Campaign handoff triggered (95% completion reached)")
                
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to update task progress: {e}")
            return False
    
    def get_campaign_status(self) -> Dict[str, Any]:
        """Get comprehensive campaign status"""
        try:
            current_state = self.captaincy_system.get_current_state()
            
            if current_state['current_campaign']:
                campaign = self.captaincy_system.current_campaign
                task_summary = {}
                for task in campaign.tasks:
                    status = task.status
                    if status not in task_summary:
                        task_summary[status] = 0
                    task_summary[status] += 1
                
                return {
                    **current_state,
                    "task_summary": task_summary,
                    "adopted_tasks_count": len(self.captaincy_system.adopted_tasks),
                    "campaign_duration": (datetime.now() - self.captaincy_system.campaign_start_date).days if self.captaincy_system.campaign_start_date else 0
                }
            else:
                return current_state
        except Exception as e:
            self.logger.error(f"Failed to get campaign status: {e}")
            return {}
    
    def get_available_campaigns(self) -> List[CampaignTaskList]:
        """Get all available campaign proposals for voting"""
        try:
            return list(self.captaincy_system.active_campaigns.values())
        except Exception as e:
            self.logger.error(f"Failed to get available campaigns: {e}")
            return []
    
    def can_start_new_campaign(self) -> bool:
        """Check if a new campaign can be started (80% completion reached)"""
        try:
            return self.captaincy_system.can_start_new_campaign()
        except Exception as e:
            self.logger.error(f"Failed to check if new campaign can start: {e}")
            return False
    
    def get_campaign_completion_status(self) -> Dict[str, Any]:
        """Get detailed campaign completion status"""
        try:
            return self.captaincy_system.check_campaign_completion()
        except Exception as e:
            self.logger.error(f"Failed to get campaign completion status: {e}")
            return {"action": "none", "completion_percentage": 0.0}
    
    def trigger_automated_campaign_workflow(self) -> bool:
        """Manually trigger the automated campaign workflow"""
        try:
            if self.campaign_workflow_state == "idle":
                self._automated_start_campaign_collection()
                return True
            else:
                self.logger.warning(f"Cannot trigger workflow - current state: {self.campaign_workflow_state}")
                return False
        except Exception as e:
            self.logger.error(f"Failed to trigger automated campaign workflow: {e}")
            return False
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status and deadlines"""
        try:
            return {
                "workflow_state": self.campaign_workflow_state,
                "deadlines": {
                    "submission": self.campaign_deadlines.get("submission"),
                    "voting": self.campaign_deadlines.get("voting")
                },
                "submissions_count": len(self._collect_submitted_campaigns()),
                "can_start_new": self.can_start_new_campaign()
            }
        except Exception as e:
            self.logger.error(f"Failed to get workflow status: {e}")
            return {}
    
    def _create_campaign_transition_knowledge(self, campaign_id: str, captain_agent: str, campaign_title: str):
        """Create knowledge item for campaign transition"""
        transition_knowledge = KnowledgeItem(
            id=str(uuid.uuid4()),
            type=KnowledgeType.STRATEGIC_INITIATIVE,
            title=f"Campaign Transition: {campaign_title}",
            content=f"New campaign initiated under {captain_agent} with campaign ID: {campaign_id}",
            agent_id=captain_agent,
            priority=KnowledgePriority.PRESIDENTIAL,
            tags=["campaign", "captaincy", "coordination", "election"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            version=1,
            dependencies=[],
            status="active",
            metadata={
                "campaign_id": campaign_id,
                "captain": captain_agent,
                "campaign_title": campaign_title,
                "transition_type": "campaign_selection"
            },
            presidential_approval=captain_agent,
            term_affiliation=CaptaincyTerm.CAMPAIGN_TERM
        )
        
        self.add_knowledge_item(transition_knowledge)

def main():
    """Main function to demonstrate the enhanced campaign-based system"""
    print("🚀 ENHANCED COLLABORATIVE KNOWLEDGE MANAGEMENT SYSTEM")
    print("🎯 CAMPAIGN-BASED CAPTAINCY SYSTEM")
    print("=" * 60)
    
    # Initialize the enhanced system
    system = EnhancedCollaborativeKnowledgeManager()
    
    # Display current campaign status
    campaign_status = system.get_campaign_status()
    print(f"\n🎯 CURRENT CAMPAIGN STATUS:")
    print(f"Term: {campaign_status['current_term']}")
    print(f"Captain: {campaign_status.get('current_captain', 'None (Election Phase)')}")
    
    if campaign_status.get('current_captain'):
        print(f"Campaign: {campaign_status.get('campaign_title', 'N/A')}")
        print(f"Progress: {campaign_status.get('campaign_progress', 0):.1%}")
        print(f"Tasks Completed: {campaign_status.get('tasks_completed', 0)}/{campaign_status.get('total_tasks', 0)}")
        print(f"Campaign Duration: {campaign_status.get('campaign_duration', 0)} days")
        
        # Show completion thresholds
        completion_status = system.get_campaign_completion_status()
        print(f"\n📊 COMPLETION THRESHOLDS:")
        print(f"  New Campaign Start: 80% (Ready: {completion_status['action'] == 'start_new'})")
        print(f"  Captain Handoff: 95% (Ready: {completion_status['action'] == 'handoff'})")
        print(f"  Current Action: {completion_status['action']}")
        
        if 'task_summary' in campaign_status:
            print(f"\n📋 TASK SUMMARY:")
            for status, count in campaign_status['task_summary'].items():
                print(f"  {status}: {count}")
    else:
        print(f"Active Campaigns: {campaign_status.get('active_campaigns', 0)}")
        print(f"Voting Open: {campaign_status.get('voting_open', False)}")
    
    # Show if new campaign can start
    if system.can_start_new_campaign():
        print(f"\n✅ NEW CAMPAIGN STATUS: Ready to start new campaign")
    else:
        print(f"\n⏳ NEW CAMPAIGN STATUS: Waiting for current campaign to reach 80% completion")
    
    # Show automated workflow status
    workflow_status = system.get_workflow_status()
    print(f"\n🤖 AUTOMATED WORKFLOW STATUS:")
    print(f"Current State: {workflow_status.get('workflow_state', 'Unknown')}")
    print(f"Submissions Count: {workflow_status.get('submissions_count', 0)}")
    
    if workflow_status.get('deadlines', {}).get('submission'):
        deadline = workflow_status['deadlines']['submission']
        if isinstance(deadline, datetime):
            print(f"Submission Deadline: {deadline.strftime('%Y-%m-%d %H:%M')}")
    
    if workflow_status.get('deadlines', {}).get('voting'):
        deadline = workflow_status['deadlines']['voting']
        if isinstance(deadline, datetime):
            print(f"Voting Deadline: {deadline.strftime('%Y-%m-%d %H:%M')}")
    
    print(f"\n📁 CAMPAIGN SUBMISSIONS:")
    print(f"Directory: {system.campaign_submissions_dir}")
    print(f"Template: campaign_template.md")
    print(f"README: README.md")
    
    print(f"\n📚 KNOWLEDGE STATUS:")
    print(f"Total Items: {len(system.knowledge_base)}")
    print(f"Presidential Decisions: {len(system.presidential_decisions)}")
    
    print(f"\n✅ System initialized successfully!")
    print("Commands:")
    print("  - Press Ctrl+C to stop")
    print("  - Use system.trigger_automated_campaign_workflow() to start campaign collection")
    print("  - Check captain_submissions/ directory for campaign files")
    
    try:
        # Keep the system running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down enhanced knowledge management system...")

if __name__ == "__main__":
    main()

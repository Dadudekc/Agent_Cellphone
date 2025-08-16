"""
🤝 Collaborative Knowledge Manager

**Agent-1 Responsibility**: Strategic coordination and knowledge management
**Purpose**: Centralized knowledge sharing and collaboration tracking
**Features**: Real-time updates, version control, agent contribution tracking

This module provides the core system for managing collaborative knowledge
across all agents, enabling strategic coordination and collective intelligence.
"""

import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

class CollaborativeKnowledgeManager:
    """
    Centralized knowledge management system for multi-agent collaboration.
    
    **Agent-1 leads this system** to coordinate strategic planning and
    knowledge sharing across all agents.
    """
    
    def __init__(self, knowledge_base_path: str = "src/collaborative/knowledge_base/data"):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.knowledge_base_path.mkdir(parents=True, exist_ok=True)
        
        # Core knowledge structures
        self.collaborative_tasks = {}
        self.agent_knowledge = {}
        self.shared_insights = {}
        self.collaboration_metrics = {}
        
        # Real-time collaboration state
        self.active_collaborations = {}
        self.collaboration_history = []
        self.agent_synergy_scores = {}
        
        # Threading for real-time updates
        self._lock = threading.RLock()
        self._monitoring_active = False
        self._monitor_thread = None
        
        # Initialize logging
        self._setup_logging()
        
        # Load existing knowledge
        self._load_existing_knowledge()
        
        logging.info("🤝 Collaborative Knowledge Manager initialized - Agent-1 coordination active")
    
    def _setup_logging(self):
        """Setup logging for collaboration tracking."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - 🤝 %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.knowledge_base_path / 'collaboration.log'),
                logging.StreamHandler()
            ]
        )
    
    def _load_existing_knowledge(self):
        """Load existing knowledge from persistent storage."""
        try:
            # Load collaborative tasks
            tasks_file = self.knowledge_base_path / 'collaborative_tasks.json'
            if tasks_file.exists():
                with open(tasks_file, 'r') as f:
                    self.collaborative_tasks = json.load(f)
            
            # Load agent knowledge
            agents_file = self.knowledge_base_path / 'agent_knowledge.json'
            if agents_file.exists():
                with open(agents_file, 'r') as f:
                    self.agent_knowledge = json.load(f)
            
            # Load collaboration metrics
            metrics_file = self.knowledge_base_path / 'collaboration_metrics.json'
            if metrics_file.exists():
                with open(metrics_file, 'r') as f:
                    self.collaboration_metrics = json.load(f)
                    
            logging.info(f"📚 Loaded existing knowledge: {len(self.collaborative_tasks)} tasks, {len(self.agent_knowledge)} agents")
            
        except Exception as e:
            logging.warning(f"⚠️ Could not load existing knowledge: {e}")
    
    def start_collaboration_monitoring(self):
        """Start real-time collaboration monitoring (Agent-1 coordination)."""
        with self._lock:
            if not self._monitoring_active:
                self._monitoring_active = True
                self._monitor_thread = threading.Thread(target=self._monitor_collaborations, daemon=True)
                self._monitor_thread.start()
                logging.info("🚀 Agent-1: Collaboration monitoring started - strategic coordination active")
    
    def stop_collaboration_monitoring(self):
        """Stop collaboration monitoring."""
        with self._lock:
            self._monitoring_active = False
            if self._monitor_thread:
                self._monitor_thread.join(timeout=5)
            logging.info("🛑 Agent-1: Collaboration monitoring stopped")
    
    def _monitor_collaborations(self):
        """Background thread for monitoring active collaborations."""
        while self._monitoring_active:
            try:
                # Monitor active collaborations
                self._update_collaboration_metrics()
                
                # Save knowledge periodically
                self._save_knowledge()
                
                # Sleep for monitoring interval
                time.sleep(30)  # 30 second monitoring interval
                
            except Exception as e:
                logging.error(f"❌ Collaboration monitoring error: {e}")
                time.sleep(60)  # Longer sleep on error
    
    def create_collaborative_task(self, task_id: str, task_type: str, 
                                description: str, agents: List[str], 
                                priority: str = "medium") -> Dict[str, Any]:
        """
        Create a new collaborative task (Agent-1 coordination).
        
        Args:
            task_id: Unique task identifier
            task_type: Type of collaborative task
            description: Task description
            agents: List of agents involved
            priority: Task priority (low/medium/high/critical)
        
        Returns:
            Created task information
        """
        with self._lock:
            task = {
                "task_id": task_id,
                "task_type": task_type,
                "description": description,
                "agents": agents,
                "priority": priority,
                "status": "created",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "progress": 0.0,
                "contributions": {},
                "dependencies": [],
                "estimated_completion": None,
                "actual_completion": None
            }
            
            self.collaborative_tasks[task_id] = task
            
            # Initialize agent contributions
            for agent in agents:
                task["contributions"][agent] = {
                    "status": "assigned",
                    "assigned_at": datetime.now().isoformat(),
                    "progress": 0.0,
                    "insights": [],
                    "blockers": []
                }
            
            logging.info(f"📋 Agent-1: Created collaborative task '{task_id}' with {len(agents)} agents")
            return task
    
    def update_task_progress(self, task_id: str, agent: str, 
                           progress: float, insights: List[str] = None,
                           blockers: List[str] = None) -> bool:
        """
        Update task progress for a specific agent.
        
        Args:
            task_id: Task identifier
            agent: Agent updating progress
            progress: Progress percentage (0.0 to 1.0)
            insights: New insights discovered
            blockers: Blockers encountered
        
        Returns:
            Success status
        """
        with self._lock:
            if task_id not in self.collaborative_tasks:
                logging.warning(f"⚠️ Task '{task_id}' not found")
                return False
            
            task = self.collaborative_tasks[task_id]
            if agent not in task["contributions"]:
                logging.warning(f"⚠️ Agent '{agent}' not assigned to task '{task_id}'")
                return False
            
            # Update agent contribution
            contribution = task["contributions"][agent]
            contribution["progress"] = progress
            contribution["updated_at"] = datetime.now().isoformat()
            
            if insights:
                contribution["insights"].extend(insights)
            
            if blockers:
                contribution["blockers"].extend(blockers)
            
            # Update overall task progress
            total_progress = sum(c["progress"] for c in task["contributions"].values())
            task["progress"] = total_progress / len(task["contributions"])
            task["updated_at"] = datetime.now().isoformat()
            
            # Check for task completion
            if task["progress"] >= 1.0 and task["status"] != "completed":
                task["status"] = "completed"
                task["actual_completion"] = datetime.now().isoformat()
                logging.info(f"🎉 Task '{task_id}' completed by collaborative effort!")
            
            logging.info(f"📊 Agent-1: Updated progress for task '{task_id}' - {agent}: {progress:.1%}")
            return True
    
    def add_shared_insight(self, insight_id: str, agent: str, 
                          insight_type: str, content: str, 
                          related_tasks: List[str] = None) -> Dict[str, Any]:
        """
        Add a shared insight to the knowledge base.
        
        Args:
            insight_id: Unique insight identifier
            agent: Agent providing the insight
            insight_type: Type of insight
            content: Insight content
            related_tasks: Related task IDs
        
        Returns:
            Created insight information
        """
        with self._lock:
            insight = {
                "insight_id": insight_id,
                "agent": agent,
                "insight_type": insight_type,
                "content": content,
                "related_tasks": related_tasks or [],
                "created_at": datetime.now().isoformat(),
                "upvotes": 0,
                "downvotes": 0,
                "verified": False,
                "impact_score": 0.0
            }
            
            self.shared_insights[insight_id] = insight
            
            # Update agent knowledge
            if agent not in self.agent_knowledge:
                self.agent_knowledge[agent] = {"insights": [], "expertise": {}, "collaboration_history": []}
            
            self.agent_knowledge[agent]["insights"].append(insight_id)
            
            logging.info(f"💡 Agent-1: Added shared insight '{insight_id}' from {agent}")
            return insight
    
    def get_collaboration_summary(self) -> Dict[str, Any]:
        """Get comprehensive collaboration summary (Agent-1 reporting)."""
        with self._lock:
            total_tasks = len(self.collaborative_tasks)
            completed_tasks = len([t for t in self.collaborative_tasks.values() if t["status"] == "completed"])
            active_tasks = len([t for t in self.collaborative_tasks.values() if t["status"] in ["created", "in_progress"]])
            
            total_insights = len(self.shared_insights)
            total_agents = len(self.agent_knowledge)
            
            # Calculate collaboration metrics
            avg_task_progress = sum(t["progress"] for t in self.collaborative_tasks.values()) / max(total_tasks, 1)
            
            summary = {
                "collaboration_status": "ACTIVE",
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "active_tasks": active_tasks,
                "completion_rate": completed_tasks / max(total_tasks, 1),
                "average_progress": avg_task_progress,
                "total_insights": total_insights,
                "active_agents": total_agents,
                "collaboration_momentum": "ACCELERATING" if avg_task_progress > 0.5 else "BUILDING",
                "last_updated": datetime.now().isoformat()
            }
            
            return summary
    
    def _update_collaboration_metrics(self):
        """Update real-time collaboration metrics."""
        with self._lock:
            summary = self.get_collaboration_summary()
            
            # Calculate synergy scores
            for agent in self.agent_knowledge:
                if agent in self.agent_synergy_scores:
                    # Update synergy based on recent contributions
                    recent_contributions = len([t for t in self.collaborative_tasks.values() 
                                             if agent in t["contributions"] and t["updated_at"] > 
                                             (datetime.now().isoformat()[:-6] + "Z")])
                    self.agent_synergy_scores[agent] = min(100, self.agent_synergy_scores[agent] + recent_contributions * 5)
                else:
                    self.agent_synergy_scores[agent] = 50  # Base synergy score
            
            # Store metrics
            self.collaboration_metrics = summary
    
    def _save_knowledge(self):
        """Save knowledge to persistent storage."""
        try:
            with open(self.knowledge_base_path / 'collaborative_tasks.json', 'w') as f:
                json.dump(self.collaborative_tasks, f, indent=2)
            
            with open(self.knowledge_base_path / 'agent_knowledge.json', 'w') as f:
                json.dump(self.agent_knowledge, f, indent=2)
            
            with open(self.knowledge_base_path / 'collaboration_metrics.json', 'w') as f:
                json.dump(self.collaboration_metrics, f, indent=2)
                
        except Exception as e:
            logging.error(f"❌ Failed to save knowledge: {e}")
    
    def get_agent_recommendations(self, agent: str) -> Dict[str, Any]:
        """
        Get personalized recommendations for an agent based on collaboration patterns.
        
        Args:
            agent: Agent identifier
        
        Returns:
            Personalized recommendations
        """
        with self._lock:
            if agent not in self.agent_knowledge:
                return {"recommendations": [], "collaboration_opportunities": []}
            
            # Analyze agent's current tasks and suggest optimizations
            agent_tasks = [t for t in self.collaborative_tasks.values() 
                          if agent in t["contributions"]]
            
            recommendations = []
            collaboration_opportunities = []
            
            # Task-specific recommendations
            for task in agent_tasks:
                if task["progress"] < 0.5:
                    recommendations.append({
                        "type": "task_optimization",
                        "task_id": task["task_id"],
                        "suggestion": f"Focus on completing core deliverables for task '{task['description']}'",
                        "priority": "high" if task["priority"] in ["high", "critical"] else "medium"
                    })
                
                # Find collaboration opportunities
                other_agents = [a for a in task["agents"] if a != agent]
                for other_agent in other_agents:
                    if other_agent in self.agent_knowledge:
                        collaboration_opportunities.append({
                            "type": "agent_collaboration",
                            "task_id": task["task_id"],
                            "partner_agent": other_agent,
                            "suggestion": f"Coordinate with {other_agent} on task '{task['description']}'",
                            "synergy_potential": self.agent_synergy_scores.get(other_agent, 50)
                        })
            
            return {
                "recommendations": recommendations,
                "collaboration_opportunities": collaboration_opportunities,
                "current_synergy_score": self.agent_synergy_scores.get(agent, 50),
                "generated_at": datetime.now().isoformat()
            }
    
    def __str__(self):
        """String representation of collaboration status."""
        summary = self.get_collaboration_summary()
        return (f"🤝 Collaborative Knowledge Manager - "
                f"Status: {summary['collaboration_status']}, "
                f"Tasks: {summary['completed_tasks']}/{summary['total_tasks']} completed, "
                f"Momentum: {summary['collaboration_momentum']}")


# Global instance for system-wide access
collaborative_knowledge_manager = CollaborativeKnowledgeManager()

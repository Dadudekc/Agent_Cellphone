#!/usr/bin/env python3
"""
Enhanced Collaborative System Integration

**Agent-2 Responsibility**: Task Breakdown & Resource Allocation
**Purpose**: Integrate enhanced task breakdown and workflow optimization systems
**Features**:
- Unified collaborative task management
- Intelligent resource allocation and optimization
- Workflow efficiency monitoring and improvement
- Seamless integration with existing collaborative framework

This module provides the main integration point for all enhanced collaborative
capabilities, creating a unified system that maximizes agent synergy and
minimizes task completion time.
"""

import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Set
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import math
from collections import defaultdict, Counter

# Import enhanced systems
from enhanced_task_breakdown import EnhancedTaskBreakdown, TaskBreakdown, TaskComponent
from workflow_optimizer import WorkflowOptimizer, CollaborativeWorkflow, WorkflowStage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CollaborationMode(Enum):
    """Collaboration modes"""
    SEQUENTIAL = "sequential"      # Tasks executed in sequence
    PARALLEL = "parallel"          # Tasks executed in parallel
    ADAPTIVE = "adaptive"          # Dynamic adaptation based on performance
    OPTIMIZED = "optimized"        # Fully optimized collaboration

class SystemPerformance(Enum):
    """System performance levels"""
    CRITICAL = "critical"          # < 0.3 efficiency
    POOR = "poor"                  # 0.3 - 0.5 efficiency
    FAIR = "fair"                  # 0.5 - 0.7 efficiency
    GOOD = "good"                  # 0.7 - 0.8 efficiency
    EXCELLENT = "excellent"        # 0.8 - 0.9 efficiency
    OUTSTANDING = "outstanding"    # > 0.9 efficiency

@dataclass
class SystemMetrics:
    """System-wide performance metrics"""
    metric_id: str
    metric_type: str
    value: float
    unit: str
    timestamp: str
    context: Dict[str, Any]
    trend: str
    impact_score: float  # 0.0 to 1.0

@dataclass
class CollaborationSession:
    """Collaboration session data"""
    session_id: str
    title: str
    description: str
    participants: List[str]
    mode: CollaborationMode
    workflows: List[str]  # Workflow IDs
    task_breakdowns: List[str]  # Breakdown IDs
    start_time: str
    end_time: Optional[str]
    efficiency_score: float
    performance_metrics: List[SystemMetrics]
    created_at: str
    updated_at: str

@dataclass
class OptimizationResult:
    """Result of system optimization"""
    optimization_id: str
    session_id: str
    optimization_type: str
    description: str
    before_score: float
    after_score: float
    improvement: float
    implementation_time: float
    created_at: str

class EnhancedCollaborativeSystem:
    """Enhanced collaborative system integration"""

    def __init__(self, base_path: Path):
        """
        Initialize Enhanced Collaborative System
        
        Args:
            base_path: Base directory for collaborative system data
        """
        self.base_path = Path(base_path)
        self.sessions_dir = self.base_path / "sessions"
        self.metrics_dir = self.base_path / "system_metrics"
        self.optimizations_dir = self.base_path / "optimization_results"
        
        # Create necessary directories
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        self.optimizations_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize enhanced systems
        self.task_breakdown = EnhancedTaskBreakdown(base_path)
        self.workflow_optimizer = WorkflowOptimizer(base_path)
        
        # System state
        self._session_cache: Dict[str, CollaborationSession] = {}
        self._metrics_cache: Dict[str, SystemMetrics] = {}
        
        # Load existing data
        self._load_existing_data()
        
        logger.info(f"Enhanced Collaborative System initialized: {self.base_path}")

    def _load_existing_data(self) -> None:
        """Load existing sessions and metrics"""
        # Load sessions
        for session_file in self.sessions_dir.glob("*.json"):
            try:
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                    session = CollaborationSession(**session_data)
                    self._session_cache[session.session_id] = session
            except Exception as e:
                logger.error(f"Error loading session {session_file}: {e}")
        
        # Load metrics
        for metric_file in self.metrics_dir.glob("*.json"):
            try:
                with open(metric_file, 'r') as f:
                    metric_data = json.load(f)
                    metric = SystemMetrics(**metric_data)
                    self._metrics_cache[metric.metric_id] = metric
            except Exception as e:
                logger.error(f"Error loading metric {metric_file}: {e}")

    def create_collaboration_session(
        self,
        title: str,
        description: str,
        participants: List[str],
        mode: CollaborationMode = CollaborationMode.OPTIMIZED
    ) -> CollaborationSession:
        """Create a new collaboration session"""
        session_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        session = CollaborationSession(
            session_id=session_id,
            title=title,
            description=description,
            participants=participants,
            mode=mode,
            workflows=[],
            task_breakdowns=[],
            start_time=now,
            end_time=None,
            efficiency_score=0.0,
            performance_metrics=[],
            created_at=now,
            updated_at=now
        )
        
        # Save session
        self._save_session(session)
        self._session_cache[session_id] = session
        
        logger.info(f"Created collaboration session: {title}")
        return session

    def add_task_to_session(
        self,
        session_id: str,
        task_id: str,
        title: str,
        description: str,
        estimated_hours: float,
        required_skills: List[str],
        priority: str = "normal"
    ) -> Tuple[TaskBreakdown, CollaborativeWorkflow]:
        """Add a task to a collaboration session with breakdown and workflow"""
        if session_id not in self._session_cache:
            raise ValueError(f"Session {session_id} not found")
        
        session = self._session_cache[session_id]
        
        # Create task breakdown
        breakdown = self.task_breakdown.breakdown_complex_task(
            task_id=task_id,
            title=title,
            description=description,
            estimated_hours=estimated_hours,
            required_skills=required_skills,
            priority=self._convert_priority(priority)
        )
        
        # Create collaborative workflow
        workflow = self.workflow_optimizer.create_collaborative_workflow(
            title=f"Workflow for {title}",
            description=f"Collaborative workflow for task: {description}",
            participants=session.participants,
            dependencies=[]
        )
        
        # Add to session
        session.task_breakdowns.append(breakdown.breakdown_id)
        session.workflows.append(workflow.workflow_id)
        session.updated_at = datetime.now().isoformat()
        
        # Save session
        self._save_session(session)
        
        logger.info(f"Added task {title} to session {session_id}")
        return breakdown, workflow

    def _convert_priority(self, priority: str) -> Any:
        """Convert string priority to enum"""
        from enhanced_task_breakdown import TaskPriority
        
        priority_mapping = {
            "low": TaskPriority.LOW,
            "normal": TaskPriority.NORMAL,
            "high": TaskPriority.HIGH,
            "urgent": TaskPriority.URGENT,
            "critical": TaskPriority.CRITICAL
        }
        
        return priority_mapping.get(priority.lower(), TaskPriority.NORMAL)

    def optimize_session_collaboration(self, session_id: str) -> OptimizationResult:
        """Optimize collaboration within a session"""
        if session_id not in self._session_cache:
            raise ValueError(f"Session {session_id} not found")
        
        session = self._session_cache[session_id]
        
        # Record before score
        before_score = session.efficiency_score
        
        # Optimize task breakdowns
        for breakdown_id in session.task_breakdowns:
            self.task_breakdown.optimize_existing_breakdown(breakdown_id)
        
        # Optimize workflows
        for workflow_id in session.workflows:
            self.workflow_optimizer.generate_optimization_recommendations(workflow_id)
        
        # Recalculate session efficiency
        session.efficiency_score = self._calculate_session_efficiency(session)
        session.updated_at = datetime.now().isoformat()
        
        # Save session
        self._save_session(session)
        
        # Create optimization result
        after_score = session.efficiency_score
        improvement = after_score - before_score
        
        optimization_result = OptimizationResult(
            optimization_id=str(uuid.uuid4()),
            session_id=session_id,
            optimization_type="session_optimization",
            description=f"Optimized collaboration session: {session.title}",
            before_score=before_score,
            after_score=after_score,
            improvement=improvement,
            implementation_time=0.0,  # Would measure actual time in real implementation
            created_at=datetime.now().isoformat()
        )
        
        # Save optimization result
        self._save_optimization_result(optimization_result)
        
        logger.info(f"Optimized session {session_id}: {improvement:.2%} improvement")
        return optimization_result

    def _calculate_session_efficiency(self, session: CollaborationSession) -> float:
        """Calculate overall session efficiency"""
        if not session.workflows and not session.task_breakdowns:
            return 0.0
        
        efficiency_scores = []
        
        # Workflow efficiency scores
        for workflow_id in session.workflows:
            workflow = self.workflow_optimizer._workflow_cache.get(workflow_id)
            if workflow:
                efficiency_scores.append(workflow.efficiency_score)
        
        # Task breakdown optimization scores
        for breakdown_id in session.task_breakdowns:
            # Load breakdown to get optimization score
            breakdown_file = self.task_breakdown.breakdowns_dir / f"{breakdown_id}.json"
            if breakdown_file.exists():
                try:
                    with open(breakdown_file, 'r') as f:
                        breakdown_data = json.load(f)
                        efficiency_scores.append(breakdown_data.get("optimization_score", 0.0))
                except Exception as e:
                    logger.error(f"Error loading breakdown {breakdown_id}: {e}")
        
        # Calculate weighted average
        if efficiency_scores:
            # Weight workflows more heavily than task breakdowns
            workflow_weight = 0.6
            breakdown_weight = 0.4
            
            workflow_scores = efficiency_scores[:len(session.workflows)]
            breakdown_scores = efficiency_scores[len(session.workflows):]
            
            workflow_avg = sum(workflow_scores) / len(workflow_scores) if workflow_scores else 0.0
            breakdown_avg = sum(breakdown_scores) / len(breakdown_scores) if breakdown_scores else 0.0
            
            total_efficiency = (workflow_avg * workflow_weight + 
                              breakdown_avg * breakdown_weight)
            
            return max(0.0, min(1.0, total_efficiency))
        
        return 0.0

    def add_system_metric(
        self,
        session_id: str,
        metric_type: str,
        value: float,
        unit: str,
        context: Dict[str, Any] = None,
        impact_score: float = 0.5
    ) -> SystemMetrics:
        """Add a system-wide performance metric"""
        if session_id not in self._session_cache:
            raise ValueError(f"Session {session_id} not found")
        
        session = self._session_cache[session_id]
        
        metric = SystemMetrics(
            metric_id=str(uuid.uuid4()),
            metric_type=metric_type,
            value=value,
            unit=unit,
            timestamp=datetime.now().isoformat(),
            context=context or {},
            trend="stable",
            impact_score=max(0.0, min(1.0, impact_score))
        )
        
        # Add metric to session
        session.performance_metrics.append(metric.metric_id)
        session.updated_at = datetime.now().isoformat()
        
        # Save metric
        self._save_system_metric(metric)
        self._metrics_cache[metric.metric_id] = metric
        
        # Save session
        self._save_session(session)
        
        # Update session efficiency
        session.efficiency_score = self._calculate_session_efficiency(session)
        self._save_session(session)
        
        logger.info(f"Added system metric {metric_type} to session {session_id}")
        return metric

    def get_session_performance_summary(self, session_id: str) -> Dict[str, Any]:
        """Get comprehensive performance summary for a session"""
        if session_id not in self._session_cache:
            return {}
        
        session = self._session_cache[session_id]
        
        # Get workflow summaries
        workflow_summaries = []
        for workflow_id in session.workflows:
            workflow = self.workflow_optimizer._workflow_cache.get(workflow_id)
            if workflow:
                workflow_summaries.append({
                    "workflow_id": workflow_id,
                    "title": workflow.title,
                    "current_stage": workflow.current_stage.value,
                    "efficiency_score": workflow.efficiency_score,
                    "total_metrics": len(workflow.metrics),
                    "total_patterns": len(workflow.patterns),
                    "total_optimizations": len(workflow.optimizations)
                })
        
        # Get task breakdown summaries
        breakdown_summaries = []
        for breakdown_id in session.task_breakdowns:
            breakdown_file = self.task_breakdown.breakdowns_dir / f"{breakdown_id}.json"
            if breakdown_file.exists():
                try:
                    with open(breakdown_file, 'r') as f:
                        breakdown_data = json.load(f)
                        breakdown_summaries.append({
                            "breakdown_id": breakdown_id,
                            "title": breakdown_data.get("original_title", "Unknown"),
                            "total_components": len(breakdown_data.get("components", [])),
                            "optimization_score": breakdown_data.get("optimization_score", 0.0),
                            "total_estimated_hours": breakdown_data.get("total_estimated_hours", 0.0)
                        })
                except Exception as e:
                    logger.error(f"Error loading breakdown {breakdown_id}: {e}")
        
        # Calculate performance indicators
        performance_indicators = self._calculate_performance_indicators(session)
        
        return {
            "session_id": session_id,
            "title": session.title,
            "mode": session.mode.value,
            "participants": session.participants,
            "start_time": session.start_time,
            "efficiency_score": session.efficiency_score,
            "performance_level": self._get_performance_level(session.efficiency_score),
            "workflows": workflow_summaries,
            "task_breakdowns": breakdown_summaries,
            "performance_indicators": performance_indicators,
            "total_metrics": len(session.performance_metrics),
            "collaboration_effectiveness": self._calculate_collaboration_effectiveness(session)
        }

    def _calculate_performance_indicators(self, session: CollaborationSession) -> Dict[str, Any]:
        """Calculate key performance indicators for the session"""
        indicators = {}
        
        # Time efficiency
        if session.start_time and not session.end_time:
            start_time = datetime.fromisoformat(session.start_time.replace('Z', '+00:00'))
            current_time = datetime.now(start_time.tzinfo)
            duration = (current_time - start_time).total_seconds() / 3600  # hours
            
            indicators["duration_hours"] = duration
            indicators["time_efficiency"] = min(1.0, 8.0 / max(duration, 1.0))  # Assume 8-hour optimal
        
        # Resource utilization
        total_participants = len(session.participants)
        total_workflows = len(session.workflows)
        total_breakdowns = len(session.task_breakdowns)
        
        indicators["resource_utilization"] = min(1.0, (total_workflows + total_breakdowns) / max(total_participants, 1))
        
        # Collaboration density
        indicators["collaboration_density"] = min(1.0, total_workflows / max(total_participants, 1))
        
        return indicators

    def _get_performance_level(self, efficiency_score: float) -> str:
        """Get performance level based on efficiency score"""
        if efficiency_score < 0.3:
            return SystemPerformance.CRITICAL.value
        elif efficiency_score < 0.5:
            return SystemPerformance.POOR.value
        elif efficiency_score < 0.7:
            return SystemPerformance.FAIR.value
        elif efficiency_score < 0.8:
            return SystemPerformance.GOOD.value
        elif efficiency_score < 0.9:
            return SystemPerformance.EXCELLENT.value
        else:
            return SystemPerformance.OUTSTANDING.value

    def _calculate_collaboration_effectiveness(self, session: CollaborationSession) -> float:
        """Calculate collaboration effectiveness score"""
        if not session.participants:
            return 0.0
        
        # Base effectiveness on participant engagement
        participant_engagement = []
        
        for participant in session.participants:
            # Calculate individual engagement based on their involvement
            engagement_score = 0.0
            
            # Check workflow involvement
            for workflow_id in session.workflows:
                workflow = self.workflow_optimizer._workflow_cache.get(workflow_id)
                if workflow and participant in workflow.participants:
                    engagement_score += 0.3
            
            # Check task breakdown involvement
            for breakdown_id in session.task_breakdowns:
                breakdown_file = self.task_breakdown.breakdowns_dir / f"{breakdown_id}.json"
                if breakdown_file.exists():
                    try:
                        with open(breakdown_file, 'r') as f:
                            breakdown_data = json.load(f)
                            resource_allocation = breakdown_data.get("resource_allocation", {})
                            if participant in resource_allocation:
                                engagement_score += 0.2
                    except Exception:
                        pass
            
            participant_engagement.append(min(1.0, engagement_score))
        
        # Return average engagement
        return sum(participant_engagement) / len(participant_engagement) if participant_engagement else 0.0

    def complete_session(self, session_id: str) -> bool:
        """Mark a collaboration session as completed"""
        if session_id not in self._session_cache:
            return False
        
        session = self._session_cache[session_id]
        session.end_time = datetime.now().isoformat()
        session.updated_at = datetime.now().isoformat()
        
        # Final efficiency calculation
        session.efficiency_score = self._calculate_session_efficiency(session)
        
        # Save session
        self._save_session(session)
        
        logger.info(f"Completed collaboration session: {session.title}")
        return True

    def get_system_summary(self) -> Dict[str, Any]:
        """Get comprehensive system summary"""
        sessions = list(self._session_cache.values())
        
        # Calculate system-wide metrics
        total_sessions = len(sessions)
        active_sessions = len([s for s in sessions if not s.end_time])
        completed_sessions = len([s for s in sessions if s.end_time])
        
        # Average efficiency scores
        efficiency_scores = [s.efficiency_score for s in sessions]
        average_efficiency = sum(efficiency_scores) / len(efficiency_scores) if efficiency_scores else 0.0
        
        # Performance distribution
        performance_distribution = Counter()
        for score in efficiency_scores:
            level = self._get_performance_level(score)
            performance_distribution[level] += 1
        
        # Collaboration mode distribution
        mode_distribution = Counter(s.mode for s in sessions)
        
        return {
            "total_sessions": total_sessions,
            "active_sessions": active_sessions,
            "completed_sessions": completed_sessions,
            "average_efficiency": average_efficiency,
            "performance_distribution": dict(performance_distribution),
            "collaboration_mode_distribution": dict(mode_distribution),
            "total_workflows": sum(len(s.workflows) for s in sessions),
            "total_task_breakdowns": sum(len(s.task_breakdowns) for s in sessions),
            "total_participants": len(set().union(*[set(s.participants) for s in sessions])),
            "system_health": self._calculate_system_health(efficiency_scores)
        }

    def _calculate_system_health(self, efficiency_scores: List[float]) -> str:
        """Calculate overall system health"""
        if not efficiency_scores:
            return "unknown"
        
        # Calculate health based on efficiency distribution
        excellent_count = sum(1 for score in efficiency_scores if score >= 0.8)
        good_count = sum(1 for score in efficiency_scores if 0.7 <= score < 0.8)
        fair_count = sum(1 for score in efficiency_scores if 0.5 <= score < 0.7)
        poor_count = sum(1 for score in efficiency_scores if score < 0.5)
        
        total = len(efficiency_scores)
        
        # Health thresholds
        if excellent_count / total >= 0.6:
            return "excellent"
        elif (excellent_count + good_count) / total >= 0.7:
            return "good"
        elif (excellent_count + good_count + fair_count) / total >= 0.8:
            return "fair"
        else:
            return "needs_attention"

    def _save_session(self, session: CollaborationSession) -> None:
        """Save session to disk"""
        session_file = self.sessions_dir / f"{session.session_id}.json"
        with open(session_file, 'w') as f:
            json.dump(asdict(session), f, indent=2, default=str)

    def _save_system_metric(self, metric: SystemMetrics) -> None:
        """Save system metric to disk"""
        metric_file = self.metrics_dir / f"{metric.metric_id}.json"
        with open(metric_file, 'w') as f:
            json.dump(asdict(metric), f, indent=2, default=str)

    def _save_optimization_result(self, result: OptimizationResult) -> None:
        """Save optimization result to disk"""
        result_file = self.optimizations_dir / f"{result.optimization_id}.json"
        with open(result_file, 'w') as f:
            json.dump(asdict(result), f, indent=2, default=str)

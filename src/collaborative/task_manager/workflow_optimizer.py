#!/usr/bin/env python3
"""
Workflow Optimization System

**Agent-2 Responsibility**: Task Breakdown & Resource Allocation
**Purpose**: Optimize collaborative workflows and process efficiency
**Features**:
- Workflow pattern analysis and optimization
- Process bottleneck identification and resolution
- Collaboration efficiency metrics and improvement
- Dynamic workflow adaptation based on performance

This module provides intelligent workflow optimization that maximizes
collaborative efficiency and minimizes process overhead.
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
import networkx as nx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowStage(Enum):
    """Workflow stages"""
    INITIATION = "initiation"
    PLANNING = "planning"
    EXECUTION = "execution"
    COLLABORATION = "collaboration"
    REVIEW = "review"
    COMPLETION = "completion"

class WorkflowEfficiency(Enum):
    """Workflow efficiency levels"""
    POOR = "poor"           # < 0.3
    FAIR = "fair"           # 0.3 - 0.5
    GOOD = "good"           # 0.5 - 0.7
    EXCELLENT = "excellent" # 0.7 - 0.9
    OUTSTANDING = "outstanding" # > 0.9

@dataclass
class WorkflowMetric:
    """Workflow performance metric"""
    metric_id: str
    workflow_id: str
    metric_type: str
    value: float
    unit: str
    timestamp: str
    context: Dict[str, Any]
    trend: str  # "improving", "stable", "declining"

@dataclass
class WorkflowPattern:
    """Identified workflow pattern"""
    pattern_id: str
    pattern_type: str
    description: str
    efficiency_score: float
    frequency: int
    agents_involved: List[str]
    average_duration: float
    success_rate: float
    identified_at: str

@dataclass
class WorkflowOptimization:
    """Workflow optimization recommendation"""
    optimization_id: str
    workflow_id: str
    optimization_type: str
    description: str
    expected_improvement: float
    implementation_effort: float
    priority: str
    created_at: str
    implemented: bool = False

@dataclass
class CollaborativeWorkflow:
    """Collaborative workflow structure"""
    workflow_id: str
    title: str
    description: str
    stages: List[WorkflowStage]
    current_stage: WorkflowStage
    participants: List[str]
    dependencies: List[str]
    metrics: List[WorkflowMetric]
    patterns: List[WorkflowPattern]
    optimizations: List[WorkflowOptimization]
    efficiency_score: float
    created_at: str
    updated_at: str
    completed_at: Optional[str] = None

class WorkflowOptimizer:
    """Intelligent workflow optimization system"""

    def __init__(self, base_path: Path):
        """
        Initialize Workflow Optimizer
        
        Args:
            base_path: Base directory for workflow optimization data
        """
        self.base_path = Path(base_path)
        self.workflows_dir = self.base_path / "workflows"
        self.metrics_dir = self.base_path / "metrics"
        self.patterns_dir = self.base_path / "patterns"
        self.optimizations_dir = self.base_path / "optimizations"
        
        # Create necessary directories
        self.workflows_dir.mkdir(parents=True, exist_ok=True)
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        self.patterns_dir.mkdir(parents=True, exist_ok=True)
        self.optimizations_dir.mkdir(parents=True, exist_ok=True)
        
        # Workflow cache
        self._workflow_cache: Dict[str, CollaborativeWorkflow] = {}
        self._pattern_cache: Dict[str, WorkflowPattern] = {}
        
        # Load existing workflows
        self._load_existing_workflows()
        
        logger.info(f"Workflow Optimizer initialized: {self.base_path}")

    def _load_existing_workflows(self) -> None:
        """Load existing workflows from disk"""
        for workflow_file in self.workflows_dir.glob("*.json"):
            try:
                with open(workflow_file, 'r') as f:
                    workflow_data = json.load(f)
                    workflow = CollaborativeWorkflow(**workflow_data)
                    self._workflow_cache[workflow.workflow_id] = workflow
            except Exception as e:
                logger.error(f"Error loading workflow {workflow_file}: {e}")

    def create_collaborative_workflow(
        self,
        title: str,
        description: str,
        participants: List[str],
        dependencies: List[str] = None
    ) -> CollaborativeWorkflow:
        """Create a new collaborative workflow"""
        workflow_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        # Define default workflow stages
        stages = [
            WorkflowStage.INITIATION,
            WorkflowStage.PLANNING,
            WorkflowStage.EXECUTION,
            WorkflowStage.COLLABORATION,
            WorkflowStage.REVIEW,
            WorkflowStage.COMPLETION
        ]
        
        workflow = CollaborativeWorkflow(
            workflow_id=workflow_id,
            title=title,
            description=description,
            stages=stages,
            current_stage=WorkflowStage.INITIATION,
            participants=participants,
            dependencies=dependencies or [],
            metrics=[],
            patterns=[],
            optimizations=[],
            efficiency_score=0.0,
            created_at=now,
            updated_at=now
        )
        
        # Save workflow
        self._save_workflow(workflow)
        self._workflow_cache[workflow_id] = workflow
        
        logger.info(f"Created collaborative workflow: {title}")
        return workflow

    def add_workflow_metric(
        self,
        workflow_id: str,
        metric_type: str,
        value: float,
        unit: str,
        context: Dict[str, Any] = None
    ) -> WorkflowMetric:
        """Add a performance metric to a workflow"""
        if workflow_id not in self._workflow_cache:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self._workflow_cache[workflow_id]
        
        metric = WorkflowMetric(
            metric_id=str(uuid.uuid4()),
            workflow_id=workflow_id,
            metric_type=metric_type,
            value=value,
            unit=unit,
            timestamp=datetime.now().isoformat(),
            context=context or {},
            trend="stable"
        )
        
        # Add metric to workflow
        workflow.metrics.append(metric)
        workflow.updated_at = datetime.now().isoformat()
        
        # Update workflow efficiency score
        workflow.efficiency_score = self._calculate_workflow_efficiency(workflow)
        
        # Save workflow
        self._save_workflow(workflow)
        
        # Analyze for patterns
        self._analyze_workflow_patterns(workflow)
        
        logger.info(f"Added metric {metric_type} to workflow {workflow_id}")
        return metric

    def advance_workflow_stage(self, workflow_id: str) -> bool:
        """Advance workflow to next stage"""
        if workflow_id not in self._workflow_cache:
            return False
        
        workflow = self._workflow_cache[workflow_id]
        
        # Find current stage index
        try:
            current_index = workflow.stages.index(workflow.current_stage)
            if current_index < len(workflow.stages) - 1:
                workflow.current_stage = workflow.stages[current_index + 1]
                workflow.updated_at = datetime.now().isoformat()
                
                # If completed, set completion time
                if workflow.current_stage == WorkflowStage.COMPLETION:
                    workflow.completed_at = datetime.now().isoformat()
                
                self._save_workflow(workflow)
                logger.info(f"Advanced workflow {workflow_id} to {workflow.current_stage}")
                return True
        except ValueError:
            logger.error(f"Invalid current stage in workflow {workflow_id}")
        
        return False

    def _calculate_workflow_efficiency(self, workflow: CollaborativeWorkflow) -> float:
        """Calculate overall workflow efficiency score"""
        if not workflow.metrics:
            return 0.0
        
        # Calculate efficiency based on various factors
        efficiency_factors = []
        
        # Stage progression efficiency
        stage_efficiency = self._calculate_stage_efficiency(workflow)
        efficiency_factors.append(stage_efficiency)
        
        # Time efficiency
        time_efficiency = self._calculate_time_efficiency(workflow)
        efficiency_factors.append(time_efficiency)
        
        # Collaboration efficiency
        collaboration_efficiency = self._calculate_collaboration_efficiency(workflow)
        efficiency_factors.append(collaboration_efficiency)
        
        # Metric-based efficiency
        metric_efficiency = self._calculate_metric_efficiency(workflow)
        efficiency_factors.append(metric_efficiency)
        
        # Weighted average of efficiency factors
        weights = [0.3, 0.25, 0.25, 0.2]  # Stage, Time, Collaboration, Metrics
        total_efficiency = sum(factor * weight for factor, weight in zip(efficiency_factors, weights))
        
        return max(0.0, min(1.0, total_efficiency))

    def _calculate_stage_efficiency(self, workflow: CollaborativeWorkflow) -> float:
        """Calculate efficiency based on stage progression"""
        if not workflow.stages:
            return 0.0
        
        # Calculate how far along the workflow is
        current_index = workflow.stages.index(workflow.current_stage)
        total_stages = len(workflow.stages)
        
        # Normalize to 0-1 range
        stage_progress = current_index / (total_stages - 1)
        
        # Consider completion status
        if workflow.completed_at:
            stage_progress = 1.0
        
        return stage_progress

    def _calculate_time_efficiency(self, workflow: CollaborativeWorkflow) -> float:
        """Calculate efficiency based on time metrics"""
        if not workflow.metrics:
            return 0.5  # Default neutral score
        
        # Look for time-related metrics
        time_metrics = [m for m in workflow.metrics if "time" in m.metric_type.lower()]
        
        if not time_metrics:
            return 0.5
        
        # Calculate average time efficiency
        time_scores = []
        for metric in time_metrics:
            # Normalize time values (lower is better for most time metrics)
            if metric.value > 0:
                # Assume optimal time is 1 hour, score decreases with longer times
                optimal_time = 1.0
                time_score = max(0.0, 1.0 - (metric.value - optimal_time) / optimal_time)
                time_scores.append(time_score)
        
        return sum(time_scores) / len(time_scores) if time_scores else 0.5

    def _calculate_collaboration_efficiency(self, workflow: CollaborativeWorkflow) -> float:
        """Calculate efficiency based on collaboration patterns"""
        if not workflow.patterns:
            return 0.5  # Default neutral score
        
        # Calculate average pattern efficiency
        pattern_scores = [pattern.efficiency_score for pattern in workflow.patterns]
        return sum(pattern_scores) / len(pattern_scores)

    def _calculate_metric_efficiency(self, workflow: CollaborativeWorkflow) -> float:
        """Calculate efficiency based on performance metrics"""
        if not workflow.metrics:
            return 0.5  # Default neutral score
        
        # Calculate average metric value (assuming higher is better)
        metric_values = [m.value for m in workflow.metrics if m.value >= 0]
        
        if not metric_values:
            return 0.5
        
        # Normalize to 0-1 range (assuming optimal value is 100)
        optimal_value = 100.0
        normalized_values = [min(1.0, value / optimal_value) for value in metric_values]
        
        return sum(normalized_values) / len(normalized_values)

    def _analyze_workflow_patterns(self, workflow: CollaborativeWorkflow) -> None:
        """Analyze workflow for recurring patterns"""
        if len(workflow.metrics) < 3:
            return  # Need more data for pattern analysis
        
        # Analyze metric patterns
        self._analyze_metric_patterns(workflow)
        
        # Analyze stage transition patterns
        self._analyze_stage_patterns(workflow)
        
        # Analyze collaboration patterns
        self._analyze_collaboration_patterns(workflow)

    def _analyze_metric_patterns(self, workflow: CollaborativeWorkflow) -> None:
        """Analyze patterns in workflow metrics"""
        # Group metrics by type
        metrics_by_type = defaultdict(list)
        for metric in workflow.metrics:
            metrics_by_type[metric.metric_type].append(metric)
        
        # Analyze trends for each metric type
        for metric_type, metrics in metrics_by_type.items():
            if len(metrics) < 2:
                continue
            
            # Sort by timestamp
            sorted_metrics = sorted(metrics, key=lambda m: m.timestamp)
            
            # Calculate trend
            values = [m.value for m in sorted_metrics]
            trend = self._calculate_trend(values)
            
            # Update metric trends
            for metric in sorted_metrics:
                metric.trend = trend
            
            # Check for significant patterns
            if len(values) >= 3:
                self._detect_metric_patterns(workflow, metric_type, values, trend)

    def _analyze_stage_patterns(self, workflow: CollaborativeWorkflow) -> None:
        """Analyze patterns in workflow stage transitions"""
        # This would analyze how workflows progress through stages
        # For now, we'll implement a basic analysis
        pass

    def _analyze_collaboration_patterns(self, workflow: CollaborativeWorkflow) -> None:
        """Analyze patterns in agent collaboration"""
        # This would analyze how agents collaborate within workflows
        # For now, we'll implement a basic analysis
        pass

    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend from a series of values"""
        if len(values) < 2:
            return "stable"
        
        # Simple linear trend calculation
        x_values = list(range(len(values)))
        y_values = values
        
        # Calculate slope
        n = len(values)
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        sum_x2 = sum(x * x for x in x_values)
        
        if n * sum_x2 - sum_x * sum_x == 0:
            return "stable"
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        
        # Determine trend based on slope
        if slope > 0.1:
            return "improving"
        elif slope < -0.1:
            return "declining"
        else:
            return "stable"

    def _detect_metric_patterns(
        self,
        workflow: CollaborativeWorkflow,
        metric_type: str,
        values: List[float],
        trend: str
    ) -> None:
        """Detect specific patterns in metric data"""
        # Detect common patterns
        patterns = []
        
        # Detect oscillation pattern
        if self._detect_oscillation(values):
            patterns.append("oscillation")
        
        # Detect plateau pattern
        if self._detect_plateau(values):
            patterns.append("plateau")
        
        # Detect acceleration pattern
        if self._detect_acceleration(values):
            patterns.append("acceleration")
        
        # Create pattern records
        for pattern_type in patterns:
            pattern = WorkflowPattern(
                pattern_id=str(uuid.uuid4()),
                pattern_type=pattern_type,
                description=f"{pattern_type} pattern detected in {metric_type}",
                efficiency_score=0.7,  # Default score
                frequency=1,
                agents_involved=workflow.participants,
                average_duration=sum(values) / len(values),
                success_rate=0.8,  # Default rate
                identified_at=datetime.now().isoformat()
            )
            
            workflow.patterns.append(pattern)
            self._pattern_cache[pattern.pattern_id] = pattern

    def _detect_oscillation(self, values: List[float]) -> bool:
        """Detect oscillation pattern in values"""
        if len(values) < 4:
            return False
        
        # Check for alternating increases and decreases
        oscillations = 0
        for i in range(1, len(values) - 1):
            if (values[i] > values[i-1] and values[i] > values[i+1]) or \
               (values[i] < values[i-1] and values[i] < values[i+1]):
                oscillations += 1
        
        # Consider it oscillation if more than 50% of points are peaks/valleys
        return oscillations / (len(values) - 2) > 0.5

    def _detect_plateau(self, values: List[float]) -> bool:
        """Detect plateau pattern in values"""
        if len(values) < 3:
            return False
        
        # Check if values are relatively constant
        mean_value = sum(values) / len(values)
        variance = sum((v - mean_value) ** 2 for v in values) / len(values)
        
        # Consider it a plateau if variance is low
        return variance < (mean_value * 0.1) ** 2

    def _detect_acceleration(self, values: List[float]) -> bool:
        """Detect acceleration pattern in values"""
        if len(values) < 3:
            return False
        
        # Check if rate of change is increasing
        changes = [values[i] - values[i-1] for i in range(1, len(values))]
        if len(changes) < 2:
            return False
        
        # Check if changes are increasing
        increasing_changes = 0
        for i in range(1, len(changes)):
            if changes[i] > changes[i-1]:
                increasing_changes += 1
        
        return increasing_changes / (len(changes) - 1) > 0.7

    def generate_optimization_recommendations(self, workflow_id: str) -> List[WorkflowOptimization]:
        """Generate optimization recommendations for a workflow"""
        if workflow_id not in self._workflow_cache:
            return []
        
        workflow = self._workflow_cache[workflow_id]
        recommendations = []
        
        # Analyze workflow for optimization opportunities
        recommendations.extend(self._analyze_stage_optimizations(workflow))
        recommendations.extend(self._analyze_collaboration_optimizations(workflow))
        recommendations.extend(self._analyze_metric_optimizations(workflow))
        
        # Add recommendations to workflow
        workflow.optimizations.extend(recommendations)
        workflow.updated_at = datetime.now().isoformat()
        
        # Save workflow
        self._save_workflow(workflow)
        
        return recommendations

    def _analyze_stage_optimizations(self, workflow: CollaborativeWorkflow) -> List[WorkflowOptimization]:
        """Analyze workflow stages for optimization opportunities"""
        recommendations = []
        
        # Check for stage bottlenecks
        if workflow.current_stage in [WorkflowStage.PLANNING, WorkflowStage.REVIEW]:
            # These stages often benefit from parallelization
            recommendation = WorkflowOptimization(
                optimization_id=str(uuid.uuid4()),
                workflow_id=workflow.workflow_id,
                optimization_type="parallelization",
                description=f"Parallelize {workflow.current_stage.value} stage to reduce bottlenecks",
                expected_improvement=0.2,
                implementation_effort=0.3,
                priority="medium",
                created_at=datetime.now().isoformat()
            )
            recommendations.append(recommendation)
        
        return recommendations

    def _analyze_collaboration_optimizations(self, workflow: CollaborativeWorkflow) -> List[WorkflowOptimization]:
        """Analyze collaboration patterns for optimization opportunities"""
        recommendations = []
        
        # Check for collaboration inefficiencies
        if workflow.participants and len(workflow.participants) > 3:
            # Large teams often benefit from structured communication
            recommendation = WorkflowOptimization(
                optimization_id=str(uuid.uuid4()),
                workflow_id=workflow.workflow_id,
                optimization_type="communication_structure",
                description="Implement structured communication protocols for large team",
                expected_improvement=0.15,
                implementation_effort=0.2,
                priority="low",
                created_at=datetime.now().isoformat()
            )
            recommendations.append(recommendation)
        
        return recommendations

    def _analyze_metric_optimizations(self, workflow: CollaborativeWorkflow) -> List[WorkflowOptimization]:
        """Analyze metrics for optimization opportunities"""
        recommendations = []
        
        # Check for declining trends
        declining_metrics = [m for m in workflow.metrics if m.trend == "declining"]
        
        for metric in declining_metrics:
            recommendation = WorkflowOptimization(
                optimization_id=str(uuid.uuid4()),
                workflow_id=workflow.workflow_id,
                optimization_type="performance_improvement",
                description=f"Address declining trend in {metric.metric_type}",
                expected_improvement=0.25,
                implementation_effort=0.4,
                priority="high",
                created_at=datetime.now().isoformat()
            )
            recommendations.append(recommendation)
        
        return recommendations

    def _save_workflow(self, workflow: CollaborativeWorkflow) -> None:
        """Save workflow to disk"""
        workflow_file = self.workflows_dir / f"{workflow.workflow_id}.json"
        with open(workflow_file, 'w') as f:
            json.dump(asdict(workflow), f, indent=2, default=str)

    def get_workflow_summary(self) -> Dict[str, Any]:
        """Get summary of all workflows"""
        workflows = list(self._workflow_cache.values())
        
        return {
            "total_workflows": len(workflows),
            "active_workflows": len([w for w in workflows if not w.completed_at]),
            "completed_workflows": len([w for w in workflows if w.completed_at]),
            "average_efficiency": sum(w.efficiency_score for w in workflows) / len(workflows) if workflows else 0.0,
            "workflows_by_stage": Counter(w.current_stage.value for w in workflows),
            "total_optimizations": sum(len(w.optimizations) for w in workflows)
        }

#!/usr/bin/env python3
"""
Enhanced Task Breakdown & Resource Allocation System

**Agent-2 Responsibility**: Task Breakdown & Resource Allocation
**Purpose**: Optimize collaborative task decomposition and resource allocation
**Features**: 
- Intelligent task decomposition algorithms
- Dynamic resource allocation based on agent capabilities
- Workflow optimization and dependency management
- Performance-based task distribution

This module provides advanced task breakdown capabilities that maximize
agent synergy and minimize task completion time through intelligent
decomposition and resource allocation.
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskComplexity(Enum):
    """Task complexity levels"""
    TRIVIAL = "trivial"      # 1-2 hours
    SIMPLE = "simple"        # 2-4 hours  
    MODERATE = "moderate"    # 4-8 hours
    COMPLEX = "complex"      # 8-16 hours
    VERY_COMPLEX = "very_complex"  # 16+ hours

class TaskPriority(Enum):
    """Task priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"

class TaskType(Enum):
    """Task type classifications"""
    DEVELOPMENT = "development"
    ANALYSIS = "analysis"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    INTEGRATION = "integration"
    OPTIMIZATION = "optimization"
    DEBUGGING = "debugging"
    RESEARCH = "research"

@dataclass
class AgentCapability:
    """Agent capability profile"""
    agent_id: str
    primary_skills: List[str]
    secondary_skills: List[str]
    experience_level: float  # 0.0 to 1.0
    current_workload: float  # 0.0 to 1.0
    availability: float      # 0.0 to 1.0
    collaboration_preference: List[str]  # Preferred agent IDs
    performance_history: Dict[str, float]  # Skill -> performance score
    last_updated: str

@dataclass
class TaskComponent:
    """Individual task component after breakdown"""
    component_id: str
    parent_task_id: str
    title: str
    description: str
    task_type: TaskType
    complexity: TaskComplexity
    priority: TaskPriority
    estimated_hours: float
    required_skills: List[str]
    dependencies: List[str]
    assigned_agent: Optional[str]
    status: str  # "pending", "assigned", "in_progress", "completed"
    created_at: str
    updated_at: str

@dataclass
class TaskBreakdown:
    """Complete task breakdown structure"""
    breakdown_id: str
    original_task_id: str
    original_title: str
    original_description: str
    components: List[TaskComponent]
    total_estimated_hours: float
    critical_path: List[str]
    resource_allocation: Dict[str, List[str]]  # Agent -> Component IDs
    optimization_score: float
    created_at: str
    updated_at: str

class EnhancedTaskBreakdown:
    """Enhanced task breakdown and resource allocation system"""

    def __init__(self, base_path: Path):
        """
        Initialize Enhanced Task Breakdown System
        
        Args:
            base_path: Base directory for task breakdown data
        """
        self.base_path = Path(base_path)
        self.breakdowns_dir = self.base_path / "task_breakdowns"
        self.capabilities_dir = self.base_path / "agent_capabilities"
        self.optimization_dir = self.base_path / "optimization_data"
        
        # Create necessary directories
        self.breakdowns_dir.mkdir(parents=True, exist_ok=True)
        self.capabilities_dir.mkdir(parents=True, exist_ok=True)
        self.optimization_dir.mkdir(parents=True, exist_ok=True)
        
        # Load agent capabilities
        self.agent_capabilities: Dict[str, AgentCapability] = {}
        self._load_agent_capabilities()
        
        logger.info(f"Enhanced Task Breakdown System initialized: {self.base_path}")

    def _load_agent_capabilities(self) -> None:
        """Load agent capabilities from disk"""
        for capability_file in self.capabilities_dir.glob("*.json"):
            try:
                with open(capability_file, 'r') as f:
                    capability_data = json.load(f)
                    capability = AgentCapability(**capability_data)
                    self.agent_capabilities[capability.agent_id] = capability
            except Exception as e:
                logger.error(f"Error loading capability {capability_file}: {e}")

    def create_agent_capability_profile(
        self,
        agent_id: str,
        primary_skills: List[str],
        secondary_skills: List[str],
        experience_level: float,
        collaboration_preference: List[str] = None
    ) -> AgentCapability:
        """Create or update agent capability profile"""
        now = datetime.now().isoformat()
        
        capability = AgentCapability(
            agent_id=agent_id,
            primary_skills=primary_skills,
            secondary_skills=secondary_skills or [],
            experience_level=max(0.0, min(1.0, experience_level)),
            current_workload=0.0,
            availability=1.0,
            collaboration_preference=collaboration_preference or [],
            performance_history={},
            last_updated=now
        )
        
        # Save capability profile
        self._save_agent_capability(capability)
        self.agent_capabilities[agent_id] = capability
        
        logger.info(f"Created capability profile for {agent_id}")
        return capability

    def breakdown_complex_task(
        self,
        task_id: str,
        title: str,
        description: str,
        estimated_hours: float,
        required_skills: List[str],
        priority: TaskPriority = TaskPriority.NORMAL
    ) -> TaskBreakdown:
        """
        Break down a complex task into manageable components
        
        Args:
            task_id: Original task ID
            title: Task title
            description: Task description
            estimated_hours: Estimated total hours
            required_skills: Skills required for the task
            priority: Task priority level
            
        Returns:
            TaskBreakdown: Complete breakdown with components and resource allocation
        """
        # Determine task complexity based on estimated hours
        complexity = self._determine_complexity(estimated_hours)
        
        # Generate task components
        components = self._generate_task_components(
            task_id, title, description, estimated_hours, 
            required_skills, complexity, priority
        )
        
        # Calculate critical path
        critical_path = self._calculate_critical_path(components)
        
        # Optimize resource allocation
        resource_allocation = self._optimize_resource_allocation(components)
        
        # Calculate optimization score
        optimization_score = self._calculate_optimization_score(
            components, resource_allocation
        )
        
        # Create breakdown
        breakdown = TaskBreakdown(
            breakdown_id=str(uuid.uuid4()),
            original_task_id=task_id,
            original_title=title,
            original_description=description,
            components=components,
            total_estimated_hours=estimated_hours,
            critical_path=critical_path,
            resource_allocation=resource_allocation,
            optimization_score=optimization_score,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        # Save breakdown
        self._save_task_breakdown(breakdown)
        
        logger.info(f"Created task breakdown for {title} with {len(components)} components")
        return breakdown

    def _determine_complexity(self, estimated_hours: float) -> TaskComplexity:
        """Determine task complexity based on estimated hours"""
        if estimated_hours <= 2:
            return TaskComplexity.TRIVIAL
        elif estimated_hours <= 4:
            return TaskComplexity.SIMPLE
        elif estimated_hours <= 8:
            return TaskComplexity.MODERATE
        elif estimated_hours <= 16:
            return TaskComplexity.COMPLEX
        else:
            return TaskComplexity.VERY_COMPLEX

    def _generate_task_components(
        self,
        task_id: str,
        title: str,
        description: str,
        estimated_hours: float,
        required_skills: List[str],
        complexity: TaskComplexity,
        priority: TaskPriority
    ) -> List[TaskComponent]:
        """Generate task components based on complexity and skills"""
        components = []
        
        # Determine number of components based on complexity
        num_components = self._get_component_count(complexity)
        
        # Split skills among components
        skill_groups = self._distribute_skills(required_skills, num_components)
        
        # Generate component titles and descriptions
        component_templates = self._get_component_templates(complexity, title)
        
        for i in range(num_components):
            component_hours = estimated_hours / num_components
            
            component = TaskComponent(
                component_id=str(uuid.uuid4()),
                parent_task_id=task_id,
                title=component_templates[i]["title"],
                description=component_templates[i]["description"],
                task_type=self._determine_component_type(required_skills[i % len(required_skills)]),
                complexity=self._determine_component_complexity(component_hours),
                priority=priority,
                estimated_hours=component_hours,
                required_skills=skill_groups[i],
                dependencies=[],
                assigned_agent=None,
                status="pending",
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
            
            components.append(component)
        
        # Add dependencies between components
        self._add_component_dependencies(components)
        
        return components

    def _get_component_count(self, complexity: TaskComplexity) -> int:
        """Get optimal number of components for given complexity"""
        complexity_counts = {
            TaskComplexity.TRIVIAL: 1,
            TaskComplexity.SIMPLE: 2,
            TaskComplexity.MODERATE: 3,
            TaskComplexity.COMPLEX: 4,
            TaskComplexity.VERY_COMPLEX: 6
        }
        return complexity_counts.get(complexity, 3)

    def _distribute_skills(self, skills: List[str], num_components: int) -> List[List[str]]:
        """Distribute skills among components"""
        skill_groups = [[] for _ in range(num_components)]
        
        for i, skill in enumerate(skills):
            group_index = i % num_components
            skill_groups[group_index].append(skill)
        
        return skill_groups

    def _get_component_templates(self, complexity: TaskComplexity, base_title: str) -> List[Dict[str, str]]:
        """Get component templates based on complexity"""
        if complexity == TaskComplexity.TRIVIAL:
            return [{"title": base_title, "description": "Complete task implementation"}]
        
        elif complexity == TaskComplexity.SIMPLE:
            return [
                {"title": f"{base_title} - Planning & Design", "description": "Initial planning and design phase"},
                {"title": f"{base_title} - Implementation", "description": "Core implementation and development"}
            ]
        
        elif complexity == TaskComplexity.MODERATE:
            return [
                {"title": f"{base_title} - Analysis & Planning", "description": "Requirements analysis and planning"},
                {"title": f"{base_title} - Core Development", "description": "Main development and implementation"},
                {"title": f"{base_title} - Testing & Validation", "description": "Testing and quality assurance"}
            ]
        
        elif complexity == TaskComplexity.COMPLEX:
            return [
                {"title": f"{base_title} - Requirements Analysis", "description": "Detailed requirements gathering and analysis"},
                {"title": f"{base_title} - Architecture Design", "description": "System architecture and design"},
                {"title": f"{base_title} - Core Implementation", "description": "Main development implementation"},
                {"title": f"{base_title} - Integration & Testing", "description": "Integration and comprehensive testing"}
            ]
        
        else:  # VERY_COMPLEX
            return [
                {"title": f"{base_title} - Strategic Planning", "description": "High-level strategic planning and analysis"},
                {"title": f"{base_title} - Requirements Engineering", "description": "Comprehensive requirements engineering"},
                {"title": f"{base_title} - Architecture & Design", "description": "System architecture and detailed design"},
                {"title": f"{base_title} - Core Development", "description": "Main development implementation"},
                {"title": f"{base_title} - Integration & Testing", "description": "Integration and comprehensive testing"},
                {"title": f"{base_title} - Deployment & Validation", "description": "Deployment and final validation"}
            ]

    def _determine_component_type(self, primary_skill: str) -> TaskType:
        """Determine component type based on primary skill"""
        skill_type_mapping = {
            "python": TaskType.DEVELOPMENT,
            "javascript": TaskType.DEVELOPMENT,
            "testing": TaskType.TESTING,
            "analysis": TaskType.ANALYSIS,
            "documentation": TaskType.DOCUMENTATION,
            "integration": TaskType.INTEGRATION,
            "optimization": TaskType.OPTIMIZATION,
            "debugging": TaskType.DEBUGGING,
            "research": TaskType.RESEARCH
        }
        return skill_type_mapping.get(primary_skill.lower(), TaskType.DEVELOPMENT)

    def _determine_component_complexity(self, component_hours: float) -> TaskComplexity:
        """Determine component complexity based on estimated hours"""
        return self._determine_complexity(component_hours)

    def _add_component_dependencies(self, components: List[TaskComponent]) -> None:
        """Add logical dependencies between components"""
        for i in range(1, len(components)):
            # Each component depends on the previous one
            components[i].dependencies.append(components[i-1].component_id)

    def _calculate_critical_path(self, components: List[TaskComponent]) -> List[str]:
        """Calculate critical path through components"""
        # Simple critical path calculation
        # In a real implementation, this would use more sophisticated algorithms
        return [comp.component_id for comp in components]

    def _optimize_resource_allocation(self, components: List[TaskComponent]) -> Dict[str, List[str]]:
        """Optimize resource allocation based on agent capabilities"""
        resource_allocation = defaultdict(list)
        
        for component in components:
            # Find best agent for this component
            best_agent = self._find_best_agent_for_component(component)
            
            if best_agent:
                resource_allocation[best_agent].append(component.component_id)
                component.assigned_agent = best_agent
                component.status = "assigned"
        
        return dict(resource_allocation)

    def _find_best_agent_for_component(self, component: TaskComponent) -> Optional[str]:
        """Find the best agent for a given component"""
        best_agent = None
        best_score = -1.0
        
        for agent_id, capability in self.agent_capabilities.items():
            # Skip if agent is overloaded
            if capability.current_workload > 0.8:
                continue
                
            # Calculate agent suitability score
            score = self._calculate_agent_suitability(capability, component)
            
            if score > best_score:
                best_score = score
                best_agent = agent_id
        
        return best_agent

    def _calculate_agent_suitability(self, capability: AgentCapability, component: TaskComponent) -> float:
        """Calculate how suitable an agent is for a component"""
        # Skill match score (0.0 to 1.0)
        skill_score = 0.0
        for required_skill in component.required_skills:
            if required_skill in capability.primary_skills:
                skill_score += 1.0
            elif required_skill in capability.secondary_skills:
                skill_score += 0.5
        
        skill_score = min(1.0, skill_score / max(len(component.required_skills), 1))
        
        # Experience score (0.0 to 1.0)
        experience_score = capability.experience_level
        
        # Availability score (0.0 to 1.0)
        availability_score = 1.0 - capability.current_workload
        
        # Performance history score (0.0 to 1.0)
        performance_score = 0.5  # Default score
        if component.required_skills:
            relevant_performances = [
                capability.performance_history.get(skill, 0.5)
                for skill in component.required_skills
            ]
            performance_score = sum(relevant_performances) / len(relevant_performances)
        
        # Weighted combination
        final_score = (
            skill_score * 0.4 +
            experience_score * 0.2 +
            availability_score * 0.2 +
            performance_score * 0.2
        )
        
        return final_score

    def _calculate_optimization_score(self, components: List[TaskComponent], resource_allocation: Dict[str, List[str]]) -> float:
        """Calculate overall optimization score for the breakdown"""
        # Component balance score
        component_balance = 1.0 - (max(len(comp.required_skills) for comp in components) - 
                                  min(len(comp.required_skills) for comp in components)) / 10.0
        
        # Resource utilization score
        total_components = len(components)
        agents_used = len(resource_allocation)
        utilization_score = min(1.0, total_components / max(agents_used, 1))
        
        # Dependency efficiency score
        dependency_score = 1.0 - (sum(len(comp.dependencies) for comp in components) / (len(components) * 2))
        
        # Overall score
        optimization_score = (
            component_balance * 0.3 +
            utilization_score * 0.4 +
            dependency_score * 0.3
        )
        
        return max(0.0, min(1.0, optimization_score))

    def _save_task_breakdown(self, breakdown: TaskBreakdown) -> None:
        """Save task breakdown to disk"""
        breakdown_file = self.breakdowns_dir / f"{breakdown.breakdown_id}.json"
        with open(breakdown_file, 'w') as f:
            json.dump(asdict(breakdown), f, indent=2, default=str)

    def _save_agent_capability(self, capability: AgentCapability) -> None:
        """Save agent capability to disk"""
        capability_file = self.capabilities_dir / f"{capability.agent_id}.json"
        with open(capability_file, 'w') as f:
            json.dump(asdict(capability), f, indent=2, default=str)

    def get_breakdown_summary(self) -> Dict[str, Any]:
        """Get summary of all task breakdowns"""
        breakdown_files = list(self.breakdowns_dir.glob("*.json"))
        
        return {
            "total_breakdowns": len(breakdown_files),
            "breakdowns_by_complexity": {},
            "average_optimization_score": 0.0,
            "total_components": 0,
            "resource_utilization": {}
        }

    def optimize_existing_breakdown(self, breakdown_id: str) -> Optional[TaskBreakdown]:
        """Optimize an existing task breakdown"""
        # Load existing breakdown
        breakdown_file = self.breakdowns_dir / f"{breakdown_id}.json"
        if not breakdown_file.exists():
            return None
            
        try:
            with open(breakdown_file, 'r') as f:
                breakdown_data = json.load(f)
                breakdown = TaskBreakdown(**breakdown_data)
            
            # Re-optimize resource allocation
            new_resource_allocation = self._optimize_resource_allocation(breakdown.components)
            breakdown.resource_allocation = new_resource_allocation
            
            # Recalculate optimization score
            breakdown.optimization_score = self._calculate_optimization_score(
                breakdown.components, new_resource_allocation
            )
            
            breakdown.updated_at = datetime.now().isoformat()
            
            # Save optimized breakdown
            self._save_task_breakdown(breakdown)
            
            logger.info(f"Optimized breakdown {breakdown_id}")
            return breakdown
            
        except Exception as e:
            logger.error(f"Error optimizing breakdown {breakdown_id}: {e}")
            return None

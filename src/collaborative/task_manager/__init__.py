"""
📋 Collaborative Task Manager Package

This package provides comprehensive task breakdown, resource allocation,
and workflow management for multi-agent collaboration.

**Agent-2 Responsibility**: Task breakdown and resource allocation
**Purpose**: Multi-agent task coordination and progress tracking
**Features**: Task assignment, progress monitoring, dependency management

Author: Collaborative Task Framework v1.0
Status: ACTIVE COLLABORATION IN PROGRESS
"""

__version__ = "1.0.0"
__author__ = "Collaborative Task Framework"
__status__ = "ACTIVE COLLABORATION"

from .collaborative_task_manager import CollaborativeTaskManager
from .enhanced_task_breakdown import EnhancedTaskBreakdown
from .workflow_optimizer import WorkflowOptimizer
from .enhanced_collaborative_system import EnhancedCollaborativeSystem

__all__ = [
    "CollaborativeTaskManager",
    "EnhancedTaskBreakdown",
    "WorkflowOptimizer",
    "EnhancedCollaborativeSystem"
]




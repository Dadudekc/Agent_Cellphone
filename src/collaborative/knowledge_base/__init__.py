"""
🤝 Collaborative Knowledge Base Package

This package provides the foundation for multi-agent knowledge sharing,
collaboration tracking, and collective intelligence enhancement.

**Agent-1 Responsibility**: Strategic coordination and knowledge management
**Purpose**: Centralized knowledge sharing and collaboration tracking
**Features**: Real-time updates, version control, agent contribution tracking

Author: Collaborative Task Framework v1.0
Status: ACTIVE COLLABORATION IN PROGRESS
"""

__version__ = "1.0.0"
__author__ = "Collaborative Task Framework"
__status__ = "ACTIVE COLLABORATION"

from .collaborative_knowledge_manager import CollaborativeKnowledgeManager
from .agent_contribution_tracker import AgentContributionTracker
from .knowledge_version_control import KnowledgeVersionControl

__all__ = [
    "CollaborativeKnowledgeManager",
    "AgentContributionTracker", 
    "KnowledgeVersionControl"
]

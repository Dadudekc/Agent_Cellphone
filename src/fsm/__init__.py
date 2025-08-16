"""
Enhanced FSM Module
==================
Provides intelligent, context-aware state management for agent coordination.
"""

from .repository_activity_monitor import RepositoryActivityMonitor, RepositoryContext
from .enhanced_fsm import EnhancedFSM, AgentState
from .autonomous_captain import AutonomousCaptain, CaptainTask
from .autonomous_standardization import AutonomousStandardization, StandardizationTask

__version__ = "2.2.0"
__author__ = "Enhanced FSM System with Autonomous CAPTAIN + Agent Instruction"

__all__ = [
    "RepositoryActivityMonitor",
    "RepositoryContext", 
    "EnhancedFSM",
    "AgentState",
    "AutonomousCaptain",
    "CaptainTask",
    "AutonomousStandardization",
    "StandardizationTask"
]

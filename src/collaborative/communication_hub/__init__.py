"""
🔐 Collaborative Communication Hub Package

This package provides secure multi-agent communication, collaborative learning,
and capability enhancement systems for multi-agent collaboration.

**Agent-4 Responsibility**: Communication protocols and security
**Purpose**: Secure multi-agent communication and learning enhancement
**Features**: Encrypted messaging, learning protocols, capability enhancement

Author: Collaborative Task Framework v1.0
Status: ACTIVE COLLABORATION IN PROGRESS
"""

__version__ = "1.0.0"
__author__ = "Collaborative Task Framework"
__status__ = "ACTIVE COLLABORATION"

from .communication_hub import CollaborativeCommunicationHub
from .secure_protocols import SecureCommunicationProtocols
from .learning_systems import CollaborativeLearningSystems
from .capability_enhancement import AgentCapabilityEnhancement

__all__ = [
    "CollaborativeCommunicationHub",
    "SecureCommunicationProtocols",
    "CollaborativeLearningSystems",
    "AgentCapabilityEnhancement"
]



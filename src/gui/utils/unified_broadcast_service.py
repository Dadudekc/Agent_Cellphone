#!/usr/bin/env python3
"""
Unified Broadcast Service
=========================
Consolidates all broadcast functionality across the codebase into a single,
consistent service to eliminate duplication and standardize message handling.
"""

import os
import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any, Union
from enum import Enum
from dataclasses import dataclass, field

# Import existing components
try:
    from services.agent_cell_phone import AgentCellPhone
    from services.inter_agent_framework import InterAgentFramework, Message, MessageType
    from core.framework.agent_autonomy_framework import AgentAutonomyFramework
except ImportError:
    # Fallback imports for when main modules aren't available
    AgentCellPhone = None
    InterAgentFramework = None
    Message = None
    MessageType = None
    AgentAutonomyFramework = None


class BroadcastType(str, Enum):
    """Types of broadcast operations"""
    MESSAGE = "message"
    COMMAND = "command"
    STATUS = "status"
    SYSTEM = "system"
    EMERGENCY = "emergency"
    COORDINATION = "coordination"


class BroadcastPriority(str, Enum):
    """Priority levels for broadcasts"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    EMERGENCY = "emergency"


@dataclass
class BroadcastRequest:
    """Structured broadcast request"""
    content: str
    broadcast_type: BroadcastType
    priority: BroadcastPriority = BroadcastPriority.NORMAL
    targets: Optional[List[str]] = None  # None means all agents
    sender: str = "system"
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    request_id: Optional[str] = None


@dataclass
class BroadcastResult:
    """Result of a broadcast operation"""
    success: bool
    message: str
    targets_reached: int
    total_targets: int
    failed_targets: List[str] = field(default_factory=list)
    response_times: Dict[str, float] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    request_id: Optional[str] = None


class UnifiedBroadcastService:
    """
    Unified service for all broadcast operations across the system.
    Consolidates functionality from:
    - InterAgentFramework.broadcast_message()
    - CoordinationUtils.broadcast_system_message()
    - MessagingUtils.broadcast_captain_message()
    - AgentAutonomyFramework.broadcast_message()
    """
    
    def __init__(self, layout_mode: str = "8-agent", test_mode: bool = True):
        """
        Initialize the unified broadcast service.
        
        Args:
            layout_mode: Layout mode for agent configuration
            test_mode: Whether to run in test mode
        """
        self.layout_mode = layout_mode
        self.test_mode = test_mode
        self.broadcast_history: List[BroadcastResult] = []
        self.max_history_size = 1000
        
        # Initialize underlying services
        self._initialize_services()
        
        # Broadcast statistics
        self.stats = {
            "total_broadcasts": 0,
            "successful_broadcasts": 0,
            "failed_broadcasts": 0,
            "total_targets_reached": 0,
            "average_response_time": 0.0
        }
    
    def _initialize_services(self):
        """Initialize underlying broadcast services"""
        self.services = {}
        
        # Initialize AgentCellPhone if available
        try:
            if AgentCellPhone:
                self.services["agent_cell_phone"] = AgentCellPhone(
                    layout_mode=self.layout_mode,
                    test_mode=self.test_mode
                )
        except Exception as e:
            print(f"Warning: Could not initialize AgentCellPhone: {e}")
        
        # Initialize InterAgentFramework if available
        try:
            if InterAgentFramework:
                self.services["inter_agent_framework"] = InterAgentFramework(
                    agent_id="broadcast_service",
                    layout_mode=self.layout_mode,
                    test=self.test_mode
                )
        except Exception as e:
            print(f"Warning: Could not initialize InterAgentFramework: {e}")
        
        # Initialize AgentAutonomyFramework if available
        try:
            if AgentAutonomyFramework:
                self.services["agent_autonomy_framework"] = AgentAutonomyFramework()
        except Exception as e:
            print(f"Warning: Could not initialize AgentAutonomyFramework: {e}")
    
    def broadcast(self, request: BroadcastRequest) -> BroadcastResult:
        """
        Execute a broadcast request using the appropriate underlying service.
        
        Args:
            request: Broadcast request to execute
            
        Returns:
            BroadcastResult with operation results
        """
        start_time = time.time()
        
        try:
            # Route to appropriate service based on broadcast type
            if request.broadcast_type == BroadcastType.COMMAND:
                result = self._broadcast_command(request)
            elif request.broadcast_type == BroadcastType.SYSTEM:
                result = self._broadcast_system_message(request)
            elif request.broadcast_type == BroadcastType.EMERGENCY:
                result = self._broadcast_emergency(request)
            elif request.broadcast_type == BroadcastType.COORDINATION:
                result = self._broadcast_coordination(request)
            else:  # Default to message broadcast
                result = self._broadcast_message(request)
            
            # Update statistics
            self._update_stats(result)
            
            # Add to history
            self._add_to_history(result)
            
            return result
            
        except Exception as e:
            # Create error result
            result = BroadcastResult(
                success=False,
                message=f"Broadcast failed: {e}",
                targets_reached=0,
                total_targets=len(request.targets) if request.targets else 0,
                failed_targets=request.targets or [],
                request_id=request.request_id
            )
            
            self._update_stats(result)
            self._add_to_history(result)
            
            return result
    
    def _broadcast_message(self, request: BroadcastRequest) -> BroadcastResult:
        """Broadcast a general message"""
        targets = request.targets or self._get_all_agents()
        results = {}
        failed_targets = []
        
        for target in targets:
            try:
                start_time = time.time()
                
                # Try different services in order of preference
                success = False
                
                # Try InterAgentFramework first
                if "inter_agent_framework" in self.services:
                    message = Message(
                        sender=request.sender,
                        recipient=target,
                        message_type=MessageType.BROADCAST,
                        command="message",
                        args=[request.content]
                    )
                    success = self.services["inter_agent_framework"].send_message(target, message)
                
                # Fallback to AgentCellPhone
                elif "agent_cell_phone" in self.services:
                    success = self.services["agent_cell_phone"].send(target, request.content)
                
                # Fallback to AgentAutonomyFramework
                elif "agent_autonomy_framework" in self.services:
                    success = self.services["agent_autonomy_framework"].send_message(
                        request.sender, target, request.content, "info"
                    )
                
                response_time = time.time() - start_time
                results[target] = {"success": success, "response_time": response_time}
                
                if not success:
                    failed_targets.append(target)
                    
            except Exception as e:
                failed_targets.append(target)
                results[target] = {"success": False, "error": str(e)}
        
        targets_reached = len(targets) - len(failed_targets)
        
        return BroadcastResult(
            success=targets_reached > 0,
            message=f"Message broadcast to {targets_reached}/{len(targets)} targets",
            targets_reached=targets_reached,
            total_targets=len(targets),
            failed_targets=failed_targets,
            response_times={k: v.get("response_time", 0) for k, v in results.items()},
            request_id=request.request_id
        )
    
    def _broadcast_command(self, request: BroadcastRequest) -> BroadcastResult:
        """Broadcast a command to agents"""
        targets = request.targets or self._get_all_agents()
        results = {}
        failed_targets = []
        
        for target in targets:
            try:
                start_time = time.time()
                
                # Try different services in order of preference
                success = False
                
                # Try InterAgentFramework first
                if "inter_agent_framework" in self.services:
                    message = Message(
                        sender=request.sender,
                        recipient=target,
                        message_type=MessageType.COMMAND,
                        command=request.content,
                        args=request.metadata.get("args", [])
                    )
                    success = self.services["inter_agent_framework"].send_message(target, message)
                
                # Fallback to AgentCellPhone
                elif "agent_cell_phone" in self.services:
                    command_text = request.content
                    if request.metadata.get("args"):
                        command_text += " " + " ".join(request.metadata["args"])
                    success = self.services["agent_cell_phone"].send(target, command_text)
                
                response_time = time.time() - start_time
                results[target] = {"success": success, "response_time": response_time}
                
                if not success:
                    failed_targets.append(target)
                    
            except Exception as e:
                failed_targets.append(target)
                results[target] = {"success": False, "error": str(e)}
        
        targets_reached = len(targets) - len(failed_targets)
        
        return BroadcastResult(
            success=targets_reached > 0,
            message=f"Command '{request.content}' broadcast to {targets_reached}/{len(targets)} targets",
            targets_reached=targets_reached,
            total_targets=len(targets),
            failed_targets=failed_targets,
            response_times={k: v.get("response_time", 0) for k, v in results.items()},
            request_id=request.request_id
        )
    
    def _broadcast_system_message(self, request: BroadcastRequest) -> BroadcastResult:
        """Broadcast a system message"""
        targets = request.targets or self._get_all_agents()
        results = {}
        failed_targets = []
        
        for target in targets:
            try:
                start_time = time.time()
                
                # Try different services in order of preference
                success = False
                
                # Try InterAgentFramework first
                if "inter_agent_framework" in self.services:
                    message = Message(
                        sender=request.sender,
                        recipient=target,
                        message_type=MessageType.SYSTEM,
                        command="system",
                        args=[request.content]
                    )
                    success = self.services["inter_agent_framework"].send_message(target, message)
                
                # Fallback to AgentCellPhone
                elif "agent_cell_phone" in self.services:
                    success = self.services["agent_cell_phone"].send(target, request.content)
                
                response_time = time.time() - start_time
                results[target] = {"success": success, "response_time": response_time}
                
                if not success:
                    failed_targets.append(target)
                    
            except Exception as e:
                failed_targets.append(target)
                results[target] = {"success": False, "error": str(e)}
        
        targets_reached = len(targets) - len(failed_targets)
        
        return BroadcastResult(
            success=targets_reached > 0,
            message=f"System message broadcast to {targets_reached}/{len(targets)} targets",
            targets_reached=targets_reached,
            total_targets=len(targets),
            failed_targets=failed_targets,
            response_times={k: v.get("response_time", 0) for k, v in results.items()},
            request_id=request.request_id
        )
    
    def _broadcast_emergency(self, request: BroadcastRequest) -> BroadcastResult:
        """Broadcast an emergency message (high priority)"""
        # Emergency broadcasts use all available services
        targets = request.targets or self._get_all_agents()
        results = {}
        failed_targets = []
        
        for target in targets:
            try:
                start_time = time.time()
                
                # Try all services for emergency broadcasts
                success = False
                
                # Try InterAgentFramework
                if "inter_agent_framework" in self.services:
                    message = Message(
                        sender=request.sender,
                        recipient=target,
                        message_type=MessageType.SYSTEM,
                        command="emergency",
                        args=[request.content]
                    )
                    success = self.services["inter_agent_framework"].send_message(target, message)
                
                # Try AgentCellPhone
                if not success and "agent_cell_phone" in self.services:
                    success = self.services["agent_cell_phone"].send(target, f"[EMERGENCY] {request.content}")
                
                # Try AgentAutonomyFramework
                if not success and "agent_autonomy_framework" in self.services:
                    success = self.services["agent_autonomy_framework"].send_message(
                        request.sender, target, request.content, "emergency"
                    )
                
                response_time = time.time() - start_time
                results[target] = {"success": success, "response_time": response_time}
                
                if not success:
                    failed_targets.append(target)
                    
            except Exception as e:
                failed_targets.append(target)
                results[target] = {"success": False, "error": str(e)}
        
        targets_reached = len(targets) - len(failed_targets)
        
        return BroadcastResult(
            success=targets_reached > 0,
            message=f"Emergency message broadcast to {targets_reached}/{len(targets)} targets",
            targets_reached=targets_reached,
            total_targets=len(targets),
            failed_targets=failed_targets,
            response_times={k: v.get("response_time", 0) for k, v in results.items()},
            request_id=request.request_id
        )
    
    def _broadcast_coordination(self, request: BroadcastRequest) -> BroadcastResult:
        """Broadcast a coordination message"""
        targets = request.targets or self._get_all_agents()
        results = {}
        failed_targets = []
        
        for target in targets:
            try:
                start_time = time.time()
                
                # Try different services in order of preference
                success = False
                
                # Try InterAgentFramework first
                if "inter_agent_framework" in self.services:
                    message = Message(
                        sender=request.sender,
                        recipient=target,
                        message_type=MessageType.COMMAND,
                        command="coordinate",
                        args=[request.content]
                    )
                    success = self.services["inter_agent_framework"].send_message(target, message)
                
                # Fallback to AgentCellPhone
                elif "agent_cell_phone" in self.services:
                    success = self.services["agent_cell_phone"].send(target, f"[COORDINATION] {request.content}")
                
                response_time = time.time() - start_time
                results[target] = {"success": success, "response_time": response_time}
                
                if not success:
                    failed_targets.append(target)
                    
            except Exception as e:
                failed_targets.append(target)
                results[target] = {"success": False, "error": str(e)}
        
        targets_reached = len(targets) - len(failed_targets)
        
        return BroadcastResult(
            success=targets_reached > 0,
            message=f"Coordination message broadcast to {targets_reached}/{len(targets)} targets",
            targets_reached=targets_reached,
            total_targets=len(targets),
            failed_targets=failed_targets,
            response_times={k: v.get("response_time", 0) for k, v in results.items()},
            request_id=request.request_id
        )
    
    def _get_all_agents(self) -> List[str]:
        """Get list of all available agents"""
        agents = []
        
        # Try to get agents from different services
        if "agent_cell_phone" in self.services:
            try:
                agents = self.services["agent_cell_phone"].get_available_agents()
            except:
                pass
        
        if not agents and "inter_agent_framework" in self.services:
            try:
                agents = self.services["inter_agent_framework"].get_available_agents()
            except:
                pass
        
        if not agents and "agent_autonomy_framework" in self.services:
            try:
                agents = list(self.services["agent_autonomy_framework"].agents.keys())
            except:
                pass
        
        # Fallback to default agents if none found
        if not agents:
            agents = [f"agent-{i}" for i in range(1, 9)]
        
        return agents
    
    def _update_stats(self, result: BroadcastResult):
        """Update broadcast statistics"""
        self.stats["total_broadcasts"] += 1
        
        if result.success:
            self.stats["successful_broadcasts"] += 1
        else:
            self.stats["failed_broadcasts"] += 1
        
        self.stats["total_targets_reached"] += result.targets_reached
        
        # Update average response time
        if result.response_times:
            avg_time = sum(result.response_times.values()) / len(result.response_times)
            current_avg = self.stats["average_response_time"]
            total_broadcasts = self.stats["total_broadcasts"]
            
            # Calculate running average
            self.stats["average_response_time"] = (
                (current_avg * (total_broadcasts - 1) + avg_time) / total_broadcasts
            )
    
    def _add_to_history(self, result: BroadcastResult):
        """Add result to broadcast history"""
        self.broadcast_history.append(result)
        
        # Trim history if it gets too large
        if len(self.broadcast_history) > self.max_history_size:
            self.broadcast_history = self.broadcast_history[-self.max_history_size:]
    
    # Convenience methods for common broadcast operations
    
    def broadcast_message(self, content: str, targets: Optional[List[str]] = None, 
                         priority: BroadcastPriority = BroadcastPriority.NORMAL) -> BroadcastResult:
        """Broadcast a general message"""
        request = BroadcastRequest(
            content=content,
            broadcast_type=BroadcastType.MESSAGE,
            priority=priority,
            targets=targets
        )
        return self.broadcast(request)
    
    def broadcast_command(self, command: str, args: Optional[List[str]] = None,
                         targets: Optional[List[str]] = None) -> BroadcastResult:
        """Broadcast a command"""
        request = BroadcastRequest(
            content=command,
            broadcast_type=BroadcastType.COMMAND,
            targets=targets,
            metadata={"args": args or []}
        )
        return self.broadcast(request)
    
    def broadcast_system_message(self, content: str, targets: Optional[List[str]] = None) -> BroadcastResult:
        """Broadcast a system message"""
        request = BroadcastRequest(
            content=content,
            broadcast_type=BroadcastType.SYSTEM,
            targets=targets
        )
        return self.broadcast(request)
    
    def broadcast_emergency(self, content: str, targets: Optional[List[str]] = None) -> BroadcastResult:
        """Broadcast an emergency message"""
        request = BroadcastRequest(
            content=content,
            broadcast_type=BroadcastType.EMERGENCY,
            priority=BroadcastPriority.EMERGENCY,
            targets=targets
        )
        return self.broadcast(request)
    
    def broadcast_coordination(self, content: str, targets: Optional[List[str]] = None) -> BroadcastResult:
        """Broadcast a coordination message"""
        request = BroadcastRequest(
            content=content,
            broadcast_type=BroadcastType.COORDINATION,
            targets=targets
        )
        return self.broadcast(request)
    
    # Utility methods
    
    def get_broadcast_history(self, limit: Optional[int] = None) -> List[BroadcastResult]:
        """Get broadcast history"""
        if limit:
            return self.broadcast_history[-limit:]
        return self.broadcast_history.copy()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get broadcast statistics"""
        return self.stats.copy()
    
    def clear_history(self):
        """Clear broadcast history"""
        self.broadcast_history.clear()
    
    def get_available_services(self) -> List[str]:
        """Get list of available underlying services"""
        return list(self.services.keys())


# Convenience functions for direct use
def create_broadcast_service(layout_mode: str = "8-agent", test_mode: bool = True) -> UnifiedBroadcastService:
    """Create a unified broadcast service instance"""
    return UnifiedBroadcastService(layout_mode, test_mode)


def quick_broadcast(content: str, broadcast_type: BroadcastType = BroadcastType.MESSAGE,
                   layout_mode: str = "8-agent") -> BroadcastResult:
    """Quick function to broadcast a message"""
    service = UnifiedBroadcastService(layout_mode, test_mode=True)
    request = BroadcastRequest(content=content, broadcast_type=broadcast_type)
    return service.broadcast(request) 
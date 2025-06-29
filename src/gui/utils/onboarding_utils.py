#!/usr/bin/env python3
"""
Onboarding Utilities for Dream.OS GUI
Provides onboarding functionality extracted from onboarding scripts
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

try:
    from agent_cell_phone import AgentCellPhone, MsgTag
except ImportError:
    print("Warning: agent_cell_phone module not found")

class OnboardingUtils:
    """Utility class for agent onboarding operations"""
    
    def __init__(self, layout_mode: str = "8-agent", test_mode: bool = True):
        """Initialize onboarding utilities"""
        self.layout_mode = layout_mode
        self.test_mode = test_mode
        self.acp = None
        self.onboarding_dir = project_root / "agent_workspaces" / "onboarding"
        self.initialize_agent_cell_phone()
    
    def initialize_agent_cell_phone(self):
        """Initialize the AgentCellPhone instance"""
        try:
            self.acp = AgentCellPhone(layout_mode=self.layout_mode, test=self.test_mode)
            return True
        except Exception as e:
            print(f"Error initializing AgentCellPhone: {e}")
            return False
    
    def get_onboarding_messages(self) -> Dict[str, str]:
        """Get available onboarding messages"""
        messages = {
            "welcome": self._get_welcome_message(),
            "system_overview": self._get_system_overview_message(),
            "communication_protocol": self._get_communication_protocol_message(),
            "roles_and_responsibilities": self._get_roles_message(),
            "best_practices": self._get_best_practices_message(),
            "getting_started": self._get_getting_started_message(),
            "troubleshooting": self._get_troubleshooting_message(),
            "quick_start": self._get_quick_start_message()
        }
        return messages
    
    def _get_welcome_message(self) -> str:
        """Get welcome message content"""
        return """Welcome to Dream.OS Autonomous Framework!

You are now part of a sophisticated multi-agent system designed for autonomous development and collaboration. This system enables agents to work together on complex projects, communicate effectively, and maintain operational excellence.

Key Features:
- Multi-agent coordination and communication
- Autonomous task execution and management
- Real-time status monitoring and reporting
- Flexible message routing and command processing
- Comprehensive logging and audit trails

Your role is crucial in maintaining system integrity and ensuring smooth operations. Please review the onboarding materials and familiarize yourself with the communication protocols.

Welcome aboard! 🚀"""
    
    def _get_system_overview_message(self) -> str:
        """Get system overview message content"""
        return """Dream.OS System Overview

ARCHITECTURE:
- Multi-agent distributed system
- Message-based communication protocol
- Real-time coordination and synchronization
- Modular design with pluggable components

CORE COMPONENTS:
1. Agent Cell Phone - Central communication hub
2. Message Router - Intelligent message distribution
3. Status Monitor - Real-time system health tracking
4. Command Processor - Automated task execution
5. Logging System - Comprehensive audit trails

OPERATIONAL MODES:
- Test Mode: Safe development and testing environment
- Live Mode: Production operations with full capabilities
- Debug Mode: Enhanced logging and diagnostics

LAYOUT CONFIGURATIONS:
- 8-agent: Standard production layout
- 4-agent: Compact development layout
- Custom: Configurable agent arrangements

The system is designed for scalability, reliability, and ease of maintenance."""
    
    def _get_communication_protocol_message(self) -> str:
        """Get communication protocol message content"""
        return """Communication Protocol

MESSAGE TYPES:
1. NORMAL - Standard operational messages
2. COMMAND - System commands and instructions
3. STATUS - Status updates and health reports
4. ERROR - Error notifications and alerts
5. CAPTAIN - High-priority captain messages
6. SYNC - Synchronization and coordination messages

MESSAGE FORMAT:
- Target: Specific agent or 'all' for broadcast
- Content: Message text or command
- Tag: Message type for proper routing
- Timestamp: Automatic timestamping

COMMAND STRUCTURE:
- ping: Test connectivity
- status: Get current status
- resume: Resume operations
- sync: Synchronize data
- verify: Verify system integrity
- task: Task management commands

BEST PRACTICES:
- Use appropriate message tags
- Include clear, concise content
- Follow command syntax precisely
- Monitor message delivery confirmations
- Log important communications"""
    
    def _get_roles_message(self) -> str:
        """Get roles and responsibilities message content"""
        return """Agent Roles and Responsibilities

CORE RESPONSIBILITIES:
1. Maintain System Health
   - Monitor operational status
   - Report issues promptly
   - Execute self-diagnostic routines

2. Execute Assigned Tasks
   - Process incoming commands
   - Complete tasks efficiently
   - Report task completion status

3. Communicate Effectively
   - Respond to ping requests
   - Provide status updates
   - Coordinate with other agents

4. Maintain Data Integrity
   - Synchronize data regularly
   - Backup critical information
   - Verify data consistency

5. Support System Operations
   - Assist with troubleshooting
   - Participate in system maintenance
   - Contribute to system improvements

EXPECTATIONS:
- 24/7 availability and responsiveness
- Proactive issue identification
- Continuous learning and adaptation
- Collaboration with team members
- Adherence to operational protocols"""
    
    def _get_best_practices_message(self) -> str:
        """Get best practices message content"""
        return """Best Practices for Dream.OS

OPERATIONAL PRACTICES:
1. Regular Status Updates
   - Send status reports every 30 minutes
   - Include operational metrics
   - Report any anomalies immediately

2. Effective Communication
   - Use clear, concise messages
   - Include relevant context
   - Respond promptly to requests

3. Task Management
   - Acknowledge task assignments
   - Provide progress updates
   - Report completion with results

4. Error Handling
   - Log all errors with details
   - Attempt self-recovery when possible
   - Escalate persistent issues

5. System Maintenance
   - Perform regular health checks
   - Update status information
   - Participate in system syncs

PERFORMANCE OPTIMIZATION:
- Minimize message overhead
- Use appropriate message tags
- Batch operations when possible
- Monitor resource usage

SECURITY CONSIDERATIONS:
- Validate all incoming messages
- Log security-relevant events
- Follow access control protocols
- Report suspicious activities"""
    
    def _get_getting_started_message(self) -> str:
        """Get getting started message content"""
        return """Getting Started with Dream.OS

INITIAL SETUP:
1. Verify System Connection
   - Test connectivity with ping command
   - Confirm message routing
   - Validate status reporting

2. Review Documentation
   - Read system overview
   - Understand communication protocols
   - Familiarize with command structure

3. Perform Self-Diagnostic
   - Run system health checks
   - Verify data integrity
   - Test core functionalities

4. Establish Baseline
   - Record initial status
   - Set up monitoring
   - Configure logging

FIRST STEPS:
1. Send a status update
2. Respond to a ping request
3. Execute a simple command
4. Participate in system sync

ONGOING ACTIVITIES:
- Monitor system health
- Process incoming tasks
- Maintain communication
- Update status regularly

Remember: You're part of a team. Collaboration and communication are key to success!"""
    
    def _get_troubleshooting_message(self) -> str:
        """Get troubleshooting message content"""
        return """Troubleshooting Guide

COMMON ISSUES:

1. Connection Problems
   - Check network connectivity
   - Verify agent coordinates
   - Test message routing
   - Restart if necessary

2. Message Delivery Issues
   - Verify target agent exists
   - Check message format
   - Confirm routing configuration
   - Retry with different tag

3. Command Execution Errors
   - Validate command syntax
   - Check permissions
   - Verify dependencies
   - Review error logs

4. Status Reporting Problems
   - Check data sources
   - Verify reporting intervals
   - Review status format
   - Test status endpoints

DIAGNOSTIC COMMANDS:
- ping: Test connectivity
- status: Get current status
- verify: System integrity check
- sync: Data synchronization
- repair: Self-repair attempt

ESCALATION PROCEDURE:
1. Attempt self-recovery
2. Log detailed error information
3. Notify system administrator
4. Follow recovery protocols
5. Document resolution steps

Remember: When in doubt, ask for help!"""
    
    def _get_quick_start_message(self) -> str:
        """Get quick start message content"""
        return """Quick Start Guide

IMMEDIATE ACTIONS:
1. Send Status: Report your current status
2. Test Ping: Verify connectivity
3. Sync Data: Synchronize with system
4. Review Tasks: Check for pending tasks

ESSENTIAL COMMANDS:
- ping: Test connectivity
- status: Report status
- sync: Synchronize data
- resume: Resume operations

QUICK REFERENCE:
- Message Tags: NORMAL, COMMAND, STATUS, ERROR, CAPTAIN, SYNC
- Targets: Specific agent name or 'all' for broadcast
- Commands: ping, status, resume, sync, verify, task

GETTING HELP:
- Review onboarding materials
- Check troubleshooting guide
- Contact system administrator
- Use diagnostic commands

You're ready to start! Begin with a status report and ping test."""
    
    def send_onboarding_message(self, target: str, message_type: str) -> Tuple[bool, str]:
        """Send a specific onboarding message to an agent"""
        try:
            if not self.acp:
                return False, "AgentCellPhone not initialized"
            
            messages = self.get_onboarding_messages()
            if message_type not in messages:
                return False, f"Invalid message type: {message_type}"
            
            message = messages[message_type]
            success, result = self.acp.send(target, message, MsgTag.NORMAL)
            
            if success:
                return True, f"Onboarding message '{message_type}' sent to {target}"
            else:
                return False, f"Failed to send message: {result}"
                
        except Exception as e:
            return False, f"Error sending onboarding message: {e}"
    
    def send_all_onboarding_messages(self, target: str) -> Dict[str, Tuple[bool, str]]:
        """Send all onboarding messages to an agent"""
        results = {}
        messages = self.get_onboarding_messages()
        
        for message_type in messages:
            success, result = self.send_onboarding_message(target, message_type)
            results[message_type] = (success, result)
            time.sleep(1)  # Delay between messages
        
        return results
    
    def onboard_all_agents(self) -> Dict[str, Dict[str, Tuple[bool, str]]]:
        """Send onboarding messages to all agents"""
        results = {}
        agents = self.acp.get_available_agents() if self.acp else []
        
        for agent in agents:
            agent_results = self.send_all_onboarding_messages(agent)
            results[agent] = agent_results
            time.sleep(2)  # Delay between agents
        
        return results
    
    def send_custom_onboarding_message(self, target: str, message: str) -> Tuple[bool, str]:
        """Send a custom onboarding message"""
        try:
            if not self.acp:
                return False, "AgentCellPhone not initialized"
            
            success, result = self.acp.send(target, message, MsgTag.NORMAL)
            
            if success:
                return True, f"Custom onboarding message sent to {target}"
            else:
                return False, f"Failed to send message: {result}"
                
        except Exception as e:
            return False, f"Error sending custom message: {e}"
    
    def get_onboarding_status(self, target: str) -> Dict:
        """Get onboarding status for an agent"""
        try:
            # This would check if onboarding files exist for the agent
            agent_workspace = project_root / "agent_workspaces" / target
            onboarding_files = [
                "notes.md",
                "status.json",
                "task_list.json"
            ]
            
            status = {
                "agent": target,
                "workspace_exists": agent_workspace.exists(),
                "onboarding_files": {},
                "last_updated": None
            }
            
            if agent_workspace.exists():
                for file_name in onboarding_files:
                    file_path = agent_workspace / file_name
                    status["onboarding_files"][file_name] = file_path.exists()
                    
                    if file_path.exists():
                        mtime = file_path.stat().st_mtime
                        status["last_updated"] = datetime.fromtimestamp(mtime).isoformat()
            
            return status
        except Exception as e:
            return {"error": f"Error getting onboarding status: {e}"}
    
    def get_all_onboarding_status(self) -> Dict[str, Dict]:
        """Get onboarding status for all agents"""
        results = {}
        agents = self.acp.get_available_agents() if self.acp else []
        
        for agent in agents:
            results[agent] = self.get_onboarding_status(agent)
        
        return results
    
    def validate_onboarding_completion(self, target: str) -> Dict:
        """Validate that onboarding is complete for an agent"""
        try:
            status = self.get_onboarding_status(target)
            
            if "error" in status:
                return status
            
            # Check if all required files exist
            required_files = ["notes.md", "status.json", "task_list.json"]
            missing_files = []
            
            for file_name in required_files:
                if not status["onboarding_files"].get(file_name, False):
                    missing_files.append(file_name)
            
            validation_result = {
                "agent": target,
                "complete": len(missing_files) == 0,
                "missing_files": missing_files,
                "status": status
            }
            
            return validation_result
        except Exception as e:
            return {"error": f"Error validating onboarding: {e}"}
    
    def get_onboarding_progress(self) -> Dict:
        """Get overall onboarding progress"""
        try:
            agents = self.acp.get_available_agents() if self.acp else []
            total_agents = len(agents)
            completed_agents = 0
            agent_details = {}
            
            for agent in agents:
                validation = self.validate_onboarding_completion(agent)
                agent_details[agent] = validation
                
                if validation.get("complete", False):
                    completed_agents += 1
            
            progress = {
                "total_agents": total_agents,
                "completed_agents": completed_agents,
                "completion_percentage": (completed_agents / total_agents * 100) if total_agents > 0 else 0,
                "agent_details": agent_details
            }
            
            return progress
        except Exception as e:
            return {"error": f"Error getting onboarding progress: {e}"}

# Convenience functions
def create_onboarding_utils(layout_mode: str = "8-agent", test_mode: bool = True) -> OnboardingUtils:
    """Create an onboarding utils instance"""
    return OnboardingUtils(layout_mode, test_mode)

def send_quick_onboarding(target: str, message_type: str = "welcome") -> Tuple[bool, str]:
    """Quick function to send an onboarding message"""
    utils = OnboardingUtils(test_mode=True)
    return utils.send_onboarding_message(target, message_type)

def get_onboarding_progress() -> Dict:
    """Quick function to get onboarding progress"""
    utils = OnboardingUtils(test_mode=True)
    return utils.get_onboarding_progress() 
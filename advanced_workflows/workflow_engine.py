#!/usr/bin/env python3
"""
Advanced Workflow Engine - Built on Bi-Directional AI Communication Foundation
Powers sophisticated AI orchestration workflows using the new cursor capture system
"""

import json
import os
import time
import asyncio
from pathlib import Path
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from urllib import request, error
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowState(Enum):
    """Workflow execution states"""
    INITIALIZED = "initialized"
    RUNNING = "running"
    WAITING_FOR_AI = "waiting_for_ai"
    PROCESSING_RESPONSE = "processing_response"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"

@dataclass
class WorkflowStep:
    """Individual step in a workflow"""
    id: str
    name: str
    description: str
    agent_target: str
    prompt_template: str
    expected_response_type: str
    timeout_seconds: int = 300
    retry_count: int = 0
    max_retries: int = 3
    dependencies: List[str] = field(default_factory=list)
    completion_criteria: Dict[str, Any] = field(default_factory=dict)
    
    def is_ready(self, completed_steps: set) -> bool:
        """Check if step dependencies are satisfied"""
        return all(dep in completed_steps for dep in self.dependencies)

@dataclass
class AIResponse:
    """Captured AI response from cursor capture system"""
    agent: str
    text: str
    timestamp: float
    message_id: str
    role: str = "assistant"
    metadata: Dict[str, Any] = field(default_factory=dict)

class WorkflowEngine:
    """Main workflow orchestration engine"""

    def __init__(
        self,
        workflow_name: str,
        agent_system_path: str = "D:/repos/Dadudekc",
        devlog_webhook: str | None = None,
        devlog_username: str = "Agent Devlog",
        devlog_embed: bool = False,
    ):
        self.workflow_name = workflow_name
        self.agent_system_path = Path(agent_system_path)
        self.steps: List[WorkflowStep] = []
        self.current_step: Optional[WorkflowStep] = None
        self.completed_steps: set = set()
        self.failed_steps: set = set()
        self.state = WorkflowState.INITIALIZED
        self.start_time = time.time()
        self.ai_responses: List[AIResponse] = []
        self.workflow_data: Dict[str, Any] = {}

        # Devlog configuration
        self.devlog_webhook = devlog_webhook or os.environ.get("DISCORD_WEBHOOK_URL")
        self.devlog_username = devlog_username or os.environ.get(
            "DEVLOG_USERNAME", "Agent Devlog"
        )
        self.devlog_use_embed = bool(devlog_embed)

        # Response monitoring
        self.response_monitor_path = self.agent_system_path / "Agent-5" / "inbox"
        self.last_response_check = time.time()

        # Workflow persistence
        self.workflow_state_path = Path(f"workflow_states/{workflow_name}")
        self.workflow_state_path.mkdir(parents=True, exist_ok=True)

        logger.info(f"Workflow Engine initialized: {workflow_name}")

    def add_step(self, step: WorkflowStep) -> None:
        """Add a step to the workflow"""
        self.steps.append(step)
        logger.info(f"Added step: {step.name} (ID: {step.id})")

    def add_conversation_loop(self, agent_a: str, agent_b: str, topic: str, 
                            iterations: int = 3) -> None:
        """Add a conversation loop between two agents"""
        for i in range(iterations):
            # Agent A prompts Agent B
            step_a = WorkflowStep(
                id=f"conversation_{i}_a",
                name=f"Agent {agent_a} prompts {agent_b} - Round {i+1}",
                description=f"Agent {agent_a} asks {agent_b} about {topic}",
                agent_target=agent_a,
                prompt_template=f"Ask Agent {agent_b} about {topic}. Be specific and build on previous responses.",
                expected_response_type="conversation_prompt"
            )
            
            # Agent B responds
            step_b = WorkflowStep(
                id=f"conversation_{i}_b",
                name=f"Agent {agent_b} responds to {agent_a} - Round {i+1}",
                description=f"Agent {agent_b} responds to {agent_a} about {topic}",
                agent_target=agent_b,
                prompt_template=f"Respond to Agent {agent_a}'s question about {topic}. Provide detailed, helpful information.",
                expected_response_type="conversation_response",
                dependencies=[f"conversation_{i}_a"]
            )
            
            self.add_step(step_a)
            self.add_step(step_b)
            
            # Add dependency for next round
            if i > 0:
                step_a.dependencies = [f"conversation_{i-1}_b"]

    def add_multi_agent_orchestration(self, task: str, agents: List[str], 
                                    coordination_strategy: str = "parallel") -> None:
        """Add multi-agent orchestration workflow"""
        if coordination_strategy == "parallel":
            # All agents work in parallel
            for i, agent in enumerate(agents):
                step = WorkflowStep(
                    id=f"parallel_{agent}_{i}",
                    name=f"Agent {agent} works on {task}",
                    description=f"Agent {agent} executes task: {task}",
                    agent_target=agent,
                    prompt_template=f"Work on the following task: {task}. Coordinate with other agents as needed.",
                    expected_response_type="task_execution"
                )
                self.add_step(step)
                
        elif coordination_strategy == "sequential":
            # Agents work in sequence, building on each other
            for i, agent in enumerate(agents):
                dependencies = [f"sequential_{agents[j]}_{j}" for j in range(i)]
                step = WorkflowStep(
                    id=f"sequential_{agent}_{i}",
                    name=f"Agent {agent} works on {task} (Step {i+1})",
                    description=f"Agent {agent} executes task: {task} after previous agents",
                    agent_target=agent,
                    prompt_template=f"Continue work on: {task}. Build upon the work of previous agents.",
                    expected_response_type="task_execution",
                    dependencies=dependencies
                )
                self.add_step(step)

    def add_decision_tree(self, decision_point: str, branches: Dict[str, Dict[str, Any]]) -> None:
        """Add intelligent decision tree based on AI responses"""
        # Decision point step
        decision_step = WorkflowStep(
            id=f"decision_{decision_point}",
            name=f"Decision Point: {decision_point}",
            description=f"AI-driven decision making at: {decision_point}",
            agent_target="Agent-1",  # Primary decision maker
            prompt_template=f"Analyze the current situation and make a decision about: {decision_point}",
            expected_response_type="decision_analysis"
        )
        self.add_step(decision_step)
        
        # Branch steps based on decision
        for branch_name, branch_config in branches.items():
            branch_step = WorkflowStep(
                id=f"branch_{decision_point}_{branch_name}",
                name=f"Branch: {branch_name}",
                description=f"Execute branch: {branch_name}",
                agent_target=branch_config.get("agent", "Agent-1"),
                prompt_template=branch_config.get("prompt", f"Execute the {branch_name} branch"),
                expected_response_type="branch_execution",
                dependencies=[f"decision_{decision_point}"]
            )
            self.add_step(branch_step)

    def add_autonomous_loop(self, goal: str, max_iterations: int = 10) -> None:
        """Add autonomous workflow loop that adapts to AI responses"""
        for i in range(max_iterations):
            # Goal assessment step
            assessment_step = WorkflowStep(
                id=f"autonomous_assessment_{i}",
                name=f"Autonomous Assessment - Iteration {i+1}",
                description=f"Assess progress toward goal: {goal}",
                agent_target="Agent-1",
                prompt_template=f"Assess current progress toward goal: {goal}. What's the next best action?",
                expected_response_type="goal_assessment"
            )
            
            # Action execution step
            action_step = WorkflowStep(
                id=f"autonomous_action_{i}",
                name=f"Autonomous Action - Iteration {i+1}",
                description=f"Execute next action toward goal: {goal}",
                agent_target="Agent-2",
                prompt_template=f"Execute the next action toward goal: {goal}",
                expected_response_type="action_execution",
                dependencies=[f"autonomous_assessment_{i}"]
            )
            
            # Add dependency for next iteration
            if i > 0:
                assessment_step.dependencies = [f"autonomous_action_{i-1}"]
            
            self.add_step(assessment_step)
            self.add_step(action_step)

    def start(self) -> None:
        """Start workflow execution"""
        if not self.steps:
            logger.error("No steps defined for workflow")
            return
            
        self.state = WorkflowState.RUNNING
        logger.info(f"Starting workflow: {self.workflow_name}")
        self.save_state()

        # Start execution loop
        try:
            asyncio.run(self._execute_workflow())
        finally:
            self._send_devlog_summary()

    async def _execute_workflow(self) -> None:
        """Main workflow execution loop"""
        try:
            while self.state == WorkflowState.RUNNING:
                # Check for completed steps
                await self._check_step_completion()
                
                # Find next executable step
                next_step = self._find_next_step()
                if next_step:
                    await self._execute_step(next_step)
                elif self.completed_steps == set(step.id for step in self.steps):
                    # All steps completed
                    self.state = WorkflowState.COMPLETED
                    logger.info(f"Workflow completed: {self.workflow_name}")
                    break
                else:
                    # Waiting for dependencies
                    self.state = WorkflowState.WAITING_FOR_AI
                    await asyncio.sleep(5)
                    
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            self.state = WorkflowState.FAILED
            self.save_state()
            raise

    async def _execute_step(self, step: WorkflowStep) -> None:
        """Execute a single workflow step"""
        logger.info(f"Executing step: {step.name}")
        self.current_step = step
        self.state = WorkflowState.RUNNING
        
        try:
            # Send prompt to agent
            await self._send_prompt_to_agent(step)
            
            # Wait for AI response
            self.state = WorkflowState.WAITING_FOR_AI
            response = await self._wait_for_ai_response(step)
            
            if response:
                # Process response
                self.state = WorkflowState.PROCESSING_RESPONSE
                await self._process_ai_response(step, response)
                
                # Mark step as completed
                self.completed_steps.add(step.id)
                logger.info(f"Step completed: {step.name}")
                
            else:
                # Step failed
                self.failed_steps.add(step.id)
                logger.error(f"Step failed: {step.name}")
                
        except Exception as e:
            logger.error(f"Error executing step {step.name}: {e}")
            self.failed_steps.add(step.id)
            
        finally:
            self.current_step = None
            self.save_state()

    async def _send_prompt_to_agent(self, step: WorkflowStep) -> None:
        """Send prompt to target agent"""
        # This would integrate with the existing AgentCellPhone system
        # For now, we'll simulate the prompt sending
        prompt = step.prompt_template.format(**self.workflow_data)
        logger.info(f"Sending prompt to {step.agent_target}: {prompt[:100]}...")
        
        # TODO: Integrate with AgentCellPhone.send() method
        # await self.agent_system.send(step.agent_target, prompt)

    async def _wait_for_ai_response(self, step: WorkflowStep) -> Optional[AIResponse]:
        """Wait for AI response from cursor capture system"""
        start_time = time.time()
        
        while time.time() - start_time < step.timeout_seconds:
            # Check for new responses
            new_responses = await self._check_for_new_responses()
            
            for response in new_responses:
                if response.agent == step.agent_target:
                    # Found response from target agent
                    self.ai_responses.append(response)
                    return response
            
            await asyncio.sleep(1)
        
        logger.warning(f"Timeout waiting for response from {step.agent_target}")
        return None

    async def _check_for_new_responses(self) -> List[AIResponse]:
        """Check for new AI responses from cursor capture system"""
        new_responses = []
        
        if not self.response_monitor_path.exists():
            return new_responses
            
        # Check for new response files
        for response_file in self.response_monitor_path.glob("*.json"):
            if response_file.stat().st_mtime > self.last_response_check:
                try:
                    with open(response_file, 'r') as f:
                        data = json.load(f)
                    
                    # Convert to AIResponse object
                    response = AIResponse(
                        agent=data.get("agent", "unknown"),
                        text=data.get("payload", {}).get("text", ""),
                        timestamp=data.get("ts", time.time()),
                        message_id=data.get("payload", {}).get("message_id", ""),
                        role=data.get("payload", {}).get("role", "assistant"),
                        metadata=data
                    )
                    
                    new_responses.append(response)
                    
                except Exception as e:
                    logger.error(f"Error reading response file {response_file}: {e}")
        
        self.last_response_check = time.time()
        return new_responses

    async def _process_ai_response(self, step: WorkflowStep, response: AIResponse) -> None:
        """Process AI response and update workflow data"""
        logger.info(f"Processing response from {response.agent}: {response.text[:100]}...")
        
        # Extract key information based on expected response type
        if step.expected_response_type == "conversation_response":
            # Extract conversation insights
            self.workflow_data[f"conversation_{step.id}"] = {
                "response": response.text,
                "timestamp": response.timestamp,
                "agent": response.agent
            }
            
        elif step.expected_response_type == "task_execution":
            # Extract task completion status
            self.workflow_data[f"task_{step.id}"] = {
                "status": "completed",
                "result": response.text,
                "agent": response.agent
            }
            
        elif step.expected_response_type == "decision_analysis":
            # Extract decision information
            self.workflow_data[f"decision_{step.id}"] = {
                "analysis": response.text,
                "timestamp": response.timestamp,
                "agent": response.agent
            }
            
        # Store response for workflow analysis
        self.workflow_data[f"response_{step.id}"] = {
            "text": response.text,
            "timestamp": response.timestamp,
            "agent": response.agent,
            "metadata": response.metadata
        }

    def _find_next_step(self) -> Optional[WorkflowStep]:
        """Find the next executable step"""
        for step in self.steps:
            if (step.id not in self.completed_steps and 
                step.id not in self.failed_steps and 
                step.is_ready(self.completed_steps)):
                return step
        return None

    def save_state(self) -> None:
        """Save workflow state to disk"""
        state_data = {
            "workflow_name": self.workflow_name,
            "state": self.state.value,
            "completed_steps": list(self.completed_steps),
            "failed_steps": list(self.failed_steps),
            "workflow_data": self.workflow_data,
            "start_time": self.start_time,
            "current_time": time.time()
        }
        
        state_file = self.workflow_state_path / f"{int(time.time())}.json"
        with open(state_file, 'w') as f:
            json.dump(state_data, f, indent=2, default=str)
        
        logger.info(f"Workflow state saved: {state_file}")

    def get_progress(self) -> Dict[str, Any]:
        """Get workflow progress information"""
        total_steps = len(self.steps)
        completed_count = len(self.completed_steps)
        failed_count = len(self.failed_steps)
        
        return {
            "workflow_name": self.workflow_name,
            "state": self.state.value,
            "progress": {
                "total_steps": total_steps,
                "completed": completed_count,
                "failed": failed_count,
                "pending": total_steps - completed_count - failed_count,
                "percentage": (completed_count / total_steps * 100) if total_steps > 0 else 0
            },
            "current_step": self.current_step.name if self.current_step else None,
            "workflow_data": self.workflow_data,
            "execution_time": time.time() - self.start_time
        }

    def _post_discord(self, title: str, description: str) -> None:
        """Send a devlog message to Discord if configured"""
        if not self.devlog_webhook:
            return
        payload: dict = {"username": self.devlog_username}
        if self.devlog_use_embed:
            payload["embeds"] = [{"title": title, "description": description, "color": 5814783}]
        else:
            payload["content"] = f"**{title}**\n{description}"
        try:
            data = json.dumps(payload).encode("utf-8")
            req = request.Request(self.devlog_webhook, data=data, headers={"Content-Type": "application/json"})
            with request.urlopen(req, timeout=6):
                pass
        except (error.HTTPError, error.URLError, Exception):
            pass

    def _send_devlog_summary(self) -> None:
        """Post a workflow summary to Discord"""
        progress = self.get_progress()
        total = progress["progress"]["total_steps"]
        completed = progress["progress"]["completed"]
        failed = progress["progress"]["failed"]
        duration = int(progress["execution_time"])
        description = f"Completed {completed}/{total} steps in {duration}s"
        if failed:
            description += f" with {failed} failed"
        self._post_discord(f"Workflow {self.workflow_name} {self.state.value}", description)

    def pause(self) -> None:
        """Pause workflow execution"""
        if self.state == WorkflowState.RUNNING:
            self.state = WorkflowState.PAUSED
            logger.info(f"Workflow paused: {self.workflow_name}")
            self.save_state()

    def resume(self) -> None:
        """Resume workflow execution"""
        if self.state == WorkflowState.PAUSED:
            self.state = WorkflowState.RUNNING
            logger.info(f"Workflow resumed: {self.workflow_name}")
            self.save_state()

    def stop(self) -> None:
        """Stop workflow execution"""
        self.state = WorkflowState.FAILED
        logger.info(f"Workflow stopped: {self.workflow_name}")
        self.save_state()

if __name__ == "__main__":
    # Example usage
    engine = WorkflowEngine("example_workflow")
    
    # Add conversation loop
    engine.add_conversation_loop("Agent-1", "Agent-2", "code architecture", 2)
    
    # Add multi-agent orchestration
    engine.add_multi_agent_orchestration("build API", ["Agent-1", "Agent-2", "Agent-3"], "parallel")
    
    # Start workflow
    engine.start()

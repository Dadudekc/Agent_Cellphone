#!/usr/bin/env python3
"""
Multi-Agent Development Workflow - Built on Bi-Directional AI Communication Foundation
Coordinated development across multiple AI agents with intelligent task distribution
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / ".."))

from advanced_workflows.workflow_engine import WorkflowEngine, WorkflowStep

class MultiAgentDevWorkflow:
    """Multi-agent development workflow using bi-directional communication"""
    
    def __init__(self, task_description: str, agents: List[str], 
                 coordination_strategy: str = "parallel"):
        self.task_description = task_description
        self.agents = agents
        self.coordination_strategy = coordination_strategy
        self.workflow_engine = WorkflowEngine("multi_agent_dev")
        self.task_breakdown = {}
        self.development_results = {}
        
        # Initialize workflow
        self._setup_workflow()
        
    def _setup_workflow(self) -> None:
        """Setup the multi-agent development workflow"""
        
        # Step 1: Task Analysis and Breakdown
        analysis_step = WorkflowStep(
            id="task_analysis",
            name="Task Analysis and Breakdown",
            description="Analyze the development task and break it down into components",
            agent_target="Agent-1",
            prompt_template="Analyze the following development task and break it down into logical components: {task_description}. Consider: architecture, dependencies, technologies, and implementation phases. Provide a structured breakdown with clear deliverables.",
            expected_response_type="task_breakdown"
        )
        self.workflow_engine.add_step(analysis_step)
        
        # Step 2: Architecture Design
        architecture_step = WorkflowStep(
            id="architecture_design",
            name="System Architecture Design",
            description="Design the overall system architecture",
            agent_target="Agent-2",
            prompt_template="Based on the task breakdown, design the system architecture. Consider: scalability, maintainability, security, performance, and technology choices. Provide architecture diagrams and design decisions.",
            expected_response_type="architecture_design",
            dependencies=["task_analysis"]
        )
        self.workflow_engine.add_step(architecture_step)
        
        # Step 3: Technology Stack Selection
        tech_stack_step = WorkflowStep(
            id="tech_stack",
            name="Technology Stack Selection",
            description="Select appropriate technologies for implementation",
            agent_target="Agent-3",
            prompt_template="Based on the architecture design, recommend the technology stack. Consider: language choices, frameworks, databases, deployment options, and development tools. Provide rationale for each choice.",
            expected_response_type="tech_stack_recommendation",
            dependencies=["architecture_design"]
        )
        self.workflow_engine.add_step(tech_stack_step)
        
        # Step 4: Implementation Planning
        planning_step = WorkflowStep(
            id="implementation_planning",
            name="Implementation Planning and Task Assignment",
            description="Create detailed implementation plan and assign tasks to agents",
            agent_target="Agent-1",
            prompt_template="Create a detailed implementation plan based on the task breakdown, architecture, and tech stack. Assign specific tasks to each agent, considering their strengths and dependencies. Include timelines and milestones.",
            expected_response_type="implementation_plan",
            dependencies=["task_analysis", "architecture_design", "tech_stack"]
        )
        self.workflow_engine.add_step(planning_step)
        
        # Step 5: Parallel Development Execution
        if self.coordination_strategy == "parallel":
            self._add_parallel_development_steps()
        else:
            self._add_sequential_development_steps()
            
        # Step 6: Integration and Testing
        integration_step = WorkflowStep(
            id="integration_testing",
            name="Integration and Testing",
            description="Integrate components and perform testing",
            agent_target="Agent-5",
            prompt_template="Coordinate the integration of all developed components. Create integration tests, resolve conflicts, and ensure system compatibility. Provide testing results and integration status.",
            expected_response_type="integration_report",
            dependencies=[f"dev_{agent}" for agent in self.agents]
        )
        self.workflow_engine.add_step(integration_step)
        
        # Step 7: Documentation and Deployment
        documentation_step = WorkflowStep(
            id="documentation_deployment",
            name="Documentation and Deployment Preparation",
            description="Create documentation and prepare for deployment",
            agent_target="Agent-1",
            prompt_template="Create comprehensive documentation including: user guides, API documentation, deployment instructions, and maintenance procedures. Prepare deployment scripts and configuration files.",
            expected_response_type="documentation_deployment",
            dependencies=["integration_testing"]
        )
        self.workflow_engine.add_step(documentation_step)
        
        # Add collaborative development loops
        self._add_collaborative_development_loops()
        
    def _add_parallel_development_steps(self) -> None:
        """Add parallel development steps for all agents"""
        for i, agent in enumerate(self.agents):
            dev_step = WorkflowStep(
                id=f"dev_{agent}",
                name=f"Development by {agent}",
                description=f"Agent {agent} implements assigned components",
                agent_target=agent,
                prompt_template="Implement your assigned development tasks. Coordinate with other agents as needed, follow the architecture and tech stack decisions, and ensure code quality. Report progress and any issues encountered.",
                expected_response_type="development_progress",
                dependencies=["implementation_planning"]
            )
            self.workflow_engine.add_step(dev_step)
            
    def _add_sequential_development_steps(self) -> None:
        """Add sequential development steps where agents build on each other"""
        for i, agent in enumerate(self.agents):
            dependencies = [f"dev_{self.agents[j]}" for j in range(i)]
            dependencies.append("implementation_planning")
            
            dev_step = WorkflowStep(
                id=f"dev_{agent}",
                name=f"Development by {agent} (Step {i+1})",
                description=f"Agent {agent} implements assigned components after previous agents",
                agent_target=agent,
                prompt_template="Continue development based on the work of previous agents. Implement your assigned tasks, integrate with existing components, and ensure compatibility. Report progress and any integration issues.",
                expected_response_type="development_progress",
                dependencies=dependencies
            )
            self.workflow_engine.add_step(dev_step)
            
    def _add_collaborative_development_loops(self) -> None:
        """Add collaborative development loops between agents"""
        
        # Architecture + Implementation collaboration
        self.workflow_engine.add_conversation_loop(
            "Agent-2", "Agent-1", 
            "architecture implementation details", 2
        )
        
        # Tech Stack + Development collaboration
        self.workflow_engine.add_conversation_loop(
            "Agent-3", "Agent-4", 
            "technology implementation best practices", 2
        )
        
        # Cross-team development coordination
        for i in range(len(self.agents) - 1):
            self.workflow_engine.add_conversation_loop(
                self.agents[i], self.agents[i+1], 
                f"coordination between {self.agents[i]} and {self.agents[i+1]}", 1
            )
            
    def start_development(self) -> None:
        """Start the multi-agent development workflow"""
        print(f"🚀 Starting Multi-Agent Development Workflow")
        print(f"📋 Task: {self.task_description}")
        print(f"👥 Agents: {', '.join(self.agents)}")
        print(f"🔄 Strategy: {self.coordination_strategy}")
        print(f"🔍 Workflow Steps: {len(self.workflow_engine.steps)}")
        print("=" * 60)
        
        # Start the workflow
        self.workflow_engine.start()
        
    def get_development_summary(self) -> Dict[str, Any]:
        """Get a summary of the development progress"""
        progress = self.workflow_engine.get_progress()
        
        summary = {
            "task_description": self.task_description,
            "agents": self.agents,
            "coordination_strategy": self.coordination_strategy,
            "workflow_status": progress["state"],
            "progress_percentage": progress["progress"]["percentage"],
            "completed_steps": progress["progress"]["completed"],
            "total_steps": progress["progress"]["total_steps"],
            "execution_time": progress["execution_time"],
            "current_step": progress["current_step"],
            "workflow_data": progress["workflow_data"]
        }
        
        return summary
        
    def export_development_report(self, output_path: str = None) -> str:
        """Export the development results to a comprehensive report"""
        if not output_path:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = f"multi_agent_dev_report_{timestamp}.json"
            
        report_data = {
            "development_metadata": {
                "task_description": self.task_description,
                "agents": self.agents,
                "coordination_strategy": self.coordination_strategy,
                "development_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "workflow_duration": self.workflow_engine.get_progress()["execution_time"]
            },
            "development_results": self.workflow_engine.workflow_data,
            "workflow_progress": self.workflow_engine.get_progress()
        }
        
        with open(output_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
            
        print(f"📄 Development report exported to: {output_path}")
        return output_path

def main():
    """Main entry point for Multi-Agent Development workflow"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Multi-Agent Development Workflow")
    parser.add_argument("--task", required=True, help="Development task description")
    parser.add_argument("--agents", required=True, nargs="+", 
                       help="List of agents to participate in development")
    parser.add_argument("--strategy", default="parallel",
                       choices=["parallel", "sequential"],
                       help="Coordination strategy for agents")
    parser.add_argument("--export-report", help="Path to export the development report")
    
    args = parser.parse_args()
    
    # Validate agents list
    if len(args.agents) < 2:
        print("❌ Multi-agent development requires at least 2 agents")
        return 1
        
    # Initialize and start the workflow
    try:
        dev_workflow = MultiAgentDevWorkflow(
            task_description=args.task,
            agents=args.agents,
            coordination_strategy=args.strategy
        )
        
        # Start the development
        dev_workflow.start_development()
        
        # Get summary
        summary = dev_workflow.get_development_summary()
        print("\n" + "=" * 60)
        print("📊 DEVELOPMENT SUMMARY")
        print("=" * 60)
        print(f"Task: {summary['task_description']}")
        print(f"Agents: {', '.join(summary['agents'])}")
        print(f"Strategy: {summary['coordination_strategy']}")
        print(f"Status: {summary['workflow_status']}")
        print(f"Progress: {summary['progress_percentage']:.1f}%")
        print(f"Completed: {summary['completed_steps']}/{summary['total_steps']} steps")
        print(f"Duration: {summary['execution_time']:.1f} seconds")
        
        # Export report if requested
        if args.export_report:
            report_path = dev_workflow.export_development_report(args.export_report)
            print(f"📄 Report exported to: {report_path}")
        else:
            # Auto-export with timestamp
            report_path = dev_workflow.export_development_report()
            
        return 0
        
    except Exception as e:
        print(f"❌ Multi-agent development workflow failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())

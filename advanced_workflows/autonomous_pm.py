#!/usr/bin/env python3
"""
Autonomous Project Management Workflow - Built on Bi-Directional AI Communication Foundation
Self-managing project workflows that adapt to AI responses and autonomously drive toward goals
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / ".."))

from advanced_workflows.workflow_engine import WorkflowEngine, WorkflowStep

class AutonomousPMWorkflow:
    """Autonomous project management workflow using bi-directional communication"""
    
    def __init__(self, goal: str, max_iterations: int = 10, 
                 adaptation_threshold: float = 0.8):
        self.goal = goal
        self.max_iterations = max_iterations
        self.adaptation_threshold = adaptation_threshold
        self.workflow_engine = WorkflowEngine("autonomous_pm")
        self.project_metrics = {}
        self.adaptation_history = []
        
        # Initialize workflow
        self._setup_workflow()
        
    def _setup_workflow(self) -> None:
        """Setup the autonomous project management workflow"""
        
        # Step 1: Goal Analysis and Planning
        goal_analysis_step = WorkflowStep(
            id="goal_analysis",
            name="Goal Analysis and Initial Planning",
            description="Analyze the project goal and create initial plan",
            agent_target="Agent-1",
            prompt_template="Analyze the following project goal: {goal}. Break it down into measurable objectives, identify key success criteria, and create an initial project plan with milestones and deliverables.",
            expected_response_type="goal_analysis"
        )
        self.workflow_engine.add_step(goal_analysis_step)
        
        # Step 2: Resource Assessment
        resource_assessment_step = WorkflowStep(
            id="resource_assessment",
            name="Resource Assessment and Allocation",
            description="Assess available resources and allocate them to project tasks",
            agent_target="Agent-2",
            prompt_template="Based on the goal analysis, assess the resources needed for this project. Consider: human resources, technical resources, time, budget, and external dependencies. Provide a resource allocation plan.",
            expected_response_type="resource_assessment",
            dependencies=["goal_analysis"]
        )
        self.workflow_engine.add_step(resource_assessment_step)
        
        # Step 3: Risk Assessment
        risk_assessment_step = WorkflowStep(
            id="risk_assessment",
            name="Risk Assessment and Mitigation Planning",
            description="Identify project risks and create mitigation strategies",
            agent_target="Agent-3",
            prompt_template="Identify potential risks for this project based on the goal and resource assessment. Categorize risks by probability and impact, and provide mitigation strategies for high-priority risks.",
            expected_response_type="risk_assessment",
            dependencies=["goal_analysis", "resource_assessment"]
        )
        self.workflow_engine.add_step(risk_assessment_step)
        
        # Add autonomous execution loops
        self._add_autonomous_execution_loops()
        
        # Add monitoring and adaptation steps
        self._add_monitoring_adaptation_steps()
        
    def _add_autonomous_execution_loops(self) -> None:
        """Add autonomous execution loops that adapt to progress"""
        
        for i in range(self.max_iterations):
            # Progress Assessment
            assessment_step = WorkflowStep(
                id=f"progress_assessment_{i}",
                name=f"Progress Assessment - Iteration {i+1}",
                description=f"Assess progress toward goal: {self.goal}",
                agent_target="Agent-1",
                prompt_template=f"Assess current progress toward goal: {self.goal}. Evaluate: completed milestones, current status, blockers, and progress against timeline. Provide a progress score (0-100) and identify the next critical actions.",
                expected_response_type="progress_assessment"
            )
            
            # Strategy Adaptation
            adaptation_step = WorkflowStep(
                id=f"strategy_adaptation_{i}",
                name=f"Strategy Adaptation - Iteration {i+1}",
                description=f"Adapt strategy based on progress assessment",
                agent_target="Agent-2",
                prompt_template=f"Based on the progress assessment, adapt the project strategy if needed. Consider: timeline adjustments, resource reallocation, scope changes, and risk mitigation updates. Provide updated strategy and action plan.",
                expected_response_type="strategy_adaptation",
                dependencies=[f"progress_assessment_{i}"]
            )
            
            # Action Execution
            action_step = WorkflowStep(
                id=f"action_execution_{i}",
                name=f"Action Execution - Iteration {i+1}",
                description=f"Execute next actions toward goal: {self.goal}",
                agent_target="Agent-3",
                prompt_template=f"Execute the next critical actions toward goal: {self.goal}. Follow the updated strategy, coordinate with team members, and report progress and any issues encountered.",
                expected_response_type="action_execution",
                dependencies=[f"strategy_adaptation_{i}"]
            )
            
            # Progress Validation
            validation_step = WorkflowStep(
                id=f"progress_validation_{i}",
                name=f"Progress Validation - Iteration {i+1}",
                description=f"Validate progress and update metrics",
                agent_target="Agent-4",
                prompt_template=f"Validate the progress made in this iteration. Update project metrics, verify milestone completion, and assess the impact of strategy adaptations. Provide validation report and updated project status.",
                expected_response_type="progress_validation",
                dependencies=[f"action_execution_{i}"]
            )
            
            # Add dependencies for next iteration
            if i > 0:
                assessment_step.dependencies = [f"progress_validation_{i-1}"]
            
            self.workflow_engine.add_step(assessment_step)
            self.workflow_engine.add_step(adaptation_step)
            self.workflow_engine.add_step(action_step)
            self.workflow_engine.add_step(validation_step)
            
    def _add_monitoring_adaptation_steps(self) -> None:
        """Add continuous monitoring and adaptation steps"""
        
        # Continuous Monitoring
        monitoring_step = WorkflowStep(
            id="continuous_monitoring",
            name="Continuous Project Monitoring",
            description="Monitor project health and performance metrics",
            agent_target="Agent-5",
            prompt_template="Continuously monitor the project's health and performance. Track: progress metrics, resource utilization, risk status, and overall project health. Alert on any issues requiring immediate attention.",
            expected_response_type="monitoring_report",
            dependencies=[f"progress_validation_{self.max_iterations-1}"]
        )
        self.workflow_engine.add_step(monitoring_step)
        
        # Final Goal Achievement Assessment
        final_assessment_step = WorkflowStep(
            id="final_assessment",
            name="Final Goal Achievement Assessment",
            description="Final assessment of goal achievement",
            agent_target="Agent-1",
            prompt_template=f"Provide a final assessment of goal achievement: {self.goal}. Evaluate: overall success, lessons learned, unexpected outcomes, and recommendations for future similar projects.",
            expected_response_type="final_assessment",
            dependencies=["continuous_monitoring"]
        )
        self.workflow_engine.add_step(final_assessment_step)
        
        # Add collaborative adaptation loops
        self._add_collaborative_adaptation_loops()
        
    def _add_collaborative_adaptation_loops(self) -> None:
        """Add collaborative adaptation loops between agents"""
        
        # Progress + Strategy collaboration
        for i in range(self.max_iterations):
            self.workflow_engine.add_conversation_loop(
                "Agent-1", "Agent-2", 
                f"progress-driven strategy adaptation in iteration {i+1}", 1
            )
            
        # Strategy + Execution collaboration
        for i in range(self.max_iterations):
            self.workflow_engine.add_conversation_loop(
                "Agent-2", "Agent-3", 
                f"strategy execution coordination in iteration {i+1}", 1
            )
            
        # Execution + Validation collaboration
        for i in range(self.max_iterations):
            self.workflow_engine.add_conversation_loop(
                "Agent-3", "Agent-4", 
                f"execution validation and feedback in iteration {i+1}", 1
            )
            
    def start_autonomous_management(self) -> None:
        """Start the autonomous project management workflow"""
        print(f"🚀 Starting Autonomous Project Management Workflow")
        print(f"🎯 Goal: {self.goal}")
        print(f"🔄 Max Iterations: {self.max_iterations}")
        print(f"📊 Adaptation Threshold: {self.adaptation_threshold}")
        print(f"🔍 Workflow Steps: {len(self.workflow_engine.steps)}")
        print("=" * 60)
        
        # Start the workflow
        self.workflow_engine.start()
        
    def get_management_summary(self) -> Dict[str, Any]:
        """Get a summary of the project management progress"""
        progress = self.workflow_engine.get_progress()
        
        summary = {
            "goal": self.goal,
            "max_iterations": self.max_iterations,
            "adaptation_threshold": self.adaptation_threshold,
            "workflow_status": progress["state"],
            "progress_percentage": progress["progress"]["percentage"],
            "completed_steps": progress["progress"]["completed"],
            "total_steps": progress["progress"]["total_steps"],
            "execution_time": progress["execution_time"],
            "current_step": progress["current_step"],
            "workflow_data": progress["workflow_data"]
        }
        
        return summary
        
    def export_management_report(self, output_path: str = None) -> str:
        """Export the project management results to a comprehensive report"""
        if not output_path:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = f"autonomous_pm_report_{timestamp}.json"
            
        report_data = {
            "project_management_metadata": {
                "goal": self.goal,
                "max_iterations": self.max_iterations,
                "adaptation_threshold": self.adaptation_threshold,
                "management_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "workflow_duration": self.workflow_engine.get_progress()["execution_time"]
            },
            "management_results": self.workflow_engine.workflow_data,
            "workflow_progress": self.workflow_engine.get_progress()
        }
        
        with open(output_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
            
        print(f"📄 Project management report exported to: {output_path}")
        return output_path

def main():
    """Main entry point for Autonomous Project Management workflow"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Autonomous Project Management Workflow")
    parser.add_argument("--goal", required=True, help="Project goal to achieve")
    parser.add_argument("--max-iterations", type=int, default=10,
                       help="Maximum number of adaptation iterations")
    parser.add_argument("--adaptation-threshold", type=float, default=0.8,
                       help="Threshold for triggering strategy adaptation (0.0-1.0)")
    parser.add_argument("--export-report", help="Path to export the management report")
    
    args = parser.parse_args()
    
    # Validate adaptation threshold
    if not 0.0 <= args.adaptation_threshold <= 1.0:
        print("❌ Adaptation threshold must be between 0.0 and 1.0")
        return 1
        
    # Initialize and start the workflow
    try:
        pm_workflow = AutonomousPMWorkflow(
            goal=args.goal,
            max_iterations=args.max_iterations,
            adaptation_threshold=args.adaptation_threshold
        )
        
        # Start the autonomous management
        pm_workflow.start_autonomous_management()
        
        # Get summary
        summary = pm_workflow.get_management_summary()
        print("\n" + "=" * 60)
        print("📊 PROJECT MANAGEMENT SUMMARY")
        print("=" * 60)
        print(f"Goal: {summary['goal']}")
        print(f"Max Iterations: {summary['max_iterations']}")
        print(f"Adaptation Threshold: {summary['adaptation_threshold']}")
        print(f"Status: {summary['workflow_status']}")
        print(f"Progress: {summary['progress_percentage']:.1f}%")
        print(f"Completed: {summary['completed_steps']}/{summary['total_steps']} steps")
        print(f"Duration: {summary['execution_time']:.1f} seconds")
        
        # Export report if requested
        if args.export_report:
            report_path = pm_workflow.export_management_report(args.export_report)
            print(f"📄 Report exported to: {report_path}")
        else:
            # Auto-export with timestamp
            report_path = pm_workflow.export_management_report()
            
        return 0
        
    except Exception as e:
        print(f"❌ Autonomous project management workflow failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())

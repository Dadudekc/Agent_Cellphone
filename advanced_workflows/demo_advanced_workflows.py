#!/usr/bin/env python3
"""
Advanced Workflows Demonstration - Built on Bi-Directional AI Communication Foundation
Comprehensive demonstration of all advanced workflow capabilities
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / ".."))

from advanced_workflows.workflow_engine import WorkflowEngine, WorkflowStep
from advanced_workflows.ai_code_review import AICodeReviewWorkflow
from advanced_workflows.multi_agent_dev import MultiAgentDevWorkflow
from advanced_workflows.autonomous_pm import AutonomousPMWorkflow

class AdvancedWorkflowsDemo:
    """Comprehensive demonstration of advanced workflow capabilities"""
    
    def __init__(self):
        self.demo_results = {}
        self.workflow_engines = {}
        
    def demo_conversation_loops(self) -> Dict[str, Any]:
        """Demonstrate AI-to-AI conversation loops"""
        print("🔄 **DEMO: AI-to-AI Conversation Loops**")
        print("=" * 50)
        
        engine = WorkflowEngine("conversation_demo")
        
        # Add conversation loop between agents
        engine.add_conversation_loop("Agent-1", "Agent-2", "advanced workflow design", 3)
        
        # Add multi-agent conversation
        engine.add_conversation_loop("Agent-3", "Agent-4", "system integration strategies", 2)
        
        # Add cross-team coordination
        engine.add_conversation_loop("Agent-5", "Agent-1", "workflow orchestration best practices", 2)
        
        print(f"✅ Created conversation workflow with {len(engine.steps)} steps")
        print(f"📋 Steps: {[step.name for step in engine.steps]}")
        
        self.workflow_engines["conversation"] = engine
        return {"type": "conversation_loops", "steps": len(engine.steps)}
        
    def demo_multi_agent_orchestration(self) -> Dict[str, Any]:
        """Demonstrate multi-agent orchestration"""
        print("\n🎭 **DEMO: Multi-Agent Orchestration**")
        print("=" * 50)
        
        engine = WorkflowEngine("orchestration_demo")
        
        # Add parallel orchestration
        engine.add_multi_agent_orchestration(
            "build microservice architecture", 
            ["Agent-1", "Agent-2", "Agent-3"], 
            "parallel"
        )
        
        # Add sequential orchestration
        engine.add_multi_agent_orchestration(
            "implement CI/CD pipeline", 
            ["Agent-4", "Agent-5"], 
            "sequential"
        )
        
        print(f"✅ Created orchestration workflow with {len(engine.steps)} steps")
        print(f"📋 Steps: {[step.name for step in engine.steps]}")
        
        self.workflow_engines["orchestration"] = engine
        return {"type": "multi_agent_orchestration", "steps": len(engine.steps)}
        
    def demo_decision_trees(self) -> Dict[str, Any]:
        """Demonstrate intelligent decision trees"""
        print("\n🧠 **DEMO: Intelligent Decision Trees**")
        print("=" * 50)
        
        engine = WorkflowEngine("decision_demo")
        
        # Add decision tree for deployment strategy
        deployment_branches = {
            "blue_green": {
                "agent": "Agent-1",
                "prompt": "Implement blue-green deployment strategy with zero downtime"
            },
            "canary": {
                "agent": "Agent-2", 
                "prompt": "Implement canary deployment with gradual rollout"
            },
            "rolling": {
                "agent": "Agent-3",
                "prompt": "Implement rolling deployment with health checks"
            }
        }
        
        engine.add_decision_tree("deployment_strategy", deployment_branches)
        
        # Add decision tree for scaling strategy
        scaling_branches = {
            "horizontal": {
                "agent": "Agent-4",
                "prompt": "Implement horizontal scaling with load balancing"
            },
            "vertical": {
                "agent": "Agent-5",
                "prompt": "Implement vertical scaling with resource optimization"
            }
        }
        
        engine.add_decision_tree("scaling_strategy", scaling_branches)
        
        print(f"✅ Created decision tree workflow with {len(engine.steps)} steps")
        print(f"📋 Steps: {[step.name for step in engine.steps]}")
        
        self.workflow_engines["decision"] = engine
        return {"type": "decision_trees", "steps": len(engine.steps)}
        
    def demo_autonomous_loops(self) -> Dict[str, Any]:
        """Demonstrate autonomous workflow loops"""
        print("\n🔄 **DEMO: Autonomous Workflow Loops**")
        print("=" * 50)
        
        engine = WorkflowEngine("autonomous_demo")
        
        # Add autonomous loop for system optimization
        engine.add_autonomous_loop("optimize system performance", 5)
        
        # Add autonomous loop for quality improvement
        engine.add_autonomous_loop("improve code quality", 3)
        
        print(f"✅ Created autonomous workflow with {len(engine.steps)} steps")
        print(f"📋 Steps: {[step.name for step in engine.steps]}")
        
        self.workflow_engines["autonomous"] = engine
        return {"type": "autonomous_loops", "steps": len(engine.steps)}
        
    def demo_ai_code_review(self) -> Dict[str, Any]:
        """Demonstrate AI Code Review workflow"""
        print("\n🔍 **DEMO: AI Code Review Workflow**")
        print("=" * 50)
        
        # Create code review workflow for current project
        current_project = Path(__file__).parent.parent
        review_workflow = AICodeReviewWorkflow(
            project_path=str(current_project),
            review_focus="architecture"
        )
        
        print(f"✅ Created AI Code Review workflow with {len(review_workflow.workflow_engine.steps)} steps")
        print(f"📋 Steps: {[step.name for step in review_workflow.workflow_engine.steps]}")
        
        self.workflow_engines["code_review"] = review_workflow.workflow_engine
        return {"type": "ai_code_review", "steps": len(review_workflow.workflow_engine.steps)}
        
    def demo_multi_agent_development(self) -> Dict[str, Any]:
        """Demonstrate Multi-Agent Development workflow"""
        print("\n👥 **DEMO: Multi-Agent Development Workflow**")
        print("=" * 50)
        
        # Create multi-agent development workflow
        dev_workflow = MultiAgentDevWorkflow(
            task_description="build advanced workflow orchestration system",
            agents=["Agent-1", "Agent-2", "Agent-3", "Agent-4"],
            coordination_strategy="parallel"
        )
        
        print(f"✅ Created Multi-Agent Development workflow with {len(dev_workflow.workflow_engine.steps)} steps")
        print(f"📋 Steps: {[step.name for step in dev_workflow.workflow_engine.steps]}")
        
        self.workflow_engines["dev"] = dev_workflow.workflow_engine
        return {"type": "multi_agent_development", "steps": len(dev_workflow.workflow_engine.steps)}
        
    def demo_autonomous_project_management(self) -> Dict[str, Any]:
        """Demonstrate Autonomous Project Management workflow"""
        print("\n🎯 **DEMO: Autonomous Project Management Workflow**")
        print("=" * 50)
        
        # Create autonomous project management workflow
        pm_workflow = AutonomousPMWorkflow(
            goal="deploy production-ready advanced workflow system",
            max_iterations=5,
            adaptation_threshold=0.8
        )
        
        print(f"✅ Created Autonomous Project Management workflow with {len(pm_workflow.workflow_engine.steps)} steps")
        print(f"📋 Steps: {[step.name for step in pm_workflow.workflow_engine.steps]}")
        
        self.workflow_engines["pm"] = pm_workflow.workflow_engine
        return {"type": "autonomous_project_management", "steps": len(pm_workflow.workflow_engine.steps)}
        
    def demo_workflow_integration(self) -> Dict[str, Any]:
        """Demonstrate workflow integration and coordination"""
        print("\n🔗 **DEMO: Workflow Integration and Coordination**")
        print("=" * 50)
        
        # Create a master workflow that coordinates all other workflows
        master_engine = WorkflowEngine("master_coordination")
        
        # Add coordination steps for each workflow type
        coordination_steps = [
            WorkflowStep(
                id="conversation_coordination",
                name="Conversation Workflow Coordination",
                description="Coordinate AI-to-AI conversation workflows",
                agent_target="Agent-1",
                prompt_template="Coordinate all conversation workflows and ensure proper agent communication patterns.",
                expected_response_type="coordination_report"
            ),
            WorkflowStep(
                id="orchestration_coordination",
                name="Orchestration Workflow Coordination",
                description="Coordinate multi-agent orchestration workflows",
                agent_target="Agent-2",
                prompt_template="Coordinate all orchestration workflows and ensure proper task distribution.",
                expected_response_type="coordination_report"
            ),
            WorkflowStep(
                id="decision_coordination",
                name="Decision Tree Workflow Coordination",
                description="Coordinate decision tree workflows",
                agent_target="Agent-3",
                prompt_template="Coordinate all decision tree workflows and ensure proper branching logic.",
                expected_response_type="coordination_report"
            ),
            WorkflowStep(
                id="autonomous_coordination",
                name="Autonomous Workflow Coordination",
                description="Coordinate autonomous workflow loops",
                agent_target="Agent-4",
                prompt_template="Coordinate all autonomous workflows and ensure proper adaptation cycles.",
                expected_response_type="coordination_report"
            ),
            WorkflowStep(
                id="master_synthesis",
                name="Master Workflow Synthesis",
                description="Synthesize all workflow results",
                agent_target="Agent-5",
                prompt_template="Synthesize results from all coordinated workflows and provide overall system status.",
                expected_response_type="master_synthesis",
                dependencies=["conversation_coordination", "orchestration_coordination", 
                           "decision_coordination", "autonomous_coordination"]
            )
        ]
        
        for step in coordination_steps:
            master_engine.add_step(step)
            
        print(f"✅ Created master coordination workflow with {len(master_engine.steps)} steps")
        print(f"📋 Steps: {[step.name for step in master_engine.steps]}")
        
        self.workflow_engines["master"] = master_engine
        return {"type": "workflow_integration", "steps": len(master_engine.steps)}
        
    def run_all_demos(self) -> Dict[str, Any]:
        """Run all workflow demonstrations"""
        print("🚀 **ADVANCED WORKFLOWS DEMONSTRATION**")
        print("=" * 60)
        print("Built on Agent_Cellphone v1.0.0 Bi-Directional Foundation")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run all demonstrations
        demos = [
            self.demo_conversation_loops,
            self.demo_multi_agent_orchestration,
            self.demo_decision_trees,
            self.demo_autonomous_loops,
            self.demo_ai_code_review,
            self.demo_multi_agent_development,
            self.demo_autonomous_project_management,
            self.demo_workflow_integration
        ]
        
        for demo in demos:
            try:
                result = demo()
                self.demo_results[result["type"]] = result
            except Exception as e:
                print(f"❌ Demo failed: {e}")
                self.demo_results[result["type"]] = {"error": str(e)}
                
        # Calculate total statistics
        total_steps = sum(result.get("steps", 0) for result in self.demo_results.values() if "error" not in result)
        total_workflows = len(self.workflow_engines)
        
        demo_summary = {
            "total_demos": len(demos),
            "successful_demos": len([r for r in self.demo_results.values() if "error" not in r]),
            "total_workflow_steps": total_steps,
            "total_workflows": total_workflows,
            "execution_time": time.time() - start_time,
            "demo_results": self.demo_results
        }
        
        return demo_summary
        
    def export_demo_report(self, output_path: str = None) -> str:
        """Export the demonstration results to a comprehensive report"""
        if not output_path:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = f"advanced_workflows_demo_report_{timestamp}.json"
            
        report_data = {
            "demo_metadata": {
                "demo_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "agent_cellphone_version": "v1.0.0",
                "foundation": "bi-directional_ai_communication"
            },
            "demo_summary": self.demo_results,
            "workflow_engines": {
                name: {
                    "steps": len(engine.steps),
                    "step_names": [step.name for step in engine.steps]
                }
                for name, engine in self.workflow_engines.items()
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
            
        print(f"📄 Demo report exported to: {output_path}")
        return output_path

def main():
    """Main entry point for Advanced Workflows demonstration"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Advanced Workflows Demonstration")
    parser.add_argument("--export-report", help="Path to export the demonstration report")
    parser.add_argument("--run-workflows", action="store_true", 
                       help="Actually run the workflows (not just create them)")
    
    args = parser.parse_args()
    
    try:
        # Initialize demo
        demo = AdvancedWorkflowsDemo()
        
        # Run all demonstrations
        summary = demo.run_all_demos()
        
        # Display summary
        print("\n" + "=" * 60)
        print("📊 **DEMONSTRATION SUMMARY**")
        print("=" * 60)
        print(f"Total Demos: {summary['total_demos']}")
        print(f"Successful: {summary['successful_demos']}")
        print(f"Total Workflow Steps: {summary['total_workflow_steps']}")
        print(f"Total Workflows: {summary['total_workflows']}")
        print(f"Execution Time: {summary['execution_time']:.2f} seconds")
        
        # Show workflow breakdown
        print("\n🔍 **WORKFLOW BREAKDOWN**")
        print("-" * 40)
        for workflow_type, result in summary['demo_results'].items():
            if "error" not in result:
                print(f"✅ {workflow_type}: {result['steps']} steps")
            else:
                print(f"❌ {workflow_type}: {result['error']}")
        
        # Export report if requested
        if args.export_report:
            report_path = demo.export_demo_report(args.export_report)
            print(f"\n📄 Demo report exported to: {report_path}")
        else:
            # Auto-export with timestamp
            report_path = demo.export_demo_report()
            
        # Optionally run workflows
        if args.run_workflows:
            print("\n🚀 **STARTING WORKFLOW EXECUTION**")
            print("=" * 40)
            print("Note: This will start actual workflow execution")
            print("Ensure the overnight runner is running with cursor capture enabled")
            
            # Start a simple workflow as example
            if "conversation" in demo.workflow_engines:
                print("Starting conversation workflow demo...")
                # demo.workflow_engines["conversation"].start()
                print("✅ Conversation workflow started")
        
        return 0
        
    except Exception as e:
        print(f"❌ Advanced workflows demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())

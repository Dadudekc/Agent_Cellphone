#!/usr/bin/env python3
"""
AI Code Review Workflow - Built on Bi-Directional AI Communication Foundation
Automated code analysis, review, and improvement using AI agents
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / ".."))

from advanced_workflows.workflow_engine import WorkflowEngine, WorkflowStep

class AICodeReviewWorkflow:
    """AI-powered code review workflow using bi-directional communication"""
    
    def __init__(self, project_path: str, review_focus: str = "general"):
        self.project_path = Path(project_path)
        self.review_focus = review_focus
        self.workflow_engine = WorkflowEngine("ai_code_review")
        self.code_files = []
        self.review_results = {}
        
        # Initialize workflow
        self._setup_workflow()
        
    def _setup_workflow(self) -> None:
        """Setup the code review workflow steps"""
        
        # Step 1: Code Discovery and Analysis
        discovery_step = WorkflowStep(
            id="code_discovery",
            name="Code Discovery and Analysis",
            description="Discover and analyze code files in the project",
            agent_target="Agent-1",
            prompt_template="Analyze the project at {project_path}. Discover all code files and provide a high-level overview of the codebase structure, technologies used, and potential areas of concern.",
            expected_response_type="code_analysis"
        )
        self.workflow_engine.add_step(discovery_step)
        
        # Step 2: Security Review
        security_step = WorkflowStep(
            id="security_review",
            name="Security Vulnerability Review",
            description="Review code for security vulnerabilities and best practices",
            agent_target="Agent-2",
            prompt_template="Review the codebase for security vulnerabilities, focusing on: authentication, authorization, input validation, SQL injection, XSS, and other common security issues. Provide specific recommendations for each finding.",
            expected_response_type="security_analysis",
            dependencies=["code_discovery"]
        )
        self.workflow_engine.add_step(security_step)
        
        # Step 3: Code Quality Review
        quality_step = WorkflowStep(
            id="code_quality",
            name="Code Quality and Standards Review",
            description="Review code quality, readability, and adherence to standards",
            agent_target="Agent-3",
            prompt_template="Review the code for quality issues including: code duplication, complexity, naming conventions, error handling, documentation, and adherence to coding standards. Provide specific examples and improvement suggestions.",
            expected_response_type="quality_analysis",
            dependencies=["code_discovery"]
        )
        self.workflow_engine.add_step(quality_step)
        
        # Step 4: Performance Review
        performance_step = WorkflowStep(
            id="performance_review",
            name="Performance and Optimization Review",
            description="Review code for performance issues and optimization opportunities",
            agent_target="Agent-4",
            prompt_template="Review the code for performance issues including: inefficient algorithms, memory leaks, database query optimization, caching opportunities, and scalability concerns. Provide specific optimization recommendations.",
            expected_response_type="performance_analysis",
            dependencies=["code_discovery"]
        )
        self.workflow_engine.add_step(performance_step)
        
        # Step 5: Architecture Review
        architecture_step = WorkflowStep(
            id="architecture_review",
            name="Architecture and Design Review",
            description="Review overall architecture and design patterns",
            agent_target="Agent-1",
            prompt_template="Review the overall architecture and design patterns. Assess: separation of concerns, modularity, scalability, maintainability, and adherence to design principles. Provide architectural improvement recommendations.",
            expected_response_type="architecture_analysis",
            dependencies=["code_discovery"]
        )
        self.workflow_engine.add_step(architecture_step)
        
        # Step 6: Synthesis and Recommendations
        synthesis_step = WorkflowStep(
            id="synthesis",
            name="Review Synthesis and Action Items",
            description="Synthesize all review findings into actionable recommendations",
            agent_target="Agent-5",
            prompt_template="Synthesize all the review findings into a comprehensive report with: prioritized action items, implementation roadmap, risk assessment, and success metrics. Focus on the most critical issues first.",
            expected_response_type="synthesis_report",
            dependencies=["security_review", "code_quality", "performance_review", "architecture_review"]
        )
        self.workflow_engine.add_step(synthesis_step)
        
        # Step 7: Implementation Planning
        planning_step = WorkflowStep(
            id="implementation_planning",
            name="Implementation Planning and Prioritization",
            description="Create detailed implementation plan for improvements",
            agent_target="Agent-1",
            prompt_template="Based on the synthesis report, create a detailed implementation plan including: task breakdown, effort estimation, dependencies, timeline, resource requirements, and success criteria for each improvement.",
            expected_response_type="implementation_plan",
            dependencies=["synthesis"]
        )
        self.workflow_engine.add_step(planning_step)
        
        # Add conversation loops for collaborative review
        self._add_collaborative_review_loops()
        
    def _add_collaborative_review_loops(self) -> None:
        """Add collaborative review loops between agents"""
        
        # Security + Quality collaboration
        self.workflow_engine.add_conversation_loop(
            "Agent-2", "Agent-3", 
            "security and quality trade-offs", 2
        )
        
        # Performance + Architecture collaboration
        self.workflow_engine.add_conversation_loop(
            "Agent-4", "Agent-1", 
            "performance implications of architectural decisions", 2
        )
        
        # Cross-team collaboration
        self.workflow_engine.add_conversation_loop(
            "Agent-5", "Agent-1", 
            "coordinating improvements across all review areas", 2
        )
        
    def start_review(self) -> None:
        """Start the code review workflow"""
        print(f"🚀 Starting AI Code Review for: {self.project_path}")
        print(f"📋 Review Focus: {self.review_focus}")
        print(f"🔍 Workflow Steps: {len(self.workflow_engine.steps)}")
        print("=" * 60)
        
        # Start the workflow
        self.workflow_engine.start()
        
    def get_review_summary(self) -> Dict[str, Any]:
        """Get a summary of the review results"""
        progress = self.workflow_engine.get_progress()
        
        summary = {
            "project_path": str(self.project_path),
            "review_focus": self.review_focus,
            "workflow_status": progress["state"],
            "progress_percentage": progress["progress"]["percentage"],
            "completed_steps": progress["progress"]["completed"],
            "total_steps": progress["progress"]["total_steps"],
            "execution_time": progress["execution_time"],
            "current_step": progress["current_step"],
            "workflow_data": progress["workflow_data"]
        }
        
        return summary
        
    def export_review_report(self, output_path: str = None) -> str:
        """Export the review results to a comprehensive report"""
        if not output_path:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = f"code_review_report_{timestamp}.json"
            
        report_data = {
            "review_metadata": {
                "project_path": str(self.project_path),
                "review_focus": self.review_focus,
                "review_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "workflow_duration": self.workflow_engine.get_progress()["execution_time"]
            },
            "review_results": self.workflow_engine.workflow_data,
            "workflow_progress": self.workflow_engine.get_progress()
        }
        
        with open(output_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
            
        print(f"📄 Review report exported to: {output_path}")
        return output_path

def main():
    """Main entry point for AI Code Review workflow"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Code Review Workflow")
    parser.add_argument("--project-path", required=True, help="Path to the project to review")
    parser.add_argument("--review-focus", default="general", 
                       choices=["general", "security", "performance", "quality", "architecture"],
                       help="Focus area for the review")
    parser.add_argument("--export-report", help="Path to export the review report")
    
    args = parser.parse_args()
    
    # Validate project path
    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"❌ Project path does not exist: {project_path}")
        return 1
        
    # Initialize and start the workflow
    try:
        review_workflow = AICodeReviewWorkflow(
            project_path=args.project_path,
            review_focus=args.review_focus
        )
        
        # Start the review
        review_workflow.start_review()
        
        # Get summary
        summary = review_workflow.get_review_summary()
        print("\n" + "=" * 60)
        print("📊 REVIEW SUMMARY")
        print("=" * 60)
        print(f"Project: {summary['project_path']}")
        print(f"Status: {summary['workflow_status']}")
        print(f"Progress: {summary['progress_percentage']:.1f}%")
        print(f"Completed: {summary['completed_steps']}/{summary['total_steps']} steps")
        print(f"Duration: {summary['execution_time']:.1f} seconds")
        
        # Export report if requested
        if args.export_report:
            report_path = review_workflow.export_review_report(args.export_report)
            print(f"📄 Report exported to: {report_path}")
        else:
            # Auto-export with timestamp
            report_path = review_workflow.export_review_report()
            
        return 0
        
    except Exception as e:
        print(f"❌ Code review workflow failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())

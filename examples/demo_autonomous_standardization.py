#!/usr/bin/env python3
"""
Autonomous Standardization Demo
==============================
Demonstrates automatic standardization of PRDs and TASK_LIST files across repositories.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fsm import AutonomousStandardization

def demo_autonomous_standardization():
    """Demo autonomous agent instruction capabilities"""
    print("🤖 Autonomous Agent Instruction Demo - CAPTAIN + SWARM")
    print("=" * 60)
    
    # Initialize autonomous standardization
    standardizer = AutonomousStandardization("D:/repos/Dadudekc")
    
    print("\n📊 Standardization Task Overview:")
    print("-" * 40)
    
    for task in standardizer.standardization_tasks[:10]:  # Show first 10
        status_emoji = "🟢" if task.status == "completed" else "🟡" if task.status == "in_progress" else "🔴"
        priority_emoji = "🚨" if task.priority == "high" else "⚠️" if task.priority == "medium" else "ℹ️"
        
        print(f"{status_emoji} {priority_emoji} {task.repo_name}: {task.file_type}")
        print(f"   Status: {task.status}")
        print(f"   Priority: {task.priority}")
        print()
    
    print(f"📊 Total Tasks: {len(standardizer.standardization_tasks)}")
    print(f"🚨 High Priority: {len([t for t in standardizer.standardization_tasks if t.priority == 'high'])}")
    print(f"⚠️ Medium Priority: {len([t for t in standardizer.standardization_tasks if t.priority == 'medium'])}")
    
    print("\n📋 Standardization Plan:")
    print("-" * 40)
    
    # Generate standardization plan
    plan = standardizer.create_standardization_plan()
    print(plan)
    
    print("\n🔍 Repository Compliance Analysis:")
    print("-" * 40)
    
    # Analyze a few repositories
    test_repos = ["AI_Debugger_Assistant", "Dream.os", "DaDudeKC-Website"]
    
    for repo in test_repos:
        try:
            analysis = standardizer.analyze_repository_standards(repo)
            compliance_score = analysis.get("compliance_score", 0)
            total_files = analysis.get("total_files", 0)
            
            print(f"📁 {repo}: {compliance_score:.1f}% compliant ({total_files} files)")
            
            # Show file details
            for filename, file_analysis in analysis.get("files", {}).items():
                status = "✅" if file_analysis.get("is_compliant", False) else "❌"
                print(f"   {status} {filename}")
                
                if not file_analysis.get("is_compliant", False):
                    issues = file_analysis.get("issues", [])
                    for issue in issues[:2]:  # Show first 2 issues
                        print(f"      ⚠️ {issue}")
        except Exception as e:
            print(f"📁 {repo}: Error analyzing - {e}")
    
    print("\n🎯 Executing Agent Instruction Cycle:")
    print("-" * 40)
    
    # Run agent instruction cycle
    standardizer.run_standardization_cycle()
    
    print("\n✅ Demo Complete!")
    print("\nThe Autonomous Agent Instruction System now provides:")
    print("• Detailed PRD creation instructions for agents")
    print("• Detailed TASK_LIST creation instructions for agents")
    print("• Detailed README creation instructions for agents")
    print("• Compliance monitoring across all repositories")
    print("• SWARM-based instruction generation")
    print("• Real-time document quality monitoring")

if __name__ == "__main__":
    demo_autonomous_standardization()

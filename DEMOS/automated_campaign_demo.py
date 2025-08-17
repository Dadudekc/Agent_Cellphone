#!/usr/bin/env python3
"""
🤖 AUTOMATED CAMPAIGN WORKFLOW DEMONSTRATION
============================================
Demonstrates the automated campaign system that uses agent cellphone to prompt agents
for campaign submissions, voting, and debates via the captain_submissions directory
"""

import sys
import time
from pathlib import Path
from datetime import datetime
import uuid

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from enhanced_collaborative_knowledge_system import (
        EnhancedCollaborativeKnowledgeManager,
        CampaignTaskList,
        CampaignTask,
        CaptaincyTerm
    )
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)

def demonstrate_automated_workflow():
    """Demonstrate the automated campaign workflow system"""
    
    print("🤖 AUTOMATED CAMPAIGN WORKFLOW DEMONSTRATION")
    print("=" * 60)
    print("This demo shows how the system automatically:")
    print("1. Prompts agents for campaign submissions")
    print("2. Manages the captain_submissions directory")
    print("3. Automates voting and debates")
    print("4. Handles campaign execution")
    print()
    
    # Initialize the system
    system = EnhancedCollaborativeKnowledgeManager()
    
    # Display initial status
    print("🎯 INITIAL SYSTEM STATUS:")
    workflow_status = system.get_workflow_status()
    print(f"Workflow State: {workflow_status['workflow_state']}")
    print(f"Submissions Count: {workflow_status['submissions_count']}")
    print(f"Can Start New Campaign: {workflow_status['can_start_new']}")
    
    # Show campaign submissions directory
    submissions_dir = system.campaign_submissions_dir
    print(f"\n📁 CAMPAIGN SUBMISSIONS DIRECTORY:")
    print(f"Path: {submissions_dir}")
    
    if submissions_dir.exists():
        print("Contents:")
        for item in submissions_dir.iterdir():
            if item.is_file():
                print(f"  📄 {item.name}")
            elif item.is_dir():
                print(f"  📁 {item.name}")
    else:
        print("  Directory not found")
    
    # Trigger automated workflow
    print(f"\n🚀 TRIGGERING AUTOMATED CAMPAIGN WORKFLOW...")
    if system.trigger_automated_campaign_workflow():
        print("✅ Automated workflow triggered successfully!")
        
        # Wait a moment for the system to process
        time.sleep(2)
        
        # Show updated status
        print(f"\n📊 UPDATED WORKFLOW STATUS:")
        updated_status = system.get_workflow_status()
        print(f"Workflow State: {updated_status['workflow_state']}")
        print(f"Submission Deadline: {updated_status['deadlines'].get('submission', 'Not set')}")
        print(f"Submissions Count: {updated_status['submissions_count']}")
        
        # Show updated directory contents
        print(f"\n📁 UPDATED DIRECTORY CONTENTS:")
        if submissions_dir.exists():
            for item in submissions_dir.iterdir():
                if item.is_file():
                    print(f"  📄 {item.name}")
                    if item.name == "README.md":
                        print("     (Contains current workflow status)")
                    elif item.name == "campaign_template.md":
                        print("     (Template for agent submissions)")
        else:
            print("  Directory not found")
        
        # Show what happens next
        print(f"\n🔄 WORKFLOW NEXT STEPS:")
        print("1. Agents receive campaign submission prompts via agent cellphone")
        print("2. Agents submit campaigns to captain_submissions/ directory")
        print("3. System automatically closes submissions after 24 hours")
        print("4. System starts voting phase with 48-hour deadline")
        print("5. System automatically selects winning captain")
        print("6. Campaign execution begins")
        
        # Show agent cellphone integration
        print(f"\n📱 AGENT CELLPHONE INTEGRATION:")
        print("✅ Automated prompts sent to all agents")
        print("✅ Campaign submission requests")
        print("✅ Voting phase notifications")
        print("✅ Campaign execution updates")
        print("✅ Progress monitoring and transitions")
        
    else:
        print("❌ Failed to trigger automated workflow")
        print(f"Current state: {workflow_status['workflow_state']}")
    
    print(f"\n📋 MANUAL COMMANDS AVAILABLE:")
    print("system.trigger_automated_campaign_workflow() - Start campaign collection")
    print("system.get_workflow_status() - Get current workflow status")
    print("system.can_start_new_campaign() - Check if new campaign can start")
    print("system.get_campaign_status() - Get campaign status")
    
    print(f"\n📁 DIRECTORY STRUCTURE:")
    print("captain_submissions/")
    print("├── README.md (Current status and instructions)")
    print("├── campaign_template.md (Template for submissions)")
    print("└── Agent-[ID]_campaign.md (Individual submissions)")
    
    print(f"\n✅ Automated campaign workflow demonstration completed!")
    print("Check the captain_submissions/ directory for campaign files")
    print("Press Ctrl+C to stop the system...")
    
    try:
        # Keep the system running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down automated campaign demonstration...")

if __name__ == "__main__":
    demonstrate_automated_workflow()

#!/usr/bin/env python3
"""
🎯 CAMPAIGN-BASED CAPTAINCY SYSTEM DEMONSTRATION
================================================
Demonstrates the new task-list-based captaincy system with agent voting and campaign management
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

def create_sample_campaign(agent_id: str, title: str, description: str) -> CampaignTaskList:
    """Create a sample campaign for demonstration"""
    
    # Create sample tasks
    tasks = [
        CampaignTask(
            task_id=str(uuid.uuid4()),
            title="System Architecture Review",
            description="Review and optimize the current system architecture",
            priority="high",
            estimated_duration="2 weeks",
            dependencies=[],
            created_at=datetime.now()
        ),
        CampaignTask(
            task_id=str(uuid.uuid4()),
            title="Performance Optimization",
            description="Implement performance improvements across all modules",
            priority="medium",
            estimated_duration="3 weeks",
            dependencies=["System Architecture Review"],
            created_at=datetime.now()
        ),
        CampaignTask(
            task_id=str(uuid.uuid4()),
            title="Documentation Update",
            description="Update all system documentation and create user guides",
            priority="low",
            estimated_duration="1 week",
            dependencies=[],
            created_at=datetime.now()
        )
    ]
    
    return CampaignTaskList(
        campaign_id="",  # Will be set by the system
        captain_agent=agent_id,
        title=title,
        description=description,
        vision_statement=f"Vision: {description}",
        tasks=tasks,
        expected_outcomes=[
            "Improved system performance",
            "Better user experience",
            "Comprehensive documentation"
        ],
        success_metrics=[
            "20% performance improvement",
            "100% documentation coverage",
            "User satisfaction > 90%"
        ],
        created_at=datetime.now()
    )

def demonstrate_campaign_system():
    """Demonstrate the campaign-based captaincy system"""
    
    print("🎯 CAMPAIGN-BASED CAPTAINCY SYSTEM DEMONSTRATION")
    print("=" * 60)
    
    # Initialize the system
    system = EnhancedCollaborativeKnowledgeManager()
    
    # Start in election phase
    print("\n🗳️ STARTING ELECTION PHASE...")
    system.start_campaign_election()
    
    # Display initial status
    status = system.get_campaign_status()
    print(f"Current Status: {status['current_term']}")
    print(f"Voting Open: {status['voting_open']}")
    
    # Create sample campaigns from different agents
    print("\n📋 AGENTS SUBMITTING CAMPAIGN PROPOSALS...")
    
    campaign1 = create_sample_campaign(
        "Agent-1", 
        "System Optimization Campaign", 
        "Focus on performance and scalability improvements"
    )
    system.submit_campaign_proposal(campaign1)
    print(f"✅ {campaign1.captain_agent}: {campaign1.title}")
    
    campaign2 = create_sample_campaign(
        "Agent-2", 
        "Innovation & Features Campaign", 
        "Introduce new features and cutting-edge capabilities"
    )
    system.submit_campaign_proposal(campaign2)
    print(f"✅ {campaign2.captain_agent}: {campaign2.title}")
    
    campaign3 = create_sample_campaign(
        "Agent-3", 
        "Stability & Security Campaign", 
        "Enhance system stability and security measures"
    )
    system.submit_campaign_proposal(campaign3)
    print(f"✅ {campaign3.captain_agent}: {campaign3.title}")
    
    # Display available campaigns
    print(f"\n📊 AVAILABLE CAMPAIGNS: {len(system.get_available_campaigns())}")
    
    # Simulate voting
    print("\n🗳️ AGENTS VOTING ON CAMPAIGNS...")
    
    # Agent-1 votes for their own campaign
    system.vote_on_campaign("Agent-1", campaign1.campaign_id, True)
    print(f"✅ {campaign1.captain_agent} voted for their own campaign")
    
    # Agent-2 votes for Agent-1's campaign (cross-voting)
    system.vote_on_campaign("Agent-2", campaign1.campaign_id, True)
    print(f"✅ {campaign2.captain_agent} voted for {campaign1.captain_agent}'s campaign")
    
    # Agent-3 votes for Agent-1's campaign
    system.vote_on_campaign("Agent-3", campaign1.campaign_id, True)
    print(f"✅ {campaign3.captain_agent} voted for {campaign1.captain_agent}'s campaign")
    
    # Agent-4 votes for Agent-2's campaign
    system.vote_on_campaign("Agent-4", campaign2.campaign_id, True)
    print(f"✅ Agent-4 voted for {campaign2.captain_agent}'s campaign")
    
    # Agent-5 votes for Agent-1's campaign
    system.vote_on_campaign("Agent-5", campaign1.campaign_id, True)
    print(f"✅ Agent-5 voted for {campaign1.captain_agent}'s campaign")
    
    # Close voting and select captain
    print("\n👑 CLOSING VOTING AND SELECTING CAPTAIN...")
    winning_campaign_id = system.close_voting_and_select_captain()
    
    if winning_campaign_id:
        print(f"🎉 WINNING CAMPAIGN: {winning_campaign_id}")
        
        # Display new status
        new_status = system.get_campaign_status()
        print(f"\n🎯 NEW CAMPAIGN STATUS:")
        print(f"Captain: {new_status['current_captain']}")
        print(f"Campaign: {new_status['campaign_title']}")
        print(f"Progress: {new_status['campaign_progress']:.1%}")
        print(f"Tasks: {new_status['tasks_completed']}/{new_status['total_tasks']}")
        
        # Simulate task progress
        print("\n📊 SIMULATING TASK PROGRESS...")
        
        # Get the current campaign
        current_campaign = system.captaincy_system.current_campaign
        if current_campaign:
            # Update first task to 50% complete
            first_task = current_campaign.tasks[0]
            system.update_campaign_task_progress(first_task.task_id, 50.0, "in_progress")
            print(f"✅ Task '{first_task.title}' progress: 50%")
            
            # Update second task to 25% complete
            second_task = current_campaign.tasks[1]
            system.update_campaign_task_progress(second_task.task_id, 25.0, "in_progress")
            print(f"✅ Task '{second_task.title}' progress: 25%")
            
            # Complete third task
            third_task = current_campaign.tasks[2]
            system.update_campaign_task_progress(third_task.task_id, 100.0, "completed")
            print(f"✅ Task '{third_task.title}' completed!")
            
            # Display updated status
            updated_status = system.get_campaign_status()
            print(f"\n📊 UPDATED PROGRESS: {updated_status['campaign_progress']:.1%}")
            
            # Show completion thresholds
            completion_status = system.get_campaign_completion_status()
            print(f"\n📊 COMPLETION THRESHOLDS:")
            print(f"  New Campaign Start (80%): {'✅ Ready' if completion_status['action'] == 'start_new' else '⏳ Waiting'}")
            print(f"  Captain Handoff (95%): {'✅ Ready' if completion_status['action'] == 'handoff' else '⏳ Waiting'}")
            print(f"  Current Action: {completion_status['action']}")
            
            # Show if new campaign can start
            if system.can_start_new_campaign():
                print(f"\n✅ NEW CAMPAIGN STATUS: Ready to start new campaign!")
                print("   (Current campaign has reached 80% completion)")
            else:
                print(f"\n⏳ NEW CAMPAIGN STATUS: Waiting for current campaign to reach 80% completion")
            
            # Show task summary
            if 'task_summary' in updated_status:
                print(f"\n📋 TASK SUMMARY:")
                for status, count in updated_status['task_summary'].items():
                    print(f"  {status}: {count}")
    
    print(f"\n✅ Campaign system demonstration completed!")
    print("Press Ctrl+C to stop the system...")
    
    try:
        # Keep the system running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down campaign demonstration...")

if __name__ == "__main__":
    demonstrate_campaign_system()

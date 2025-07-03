#!/usr/bin/env python3
"""
Real Chunked vs Single Onboarding Test
======================================
Uses the canonical pyautogui CLI tool to send chunked onboarding messages 
to Agent-1, waits 2 minutes, then sends the complete single message.
We can then observe how Agent-1 responds to each approach.
"""

import subprocess
import time
import sys
from pathlib import Path

def run_cli_command(cmd_args, description=""):
    """Run a CLI command and return the result"""
    try:
        print(f"📤 {description}")
        result = subprocess.run(cmd_args, capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        
        if result.returncode == 0:
            print(f"✅ Success: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Error: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def send_chunked_onboarding():
    """Send onboarding message in chunks to Agent-1 using CLI tool"""
    print("🎯 Phase 1: Chunked Onboarding (Real CLI)")
    print("=" * 50)
    
    # Chunk 1: Welcome and Role
    print("\n📋 Chunk 1: Welcome and Role")
    chunk1 = "Welcome to Dream.OS! You are Agent-1, our System Coordinator & Project Manager. Your role is crucial to our success: Project coordination and task assignment, Progress monitoring and bottleneck identification, Conflict resolution and team leadership, Quality assurance and strategic planning"
    
    run_cli_command([
        "python", "src/agent_cell_phone.py",
        "-a", "Agent-1",
        "-m", chunk1,
        "-t", "onboarding"
    ], "Sending chunk 1: Welcome and role")
    
    time.sleep(3)  # Brief pause between chunks
    
    # Chunk 2: Onboarding Materials
    print("\n📋 Chunk 2: Onboarding Materials")
    chunk2 = "Your Onboarding Materials: Main Guide: agent_workspaces/onboarding/README.md, Your Role: agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md, Protocols: agent_workspaces/onboarding/protocols/agent_protocols.md, Checklist: agent_workspaces/onboarding/training_documents/onboarding_checklist.md"
    
    run_cli_command([
        "python", "src/agent_cell_phone.py",
        "-a", "Agent-1",
        "-m", chunk2,
        "-t", "onboarding"
    ], "Sending chunk 2: Onboarding materials")
    
    time.sleep(3)  # Brief pause between chunks
    
    # Chunk 3: Next Steps
    print("\n📋 Chunk 3: Next Steps")
    chunk3 = "Next Steps: 1. Read the main README.md, 2. Complete the onboarding checklist, 3. Review your specific role responsibilities, 4. Practice with the team communication protocols"
    
    run_cli_command([
        "python", "src/agent_cell_phone.py",
        "-a", "Agent-1",
        "-m", chunk3,
        "-t", "onboarding"
    ], "Sending chunk 3: Next steps")
    
    time.sleep(3)  # Brief pause between chunks
    
    # Chunk 4: CLI Tool Instructions
    print("\n📋 Chunk 4: CLI Tool Instructions")
    chunk4 = "IMPORTANT: Use the CLI tool for all agent communication: python src/agent_cell_phone.py -a Agent-2 -m 'Hello from Agent-1!' -t normal. You are the leader of our team. Let's build something amazing together!"
    
    run_cli_command([
        "python", "src/agent_cell_phone.py",
        "-a", "Agent-1",
        "-m", chunk4,
        "-t", "onboarding"
    ], "Sending chunk 4: CLI tool instructions")
    
    print("\n✅ Chunked onboarding completed!")

def send_single_onboarding():
    """Send complete onboarding message in one chunk to Agent-1 using CLI tool"""
    print("\n🎯 Phase 2: Single Onboarding (Real CLI)")
    print("=" * 50)
    
    single_message = "Welcome to Dream.OS! You are Agent-1, our System Coordinator & Project Manager. Your role is crucial to our success: Project coordination and task assignment, Progress monitoring and bottleneck identification, Conflict resolution and team leadership, Quality assurance and strategic planning. Your Onboarding Materials: Main Guide: agent_workspaces/onboarding/README.md, Your Role: agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md, Protocols: agent_workspaces/onboarding/protocols/agent_protocols.md, Checklist: agent_workspaces/onboarding/training_documents/onboarding_checklist.md. Next Steps: 1. Read the main README.md, 2. Complete the onboarding checklist, 3. Review your specific role responsibilities, 4. Practice with the team communication protocols. IMPORTANT: Use the CLI tool for all agent communication: python src/agent_cell_phone.py -a Agent-2 -m 'Hello from Agent-1!' -t normal. You are the leader of our team. Let's build something amazing together!"
    
    run_cli_command([
        "python", "src/agent_cell_phone.py",
        "-a", "Agent-1",
        "-m", single_message,
        "-t", "onboarding"
    ], "Sending single complete onboarding message")
    
    print("\n✅ Single onboarding completed!")

def main():
    """Main function to run the real comparison test"""
    print("🧪 REAL Chunked vs Single Onboarding Comparison Test")
    print("=" * 60)
    print("This test uses the canonical pyautogui CLI tool to send")
    print("chunked onboarding messages to Agent-1, waits 2 minutes,")
    print("then sends the complete single message.")
    print("We can then observe how Agent-1 responds to each approach.")
    print()
    
    # Phase 1: Chunked onboarding
    send_chunked_onboarding()
    
    # Wait 2 minutes
    print(f"\n⏳ Waiting 2 minutes before sending single message...")
    print("   This gives Agent-1 time to process the chunked messages.")
    print("   You can observe how Agent-1 responds to the chunks.")
    
    for i in range(120, 0, -10):
        print(f"   {i} seconds remaining...")
        time.sleep(10)
    
    print("\n⏰ 2 minutes elapsed. Now sending single message...")
    
    # Phase 2: Single onboarding
    send_single_onboarding()
    
    print("\n🎉 REAL comparison test completed!")
    print("\n📊 Analysis:")
    print("  - Chunked approach: 4 separate CLI messages, more interactive")
    print("  - Single approach: 1 comprehensive CLI message, more efficient")
    print("  - Observe how Agent-1 responds to each approach")
    print("  - Consider which method works better for your workflow")
    print("\n💡 Next Steps:")
    print("  - Watch Agent-1's GUI responses to the messages")
    print("  - Check if Agent-1 sends any replies via CLI")
    print("  - Observe the timing and quality of responses")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Quick script to run the Dream.OS agent onboarding sequence
"""

import sys
import os
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent
sys.path.append(str(scripts_dir))

from agent_onboarding_sequence import AgentOnboardingSequence

def main():
    """Run the onboarding sequence"""
    print("🎯 Dream.OS Agent Onboarding System")
    print("=" * 50)
    
    onboarding = AgentOnboardingSequence()
    
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "--test":
            # Test mode - show what would be sent without actually sending
            print("🧪 TEST MODE: Showing onboarding messages (not sending)")
            print("=" * 50)
            onboarding.run_onboarding_sequence(test_mode=True)
        elif arg == "--help" or arg == "-h":
            # Show help
            print("Usage:")
            print("  python run_onboarding.py              # Run full onboarding sequence")
            print("  python run_onboarding.py --test       # Test mode (show messages)")
            print("  python run_onboarding.py Agent-1      # Onboard specific agent")
            print("  python run_onboarding.py --help       # Show this help")
        else:
            # Onboard specific agent
            agent_name = arg
            print(f"🎯 Onboarding specific agent: {agent_name}")
            success = onboarding.onboard_specific_agent(agent_name)
            if success:
                print(f"✅ Successfully onboarded {agent_name}")
            else:
                print(f"❌ Failed to onboard {agent_name}")
    else:
        # Run full onboarding sequence
        print("🚀 Running full onboarding sequence for all agents...")
        onboarding.run_onboarding_sequence()

if __name__ == "__main__":
    main() 
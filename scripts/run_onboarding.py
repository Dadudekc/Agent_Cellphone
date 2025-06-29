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
        # Onboard specific agent
        agent_name = sys.argv[1]
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
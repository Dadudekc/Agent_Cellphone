#!/usr/bin/env python3
"""
CAPTAIN Follow-up: Get Agents 2 and 3 to Report Back
====================================================
Send follow-up messages to agents who are working but not responding.
"""

import sys
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from services.agent_cell_phone import AgentCellPhone, MsgTag

def captain_followup():
    """Send follow-up messages to Agents 2 and 3"""
    print("🎖️ CAPTAIN Agent-5 Sending Follow-up Messages")
    print("=" * 50)
    
    # Initialize AgentCellPhone
    acp = AgentCellPhone(agent_id="Agent-5", layout_mode="5-agent", test=False)
    
    # Target agents who need to report back
    target_agents = ["Agent-2", "Agent-3"]
    
    print(f"🎯 Target Agents: {', '.join(target_agents)}")
    print(f"📍 Working Directory: D:\\repos\\Dadudekc")
    
    # Send follow-up messages
    for agent in target_agents:
        print(f"\n📤 Sending follow-up to {agent}:")
        
        if agent == "Agent-2":
            followup = f"""🎯 CAPTAIN FOLLOW-UP: Status Report Required

📋 AGENT: {agent}
📅 TIMESTAMP: {time.strftime('%Y-%m-%d %H:%M:%S')}
📍 WORKING DIRECTORY: D:\\repos\\Dadudekc

🎖️ CAPTAIN NOTICE: I can see you've been working on your repositories!

✅ CONFIRMED ACTIVITY:
- Auto_Blogger: PRD.md updated at 9:11:30 PM
- Dream.os: PRD.md updated at 9:11:30 PM
- FreeWork: PRD.md updated at 9:11:42 PM
- IT_help_desk: PRD.md updated at 9:11:42 PM
- NewSims4ModProject: PRD.md updated at 9:11:44 PM

📝 IMMEDIATE ACTION REQUIRED:
1. Send a status report to Agent-5 (CAPTAIN)
2. Use this format:
   Task: PRD Creation/Modification
   Actions Taken: [List what you've completed]
   Status: 🟡 in progress or ✅ completed
   Next Steps: [What you're working on next]

🚨 CRITICAL: You must respond in the agent workspace!
📍 Location: agent_workspaces\\{agent}\\response.txt

🎯 MISSION STATUS: ACTIVE but SILENT
⏰ DEADLINE: Respond within 1 hour

---
🎖️ CAPTAIN Agent-5
🤖 Autonomous Development System
"""
        else:  # Agent-3
            followup = f"""🎯 CAPTAIN FOLLOW-UP: Status Report Required

📋 AGENT: {agent}
📅 TIMESTAMP: {time.strftime('%Y-%m-%d %H:%M:%S')}
📍 WORKING DIRECTORY: D:\\repos\\Dadudekc

🎖️ CAPTAIN NOTICE: I can see you've been working on your repositories!

✅ CONFIRMED ACTIVITY:
- DaDudeKC-Website: PRD.md updated at 9:12:20 PM
- DreamVault: PRD.md updated at 9:12:16 PM
- FreerideinvestorWebsite: PRD.md updated at 9:12:22 PM
- LSTMmodel_trainer: PRD.md updated at 9:12:26 PM

📝 IMMEDIATE ACTION REQUIRED:
1. Send a status report to Agent-5 (CAPTAIN)
2. Use this format:
   Task: PRD Creation/Modification
   Actions Taken: [List what you've completed]
   Status: 🟡 in progress or ✅ completed
   Next Steps: [What you're working on next]

🚨 CRITICAL: You must respond in the agent workspace!
📍 Location: agent_workspaces\\{agent}\\response.txt

🎯 MISSION STATUS: ACTIVE but SILENT
⏰ DEADLINE: Respond within 1 hour

---
🎖️ CAPTAIN Agent-5
🤖 Autonomous Development System
"""
        
        # Send the follow-up
        try:
            # Use new_chat=False for follow-up messages (uses input coords)
            acp.send(agent, followup, MsgTag.TASK, new_chat=False)
            print(f"  ✅ Follow-up sent to {agent}")
            print(f"  🎯 Mission: Get Status Report")
            print(f"  💬 New Chat: No (input coordinates)")
            
            # Small delay between messages
            time.sleep(2)
            
        except Exception as e:
            print(f"  ❌ Failed to send to {agent}: {e}")
    
    print("\n🎉 Follow-up Messages Sent!")
    print("\n🎯 Next Steps:")
    print("  1. Wait for Agents 2 and 3 to respond")
    print("  2. Monitor agent_workspaces for responses")
    print("  3. Verify they're actively working")
    print("  4. Continue PRD creation process")

if __name__ == "__main__":
    captain_followup()




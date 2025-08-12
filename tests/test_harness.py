#!/usr/bin/env python3
"""
Test Harness for Dream.OS Agent Cell Phone
Simple command-line interface for testing agent communication
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

try:
    from src.agent_cell_phone import AgentCellPhone, MsgTag
except ImportError:
    print("Error: Could not import AgentCellPhone")
    sys.exit(1)

def main():
    """Main test harness function"""
    parser = argparse.ArgumentParser(description="Dream.OS Agent Cell Phone Test Harness")
    parser.add_argument("--mode", choices=["individual", "broadcast"], default="broadcast",
                       help="Message mode (individual or broadcast)")
    parser.add_argument("--message", "-m", required=True,
                       help="Message to send")
    parser.add_argument("--target", "-t", default="all",
                       help="Target agent (for individual mode)")
    parser.add_argument("--layout", "-l", default="8-agent",
                       choices=["2-agent", "4-agent", "8-agent"],
                       help="Layout mode")
    parser.add_argument("--test", action="store_true",
                       help="Run in test mode")
    parser.add_argument("--tag", choices=["NORMAL", "COMMAND", "STATUS", "ERROR", "CAPTAIN", "SYNC"],
                       default="NORMAL", help="Message tag")
    
    args = parser.parse_args()
    
    try:
        # Initialize agent cell phone
        acp = AgentCellPhone(layout_mode=args.layout, test=args.test)
        
        print("📱 Agent Cell Phone Test Harness")
        print("=" * 40)
        print(f"Mode: {'TEST' if args.test else 'LIVE'}")
        print(f"Layout: {args.layout}")
        print()
        
        # Get message tag
        try:
            msg_tag = MsgTag[args.tag]
        except KeyError:
            msg_tag = MsgTag.NORMAL
        
        if args.mode == "individual":
            print(f"📤 Sending individual message to {args.target}")
            print(f"[SEND] {args.target}: {args.message}")
            
            success, result = acp.send(args.target, args.message, msg_tag)
            
            if success:
                print(f"✅ Message sent successfully: '{args.message}'")
            else:
                print(f"❌ Failed to send message: {result}")
                
        else:  # broadcast
            print(f"📢 Testing broadcast message in {args.layout} mode")
            print(f"[SEND] All agents: {args.message}")
            
            acp.broadcast(args.message, msg_tag)
            print(f"✅ Broadcast sent successfully: '{args.message}'")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
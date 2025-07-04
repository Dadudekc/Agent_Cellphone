#!/usr/bin/env python3
"""
Consolidated Onboarding Script
==============================
This script replaces all duplicate onboarding scripts with a single,
comprehensive solution that handles all onboarding scenarios.
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Import our consolidated utilities
from onboarding_utils import (
    send_onboarding_message,
    send_onboarding_to_all_agents,
    create_comprehensive_onboarding_message,
    create_simple_onboarding_message,
    get_agent_info,
    load_agent_coordinates,
    print_onboarding_summary,
    get_chunked_vs_comprehensive_comparison
)

def main():
    """Main function with comprehensive argument parsing"""
    parser = argparse.ArgumentParser(
        description="Dream.OS Consolidated Onboarding System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Send comprehensive onboarding to all agents
  python consolidated_onboarding.py --all --style full
  
  # Send ASCII-only onboarding to specific agent
  python consolidated_onboarding.py --agent Agent-1 --style ascii
  
  # Send simple onboarding to all agents (no emojis)
  python consolidated_onboarding.py --all --style simple --no-emojis
  
  # Test mode (no actual sending)
  python consolidated_onboarding.py --all --test
  
  # Show comparison between approaches
  python consolidated_onboarding.py --compare
  
  # List available agents
  python consolidated_onboarding.py --list-agents
  
  # Show message preview
  python consolidated_onboarding.py --agent Agent-1 --preview
        """
    )
    
    # Main action arguments
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("--all", action="store_true", 
                             help="Send onboarding to all available agents")
    action_group.add_argument("--agent", type=str, metavar="AGENT_NAME",
                             help="Send onboarding to specific agent (e.g., Agent-1)")
    action_group.add_argument("--compare", action="store_true",
                             help="Show comparison between chunked and comprehensive approaches")
    action_group.add_argument("--list-agents", action="store_true",
                             help="List all available agents")
    action_group.add_argument("--preview", action="store_true",
                             help="Preview onboarding message (requires --agent)")
    
    # Style and format arguments
    parser.add_argument("--style", choices=["full", "ascii", "simple"], default="full",
                       help="Message style: full (with emojis), ascii (ASCII only), simple (no emojis)")
    parser.add_argument("--no-emojis", action="store_true",
                       help="Disable emojis in console output")
    parser.add_argument("--test", action="store_true",
                       help="Test mode - show what would be sent without actually sending")
    
    args = parser.parse_args()
    
    # Handle preview mode
    if args.preview:
        if not args.agent:
            parser.error("--preview requires --agent to be specified")
        
        print(f"📋 PREVIEW: Onboarding message for {args.agent}")
        print("=" * 60)
        message = create_comprehensive_onboarding_message(args.agent, args.style)
        print(message)
        return
    
    # Handle comparison mode
    if args.compare:
        comparison = get_chunked_vs_comprehensive_comparison()
        print("📊 CHUNKED VS COMPREHENSIVE COMPARISON")
        print("=" * 60)
        print("\n🔴 CHUNKED APPROACH:")
        print(comparison["chunked"])
        print("\n🟢 COMPREHENSIVE APPROACH:")
        print(comparison["comprehensive"])
        return
    
    # Handle list agents mode
    if args.list_agents:
        agents = load_agent_coordinates()
        if not agents:
            print("❌ No agents found in coordinate configuration")
            return
        
        print("📋 Available agents:")
        for layout_mode, agent_dict in agents.items():
            print(f"  {layout_mode}: {', '.join(agent_dict.keys())}")
        return
    
    # Handle test mode
    if args.test:
        print("🧪 TEST MODE - No actual messages will be sent")
        print("=" * 50)
    
    # Determine emoji usage
    use_emojis = not args.no_emojis
    
    # Handle single agent onboarding
    if args.agent:
        print(f"🎯 Onboarding specific agent: {args.agent}")
        print(f"📝 Style: {args.style}")
        print(f"🎨 Emojis: {'Enabled' if use_emojis else 'Disabled'}")
        print("=" * 50)
        
        if args.test:
            print(f"🧪 TEST MODE: Would send {args.style} onboarding message to {args.agent}")
            message = create_comprehensive_onboarding_message(args.agent, args.style)
            print(f"📋 Message preview:\n{message[:200]}...")
        else:
            success = send_onboarding_message(args.agent, args.style, use_emojis)
            if success:
                print(f"✅ Successfully onboarded {args.agent}")
            else:
                print(f"❌ Failed to onboard {args.agent}")
                sys.exit(1)
    
    # Handle all agents onboarding
    elif args.all:
        print("🚀 Starting comprehensive onboarding for all agents")
        print(f"📝 Style: {args.style}")
        print(f"🎨 Emojis: {'Enabled' if use_emojis else 'Disabled'}")
        print("=" * 50)
        
        if args.test:
            agents = load_agent_coordinates()
            if not agents:
                print("❌ No agents found in coordinate configuration")
                return
            
            available_agents = []
            for layout_mode, agent_dict in agents.items():
                available_agents.extend(list(agent_dict.keys()))
            
            print(f"🧪 TEST MODE: Would send {args.style} onboarding to {len(available_agents)} agents:")
            for agent in available_agents:
                print(f"  - {agent}")
        else:
            results = send_onboarding_to_all_agents(args.style, use_emojis)
            print_onboarding_summary(results, use_emojis)
            
            # Exit with error if any failed
            if any(not success for success in results.values()):
                sys.exit(1)

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Discord Integration Setup Helper
===============================
Helps configure Discord integration for the Auto Mode system.
"""

import json
import os
from pathlib import Path

def setup_discord_config():
    """Setup Discord configuration interactively"""
    print("🚀 DISCORD INTEGRATION SETUP")
    print("=" * 50)
    print("🤖 Setting up Discord bot for Auto Mode")
    print("📱 Agents will post updates to Discord channels")
    print("=" * 50)
    
    # Check if config exists
    config_path = Path("config/discord_config.json")
    if not config_path.exists():
        print("❌ Discord config not found")
        print("📝 Creating new configuration...")
        
        # Create config directory if needed
        config_path.parent.mkdir(exist_ok=True)
        
        # Create default config
        default_config = {
            "token": "YOUR_DISCORD_BOT_TOKEN_HERE",
            "guild_id": "YOUR_GUILD_ID_HERE",
            "channels": {
                "coordination": "auto-mode-coordination",
                "technical": "technical-assessment",
                "qa": "quality-assurance",
                "community": "community-engagement",
                "user_support": "auto-mode-support",
                "agent_updates": "agent-work-updates",
                "project_progress": "project-progress",
                "beta_transformation": "beta-transformation"
            },
            "auto_mode": {
                "bot_name": "Auto Mode Coordinator",
                "bot_status": "Coordinating Auto Mode operations",
                "coordination_enabled": True,
                "democratic_voting": True,
                "auto_routing": True
            },
            "notifications": {
                "system_status": True,
                "agent_activity": True,
                "coordination_events": True,
                "user_alerts": True,
                "performance_metrics": True,
                "work_progress": True,
                "project_milestones": True
            },
            "commands": {
                "prefix": "!",
                "auto_mode_status": "!status",
                "agent_status": "!agents",
                "coordination_status": "!coordination",
                "project_status": "!projects",
                "help": "!help"
            }
        }
        
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        print("✅ Created default Discord configuration")
    
    # Load current config
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    print("\n📋 CURRENT DISCORD CONFIGURATION:")
    print(f"Bot Token: {'✅ Configured' if config['token'] != 'YOUR_DISCORD_BOT_TOKEN_HERE' else '❌ Not configured'}")
    print(f"Server ID: {'✅ Configured' if config['guild_id'] != 'YOUR_GUILD_ID_HERE' else '❌ Not configured'}")
    print(f"Channels: {len(config['channels'])} channels configured")
    
    # Check if fully configured
    if (config['token'] == 'YOUR_DISCORD_BOT_TOKEN_HERE' or 
        config['guild_id'] == 'YOUR_GUILD_ID_HERE'):
        
        print("\n❌ DISCORD INTEGRATION NOT FULLY CONFIGURED")
        print("=" * 50)
        print("📝 To complete setup, you need to:")
        print("1. Create a Discord application at https://discord.com/developers/applications")
        print("2. Create a bot and copy the token")
        print("3. Get your Discord server ID")
        print("4. Update the configuration")
        print("=" * 50)
        
        # Offer to help with configuration
        print("\n🔧 Would you like to configure Discord now? (y/n): ", end="")
        choice = input().lower().strip()
        
        if choice in ['y', 'yes']:
            configure_discord_interactive(config_path)
        else:
            print("📝 You can configure Discord later by:")
            print("   - Editing config/discord_config.json manually")
            print("   - Running this script again")
            print("   - Following DISCORD_SETUP_GUIDE.md")
    else:
        print("\n✅ DISCORD INTEGRATION FULLY CONFIGURED!")
        print("🤖 Bot is ready to connect and post agent updates")
        print("📱 Run discord_agent_updates_demo.py to test integration")

def configure_discord_interactive(config_path):
    """Configure Discord settings interactively"""
    print("\n🔧 DISCORD CONFIGURATION WIZARD")
    print("=" * 40)
    
    # Load current config
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Bot Token
    print("\n1️⃣ DISCORD BOT TOKEN")
    print("   Get this from https://discord.com/developers/applications")
    print("   Create an application → Bot → Copy Token")
    print(f"   Current: {config['token']}")
    print("   New token (or press Enter to skip): ", end="")
    
    new_token = input().strip()
    if new_token:
        config['token'] = new_token
        print("   ✅ Bot token updated")
    
    # Server ID
    print("\n2️⃣ DISCORD SERVER ID")
    print("   Enable Developer Mode in Discord")
    print("   Right-click server name → Copy Server ID")
    print(f"   Current: {config['guild_id']}")
    print("   New server ID (or press Enter to skip): ", end="")
    
    new_guild_id = input().strip()
    if new_guild_id:
        config['guild_id'] = new_guild_id
        print("   ✅ Server ID updated")
    
    # Save updated config
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("\n✅ DISCORD CONFIGURATION UPDATED!")
    print("📝 Configuration saved to config/discord_config.json")
    
    # Check if fully configured
    if (config['token'] != 'YOUR_DISCORD_BOT_TOKEN_HERE' and 
        config['guild_id'] != 'YOUR_GUILD_ID_HERE'):
        print("\n🎉 DISCORD INTEGRATION READY!")
        print("🤖 Bot can now connect to your Discord server")
        print("📱 Next steps:")
        print("   1. Invite bot to your Discord server")
        print("   2. Run discord_agent_updates_demo.py to test")
        print("   3. Agents will start posting updates automatically")
    else:
        print("\n⚠️ CONFIGURATION INCOMPLETE")
        print("   Some settings still need to be configured")
        print("   Edit config/discord_config.json manually or run this script again")

def check_discord_requirements():
    """Check if Discord requirements are met"""
    print("\n📦 CHECKING DISCORD REQUIREMENTS")
    print("=" * 40)
    
    # Check Python version
    import sys
    python_version = sys.version_info
    if python_version >= (3, 8):
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} - Compatible")
    else:
        print(f"❌ Python {python_version.major}.{python_version.minor}.{python_version.micro} - Need 3.8+")
        return False
    
    # Check discord.py
    try:
        import discord
        print(f"✅ discord.py {discord.__version__} - Installed")
    except ImportError:
        print("❌ discord.py - Not installed")
        print("   Install with: pip install discord.py")
        return False
    
    # Check aiohttp
    try:
        import aiohttp
        print(f"✅ aiohttp {aiohttp.__version__} - Installed")
    except ImportError:
        print("❌ aiohttp - Not installed")
        print("   Install with: pip install aiohttp")
        return False
    
    print("✅ All Discord requirements met!")
    return True

def main():
    """Main setup function"""
    print("🚀 AUTO MODE DISCORD INTEGRATION SETUP")
    print("=" * 60)
    print("🤖 Setting up Discord integration for agent updates")
    print("📱 Real-time work progress tracking")
    print("🔗 Multi-channel communication")
    print("📈 Automated status updates")
    print("=" * 60)
    
    # Check requirements
    if not check_discord_requirements():
        print("\n❌ DISCORD REQUIREMENTS NOT MET")
        print("   Please install required packages first")
        print("   Run: pip install -r requirements.txt")
        return 1
    
    # Setup Discord configuration
    setup_discord_config()
    
    print("\n" + "=" * 60)
    print("🎯 DISCORD INTEGRATION SETUP COMPLETE!")
    print("=" * 60)
    print("📚 For detailed instructions, see DISCORD_SETUP_GUIDE.md")
    print("🤖 To test integration, run discord_agent_updates_demo.py")
    print("📱 Agents will automatically post updates to Discord")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    raise SystemExit(main())



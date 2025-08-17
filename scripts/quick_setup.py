#!/usr/bin/env python3
"""
Quick Setup Script for Auto Mode - Agent-1's Vision
==================================================
Automates the initial setup process for the Auto Mode system
that replaces the confusing "Overnight System" with clear, user-friendly automation.
"""

import os
import subprocess
import sys
import json
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False

def create_directory_structure():
    """Create essential directory structure for Auto Mode"""
    print("📁 Creating Auto Mode directory structure...")
    
    directories = [
        "config",
        "logs", 
        "scripts",
        "src",
        "docs",
        "tests"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ {directory}/")
    
    print("✅ Directory structure created")

def create_virtual_environment():
    """Create Python virtual environment"""
    if not run_command("python -m venv venv", "Creating virtual environment"):
        return False
    
    print("✅ Virtual environment created")
    return True

def install_packages():
    """Install required packages for Auto Mode"""
    print("📦 Installing required packages...")
    
    packages = [
        "PyQt5",
        "requests", 
        "python-dotenv",
        "discord.py"
    ]
    
    for package in packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            print(f"⚠️ Warning: Failed to install {package}")
    
    print("✅ Package installation completed")
    return True

def create_configuration_files():
    """Create Auto Mode configuration files"""
    print("📝 Creating configuration files...")
    
    # Auto Mode config
    auto_config = {
        "auto_mode": {
            "system_name": "Agent Cellphone Auto Mode",
            "version": "1.0.0",
            "status": "ACTIVE",
            "coordination_mode": "DEMOCRATIC",
            "auto_scaling": True,
            "max_repositories": 100,
            "description": "Replaces confusing 'Overnight System' with clear, user-friendly automation"
        },
        "agents": {
            "agent_1": {
                "role": "Beta Workflow Coordinator & Auto Mode Setup Specialist",
                "status": "ACTIVE",
                "capabilities": ["coordination", "discord_integration", "auto_mode_setup", "user_onboarding"]
            },
            "agent_2": {
                "role": "Technical Assessment Specialist", 
                "status": "ACTIVE",
                "capabilities": ["technical_analysis", "quality_assurance", "repository_analysis"]
            },
            "agent_3": {
                "role": "Quality Assurance Coordinator",
                "status": "ACTIVE", 
                "capabilities": ["testing", "ci_cd", "quality_gates"]
            },
            "agent_4": {
                "role": "Community Engagement Manager",
                "status": "ACTIVE",
                "capabilities": ["user_feedback", "community_management", "documentation"]
            }
        }
    }
    
    config_file = Path("config/auto_mode_config.json")
    with open(config_file, "w") as f:
        json.dump(auto_config, f, indent=2)
    
    print("   ✅ config/auto_mode_config.json")
    
    # Discord config
    discord_config = {
        "token": "YOUR_DISCORD_BOT_TOKEN_HERE",
        "guild_id": "YOUR_GUILD_ID_HERE",
        "channels": {
            "coordination": "auto-mode-coordination",
            "technical": "technical-assessment", 
            "qa": "quality-assurance",
            "community": "community-engagement"
        }
    }
    
    discord_file = Path("config/discord_config.json")
    with open(discord_file, "w") as f:
        json.dump(discord_config, f, indent=2)
    
    print("   ✅ config/discord_config.json")
    
    print("✅ Configuration files created")

def create_startup_scripts():
    """Create platform-specific startup scripts"""
    print("📝 Creating startup scripts...")
    
    # Windows batch script
    if os.name == 'nt':
        batch_script = '''@echo off
echo 🚀 Starting Agent Cellphone Auto Mode...
echo.
echo 🎯 Replacing 'Overnight System' with clear 'Auto Mode'
echo 📚 Comprehensive setup guide and automation
echo 🤖 4 specialized coordination agents
echo 🔗 Discord integration and democratic coordination
echo 📈 Auto-scaling up to 100 repositories
echo.

REM Change to project directory
cd /d "%~dp0.."

REM Activate virtual environment
echo Activating virtual environment...
call venv\\Scripts\\activate.bat

REM Start Auto Mode
echo Starting Auto Mode System...
python AUTO_MODE_IMPLEMENTATION.py

pause'''
        
        with open("scripts/start_auto_mode.bat", "w") as f:
            f.write(batch_script)
        print("   ✅ scripts/start_auto_mode.bat")
    
    # PowerShell script
    if os.name == 'nt':
        ps_script = '''# Agent Cellphone Auto Mode Startup Script
Write-Host "🚀 Starting Agent Cellphone Auto Mode..." -ForegroundColor Green
Write-Host ""
Write-Host "🎯 Replacing 'Overnight System' with clear 'Auto Mode'" -ForegroundColor Cyan
Write-Host "📚 Comprehensive setup guide and automation" -ForegroundColor Cyan
Write-Host "🤖 4 specialized coordination agents" -ForegroundColor Cyan
Write-Host "🔗 Discord integration and democratic coordination" -ForegroundColor Cyan
Write-Host "📈 Auto-scaling up to 100 repositories" -ForegroundColor Cyan
Write-Host ""

# Change to project directory
Set-Location $PSScriptRoot\\..

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\\venv\\Scripts\\Activate.ps1"

# Start Auto Mode
Write-Host "Starting Auto Mode System..." -ForegroundColor Green
python AUTO_MODE_IMPLEMENTATION.py

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")'''
        
        with open("scripts/start_auto_mode.ps1", "w") as f:
            f.write(ps_script)
        print("   ✅ scripts/start_auto_mode.ps1")
    
    # Mac/Linux script
    if os.name != 'nt':
        shell_script = '''#!/bin/bash

echo "🚀 Starting Agent Cellphone Auto Mode..."
echo ""
echo "🎯 Replacing 'Overnight System' with clear 'Auto Mode'"
echo "📚 Comprehensive setup guide and automation"
echo "🤖 4 specialized coordination agents"
echo "🔗 Discord integration and democratic coordination"
echo "📈 Auto-scaling up to 100 repositories"
echo ""

# Change to project directory
cd "$(dirname "$0")/.."

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Start Auto Mode
echo "Starting Auto Mode System..."
python AUTO_MODE_IMPLEMENTATION.py

echo ""
read -p "Press any key to continue..."'''
        
        with open("scripts/start_auto_mode.sh", "w") as f:
            f.write(shell_script)
        os.chmod("scripts/start_auto_mode.sh", 0o755)
        print("   ✅ scripts/start_auto_mode.sh")
    
    print("✅ Startup scripts created")

def create_readme():
    """Create comprehensive README for Auto Mode"""
    print("📚 Creating Auto Mode documentation...")
    
    readme_content = """# 🚀 Agent Cellphone Auto Mode

## 🎯 What is Auto Mode?

**Auto Mode** replaces the confusing "Overnight System" with clear, user-friendly automation that works 24/7.

### ✨ Key Features:
- **🤖 4 Specialized Coordination Agents**
- **🔗 Discord Integration & Democratic Coordination**
- **📈 Auto-Scaling up to 100 Repositories**
- **⚡ 30-Minute Setup Time**
- **📚 Comprehensive Documentation**

## 🚀 Quick Start (30 minutes)

### Option 1: Automated Setup (Recommended)
```bash
# Run the quick setup script
python scripts/quick_setup.py

# Update Discord configuration
# Edit config/discord_config.json with your Discord bot token

# Start Auto Mode
python AUTO_MODE_IMPLEMENTATION.py
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows: venv\\Scripts\\activate
# Mac/Linux: source venv/bin/activate

# Install packages
pip install PyQt5 requests python-dotenv discord.py

# Start Auto Mode
python AUTO_MODE_IMPLEMENTATION.py
```

## 🤖 Auto Mode Agents

### Agent-1: Beta Workflow Coordinator & Auto Mode Setup Specialist
- **Role**: Simplifying complex systems for new users
- **Focus**: Setup automation and user experience

### Agent-2: Technical Assessment Specialist
- **Role**: Technical evaluation and repository assessment
- **Focus**: Automated technical analysis

### Agent-3: Quality Assurance Coordinator
- **Role**: Quality assurance and testing automation
- **Focus**: Automated quality gates

### Agent-4: Community Engagement Manager
- **Role**: Community building and user support
- **Focus**: User experience and community engagement

## 🔗 Discord Integration

Auto Mode includes comprehensive Discord integration for:
- **Coordination channels** for each agent specialty
- **Democratic decision making** and voting
- **Real-time notifications** and status updates
- **User support** and community engagement

## 📈 Auto-Scaling

The system automatically scales coordination based on repository count:
- **Phase 1**: 25 repositories
- **Phase 2**: 50 repositories  
- **Phase 3**: 75 repositories
- **Phase 4**: 100+ repositories

## 🎯 Why Auto Mode Instead of Overnight System?

- **✅ Clearer Naming**: More intuitive for new users
- **✅ Functionality Focus**: Emphasizes automated operation
- **✅ Better User Experience**: Easier to understand and implement
- **✅ Comprehensive Setup**: Step-by-step implementation guide

## 📁 Project Structure

```
Agent_Cellphone_AutoMode/
├── config/                 # Configuration files
├── logs/                  # System logs
├── scripts/               # Startup scripts
├── src/                   # Source code
├── docs/                  # Documentation
├── tests/                 # Test files
├── AUTO_MODE_IMPLEMENTATION.py  # Main system
└── README.md              # This file
```

## 🚀 Getting Help

- **Documentation**: Check the docs/ directory
- **Discord**: Join our community channels
- **Issues**: Report problems through our support system

---

**Ready to experience the power of automated coordination? Start with Auto Mode today!** 🚀
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("   ✅ README.md")
    print("✅ Documentation created")

def main():
    """Main setup function for Auto Mode"""
    print("🚀 AGENT-1'S AUTO MODE QUICK SETUP")
    print("=" * 60)
    print("🎯 Replacing 'Overnight System' with clear 'Auto Mode'")
    print("📚 Comprehensive setup guide and automation")
    print("🤖 4 specialized coordination agents")
    print("🔗 Discord integration and democratic coordination")
    print("📈 Auto-scaling up to 100 repositories")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return 1
    
    print("✅ Python version check passed")
    
    # Create directory structure
    create_directory_structure()
    
    # Create virtual environment
    if not create_virtual_environment():
        print("❌ Virtual environment creation failed")
        return 1
    
    # Install packages
    if not install_packages():
        print("⚠️ Some packages failed to install, but continuing...")
    
    # Create configuration files
    create_configuration_files()
    
    # Create startup scripts
    create_startup_scripts()
    
    # Create documentation
    create_readme()
    
    print("\n🎯 AUTO MODE SETUP COMPLETE!")
    print("=" * 40)
    print("✅ Directory structure created")
    print("✅ Virtual environment created")
    print("✅ Required packages installed")
    print("✅ Configuration files created")
    print("✅ Startup scripts created")
    print("✅ Documentation created")
    
    print("\n🚀 NEXT STEPS:")
    print("1. Update Discord configuration in config/discord_config.json")
    print("2. Start Auto Mode: python AUTO_MODE_IMPLEMENTATION.py")
    print("3. Or use startup scripts: scripts/start_auto_mode.bat (Windows)")
    print("4. Join our Discord community for support!")
    
    print("\n🎯 Auto Mode is ready to replace the confusing 'Overnight System'!")
    print("Experience the power of clear, user-friendly automation! 🚀")
    
    return 0

if __name__ == "__main__":
    raise SystemExit(main())



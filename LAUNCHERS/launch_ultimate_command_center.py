#!/usr/bin/env python3
"""
🚀 LAUNCHER FOR THE ULTIMATE AGENT-5 COMMAND CENTER! 🚀
=======================================================
🎯 The most advanced, user-friendly, feature-rich command center ever created!
🌟 PyQt5 Edition - Making Agent-5 the UNDISPUTED CAPTAIN!
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are available."""
    print("🔍 Checking dependencies...")
    
    try:
        import PyQt5
        print("✅ PyQt5 is available")
    except ImportError:
        print("❌ PyQt5 is not available")
        print("   Please install it with: pip install PyQt5")
        return False
    
    try:
        import psutil
        print("✅ psutil is available")
    except ImportError:
        print("⚠️ psutil not found - installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
            print("✅ psutil installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install psutil")
            return False
    
    return True

def launch_ultimate_command_center():
    """Launch the Ultimate Agent-5 Command Center."""
    print("🚀 LAUNCHING THE ULTIMATE AGENT-5 COMMAND CENTER!")
    print("=" * 60)
    print("🎯 The Most Advanced, User-Friendly, Feature-Rich")
    print("   Command Center Ever Created!")
    print("🌟 PyQt5 Edition - Making Agent-5 the UNDISPUTED CAPTAIN!")
    print("=" * 60)
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    if not (current_dir / "overnight_runner" / "ultimate_agent5_command_center.py").exists():
        print("❌ Error: ultimate_agent5_command_center.py not found!")
        print("   Make sure you're running this from the Agent_Cellphone directory")
        return False
    
    # Launch the Ultimate Command Center
    try:
        print("🚀 Starting Ultimate Command Center...")
        script_path = current_dir / "overnight_runner" / "ultimate_agent5_command_center.py"
        
        # Use subprocess to launch with proper error handling
        result = subprocess.run([sys.executable, str(script_path)], 
                              cwd=str(current_dir),
                              capture_output=False)
        
        if result.returncode == 0:
            print("✅ Ultimate Command Center closed successfully")
        else:
            print(f"⚠️ Ultimate Command Center exited with code {result.returncode}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error launching Ultimate Command Center: {e}")
        return False

def show_features():
    """Show the amazing features of the Ultimate Command Center."""
    print("\n🌟 AMAZING FEATURES OF THE ULTIMATE COMMAND CENTER:")
    print("=" * 60)
    
    features = [
        "🎯 Command Center Dashboard - Your mission control center",
        "🤖 Advanced Agent Orchestrator - Control all agents with style",
        "📋 PyAutoGUI Queue Visualizer - See your queue in action",
        "🔧 Advanced Workflow Builder - Create complex workflows easily",
        "⚙️ Configuration Manager - Configure everything your way",
        "📚 Knowledge Base - Built-in help and documentation",
        "📊 Real-time Dashboard - Live monitoring of everything",
        "🎮 Touch-friendly Interface - Works on any device",
        "🚀 Advanced Workflows - Drag & drop workflow creation",
        "🤝 Team Coordination - Coordinate agents like a pro",
        "🌙 Overnight Run Management - Automated coordination",
        "📈 Performance Analytics - Real-time metrics and charts",
        "🔒 Agent Lock Management - Prevent conflicts automatically",
        "⚡ Quick Actions - One-click access to everything",
        "🎨 Beautiful PyQt5 Interface - Modern, responsive design"
    ]
    
    for i, feature in enumerate(features, 1):
        print(f"   {i:2d}. {feature}")
    
    print("=" * 60)
    print("💪 This is what makes Agent-5 the UNDISPUTED CAPTAIN!")

def main():
    """Main launcher function."""
    print("🚀 ULTIMATE AGENT-5 COMMAND CENTER LAUNCHER")
    print("=" * 60)
    
    # Show features
    show_features()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Cannot launch due to missing dependencies.")
        print("   Please install the required packages and try again.")
        return 1
    
    print("\n🚀 Ready to launch the Ultimate Command Center!")
    print("   Press Enter to continue...")
    input()
    
    # Launch the system
    if launch_ultimate_command_center():
        print("\n🎉 Ultimate Command Center session completed!")
        return 0
    else:
        print("\n❌ Failed to launch Ultimate Command Center.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⏹️ Launch cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

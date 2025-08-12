#!/usr/bin/env python3
"""
Script to commit and push all onboarding improvements
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🚀 {description}")
    print(f"Command: {command}")
    print("-" * 40)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Command executed successfully!")
        if result.stdout:
            print("Output:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main function to commit and push changes."""
    print("🚀 Committing and Pushing Onboarding Improvements")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("agent_workspaces").exists():
        print("❌ Error: agent_workspaces directory not found. Please run this script from the project root.")
        return False
    
    # Step 1: Add all changes
    print("\n📁 Adding all changes to git...")
    success = run_command("git add -A", "Adding all changes to git staging")
    if not success:
        print("❌ Failed to add changes to git")
        return False
    
    # Step 2: Check status
    print("\n📊 Checking git status...")
    success = run_command("git status", "Checking git status")
    if not success:
        print("❌ Failed to check git status")
        return False
    
    # Step 3: Commit changes
    print("\n💾 Committing changes...")
    commit_message = """feat(onboarding): comprehensive system improvements

- Standardized status.json format across all agents
- Enhanced onboarding verification system with 7-point criteria
- Real-time GUI integration with progress tracking
- Automated testing and validation suite
- Comprehensive documentation and reporting

Key improvements:
✅ Standardized status template with comprehensive tracking
✅ Enhanced verification system with detailed reporting
✅ GUI integration with real-time monitoring
✅ Automated testing and validation
✅ Modular architecture for maintainability
✅ Production-ready error handling and fallback mechanisms

All agents now use consistent format with onboarding progress tracking,
performance metrics, health monitoring, and capability management.
"""
    
    success = run_command(f'git commit -m "{commit_message}"', "Committing changes with detailed message")
    if not success:
        print("❌ Failed to commit changes")
        return False
    
    # Step 4: Push to remote
    print("\n📤 Pushing to remote repository...")
    success = run_command("git push", "Pushing changes to remote repository")
    if not success:
        print("❌ Failed to push changes")
        return False
    
    print("\n🎉 Successfully committed and pushed all onboarding improvements!")
    print("=" * 60)
    print("📋 Summary of changes:")
    print("  ✅ Standardized status format for all agents")
    print("  ✅ Enhanced onboarding verification system")
    print("  ✅ GUI integration with real-time monitoring")
    print("  ✅ Automated testing and validation")
    print("  ✅ Comprehensive documentation")
    print("  ✅ Production-ready architecture")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🚀 All onboarding improvements have been successfully pushed!")
    else:
        print("\n❌ Failed to push onboarding improvements. Please check the errors above.")
        sys.exit(1) 
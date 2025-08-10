#!/usr/bin/env python3
"""
Agent Cell Phone - Main Launcher
================================
Central launcher for all components of the Agent Cell Phone system.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_banner():
    """Print the application banner."""
    print("=" * 60)
    print("📱 AGENT CELL PHONE - DREAM.OS AUTONOMY FRAMEWORK")
    print("=" * 60)
    print("Modern Multi-Agent Communication & Coordination System")
    print("Version 2.0 - Enhanced Interface & Controls")
    print("=" * 60)

def print_menu():
    """Print the main menu options."""
    print("\n🚀 MAIN LAUNCHER MENU")
    print("-" * 40)
    print("1.  📱 Launch Dream.OS GUI v2.0 (Modern Interface)")
    print("2.  🤖 Launch Two Agent Horizontal GUI (New!)")
    print("3.  🎨 Launch Dream.OS Splash GUI")
    print("4.  🧪 Run Test Harness")
    print("5.  📊 Run Diagnostic Tests")
    print("6.  📚 View Documentation")
    print("7.  🎯 Run Examples")
    print("8.  📜 Run Scripts")
    print("9.  📈 Show Project Status")
    print("0.  ❌ Exit")
    print("-" * 40)

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🚀 {description}")
    print("-" * 40)
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Command executed successfully!")
        if result.stdout:
            print("Output:")
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
    except FileNotFoundError:
        print(f"❌ Command not found: {command}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def launch_gui(gui_path, description):
    """Launch a GUI application."""
    print(f"\n🚀 {description}")
    print("-" * 40)
    
    if not os.path.exists(gui_path):
        print(f"❌ GUI file not found: {gui_path}")
        return
    
    try:
        # Set PYTHONPATH to include src directory
        env = os.environ.copy()
        src_path = os.path.join(os.getcwd(), 'src')
        if 'PYTHONPATH' in env:
            env['PYTHONPATH'] = f"{src_path};{env['PYTHONPATH']}"
        else:
            env['PYTHONPATH'] = src_path
        
        print(f"📁 Running: {gui_path}")
        print(f"🔧 PYTHONPATH: {env['PYTHONPATH']}")
        
        result = subprocess.run([sys.executable, gui_path], 
                              env=env, 
                              check=True, 
                              capture_output=True, 
                              text=True)
        
        print("✅ GUI launched successfully!")
        if result.stdout:
            print("Output:")
            print(result.stdout)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching GUI: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def show_project_status():
    """Show current project status."""
    print("\n📈 PROJECT STATUS")
    print("-" * 40)
    
    # Check key directories and files
    status_items = [
        ("📁 Agent Workspaces", "agent_workspaces/"),
        ("📁 Source Code", "src/"),
        ("📁 GUI Components", "gui/"),
        ("📁 Configuration", "config/"),
        ("📁 Documentation", "docs/"),
        ("📁 Examples", "examples/"),
        ("📁 Tests", "tests/"),
        ("📁 Scripts", "scripts/"),
        ("📁 PRDs", "project_repository/PRDs/"),
        ("📁 Orchestrator", "project_repository/orchestrator/"),
    ]
    
    for name, path in status_items:
        if os.path.exists(path):
            print(f"✅ {name}: {path}")
        else:
            print(f"❌ {name}: {path} (Missing)")
    
    # Check key files
    key_files = [
        ("📄 Main Launcher", "main.py"),
        ("📄 Requirements", "requirements.txt"),
        ("📄 README", "README.md"),
        ("📄 Coordinate Finder", "src/core/utils/coordinate_finder.py"),
        ("📄 Agent Framework", "src/core/framework/agent_autonomy_framework.py"),
    ]
    
    print("\n📄 KEY FILES:")
    for name, file_path in key_files:
        if os.path.exists(file_path):
            print(f"✅ {name}: {file_path}")
        else:
            print(f"❌ {name}: {file_path} (Missing)")
    
    # Show recent activity
    print("\n🔄 RECENT ACTIVITY:")
    print("✅ Phase 1 (MVP) completed - Core messaging system")
    print("✅ GUI development completed - Multiple interfaces")
    print("✅ Agent onboarding system implemented")
    print("✅ PRD management system added")
    print("✅ Project reorganization completed")
    print("✅ Modern GUI v2.0 created")
    print("🔄 Phase 2 (Full Listener Loop) - Ready to begin")

def main():
    """Main launcher function."""
    while True:
        print_banner()
        print_menu()
        
        try:
            choice = input("\n🎯 Enter your choice (0-9): ").strip()
            
            if choice == "0":
                print("\n👋 Thank you for using Agent Cell Phone!")
                print("🚀 Dream.OS Autonomy Framework - Ready for Phase 2")
                break
                
            elif choice == "1":
                # Launch Dream.OS GUI v2.0
                launch_gui("gui/dream_os_gui_v2.py", "Launching Dream.OS GUI v2.0 (Modern Interface)")
                
            elif choice == "2":
                # Launch Two Agent Horizontal GUI
                launch_gui("gui/two_agent_horizontal_gui.py", "Launching Two Agent Horizontal GUI")
                
            elif choice == "3":
                # Launch Dream.OS Splash GUI
                launch_gui("dream_os_splash_gui.py", "Launching Dream.OS Splash GUI")
                
            elif choice == "4":
                # Run Test Harness
                run_command("python test_harness.py", "Running Test Harness")
                
            elif choice == "5":
                # Run Diagnostic Tests
                run_command("python tests/diagnostic_test.py", "Running Diagnostic Tests")
                
            elif choice == "6":
                # View Documentation
                print("\n📚 DOCUMENTATION")
                print("-" * 40)
                docs = [
                    ("📄 README", "README.md"),
                    ("📄 Project Status", "docs/PROJECT_STATUS.md"),
                    ("📄 Product Requirements", "docs/PRODUCT_REQUIREMENTS_DOCUMENT.md"),
                    ("📄 Project Roadmap", "docs/PROJECT_ROADMAP.md"),
                    ("📄 GUI Development", "docs/GUI_DEVELOPMENT_SUMMARY.md"),
                    ("📄 Inter-Agent Framework", "docs/INTER_AGENT_FRAMEWORK_SUMMARY.md"),
                ]
                
                for name, doc_path in docs:
                    if os.path.exists(doc_path):
                        print(f"✅ {name}: {doc_path}")
                    else:
                        print(f"❌ {name}: {doc_path} (Missing)")
                
                print("\n💡 To view a document, open it in your text editor or browser.")
                
            elif choice == "7":
                # Run Examples
                print("\n🎯 EXAMPLES")
                print("-" * 40)
                examples = [
                    ("📄 Agent Conversation Demo", "examples/agent_conversation_demo.py"),
                    ("📄 Coordination Demo", "examples/coordination_demo.py"),
                    ("📄 Example Usage", "examples/example_usage.py"),
                    ("📄 Real Agent Messages", "examples/real_agent_messages.py"),
                ]
                
                for name, example_path in examples:
                    if os.path.exists(example_path):
                        print(f"✅ {name}: {example_path}")
                        try:
                            subprocess.run([sys.executable, example_path], check=True)
                        except Exception as e:
                            print(f"❌ Error running {name}: {e}")
                    else:
                        print(f"❌ {name}: {example_path} (Missing)")
                
            elif choice == "8":
                # Run Scripts
                print("\n📜 SCRIPTS")
                print("-" * 40)
                scripts = [
                    ("📄 Agent Messenger", "scripts/agent_messenger.py"),
                    ("📄 Agent Onboarding", "scripts/agent_onboarding_sequence.py"),
                    ("📄 Onboard All Agents", "scripts/onboard_all_agents.py"),
                    ("📄 Send Onboarding", "scripts/send_onboarding.py"),
                ]
                
                for name, script_path in scripts:
                    if os.path.exists(script_path):
                        print(f"✅ {name}: {script_path}")
                        try:
                            subprocess.run([sys.executable, script_path], check=True)
                        except Exception as e:
                            print(f"❌ Error running {name}: {e}")
                    else:
                        print(f"❌ {name}: {script_path} (Missing)")
                
            elif choice == "9":
                # Show Project Status
                show_project_status()
                
            else:
                print("❌ Invalid choice. Please enter a number between 0 and 9.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        
        if choice not in ["0", "10"]:  # Don't pause for exit or status
            input("\n⏸️  Press Enter to continue...")

if __name__ == "__main__":
    main() 
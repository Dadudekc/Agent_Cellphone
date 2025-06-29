#!/usr/bin/env python3
"""
Dream.OS Cell Phone - Main Launcher
===================================
Central launcher for all Dream.OS Cell Phone components
"""

import sys
import subprocess
import os
from pathlib import Path

def print_banner():
    """Print the Dream.OS Cell Phone banner."""
    print("=" * 60)
    print("📱  Dream.OS Cell Phone - Main Launcher")
    print("=" * 60)
    print()

def print_menu():
    """Print the main menu options."""
    print("🚀 Available Components:")
    print()
    print("1. 📱 Launch Main GUI (PyQt5) - Full Interface")
    print("2. 🖥️  Launch Simple GUI (Tkinter) - Lightweight")
    print("3. 🌐 Launch Web GUI - Browser Interface")
    print("4. 🔧 Start Web Backend Server - For Web GUI")
    print("5. 🧪 Run Test Suite - System Validation")
    print("6. 📚 View Documentation - Project Info")
    print("7. 📋 Show Project Status - System Overview")
    print("8. 🚪 Exit")
    print()

def launch_main_gui():
    """Launch the main PyQt5 GUI."""
    print("🚀 Launching Dream.OS Cell Phone Main GUI...")
    print("📱 Starting PyQt5 interface...")
    try:
        # Set PYTHONPATH to include src directory
        env = os.environ.copy()
        env['PYTHONPATH'] = os.path.join(os.getcwd(), 'src') + os.pathsep + env.get('PYTHONPATH', '')
        subprocess.run([sys.executable, "gui/dream_os_gui.py"], check=True, env=env)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching GUI: {e}")
        print("💡 Make sure PyQt5 is installed: pip install PyQt5")
    except FileNotFoundError:
        print("❌ GUI file not found: gui/dream_os_gui.py")
    except KeyboardInterrupt:
        print("\n👋 GUI closed by user")

def launch_simple_gui():
    """Launch the simple Tkinter GUI."""
    print("🖥️  Launching Simple Cell Phone GUI...")
    print("📱 Starting Tkinter interface...")
    try:
        # Set PYTHONPATH to include src directory
        env = os.environ.copy()
        env['PYTHONPATH'] = os.path.join(os.getcwd(), 'src') + os.pathsep + env.get('PYTHONPATH', '')
        subprocess.run([sys.executable, "src/gui/simple_gui.py"], check=True, env=env)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching GUI: {e}")
    except FileNotFoundError:
        print("❌ GUI file not found: src/gui/simple_gui.py")
    except KeyboardInterrupt:
        print("\n👋 GUI closed by user")

def launch_web_gui():
    """Launch the web GUI."""
    print("🌐 Opening Web GUI...")
    try:
        import webbrowser
        web_gui_path = os.path.join(os.getcwd(), "gui", "agent_resume_web_gui.html")
        if os.path.exists(web_gui_path):
            webbrowser.open(f"file://{web_gui_path}")
            print("✅ Web GUI opened in browser")
            print("💡 Note: Start the Web Backend Server (option 4) for full functionality")
        else:
            print("❌ Web GUI file not found")
    except Exception as e:
        print(f"❌ Error opening web GUI: {e}")

def start_web_backend():
    """Start the web backend server."""
    print("🔧 Starting Web Backend Server...")
    print("🌐 Server will run on http://localhost:8080")
    print("📱 Web GUI will be able to communicate with the Agent Cell Phone system")
    print("Press Ctrl+C to stop the server")
    try:
        # Set PYTHONPATH to include src directory
        env = os.environ.copy()
        env['PYTHONPATH'] = os.path.join(os.getcwd(), 'src') + os.pathsep + env.get('PYTHONPATH', '')
        subprocess.run([sys.executable, "gui/web_backend_server.py"], check=True, env=env)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting web backend: {e}")
    except FileNotFoundError:
        print("❌ Web backend server not found: gui/web_backend_server.py")
    except KeyboardInterrupt:
        print("\n👋 Web backend server stopped by user")

def run_tests():
    """Run test suite."""
    print("🧪 Running System Test Suite...")
    try:
        # Set PYTHONPATH to include src directory
        env = os.environ.copy()
        env['PYTHONPATH'] = os.path.join(os.getcwd(), 'src') + os.pathsep + env.get('PYTHONPATH', '')
        subprocess.run([sys.executable, "tests/test_harness.py", "--mode", "demo"], check=True, env=env)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running tests: {e}")
    except FileNotFoundError:
        print("❌ Test harness not found")
    except KeyboardInterrupt:
        print("\n👋 Tests interrupted by user")

def view_docs():
    """View documentation."""
    print("📚 Documentation Options:")
    print("1. Project Status")
    print("2. Project Roadmap")
    print("3. Product Requirements")
    print("4. GUI Development Summary")
    print("5. Inter-Agent Framework Summary")
    print("6. Back to main menu")
    
    choice = input("\nSelect option (1-6): ").strip()
    
    doc_files = {
        "1": "docs/PROJECT_STATUS.md",
        "2": "docs/PROJECT_ROADMAP.md",
        "3": "docs/PRODUCT_REQUIREMENTS_DOCUMENT.md",
        "4": "docs/GUI_DEVELOPMENT_SUMMARY.md",
        "5": "docs/INTER_AGENT_FRAMEWORK_SUMMARY.md"
    }
    
    if choice in doc_files:
        doc_file = doc_files[choice]
        try:
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"\n📖 {doc_file}:")
                print("=" * 60)
                print(content[:1000] + "..." if len(content) > 1000 else content)
                print("=" * 60)
                input("\nPress Enter to continue...")
        except Exception as e:
            print(f"❌ Error reading documentation: {e}")

def show_status():
    """Show project status."""
    print("📋 Dream.OS Cell Phone Status:")
    print("=" * 40)
    print("✅ Core System: Operational")
    print("✅ GUI Interface: PyQt5 Ready")
    print("✅ Agent Communication: Active")
    print("✅ Test Suite: Available")
    print("✅ Documentation: Complete")
    print("=" * 40)
    print()
    print("📁 Project Structure:")
    print("├── src/          - Source code")
    print("│   ├── framework/    - Core framework")
    print("│   ├── orchestrator/ - Orchestration system")
    print("│   ├── utils/        - Utility scripts")
    print("│   ├── gui/          - GUI interfaces")
    print("│   ├── testing/      - Test files")
    print("│   ├── scripts/      - Management scripts")
    print("│   └── training/     - Training system")
    print("├── gui/          - Web GUI components")
    print("├── tests/        - Test suite")
    print("├── scripts/      - Utility scripts")
    print("├── examples/     - Example code")
    print("├── docs/         - Documentation")
    print("├── PRDs/         - Product Requirements")
    print("└── agent_workspaces/ - Agent workspaces")
    print()
    print("🎮 GUI Features:")
    print("├── Agent Management - Individual & Broadcast")
    print("├── Message Sending - Custom & Predefined")
    print("├── Status Monitoring - Real-time Updates")
    print("├── Script Execution - Built-in Buttons")
    print("├── Log Management - Message History")
    print("└── System Control - Start/Stop/Reset")
    print()
    input("Press Enter to continue...")

def main():
    """Main launcher function."""
    while True:
        print_banner()
        print_menu()
        
        choice = input("Select option (1-8): ").strip()
        
        if choice == "1":
            launch_main_gui()
        elif choice == "2":
            launch_simple_gui()
        elif choice == "3":
            launch_web_gui()
        elif choice == "4":
            start_web_backend()
        elif choice == "5":
            run_tests()
        elif choice == "6":
            view_docs()
        elif choice == "7":
            show_status()
        elif choice == "8":
            print("👋 Thank you for using Dream.OS Cell Phone!")
            print("🚀 Keep building amazing things!")
            break
        else:
            print("❌ Invalid option. Please select 1-8.")
        
        print()

if __name__ == "__main__":
    main() 
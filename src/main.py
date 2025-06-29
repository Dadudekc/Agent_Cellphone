#!/usr/bin/env python3
"""
Agent Cell Phone - Main Entry Point
===================================

Primary launcher for the Agent Cell Phone system with multiple GUI options.
"""

import sys
import os
import subprocess
from pathlib import Path

def print_banner():
    """Print the Agent Cell Phone banner."""
    print("=" * 60)
    print("📱  AGENT CELL PHONE v1.0.0")
    print("=" * 60)
    print("Inter-agent communication and collaboration platform")
    print("Phase 1 Complete - Production Ready")
    print("=" * 60)

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import PyQt5
        return True
    except ImportError:
        return False

def show_menu():
    """Show the main menu options."""
    print("\n🎮 Available Options:")
    print("1. 🖥️  Dream.OS GUI (PyQt5) - Modern interface")
    print("2. 🖥️  Simple GUI (Tkinter) - Reliable interface")
    print("3. 🧪 Test Harness - CLI testing")
    print("4. 📍 Coordinate Finder - Setup utility")
    print("5. 🔧 Diagnostic Test - System validation")
    print("6. 📚 Documentation - View project info")
    print("7. 🚪 Exit")
    print()

def run_dream_os_gui():
    """Launch the Dream.OS PyQt5 GUI."""
    print("🚀 Launching Dream.OS Cell Phone GUI...")
    print("📱 Starting PyQt interface...")
    
    try:
        subprocess.run([sys.executable, "gui/dream_os_gui.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching GUI: {e}")
        print("💡 Make sure PyQt5 is installed: pip install PyQt5")
    except FileNotFoundError:
        print("❌ GUI file not found: gui/dream_os_gui.py")
    except KeyboardInterrupt:
        print("\n👋 GUI closed by user")

def run_simple_gui():
    """Launch the Simple Tkinter GUI."""
    print("🚀 Launching Simple Cell Phone GUI...")
    print("📱 Starting Tkinter interface...")
    
    try:
        subprocess.run([sys.executable, "simple_gui.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching GUI: {e}")
    except FileNotFoundError:
        print("❌ GUI file not found: simple_gui.py")
    except KeyboardInterrupt:
        print("\n👋 GUI closed by user")

def run_test_harness():
    """Run the CLI test harness."""
    print("🧪 Launching Test Harness...")
    try:
        subprocess.run([sys.executable, "test_harness.py", "--mode", "demo"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running test harness: {e}")
    except KeyboardInterrupt:
        print("\n👋 Test harness closed by user")

def run_coordinate_finder():
    """Run the coordinate finder utility."""
    print("📍 Launching Coordinate Finder...")
    try:
        subprocess.run([sys.executable, "coordinate_finder.py", "--mode", "find"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running coordinate finder: {e}")
    except KeyboardInterrupt:
        print("\n👋 Coordinate finder closed by user")

def run_diagnostic_test():
    """Run the diagnostic test."""
    print("🔧 Running Diagnostic Test...")
    try:
        subprocess.run([sys.executable, "diagnostic_test.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running diagnostic test: {e}")
    except KeyboardInterrupt:
        print("\n👋 Diagnostic test closed by user")

def show_documentation():
    """Show documentation options."""
    print("\n📚 Documentation Options:")
    print("1. README.md - Project overview")
    print("2. PROJECT_STATUS.md - Current status")
    print("3. PROJECT_ROADMAP.md - Development roadmap")
    print("4. PRODUCT_REQUIREMENTS_DOCUMENT.md - PRD")
    print("5. Back to main menu")
    
    try:
        choice = input("\nSelect documentation (1-5): ").strip()
        if choice == "1":
            subprocess.run(["notepad", "README.md"])
        elif choice == "2":
            subprocess.run(["notepad", "PROJECT_STATUS.md"])
        elif choice == "3":
            subprocess.run(["notepad", "PROJECT_ROADMAP.md"])
        elif choice == "4":
            subprocess.run(["notepad", "PRODUCT_REQUIREMENTS_DOCUMENT.md"])
        elif choice == "5":
            return
        else:
            print("❌ Invalid choice")
    except Exception as e:
        print(f"❌ Error opening documentation: {e}")

def main():
    """Main entry point."""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("⚠️  PyQt5 not found. Installing...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "PyQt5"], check=True)
            print("✅ PyQt5 installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install PyQt5. Some features may not work.")
    
    while True:
        show_menu()
        
        try:
            choice = input("Select option (1-7): ").strip()
            
            if choice == "1":
                run_dream_os_gui()
            elif choice == "2":
                run_simple_gui()
            elif choice == "3":
                run_test_harness()
            elif choice == "4":
                run_coordinate_finder()
            elif choice == "5":
                run_diagnostic_test()
            elif choice == "6":
                show_documentation()
            elif choice == "7":
                print("\n👋 Thank you for using Agent Cell Phone!")
                print("📱 System shutting down...")
                break
            else:
                print("❌ Invalid choice. Please select 1-7.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main() 
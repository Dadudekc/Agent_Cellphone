#!/usr/bin/env python3
"""
Dream.OS Cell Phone - Two Agent GUI Launcher
============================================
Launcher script for the horizontal 2-agent GUI.
"""

import sys
import os

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def main():
    """Launch the two agent horizontal GUI."""
    try:
        from two_agent_horizontal_gui import main as gui_main
        print("🚀 Launching Dream.OS Cell Phone - Two Agent Horizontal GUI...")
        gui_main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install PyQt5 pyautogui")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
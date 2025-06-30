#!/usr/bin/env python3
"""
Dream.OS Cell Phone - Two Agent Horizontal GUI Launcher
=======================================================
Simple launcher for the horizontal 2-agent GUI from project root.
"""

import sys
import os

def main():
    """Launch the two agent horizontal GUI."""
    try:
        # Add gui directory to path
        gui_path = os.path.join(os.path.dirname(__file__), 'gui')
        sys.path.insert(0, gui_path)
        
        from two_agent_horizontal_gui import main as gui_main
        print("🚀 Launching Dream.OS Cell Phone - Two Agent Horizontal GUI...")
        print("📱 Horizontal layout with Agent-1 (left) and Agent-2 (right)")
        print("🎨 Modern v2-inspired design with clean, minimal interface")
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
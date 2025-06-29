#!/usr/bin/env python3
"""
Dream.OS GUI Launcher
Launches the Dream.OS Autonomous Framework GUI
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Main launcher function"""
    try:
        # Import and run the GUI
        from src.gui.dream_os_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Error importing GUI components: {e}")
        print("Please ensure all required modules are available.")
        sys.exit(1)
    except Exception as e:
        print(f"Error launching GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
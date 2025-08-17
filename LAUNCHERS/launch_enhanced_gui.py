#!/usr/bin/env python3
"""
Enhanced GUI Launcher
---------------------
Simple launcher script for the Enhanced Overnight Runner GUI
"""

import sys
from pathlib import Path

# Add the overnight_runner directory to the path
sys.path.insert(0, str(Path(__file__).parent / "overnight_runner"))

try:
    from enhanced_gui import main
    print("🚀 Launching Enhanced Overnight Runner GUI...")
    print("📋 Features:")
    print("  • Agent-5 Command Center")
    print("  • PyAutoGUI Queue Management")
    print("  • Agent Coordination & Monitoring")
    print("  • Overnight Run Facilitation")
    print("=" * 50)
    
    # Launch the GUI
    main()
    
except ImportError as e:
    print(f"❌ Error importing enhanced GUI: {e}")
    print("   Make sure you're running this from the Agent_Cellphone directory")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error launching GUI: {e}")
    sys.exit(1)

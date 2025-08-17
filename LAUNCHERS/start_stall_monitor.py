#!/usr/bin/env python3
"""
START STALL MONITOR
===================
Simple script to start the Agent5Monitor system that will:
- Detect when agents stall (every 15 seconds)
- Send rescue messages automatically
- Monitor agent activity continuously
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.agent_monitors.agent5_monitor import main as start_monitor
    print("✅ Agent5Monitor imported successfully")
    print("🚀 Starting stall detection and rescue system...")
    print("📊 This will monitor agents every 15 seconds and send rescue messages automatically")
    print("🛑 Press Ctrl+C to stop")
    
    # Start the monitor
    start_monitor()
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you're running this from the Agent_Cellphone directory")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting monitor: {e}")
    sys.exit(1)



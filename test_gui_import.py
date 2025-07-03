#!/usr/bin/env python3
"""
Test script to verify GUI imports and functionality
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported."""
    try:
        print("Testing PyQt5 import...")
        import PyQt5
        print("✅ PyQt5 imported successfully")
        
        print("Testing GUI import...")
        from gui.two_agent_horizontal_gui import TwoAgentHorizontalGUI
        print("✅ GUI class imported successfully")
        
        print("Testing coordinate finder import...")
        from src.utils.coordinate_finder import CoordinateFinder
        print("✅ CoordinateFinder imported successfully")
        
        print("Testing agent autonomy framework import...")
        from src.framework.agent_autonomy_framework import AgentAutonomyFramework
        print("✅ AgentAutonomyFramework imported successfully")
        
        print("\n🎉 All imports successful! GUI should work correctly.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1) 
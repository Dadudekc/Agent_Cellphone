#!/usr/bin/env python3
"""
Test Calibrated Coordinates
===========================
Tests the newly calibrated 5-agent mode coordinates to ensure they work correctly.
"""

import json
import time
import sys
from pathlib import Path
from typing import Dict, Any

try:
    import pyautogui
    pyautogui.FAILSAFE = True
except ImportError:
    print("❌ PyAutoGUI not installed. Install with: pip install pyautogui")
    sys.exit(1)

class CoordinateTester:
    """Test calibrated coordinates for 5-agent mode"""
    
    def __init__(self):
        self.coord_file = Path("runtime/agent_comms/cursor_agent_coords.json")
        self.coords = {}
        self.test_results = {}
        
        # Load coordinates
        self.load_coordinates()
    
    def load_coordinates(self):
        """Load coordinate configuration"""
        try:
            if self.coord_file.exists():
                with open(self.coord_file, 'r') as f:
                    all_coords = json.load(f)
                    self.coords = all_coords.get("5-agent", {})
                print("✅ 5-agent coordinates loaded")
            else:
                print("❌ Coordinate file not found")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Error loading coordinates: {e}")
            sys.exit(1)
    
    def test_agent_coordinates(self, agent_name: str) -> Dict[str, Any]:
        """Test coordinates for a specific agent"""
        print(f"\n🧪 Testing {agent_name} coordinates...")
        
        if agent_name not in self.coords:
            return {"status": "error", "message": "Agent not found in coordinates"}
        
        agent_coords = self.coords[agent_name]
        results = {
            "agent": agent_name,
            "starter_location": {"status": "pending", "coords": agent_coords.get("starter_location_box")},
            "input_box": {"status": "pending", "coords": agent_coords.get("input_box")}
        }
        
        # Test starter location
        print(f"   📍 Testing starter location: {agent_coords.get('starter_location_box')}")
        try:
            # Move to starter location
            starter = agent_coords["starter_location_box"]
            pyautogui.moveTo(starter["x"], starter["y"], duration=0.5)
            print(f"      ✅ Moved to starter location")
            results["starter_location"]["status"] = "success"
        except Exception as e:
            print(f"      ❌ Error moving to starter location: {e}")
            results["starter_location"]["status"] = "error"
            results["starter_location"]["error"] = str(e)
        
        # Test input box
        print(f"   ⌨️  Testing input box: {agent_coords.get('input_box')}")
        try:
            # Move to input box
            input_box = agent_coords["input_box"]
            pyautogui.moveTo(input_box["x"], input_box["y"], duration=0.5)
            print(f"      ✅ Moved to input box")
            results["input_box"]["status"] = "success"
        except Exception as e:
            print(f"      ❌ Error moving to input box: {e}")
            results["input_box"]["status"] = "error"
            results["input_box"]["error"] = str(e)
        
        return results
    
    def run_coordinate_test(self):
        """Run complete coordinate testing"""
        print("🧪 TESTING CALIBRATED 5-AGENT COORDINATES")
        print("=" * 60)
        print("This will test all agent coordinates by moving the mouse")
        print("Make sure your Cursor is visible and in 5-agent mode")
        print("=" * 60)
        
        # Show current coordinates
        print("\n📱 Current 5-Agent Coordinates:")
        for agent_name, coords in self.coords.items():
            print(f"\n   {agent_name}:")
            print(f"      Starter: {coords.get('starter_location_box', 'Not set')}")
            print(f"      Input:  {coords.get('input_box', 'Not set')}")
        
        # Confirm testing
        print(f"\n⚠️  This will move your mouse to test each coordinate")
        response = input("Continue with testing? (y/N): ").strip().lower()
        if response != 'y':
            print("❌ Testing cancelled")
            return
        
        print("\n🎯 Starting coordinate testing...")
        print("Watch your mouse move to each location")
        print("Use Ctrl+C to cancel at any time")
        
        try:
            # Test each agent
            for agent_name in self.coords.keys():
                result = self.test_agent_coordinates(agent_name)
                self.test_results[agent_name] = result
                
                # Pause between agents to allow observation
                if agent_name != "Agent-5":
                    print("\n⏳ Ready for next agent")
                    input("Press Enter to continue...")
            
            # Show test results
            self.show_test_results()
            
        except KeyboardInterrupt:
            print("\n\n🛑 Testing interrupted by user")
            return
        except Exception as e:
            print(f"\n❌ Testing error: {e}")
            return
    
    def show_test_results(self):
        """Display test results summary"""
        print("\n📊 COORDINATE TEST RESULTS")
        print("=" * 60)
        
        all_success = True
        
        for agent_name, result in self.test_results.items():
            print(f"\n🤖 {agent_name}:")
            
            # Starter location result
            starter = result["starter_location"]
            if starter["status"] == "success":
                print(f"   📍 Starter: ✅ SUCCESS")
            else:
                print(f"   📍 Starter: ❌ ERROR - {starter.get('error', 'Unknown error')}")
                all_success = False
            
            # Input box result
            input_box = result["input_box"]
            if input_box["status"] == "success":
                print(f"   ⌨️  Input:  ✅ SUCCESS")
            else:
                print(f"   ⌨️  Input:  ❌ ERROR - {input_box.get('error', 'Unknown error')}")
                all_success = False
        
        print("\n" + "=" * 60)
        if all_success:
            print("🎉 ALL COORDINATES TESTED SUCCESSFULLY!")
            print("✅ Your 5-agent mode is ready to use")
            print("\nNext steps:")
            print("1. Test with actual agent communication")
            print("2. Run: python test_agent_communication.py")
        else:
            print("❌ SOME COORDINATES FAILED TESTING")
            print("⚠️  You may need to recalibrate")
            print("\nTroubleshooting:")
            print("1. Check if Cursor is in correct 5-agent mode")
            print("2. Ensure windows are not minimized")
            print("3. Run calibration again: python calibrate_5_agent_coordinates.py")
        
        print("=" * 60)
    
    def quick_test_single_agent(self, agent_name: str):
        """Quick test of a single agent's coordinates"""
        if agent_name not in self.coords:
            print(f"❌ Agent {agent_name} not found in coordinates")
            return
        
        print(f"🧪 Quick test of {agent_name} coordinates...")
        result = self.test_agent_coordinates(agent_name)
        
        print(f"\n📊 {agent_name} Test Result:")
        print(f"   Starter: {'✅' if result['starter_location']['status'] == 'success' else '❌'}")
        print(f"   Input:  {'✅' if result['input_box']['status'] == 'success' else '❌'}")

def main():
    """Main testing function"""
    try:
        tester = CoordinateTester()
        
        # Check if specific agent test requested
        if len(sys.argv) > 1:
            agent_name = sys.argv[1]
            tester.quick_test_single_agent(agent_name)
        else:
            tester.run_coordinate_test()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Testing cancelled")
        return 1
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

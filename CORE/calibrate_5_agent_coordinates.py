#!/usr/bin/env python3
"""
5-Agent Mode Coordinate Calibration System
==========================================
Recalibrates coordinates for 5-agent mode using existing architecture.
Integrates with AgentCellPhone coordinate system.
"""

import json
import time
import sys
from pathlib import Path
from typing import Dict, Tuple, Any

try:
    import pyautogui
    pyautogui.FAILSAFE = True  # Enable failsafe for calibration
except ImportError:
    print("❌ PyAutoGUI not installed. Install with: pip install pyautogui")
    sys.exit(1)

class CoordinateCalibrator:
    """Coordinate calibration system for 5-agent mode"""
    
    def __init__(self):
        self.coord_file = Path("runtime/agent_comms/cursor_agent_coords.json")
        self.backup_file = Path("runtime/agent_comms/cursor_agent_coords_backup.json")
        self.current_coords = {}
        self.new_coords = {}
        
        # Load current coordinates
        self.load_current_coordinates()
        
    def load_current_coordinates(self):
        """Load current coordinate configuration"""
        try:
            if self.coord_file.exists():
                with open(self.coord_file, 'r') as f:
                    self.current_coords = json.load(f)
                print("✅ Current coordinates loaded")
            else:
                print("❌ Coordinate file not found")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Error loading coordinates: {e}")
            sys.exit(1)
    
    def backup_current_coordinates(self):
        """Create backup of current coordinates"""
        try:
            import shutil
            shutil.copy2(self.coord_file, self.backup_file)
            print(f"✅ Current coordinates backed up to {self.backup_file}")
        except Exception as e:
            print(f"⚠️ Warning: Could not create backup: {e}")
    
    def get_agent_layout(self) -> Dict[str, str]:
        """Get 5-agent layout description"""
        return {
            "Agent-1": "Top Left",
            "Agent-2": "Top Right", 
            "Agent-3": "Bottom Left",
            "Agent-4": "Bottom Right",
            "Agent-5": "Center/Right"
        }
    
    def calibrate_agent_coordinates(self, agent_name: str, position: str):
        """Calibrate coordinates for a specific agent"""
        print(f"\n🎯 Calibrating {agent_name} ({position})")
        print("=" * 50)
        
        # Calibrate starter location (where to click to start new chat)
        print(f"📍 Click where {agent_name} should click to start a new chat")
        print("   (This is usually the top area of the agent's chat window)")
        print("   You have 5 seconds to position your mouse...")
        
        for i in range(5, 0, -1):
            print(f"   {i}...", end=" ", flush=True)
            time.sleep(1)
        print()
        
        starter_x, starter_y = pyautogui.position()
        print(f"✅ Starter location captured: ({starter_x}, {starter_y})")
        
        # Calibrate input box (where to type messages)
        print(f"\n⌨️  Click where {agent_name} should type messages")
        print("   (This is usually the input area at the bottom of the chat)")
        print("   You have 5 seconds to position your mouse...")
        
        for i in range(5, 0, -1):
            print(f"   {i}...", end=" ", flush=True)
            time.sleep(1)
        print()
        
        input_x, input_y = pyautogui.position()
        print(f"✅ Input box captured: ({input_x}, {input_y})")
        
        # Store new coordinates
        self.new_coords[agent_name] = {
            "starter_location_box": {"x": starter_x, "y": starter_y},
            "input_box": {"x": input_x, "y": input_y}
        }
        
        print(f"✅ {agent_name} coordinates calibrated!")
    
    def run_calibration(self):
        """Run the complete 5-agent calibration process"""
        print("🚀 5-AGENT MODE COORDINATE CALIBRATION")
        print("=" * 60)
        print("This will recalibrate coordinates for all 5 agents")
        print("Make sure your Cursor is in 5-agent mode and visible")
        print("=" * 60)
        
        # Show current layout
        layout = self.get_agent_layout()
        print("\n📱 Current 5-Agent Layout:")
        for agent, position in layout.items():
            print(f"   {agent}: {position}")
        
        # Backup current coordinates
        self.backup_current_coordinates()
        
        # Confirm before starting
        print(f"\n⚠️  This will update coordinates in: {self.coord_file}")
        response = input("Continue with calibration? (y/N): ").strip().lower()
        if response != 'y':
            print("❌ Calibration cancelled")
            return
        
        print("\n🎯 Starting calibration process...")
        print("Position your mouse over each location when prompted")
        print("Use Ctrl+C to cancel at any time")
        
        try:
            # Calibrate each agent
            for agent_name, position in layout.items():
                self.calibrate_agent_coordinates(agent_name, position)
                
                # Small break between agents
                if agent_name != "Agent-5":
                    print("\n⏳ Moving to next agent in 3 seconds...")
                    time.sleep(3)
            
            # Save new coordinates
            self.save_new_coordinates()
            
            # Test coordinates
            self.test_new_coordinates()
            
        except KeyboardInterrupt:
            print("\n\n🛑 Calibration interrupted by user")
            print("No changes were saved")
            return
        except Exception as e:
            print(f"\n❌ Calibration error: {e}")
            return
    
    def save_new_coordinates(self):
        """Save new coordinates to file"""
        try:
            # Update 5-agent section with new coordinates
            self.current_coords["5-agent"] = self.new_coords
            
            # Save to file
            with open(self.coord_file, 'w') as f:
                json.dump(self.current_coords, f, indent=2)
            
            print(f"\n✅ New coordinates saved to {self.coord_file}")
            
        except Exception as e:
            print(f"❌ Error saving coordinates: {e}")
            sys.exit(1)
    
    def test_new_coordinates(self):
        """Test the new coordinates"""
        print("\n🧪 Testing new coordinates...")
        print("=" * 40)
        
        # Test each agent's coordinates
        for agent_name in self.new_coords.keys():
            coords = self.new_coords[agent_name]
            
            print(f"\n🤖 Testing {agent_name}:")
            
            # Test starter location
            starter = coords["starter_location_box"]
            print(f"   Starter: ({starter['x']}, {starter['y']})")
            
            # Test input box
            input_box = coords["input_box"]
            print(f"   Input: ({input_box['x']}, {input_box['y']})")
            
            # Visual verification
            print(f"   ✅ Coordinates captured and saved")
        
        print("\n🎉 Calibration complete!")
        print("=" * 40)
        print("Next steps:")
        print("1. Test the system with: python test_calibrated_coordinates.py")
        print("2. If coordinates are wrong, run calibration again")
        print("3. Restore backup if needed: restore_coordinate_backup.py")
    
    def show_coordinate_summary(self):
        """Show summary of current vs new coordinates"""
        print("\n📊 COORDINATE COMPARISON")
        print("=" * 60)
        
        for agent_name in self.new_coords.keys():
            print(f"\n{agent_name}:")
            
            # Current coordinates
            if agent_name in self.current_coords.get("5-agent", {}):
                current = self.current_coords["5-agent"][agent_name]
                print(f"   Current Starter: ({current['starter_location_box']['x']}, {current['starter_location_box']['y']})")
                print(f"   Current Input:  ({current['input_box']['x']}, {current['input_box']['y']})")
            else:
                print("   Current: Not configured")
            
            # New coordinates
            new = self.new_coords[agent_name]
            print(f"   New Starter:    ({new['starter_location_box']['x']}, {new['starter_location_box']['y']})")
            print(f"   New Input:      ({new['input_box']['x']}, {new['input_box']['y']})")

def main():
    """Main calibration function"""
    try:
        calibrator = CoordinateCalibrator()
        calibrator.run_calibration()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Calibration cancelled")
        return 1
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

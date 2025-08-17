#!/usr/bin/env python3
"""
Improved 5-Agent Coordinate Calibration
=======================================
This version ensures each agent has distinct coordinates
and provides better guidance during calibration.
"""

import json
import time
import sys
from pathlib import Path
from typing import Dict, Tuple, Any

try:
    import pyautogui
    pyautogui.FAILSAFE = True
except ImportError:
    print("❌ PyAutoGUI not installed. Install with: pip install pyautogui")
    sys.exit(1)

class ImprovedCoordinateCalibrator:
    """Improved coordinate calibration with coordinate validation"""
    
    def __init__(self):
        self.coord_file = Path("runtime/agent_comms/cursor_agent_coords.json")
        self.backup_file = Path("runtime/agent_comms/cursor_agent_coords_backup.json")
        self.current_coords = {}
        self.new_coords = {}
        self.min_distance = 50  # Minimum distance between agent coordinates
        
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
        """Get 5-agent layout description with better positioning guidance"""
        return {
            "Agent-1": "Top Left (upper left quadrant)",
            "Agent-2": "Top Right (upper right quadrant)", 
            "Agent-3": "Bottom Left (lower left quadrant)",
            "Agent-4": "Bottom Right (lower right quadrant)",
            "Agent-5": "Center/Right (middle area)"
        }
    
    def calculate_distance(self, coord1: Dict, coord2: Dict) -> float:
        """Calculate distance between two coordinates"""
        dx = coord1['x'] - coord2['x']
        dy = coord1['y'] - coord2['y']
        return (dx**2 + dy**2)**0.5
    
    def validate_coordinate_separation(self, new_coord: Dict, agent_name: str) -> bool:
        """Validate that new coordinate is sufficiently separated from others"""
        for existing_agent, existing_coords in self.new_coords.items():
            if existing_agent == agent_name:
                continue
            
            # Check starter location separation
            if 'starter_location_box' in existing_coords:
                distance = self.calculate_distance(new_coord['starter_location_box'], 
                                                existing_coords['starter_location_box'])
                if distance < self.min_distance:
                    print(f"⚠️  Warning: {agent_name} starter location too close to {existing_agent}")
                    print(f"   Distance: {distance:.1f} pixels (minimum: {self.min_distance})")
                    return False
            
            # Check input box separation
            if 'input_box' in existing_coords:
                distance = self.calculate_distance(new_coord['input_box'], 
                                                existing_coords['input_box'])
                if distance < self.min_distance:
                    print(f"⚠️  Warning: {agent_name} input box too close to {existing_agent}")
                    print(f"   Distance: {distance:.1f} pixels (minimum: {self.min_distance})")
                    return False
        
        return True
    
    def calibrate_agent_coordinates(self, agent_name: str, position: str):
        """Calibrate coordinates for a specific agent with validation"""
        print(f"\n🎯 Calibrating {agent_name} ({position})")
        print("=" * 60)
        print(f"📱 Position: {position}")
        print("💡 Make sure this is a DIFFERENT area from other agents!")
        print("=" * 60)
        
        # Calibrate starter location
        print(f"📍 Click where {agent_name} should click to start a new chat")
        print("   (This should be in the TOP area of this agent's chat window)")
        print("   ⚠️  IMPORTANT: Make sure this is NOT the same area as other agents!")
        print("   You have 8 seconds to position your mouse...")
        
        for i in range(8, 0, -1):
            print(f"   {i}...", end=" ", flush=True)
            time.sleep(1)
        print()
        
        starter_x, starter_y = pyautogui.position()
        print(f"✅ Starter location captured: ({starter_x}, {starter_y})")
        
        # Calibrate input box
        print(f"\n⌨️  Click where {agent_name} should type messages")
        print("   (This should be in the BOTTOM area of this agent's chat window)")
        print("   ⚠️  IMPORTANT: Make sure this is NOT the same area as other agents!")
        print("   You have 8 seconds to position your mouse...")
        
        for i in range(8, 0, -1):
            print(f"   {i}...", end=" ", flush=True)
            time.sleep(1)
        print()
        
        input_x, input_y = pyautogui.position()
        print(f"✅ Input box captured: ({input_x}, {input_y})")
        
        # Store coordinates
        agent_coords = {
            "starter_location_box": {"x": starter_x, "y": starter_y},
            "input_box": {"x": input_x, "y": input_y}
        }
        
        # Validate separation
        if self.validate_coordinate_separation(agent_coords, agent_name):
            self.new_coords[agent_name] = agent_coords
            print(f"✅ {agent_name} coordinates calibrated and validated!")
        else:
            print(f"⚠️  {agent_name} coordinates may be too close to other agents")
            print("   Consider recalibrating this agent with more separation")
            
            # Ask if user wants to continue or recalibrate
            response = input("Continue anyway? (y/N): ").strip().lower()
            if response == 'y':
                self.new_coords[agent_name] = agent_coords
                print(f"✅ {agent_name} coordinates saved (with warning)")
            else:
                print(f"🔄 Recalibrating {agent_name}...")
                return self.calibrate_agent_coordinates(agent_name, position)
    
    def run_calibration(self):
        """Run the improved 5-agent calibration process"""
        print("🚀 IMPROVED 5-AGENT MODE COORDINATE CALIBRATION")
        print("=" * 70)
        print("This will recalibrate coordinates for all 5 agents")
        print("⚠️  CRITICAL: Each agent must have DISTINCT coordinates!")
        print("Make sure your Cursor is in 5-agent mode and visible")
        print("=" * 70)
        
        # Show current layout
        layout = self.get_agent_layout()
        print("\n📱 5-Agent Layout Guide:")
        for agent, position in layout.items():
            print(f"   {agent}: {position}")
        
        print(f"\n📏 Minimum separation between agents: {self.min_distance} pixels")
        print("💡 This ensures agents don't interfere with each other")
        
        # Backup current coordinates
        self.backup_current_coordinates()
        
        # Confirm before starting
        print(f"\n⚠️  This will update coordinates in: {self.coord_file}")
        response = input("Continue with improved calibration? (y/N): ").strip().lower()
        if response != 'y':
            print("❌ Calibration cancelled")
            return
        
        print("\n🎯 Starting improved calibration process...")
        print("Position your mouse over DISTINCT locations for each agent")
        print("Use Ctrl+C to cancel at any time")
        
        try:
            # Calibrate each agent
            for agent_name, position in layout.items():
                self.calibrate_agent_coordinates(agent_name, position)
                
                # Show current progress
                print(f"\n📊 Progress: {len(self.new_coords)}/5 agents calibrated")
                
                # Small break between agents
                if agent_name != "Agent-5":
                    print("\n⏳ Moving to next agent in 5 seconds...")
                    print("💡 Remember: Each agent needs DISTINCT coordinates!")
                    time.sleep(5)
            
            # Save new coordinates
            self.save_new_coordinates()
            
            # Show coordinate summary
            self.show_coordinate_summary()
            
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
    
    def show_coordinate_summary(self):
        """Show detailed coordinate summary with separation analysis"""
        print("\n📊 COORDINATE CALIBRATION SUMMARY")
        print("=" * 70)
        
        # Show all coordinates
        for agent_name in self.new_coords.keys():
            coords = self.new_coords[agent_name]
            print(f"\n🤖 {agent_name}:")
            print(f"   📍 Starter: ({coords['starter_location_box']['x']}, {coords['starter_location_box']['y']})")
            print(f"   ⌨️  Input:  ({coords['input_box']['x']}, {coords['input_box']['y']})")
        
        # Analyze separation
        print(f"\n🔍 COORDINATE SEPARATION ANALYSIS:")
        print(f"   Minimum required separation: {self.min_distance} pixels")
        
        all_good = True
        for i, agent1 in enumerate(self.new_coords.keys()):
            for j, agent2 in enumerate(self.new_coords.keys()):
                if i >= j:
                    continue
                
                coords1 = self.new_coords[agent1]
                coords2 = self.new_coords[agent2]
                
                # Check starter locations
                starter_distance = self.calculate_distance(
                    coords1['starter_location_box'], 
                    coords2['starter_location_box']
                )
                
                # Check input boxes
                input_distance = self.calculate_distance(
                    coords1['input_box'], 
                    coords2['input_box']
                )
                
                if starter_distance < self.min_distance:
                    print(f"   ⚠️  {agent1} ↔ {agent2} starters: {starter_distance:.1f}px")
                    all_good = False
                else:
                    print(f"   ✅ {agent1} ↔ {agent2} starters: {starter_distance:.1f}px")
                
                if input_distance < self.min_distance:
                    print(f"   ⚠️  {agent1} ↔ {agent2} inputs: {input_distance:.1f}px")
                    all_good = False
                else:
                    print(f"   ✅ {agent1} ↔ {agent2} inputs: {input_distance:.1f}px")
        
        print("\n" + "=" * 70)
        if all_good:
            print("🎉 ALL COORDINATES PROPERLY SEPARATED!")
            print("✅ Your 5-agent mode is ready for reliable communication")
        else:
            print("⚠️  SOME COORDINATES MAY BE TOO CLOSE")
            print("💡 Consider recalibrating agents with insufficient separation")
        
        print("\n📋 Next steps:")
        print("1. Test coordinates: python test_calibrated_coordinates.py")
        print("2. If issues persist, run calibration again")
        print("3. Restore backup if needed: python restore_coordinate_backup.py")

def main():
    """Main calibration function"""
    try:
        calibrator = ImprovedCoordinateCalibrator()
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

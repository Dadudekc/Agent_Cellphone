#!/usr/bin/env python3
"""
Restore Coordinate Backup
========================
Restores coordinates from backup if calibration goes wrong.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any

class CoordinateRestorer:
    """Restore coordinate configuration from backup"""
    
    def __init__(self):
        self.coord_file = Path("runtime/agent_comms/cursor_agent_coords.json")
        self.backup_file = Path("runtime/agent_comms/cursor_agent_coords_backup.json")
        self.current_coords = {}
        self.backup_coords = {}
        
    def load_coordinates(self):
        """Load current and backup coordinates"""
        try:
            # Load current coordinates
            if self.coord_file.exists():
                with open(self.coord_file, 'r') as f:
                    self.current_coords = json.load(f)
                print("✅ Current coordinates loaded")
            else:
                print("❌ Current coordinate file not found")
                return False
            
            # Load backup coordinates
            if self.backup_file.exists():
                with open(self.backup_file, 'r') as f:
                    self.backup_coords = json.load(f)
                print("✅ Backup coordinates loaded")
                return True
            else:
                print("❌ Backup file not found")
                return False
                
        except Exception as e:
            print(f"❌ Error loading coordinates: {e}")
            return False
    
    def show_coordinate_comparison(self):
        """Show comparison between current and backup coordinates"""
        print("\n📊 COORDINATE COMPARISON")
        print("=" * 60)
        
        if "5-agent" not in self.current_coords or "5-agent" not in self.backup_coords:
            print("❌ Cannot compare - missing 5-agent configuration")
            return
        
        current_5agent = self.current_coords["5-agent"]
        backup_5agent = self.backup_coords["5-agent"]
        
        for agent_name in backup_5agent.keys():
            print(f"\n🤖 {agent_name}:")
            
            # Current coordinates
            if agent_name in current_5agent:
                current = current_5agent[agent_name]
                print(f"   Current Starter: ({current.get('starter_location_box', {}).get('x', 'N/A')}, {current.get('starter_location_box', {}).get('y', 'N/A')})")
                print(f"   Current Input:  ({current.get('input_box', {}).get('x', 'N/A')}, {current.get('input_box', {}).get('y', 'N/A')})")
            else:
                print("   Current: Not configured")
            
            # Backup coordinates
            backup = backup_5agent[agent_name]
            print(f"   Backup Starter: ({backup.get('starter_location_box', {}).get('x', 'N/A')}, {backup.get('starter_location_box', {}).get('y', 'N/A')})")
            print(f"   Backup Input:  ({backup.get('input_box', {}).get('x', 'N/A')}, {backup.get('input_box', {}).get('y', 'N/A')})")
    
    def restore_backup(self):
        """Restore coordinates from backup"""
        try:
            # Create new backup of current state
            import shutil
            current_backup = Path("runtime/agent_comms/cursor_agent_coords_current_backup.json")
            shutil.copy2(self.coord_file, current_backup)
            print(f"✅ Current coordinates backed up to {current_backup}")
            
            # Restore from backup
            self.current_coords["5-agent"] = self.backup_coords["5-agent"]
            
            # Save restored coordinates
            with open(self.coord_file, 'w') as f:
                json.dump(self.current_coords, f, indent=2)
            
            print("✅ Backup coordinates restored successfully!")
            print(f"📁 Restored to: {self.coord_file}")
            
        except Exception as e:
            print(f"❌ Error restoring backup: {e}")
            return False
        
        return True
    
    def run_restoration(self):
        """Run the coordinate restoration process"""
        print("🔄 COORDINATE BACKUP RESTORATION")
        print("=" * 60)
        print("This will restore 5-agent coordinates from backup")
        print("=" * 60)
        
        # Load coordinates
        if not self.load_coordinates():
            print("❌ Cannot proceed - missing coordinate files")
            return
        
        # Show comparison
        self.show_coordinate_comparison()
        
        # Confirm restoration
        print(f"\n⚠️  This will overwrite current coordinates with backup")
        response = input("Continue with restoration? (y/N): ").strip().lower()
        if response != 'y':
            print("❌ Restoration cancelled")
            return
        
        # Perform restoration
        if self.restore_backup():
            print("\n🎉 Restoration complete!")
            print("=" * 40)
            print("Next steps:")
            print("1. Test restored coordinates: python test_calibrated_coordinates.py")
            print("2. If still wrong, recalibrate: python calibrate_5_agent_coordinates.py")
            print("3. Check if Cursor layout has changed")
        else:
            print("\n❌ Restoration failed")
            print("Check error messages above")

def main():
    """Main restoration function"""
    try:
        restorer = CoordinateRestorer()
        restorer.run_restoration()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Restoration cancelled")
        return 1
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

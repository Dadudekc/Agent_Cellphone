#!/usr/bin/env python3
"""
Coordinate Finder for Agent Cell Phone
======================================
Utility for finding and managing cursor coordinates for agent communication.
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class CoordinateFinder:
    """
    Utility for finding and managing cursor coordinates for agent communication.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the Coordinate Finder.
        
        Args:
            config_path: Path to coordinates configuration file
        """
        self.config_path = config_path or "runtime/config/cursor_agent_coords.json"
        self.coordinates = self._load_coordinates()
        self.logger = logger
    
    def _load_coordinates(self) -> Dict[str, Dict[str, int]]:
        """Load coordinates from configuration file."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    coords = json.load(f)
                logger.info(f"Loaded coordinates from {self.config_path}")
                return coords
            else:
                logger.warning(f"Coordinates file not found: {self.config_path}")
                return self._create_default_coordinates()
        except Exception as e:
            logger.error(f"Failed to load coordinates: {e}")
            return self._create_default_coordinates()
    
    def _create_default_coordinates(self) -> Dict[str, Dict[str, int]]:
        """Create default coordinates for 8-agent layout."""
        default_coords = {
            "agent-1": {"x": 100, "y": 100},
            "agent-2": {"x": 300, "y": 100},
            "agent-3": {"x": 500, "y": 100},
            "agent-4": {"x": 700, "y": 100},
            "agent-5": {"x": 100, "y": 300},
            "agent-6": {"x": 300, "y": 300},
            "agent-7": {"x": 500, "y": 300},
            "agent-8": {"x": 700, "y": 300}
        }
        
        # Save default coordinates
        self._save_coordinates(default_coords)
        return default_coords
    
    def _save_coordinates(self, coordinates: Dict[str, Dict[str, int]]):
        """Save coordinates to configuration file."""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(coordinates, f, indent=2)
            logger.info(f"Saved coordinates to {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to save coordinates: {e}")
    
    def get_coordinates(self, agent_id: str) -> Optional[Tuple[int, int]]:
        """
        Get coordinates for a specific agent.
        
        Args:
            agent_id: ID of the agent
            
        Returns:
            Tuple of (x, y) coordinates or None if not found
        """
        if agent_id in self.coordinates:
            coords = self.coordinates[agent_id]
            return (coords["x"], coords["y"])
        else:
            logger.warning(f"Coordinates not found for agent: {agent_id}")
            return None
    
    def set_coordinates(self, agent_id: str, x: int, y: int):
        """
        Set coordinates for a specific agent.
        
        Args:
            agent_id: ID of the agent
            x: X coordinate
            y: Y coordinate
        """
        self.coordinates[agent_id] = {"x": x, "y": y}
        self._save_coordinates(self.coordinates)
        logger.info(f"Set coordinates for {agent_id}: ({x}, {y})")
    
    def get_all_coordinates(self) -> Dict[str, Tuple[int, int]]:
        """
        Get coordinates for all agents.
        
        Returns:
            Dictionary mapping agent IDs to coordinate tuples
        """
        return {agent_id: (coords["x"], coords["y"]) 
                for agent_id, coords in self.coordinates.items()}
    
    def validate_coordinates(self) -> List[str]:
        """
        Validate all coordinates are within reasonable bounds.
        
        Returns:
            List of agent IDs with invalid coordinates
        """
        invalid_agents = []
        
        for agent_id, coords in self.coordinates.items():
            x, y = coords["x"], coords["y"]
            
            # Check if coordinates are within reasonable bounds
            if x < 0 or y < 0 or x > 2000 or y > 2000:
                invalid_agents.append(agent_id)
                logger.warning(f"Invalid coordinates for {agent_id}: ({x}, {y})")
        
        return invalid_agents
    
    def auto_detect_coordinates(self) -> bool:
        """
        Attempt to auto-detect coordinates by scanning screen.
        This is a placeholder for actual screen scanning logic.
        
        Returns:
            True if detection was successful, False otherwise
        """
        logger.info("Auto-detection of coordinates not implemented yet")
        logger.info("Please manually set coordinates using set_coordinates()")
        return False
    
    def export_coordinates(self, export_path: str):
        """
        Export coordinates to a file.
        
        Args:
            export_path: Path to export file
        """
        try:
            with open(export_path, 'w') as f:
                json.dump(self.coordinates, f, indent=2)
            logger.info(f"Exported coordinates to {export_path}")
        except Exception as e:
            logger.error(f"Failed to export coordinates: {e}")
    
    def import_coordinates(self, import_path: str):
        """
        Import coordinates from a file.
        
        Args:
            import_path: Path to import file
        """
        try:
            with open(import_path, 'r') as f:
                imported_coords = json.load(f)
            
            # Validate imported coordinates
            for agent_id, coords in imported_coords.items():
                if not isinstance(coords, dict) or "x" not in coords or "y" not in coords:
                    logger.error(f"Invalid coordinate format for {agent_id}")
                    return
            
            self.coordinates = imported_coords
            self._save_coordinates(self.coordinates)
            logger.info(f"Imported coordinates from {import_path}")
            
        except Exception as e:
            logger.error(f"Failed to import coordinates: {e}")
    
    def get_layout_info(self) -> Dict[str, any]:
        """
        Get information about the current layout.
        
        Returns:
            Dictionary with layout information
        """
        return {
            "total_agents": len(self.coordinates),
            "agent_ids": list(self.coordinates.keys()),
            "bounds": {
                "min_x": min(coords["x"] for coords in self.coordinates.values()),
                "max_x": max(coords["x"] for coords in self.coordinates.values()),
                "min_y": min(coords["y"] for coords in self.coordinates.values()),
                "max_y": max(coords["y"] for coords in self.coordinates.values())
            },
            "config_path": self.config_path
        }

def main():
    """Main function for testing the coordinate finder."""
    finder = CoordinateFinder()
    
    # Test getting coordinates
    coords = finder.get_coordinates("agent-1")
    if coords:
        print(f"Agent-1 coordinates: {coords}")
    
    # Test setting coordinates
    finder.set_coordinates("agent-1", 150, 150)
    
    # Test validation
    invalid = finder.validate_coordinates()
    if invalid:
        print(f"Invalid coordinates for: {invalid}")
    
    # Get layout info
    layout = finder.get_layout_info()
    print("Layout info:", json.dumps(layout, indent=2))

if __name__ == "__main__":
    main() 
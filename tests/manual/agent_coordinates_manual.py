#!/usr/bin/env python3
"""
Test script for 8-Agent Coordinate System
Tests the coordinate calculation and agent positioning functionality
"""

import json
from pathlib import Path

def test_coordinate_calculation():
    """Test coordinate calculation for 8-agent layout"""
    print("🧪 Testing 8-agent coordinate calculation...")
    
    try:
        from src.core.coordinate_system import calculate_agent_coordinates
        
        # Test with 8 agents
        coordinates = calculate_agent_coordinates(8)
        print(f"✅ Calculated coordinates for 8 agents")
        
        for i, coord in enumerate(coordinates):
            print(f"   Agent-{i+1}: ({coord['x']}, {coord['y']})")
            
    except Exception as e:
        print(f"❌ Error calculating coordinates: {e}")

def test_agent_positioning():
    """Test agent positioning in 8-agent layout"""
    print("\n🧪 Testing agent positioning...")
    
    try:
        from src.core.agent_positioning import position_agents
        
        # Test positioning 8 agents
        positions = position_agents(8)
        print(f"✅ Positioned {len(positions)} agents")
        
        for agent, pos in positions.items():
            print(f"   {agent}: x={pos['x']}, y={pos['y']}, width={pos['width']}, height={pos['height']}")
            
    except Exception as e:
        print(f"❌ Error positioning agents: {e}")

def test_layout_validation():
    """Test layout validation for different agent counts"""
    print("\n🧪 Testing layout validation...")
    
    try:
        from src.core.layout_validator import validate_layout
        
        # Test valid layouts
        valid_counts = [2, 4, 8]
        for count in valid_counts:
            is_valid = validate_layout(count)
            print(f"   {count} agents: {'✅ Valid' if is_valid else '❌ Invalid'}")
            
        # Test invalid layouts
        invalid_counts = [1, 3, 5, 6, 7, 9]
        for count in invalid_counts:
            is_valid = validate_layout(count)
            print(f"   {count} agents: {'✅ Valid' if is_valid else '❌ Invalid'}")
            
    except Exception as e:
        print(f"❌ Error validating layouts: {e}")

def test_coordinate_file_loading():
    """Test loading coordinate configuration from file"""
    print("\n🧪 Testing coordinate file loading...")
    
    coord_file = Path("runtime/agent_comms/cursor_agent_coords.json")
    if coord_file.exists():
        try:
            with open(coord_file, 'r') as f:
                coords = json.load(f)
            print(f"✅ Loaded coordinate file: {len(coords)} agent configurations")
            
            for agent, config in coords.items():
                x = config.get('x', 'unknown')
                y = config.get('y', 'unknown')
                print(f"   {agent}: ({x}, {y})")
                
        except Exception as e:
            print(f"❌ Error loading coordinate file: {e}")
    else:
        print(f"⚠️  Coordinate file not found: {coord_file}")

def test_agent_communication_zones():
    """Test agent communication zone calculations"""
    print("\n🧪 Testing communication zones...")
    
    try:
        from src.core.communication_zones import calculate_communication_zones
        
        # Test with sample agent positions
        agent_positions = {
            "Agent-1": {"x": 0, "y": 0, "width": 800, "height": 600},
            "Agent-2": {"x": 800, "y": 0, "width": 800, "height": 600},
            "Agent-3": {"x": 0, "y": 600, "width": 800, "height": 600},
            "Agent-4": {"x": 800, "y": 600, "width": 800, "height": 600}
        }
        
        zones = calculate_communication_zones(agent_positions)
        print(f"✅ Calculated communication zones for {len(zones)} agents")
        
        for agent, zone in zones.items():
            print(f"   {agent}: overlap={zone['overlap']}, neighbors={zone['neighbors']}")
            
    except Exception as e:
        print(f"❌ Error calculating communication zones: {e}")

def test_full_coordinate_workflow():
    """Test the complete coordinate workflow"""
    print("\n🧪 Testing complete coordinate workflow...")
    
    try:
        from src.core.coordinate_system import calculate_agent_coordinates
        from src.core.agent_positioning import position_agents
        from src.core.layout_validator import validate_layout
        
        # Test with 8 agents
        agent_count = 8
        
        # Validate layout
        is_valid = validate_layout(agent_count)
        print(f"✅ Layout validation for {agent_count} agents: {'Valid' if is_valid else 'Invalid'}")
        
        if is_valid:
            # Calculate coordinates
            coordinates = calculate_agent_coordinates(agent_count)
            print(f"✅ Calculated {len(coordinates)} coordinates")
            
            # Position agents
            positions = position_agents(agent_count)
            print(f"✅ Positioned {len(positions)} agents")
            
            # Display results
            for i in range(agent_count):
                agent_name = f"Agent-{i+1}"
                coord = coordinates[i]
                pos = positions[agent_name]
                print(f"   {agent_name}: coord=({coord['x']}, {coord['y']}), pos=({pos['x']}, {pos['y']})")
        else:
            print("⚠️  Skipping coordinate calculation for invalid layout")
            
    except Exception as e:
        print(f"❌ Error in coordinate workflow: {e}")

if __name__ == "__main__":
    print("🧪 Running 8-Agent Coordinate System Tests\n")
    print("=" * 50)
    
    test_coordinate_calculation()
    test_agent_positioning()
    test_layout_validation()
    test_coordinate_file_loading()
    test_agent_communication_zones()
    test_full_coordinate_workflow()
    
    print("\n" + "=" * 50)
    print("✅ All coordinate tests completed!")

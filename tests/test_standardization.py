#!/usr/bin/env python3
"""
Test script for Agent Status Standardization
Tests the standardization functionality for agent status and metadata
"""

import json
from pathlib import Path

def test_status_standardization():
    """Test agent status standardization"""
    print("🧪 Testing agent status standardization...")
    
    try:
        from src.core.status_standardizer import standardize_agent_status
        
        # Test with sample status data
        sample_status = {
            "agent_id": "Agent-1",
            "status": "active",
            "last_seen": "2025-08-16T10:00:00Z",
            "metadata": {
                "workspace": "D:/repos/project-A",
                "cursor_version": "0.45.0"
            }
        }
        
        standardized = standardize_agent_status(sample_status)
        print(f"✅ Standardized status for {standardized['agent_id']}")
        print(f"   Status: {standardized['status']}")
        print(f"   Last seen: {standardized['last_seen']}")
        print(f"   Metadata keys: {list(standardized['metadata'].keys())}")
        
    except Exception as e:
        print(f"❌ Error standardizing status: {e}")

def test_metadata_validation():
    """Test metadata validation"""
    print("\n🧪 Testing metadata validation...")
    
    try:
        from src.core.metadata_validator import validate_metadata
        
        # Test valid metadata
        valid_metadata = {
            "workspace": "D:/repos/project-A",
            "cursor_version": "0.45.0",
            "os": "Windows",
            "python_version": "3.11.0"
        }
        
        is_valid = validate_metadata(valid_metadata)
        print(f"✅ Valid metadata: {'Valid' if is_valid else 'Invalid'}")
        
        # Test invalid metadata
        invalid_metadata = {
            "workspace": "",  # Empty workspace
            "cursor_version": "invalid_version"
        }
        
        is_valid = validate_metadata(invalid_metadata)
        print(f"   Invalid metadata: {'Valid' if is_valid else 'Invalid'}")
        
    except Exception as e:
        print(f"❌ Error validating metadata: {e}")

def test_status_file_loading():
    """Test loading status files"""
    print("\n🧪 Testing status file loading...")
    
    status_dir = Path("runtime/agent_monitors")
    if status_dir.exists():
        try:
            # Find status files
            status_files = list(status_dir.rglob("*.json"))
            print(f"✅ Found {len(status_files)} status files")
            
            for status_file in status_files[:5]:  # Show first 5
                try:
                    with open(status_file, 'r') as f:
                        status_data = json.load(f)
                    agent_name = status_file.parent.name
                    print(f"   {agent_name}: {status_data.get('status', 'unknown')}")
                except Exception as e:
                    print(f"   {status_file.name}: Error reading - {e}")
                    
        except Exception as e:
            print(f"❌ Error scanning status directory: {e}")
    else:
        print(f"⚠️  Status directory not found: {status_dir}")

def test_status_aggregation():
    """Test status aggregation across agents"""
    print("\n🧪 Testing status aggregation...")
    
    try:
        from src.core.status_aggregator import aggregate_agent_statuses
        
        # Test with sample agent statuses
        agent_statuses = {
            "Agent-1": {"status": "active", "last_seen": "2025-08-16T10:00:00Z"},
            "Agent-2": {"status": "idle", "last_seen": "2025-08-16T09:55:00Z"},
            "Agent-3": {"status": "active", "last_seen": "2025-08-16T10:02:00Z"},
            "Agent-4": {"status": "offline", "last_seen": "2025-08-16T09:30:00Z"}
        }
        
        aggregated = aggregate_agent_statuses(agent_statuses)
        print(f"✅ Aggregated status for {len(agent_statuses)} agents")
        print(f"   Active: {aggregated['active']}")
        print(f"   Idle: {aggregated['idle']}")
        print(f"   Offline: {aggregated['offline']}")
        print(f"   Total: {aggregated['total']}")
        
    except Exception as e:
        print(f"❌ Error aggregating statuses: {e}")

def test_status_persistence():
    """Test status persistence functionality"""
    print("\n🧪 Testing status persistence...")
    
    try:
        from src.core.status_persistence import save_agent_status, load_agent_status
        
        # Test saving status
        test_status = {
            "agent_id": "Test-Agent",
            "status": "testing",
            "last_seen": "2025-08-16T10:00:00Z",
            "metadata": {"test": True}
        }
        
        save_agent_status(test_status)
        print("✅ Status saved successfully")
        
        # Test loading status
        loaded_status = load_agent_status("Test-Agent")
        if loaded_status:
            print(f"✅ Status loaded: {loaded_status['status']}")
        else:
            print("⚠️  Status not found after save")
            
    except Exception as e:
        print(f"❌ Error with status persistence: {e}")

def test_full_standardization_workflow():
    """Test the complete standardization workflow"""
    print("\n🧪 Testing complete standardization workflow...")
    
    try:
        from src.core.status_standardizer import standardize_agent_status
        from src.core.metadata_validator import validate_metadata
        from src.core.status_aggregator import aggregate_agent_statuses
        
        # Sample agent data
        agents = {
            "Agent-1": {
                "status": "active",
                "last_seen": "2025-08-16T10:00:00Z",
                "metadata": {"workspace": "D:/repos/project-A", "cursor_version": "0.45.0"}
            },
            "Agent-2": {
                "status": "idle",
                "last_seen": "2025-08-16T09:55:00Z",
                "metadata": {"workspace": "D:/repos/project-B", "cursor_version": "0.45.0"}
            }
        }
        
        # Standardize each agent
        standardized_agents = {}
        for agent_id, status in agents.items():
            standardized = standardize_agent_status(status)
            if validate_metadata(standardized.get('metadata', {})):
                standardized_agents[agent_id] = standardized
                print(f"✅ {agent_id}: Standardized and validated")
            else:
                print(f"⚠️  {agent_id}: Standardized but metadata invalid")
        
        # Aggregate statuses
        if standardized_agents:
            aggregated = aggregate_agent_statuses(standardized_agents)
            print(f"✅ Workflow complete: {aggregated['total']} agents processed")
        else:
            print("⚠️  No agents processed successfully")
            
    except Exception as e:
        print(f"❌ Error in standardization workflow: {e}")

if __name__ == "__main__":
    print("🧪 Running Agent Status Standardization Tests\n")
    print("=" * 50)
    
    test_status_standardization()
    test_metadata_validation()
    test_status_file_loading()
    test_status_aggregation()
    test_status_persistence()
    test_full_standardization_workflow()
    
    print("\n" + "=" * 50)
    print("✅ All standardization tests completed!")

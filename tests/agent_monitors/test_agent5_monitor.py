#!/usr/bin/env python3
"""
Contract Tests for Agent-5 Monitor
==================================
Tests that prove the production monitor works correctly:
- Stall detection triggers rescue messages
- Cooldown prevents spam
- File activity updates are detected
"""

import time
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import pytest

# Import the monitor
try:
    from src.agent_monitors.agent5_monitor import Agent5Monitor, MonitorConfig
except ImportError:
    # Fallback for test environment
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from src.agent_monitors.agent5_monitor import Agent5Monitor, MonitorConfig

class DummyACP:
    """Mock AgentCellPhone for testing"""
    def __init__(self):
        self.sent = []
        self.available_agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]
    
    def send(self, agent, content, tag, new_chat=False):
        self.sent.append({
            "agent": agent,
            "content": content,
            "tag": tag,
            "new_chat": new_chat,
            "timestamp": time.time()
        })
    
    def get_available_agents(self):
        return self.available_agents

class TestAgent5Monitor:
    """Test suite for Agent-5 monitor"""
    
    def setup_method(self):
        """Setup before each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.agent_workspace = Path(self.temp_dir) / "agent_workspaces"
        self.agent_workspace.mkdir(parents=True)
        
        # Create test agent directories
        for agent in ["Agent-1", "Agent-2", "Agent-3"]:
            agent_dir = self.agent_workspace / agent
            agent_dir.mkdir()
            
            # Create initial state.json
            state_file = agent_dir / "state.json"
            state_file.write_text(json.dumps({
                "agent": agent,
                "status": "active",
                "updated": "2025-01-01T00:00:00Z"
            }))
    
    def teardown_method(self):
        """Cleanup after each test"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_stall_detection_triggers_rescue(self):
        """Test that stalled agents receive rescue messages"""
        # Configure monitor with short stall threshold for testing
        cfg = MonitorConfig(
            agents=["Agent-1", "Agent-2"],
            stall_threshold_sec=1,  # 1 second for testing
            check_every_sec=1,
            file_watch_root=str(self.agent_workspace),
            rescue_cooldown_sec=0  # No cooldown for testing
        )
        
        # Create monitor with mock ACP
        monitor = Agent5Monitor(cfg, test=True)
        monitor.acp = DummyACP()
        
        # Simulate Agent-1 being stalled (no recent activity)
        monitor.last_activity["Agent-1"] = time.time() - 5  # 5 seconds ago
        
        # Run one tick
        monitor._tick()
        
        # Verify rescue was sent
        assert len(monitor.acp.sent) == 1, "Rescue message should have been sent"
        assert monitor.acp.sent[0]["agent"] == "Agent-1", "Rescue should be sent to stalled agent"
        assert "[RESCUE]" in monitor.acp.sent[0]["content"], "Message should contain rescue content"
    
    def test_rescue_cooldown_prevents_spam(self):
        """Test that rescue cooldown prevents duplicate messages"""
        cfg = MonitorConfig(
            agents=["Agent-1"],
            stall_threshold_sec=1,
            check_every_sec=1,
            file_watch_root=str(self.agent_workspace),
            rescue_cooldown_sec=10  # 10 second cooldown
        )
        
        monitor = Agent5Monitor(cfg, test=True)
        monitor.acp = DummyACP()
        
        # Simulate stalled agent
        monitor.last_activity["Agent-1"] = time.time() - 5
        
        # First tick should send rescue
        monitor._tick()
        assert len(monitor.acp.sent) == 1, "First rescue should be sent"
        
        # Second tick should not send rescue (cooldown)
        monitor._tick()
        assert len(monitor.acp.sent) == 1, "Second rescue should be blocked by cooldown"
    
    def test_file_activity_updates_timestamp(self):
        """Test that file modifications update activity timestamps"""
        cfg = MonitorConfig(
            agents=["Agent-1"],
            file_watch_root=str(self.agent_workspace),
            check_every_sec=1
        )
        
        monitor = Agent5Monitor(cfg, test=True)
        monitor.acp = DummyACP()
        
        # Set initial activity to old timestamp
        old_time = time.time() - 100
        monitor.last_activity["Agent-1"] = old_time
        
        # Update a file to trigger activity
        agent1_dir = self.agent_workspace / "Agent-1"
        response_file = agent1_dir / "response.txt"
        response_file.write_text("Test response")
        
        # Wait a moment for file system
        time.sleep(0.1)
        
        # Run tick to update activity
        monitor._tick()
        
        # Verify activity timestamp was updated
        new_time = monitor.last_activity["Agent-1"]
        assert new_time > old_time, "Activity timestamp should be updated"
    
    def test_state_restoration_on_restart(self):
        """Test that monitor state is restored after restart"""
        cfg = MonitorConfig(
            agents=["Agent-1"],
            file_watch_root=str(self.agent_workspace)
        )
        
        # Create first monitor instance
        monitor1 = Agent5Monitor(cfg, test=True)
        monitor1.acp = DummyACP()
        
        # Set some activity data
        monitor1.last_activity["Agent-1"] = time.time() - 50
        monitor1.last_rescue["Agent-1"] = time.time() - 30
        
        # Persist state
        monitor1._persist_state()
        
        # Create second monitor instance (simulating restart)
        monitor2 = Agent5Monitor(cfg, test=True)
        monitor2.acp = DummyACP()
        
        # Restore state
        monitor2._restore_state()
        
        # Verify state was restored
        assert "Agent-1" in monitor2.last_activity, "Activity should be restored"
        assert "Agent-1" in monitor2.last_rescue, "Rescue timestamps should be restored"
    
    def test_health_and_metrics_writing(self):
        """Test that health and metrics are written correctly"""
        cfg = MonitorConfig(
            agents=["Agent-1"],
            file_watch_root=str(self.agent_workspace)
        )
        
        monitor = Agent5Monitor(cfg, test=True)
        monitor.acp = DummyACP()
        
        # Run a tick to generate metrics
        monitor._tick()
        
        # Check that health file was written
        health_file = Path("runtime/agent_monitors/agent5/health.json")
        assert health_file.exists(), "Health file should be written"
        
        # Check that metrics file was written
        metrics_file = Path("runtime/agent_monitors/agent5/metrics.json")
        assert metrics_file.exists(), "Metrics file should be written"
        
        # Verify health content
        health_data = json.loads(health_file.read_text())
        assert health_data["ok"] is True, "Health should show running"
        assert "running" in health_data["note"], "Health note should indicate running"
        
        # Verify metrics content
        metrics_data = json.loads(metrics_file.read_text())
        assert "agents" in metrics_data, "Metrics should contain agent data"
        assert "Agent-1" in metrics_data["agents"], "Metrics should include Agent-1"

def test_monitor_config_defaults():
    """Test that MonitorConfig has sensible defaults"""
    cfg = MonitorConfig(agents=["Agent-1"])
    
    assert cfg.stall_threshold_sec == 1200, "Default stall threshold should be 20 minutes"
    assert cfg.check_every_sec == 5, "Default check interval should be 5 seconds"
    assert cfg.rescue_cooldown_sec == 300, "Default rescue cooldown should be 5 minutes"
    assert cfg.active_grace_sec == 300, "Default active grace should be 5 minutes"

def test_monitor_config_environment_override():
    """Test that environment variables override defaults"""
    import os
    
    # Set environment variables
    os.environ["AGENT_STALL_SEC"] = "600"
    os.environ["AGENT_CHECK_SEC"] = "10"
    
    try:
        # Create config (should pick up environment variables)
        cfg = MonitorConfig(agents=["Agent-1"])
        
        # Verify overrides
        assert cfg.stall_threshold_sec == 600, "Environment should override stall threshold"
        assert cfg.check_every_sec == 10, "Environment should override check interval"
        
    finally:
        # Clean up environment
        if "AGENT_STALL_SEC" in os.environ:
            del os.environ["AGENT_STALL_SEC"]
        if "AGENT_CHECK_SEC" in os.environ:
            del os.environ["AGENT_CHECK_SEC"]

if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v"])

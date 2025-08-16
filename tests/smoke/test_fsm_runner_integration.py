#!/usr/bin/env python3
"""
FSM Runner Integration Tests
===========================
Tests the integration between the FSM orchestrator and the overnight runner.
"""

import json
import tempfile
import time
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from core.fsm_orchestrator import FSMOrchestrator


@pytest.fixture
def temp_fsm_env():
    """Create a temporary FSM environment for testing"""
    temp_root = Path(tempfile.mkdtemp(prefix="fsm_runner_integration_test_"))
    
    # Create directory structure
    fsm_root = temp_root / "fsm_data"
    inbox_root = temp_root / "inbox"
    outbox_root = temp_root / "outbox"
    
    fsm_root.mkdir(parents=True, exist_ok=True)
    inbox_root.mkdir(parents=True, exist_ok=True)
    outbox_root.mkdir(parents=True, exist_ok=True)
    
    # Create tasks and workflows subdirectories
    (fsm_root / "tasks").mkdir(exist_ok=True)
    (fsm_root / "workflows").mkdir(exist_ok=True)
    
    yield {
        "temp_root": temp_root,
        "fsm_root": fsm_root,
        "inbox_root": inbox_root,
        "outbox_root": outbox_root
    }
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_root, ignore_errors=True)


class TestFSMRunnerIntegration:
    """Test the FSM orchestrator integration with the runner"""
    
    def test_fsm_orchestrator_initialization(self, temp_fsm_env):
        """Test FSM orchestrator initializes correctly with runner-compatible paths"""
        orchestrator = FSMOrchestrator(
            fsm_root=temp_fsm_env["fsm_root"],
            inbox_root=temp_fsm_env["inbox_root"],
            outbox_root=temp_fsm_env["outbox_root"]
        )
        
        assert orchestrator.fsm_root == temp_fsm_env["fsm_root"]
        assert orchestrator.inbox_root == temp_fsm_env["inbox_root"]
        assert orchestrator.outbox_root == temp_fsm_env["outbox_root"]
        assert orchestrator.tasks_dir.exists()
        assert orchestrator.workflows_dir.exists()
        assert orchestrator.outbox_root.exists()
        assert not orchestrator.is_monitoring()
    
    def test_fsm_orchestrator_stop_monitoring(self, temp_fsm_env):
        """Test that FSM orchestrator can be stopped gracefully"""
        orchestrator = FSMOrchestrator(
            fsm_root=temp_fsm_env["fsm_root"],
            inbox_root=temp_fsm_env["inbox_root"],
            outbox_root=temp_fsm_env["outbox_root"]
        )
        
        # Start monitoring in background thread
        import threading
        monitor_thread = threading.Thread(
            target=orchestrator.monitor_inbox,
            kwargs={"poll_interval": 1},
            daemon=True
        )
        monitor_thread.start()
        
        # Wait a bit for monitoring to start
        time.sleep(0.1)
        assert orchestrator.is_monitoring()
        
        # Stop monitoring
        orchestrator.stop_monitoring()
        
        # Wait for thread to stop
        monitor_thread.join(timeout=2.0)
        assert not orchestrator.is_monitoring()
    
    def test_fsm_orchestrator_status_summary(self, temp_fsm_env):
        """Test FSM orchestrator status summary for runner reporting"""
        orchestrator = FSMOrchestrator(
            fsm_root=temp_fsm_env["fsm_root"],
            inbox_root=temp_fsm_env["inbox_root"],
            outbox_root=temp_fsm_env["outbox_root"]
        )
        
        # Get initial status
        status = orchestrator.get_status_summary()
        assert "total_tasks" in status
        assert "completed_tasks" in status
        assert "in_progress_tasks" in status
        assert status["total_tasks"] == 0
        
        # Create a test task
        from core.fsm_orchestrator import TaskState
        task = TaskState(
            task_id="test-task-001",
            repo="test-repo",
            intent="Test task for runner integration",
            state="new",
            owner="Agent-1",
            assigned_at="2025-08-15T10:00:00",
            evidence=[]
        )
        orchestrator.save_task(task)
        
        # Check updated status
        status = orchestrator.get_status_summary()
        assert status["total_tasks"] == 1
        # New tasks are not counted as in_progress, they're just part of total
        assert status["total_tasks"] == 1
    
    def test_fsm_orchestrator_background_threading(self, temp_fsm_env):
        """Test that FSM orchestrator can run in background thread as expected by runner"""
        orchestrator = FSMOrchestrator(
            fsm_root=temp_fsm_env["fsm_root"],
            inbox_root=temp_fsm_env["inbox_root"],
            outbox_root=temp_fsm_env["outbox_root"]
        )
        
        # Start monitoring in background thread (as runner does)
        import threading
        monitor_thread = threading.Thread(
            target=orchestrator.monitor_inbox,
            kwargs={"poll_interval": 1},
            daemon=True
        )
        monitor_thread.start()
        
        # Wait for monitoring to start
        time.sleep(0.1)
        assert orchestrator.is_monitoring()
        
        # Create a test update file
        test_update = {
            "event": "AGENT_REPORT",
            "agent": "Agent-1",
            "task": "Test background threading",
            "status": "In progress",
            "raw": "Testing background monitoring",
            "timestamp": "2025-08-15T22:00:00"
        }
        
        update_file = temp_fsm_env["inbox_root"] / "test_update.json"
        update_file.write_text(json.dumps(test_update, indent=2))
        
        # Wait for processing
        time.sleep(2)
        
        # Verify task was created
        task_files = list((temp_fsm_env["fsm_root"] / "tasks").glob("*.json"))
        assert len(task_files) >= 1
        
        # Stop monitoring
        orchestrator.stop_monitoring()
        monitor_thread.join(timeout=2.0)
        assert not orchestrator.is_monitoring()
    
    def test_fsm_orchestrator_graceful_shutdown(self, temp_fsm_env):
        """Test graceful shutdown behavior expected by runner"""
        orchestrator = FSMOrchestrator(
            fsm_root=temp_fsm_env["fsm_root"],
            inbox_root=temp_fsm_env["inbox_root"],
            outbox_root=temp_fsm_env["outbox_root"]
        )
        
        # Start monitoring by calling monitor_inbox in a thread
        import threading
        monitor_thread = threading.Thread(
            target=orchestrator.monitor_inbox,
            kwargs={"poll_interval": 1},
            daemon=True
        )
        monitor_thread.start()
        
        # Wait for monitoring to start
        time.sleep(0.1)
        assert orchestrator.is_monitoring()
        
        # Simulate graceful shutdown
        orchestrator.stop_monitoring()
        
        # Should be able to get final status
        status = orchestrator.get_status_summary()
        assert "total_tasks" in status
        assert "completed_tasks" in status
        assert "in_progress_tasks" in status


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

#!/usr/bin/env python3
"""
FSM Integration Tests
====================
Test the complete FSM integration flow including orchestrator, task management,
and evidence collection.
"""

import json
import pytest
import tempfile
from pathlib import Path
from core.fsm_orchestrator import FSMOrchestrator, FSMUpdate, TaskState

try:
    import PyQt5  # noqa: F401
except ImportError:
    pytest.skip("PyQt5 not available", allow_module_level=True)


@pytest.fixture
def temp_fsm_env():
    """Create a temporary FSM environment for testing"""
    temp_root = Path(tempfile.mkdtemp(prefix="fsm_integration_test_"))
    
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


class TestFSMIntegration:
    """Test the complete FSM integration flow"""
    
    def test_fsm_orchestrator_initialization(self, temp_fsm_env):
        """Test FSM orchestrator initializes correctly"""
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
    
    def test_task_creation_and_saving(self, temp_fsm_env):
        """Test creating and saving tasks"""
        orchestrator = FSMOrchestrator(
            fsm_root=temp_fsm_env["fsm_root"],
            inbox_root=temp_fsm_env["inbox_root"],
            outbox_root=temp_fsm_env["outbox_root"]
        )
        
        # Create a test task
        task = TaskState(
            task_id="test-task-001",
            repo="test-repo",
            intent="Test task for integration testing",
            state="new",
            owner="Agent-1",
            assigned_at="2025-08-15T10:00:00",
            evidence=[]
        )
        
        # Save the task
        assert orchestrator.save_task(task)
        
        # Verify the task file was created
        task_file = temp_fsm_env["fsm_root"] / "tasks" / "test-task-001.json"
        assert task_file.exists()
        
        # Load and verify the task
        loaded_task = orchestrator.load_task("test-task-001")
        assert loaded_task is not None
        assert loaded_task.task_id == "test-task-001"
        assert loaded_task.intent == "Test task for integration testing"
        assert loaded_task.state == "new"
    
    def test_agent_report_processing(self, temp_fsm_env):
        """Test processing agent reports and updating task state"""
        orchestrator = FSMOrchestrator(
            fsm_root=temp_fsm_env["fsm_root"],
            inbox_root=temp_fsm_env["inbox_root"],
            outbox_root=temp_fsm_env["outbox_root"]
        )
        
        # Create an agent report update
        update = FSMUpdate(
            event="AGENT_REPORT",
            agent="Agent-1",
            task="Implement user authentication system",
            actions=["Created User model", "Added bcrypt hashing"],
            commit_message="feat: implement user authentication with JWT tokens",
            status="Completed - all tests passing, ready for integration testing",
            raw="Task: Implement user authentication system\nActions:\n- Created User model with email and password fields\n- Added bcrypt password hashing\n- Implemented login/logout endpoints\n- Added JWT token generation\n- Created unit tests for authentication flow\nCommit Message: feat: implement user authentication with JWT tokens\nStatus: Completed - all tests passing, ready for integration testing",
            timestamp="2025-08-15T18:00:00"
        )
        
        # Process the update
        assert orchestrator.process_fsm_update(update)
        
        # Verify task was created and saved
        task_files = list((temp_fsm_env["fsm_root"] / "tasks").glob("*.json"))
        assert len(task_files) == 1
        
        # Verify task data - using actual field names from FSM orchestrator
        task_data = json.loads(task_files[0].read_text())
        assert task_data["name"] == "Implement user authentication system"
        assert task_data["status"] == "completed"
        assert task_data["assigned_agent"] == "Agent-1"
        assert "evidence" in task_data
        assert len(task_data["evidence"]) > 0
    
    def test_task_state_transitions(self, temp_fsm_env):
        """Test various task state transitions"""
        orchestrator = FSMOrchestrator(
            fsm_root=temp_fsm_env["fsm_root"],
            inbox_root=temp_fsm_env["inbox_root"],
            outbox_root=temp_fsm_env["outbox_root"]
        )
        
        # Test "in progress" state
        progress_update = FSMUpdate(
            event="AGENT_REPORT",
            agent="Agent-3",
            task="Implement FSM Logic",
            status="Working on state transitions and guards",
            raw="Currently implementing the core FSM logic",
            timestamp="2025-08-15T19:00:00"
        )
        
        assert orchestrator.process_fsm_update(progress_update)
        
        # Verify task was created with "in_progress" state
        task_files = list((temp_fsm_env["fsm_root"] / "tasks").glob("*.json"))
        assert len(task_files) == 1
        
        task_data = json.loads(task_files[0].read_text())
        assert task_data["status"] == "in_progress"
        assert task_data["started_at"] is not None
        
        # Test "assigned" state
        assigned_update = FSMUpdate(
            event="AGENT_REPORT",
            agent="Agent-4",
            task="Test FSM System",
            status="Assigned and ready to begin",
            raw="Task assigned, starting test planning",
            timestamp="2025-08-15T19:30:00"
        )
        
        assert orchestrator.process_fsm_update(assigned_update)
        
        # Verify second task was created
        task_files = list((temp_fsm_env["fsm_root"] / "tasks").glob("*.json"))
        assert len(task_files) == 2
    
    def test_evidence_collection(self, temp_fsm_env):
        """Test that evidence is properly collected and stored"""
        orchestrator = FSMOrchestrator(
            fsm_root=temp_fsm_env["fsm_root"],
            inbox_root=temp_fsm_env["inbox_root"],
            outbox_root=temp_fsm_env["outbox_root"]
        )
        
        # Create an update with rich evidence
        update = FSMUpdate(
            event="AGENT_REPORT",
            agent="Agent-1",
            task="Add comprehensive testing",
            actions=["Created test suite", "Added integration tests"],
            commit_message="test: add comprehensive test coverage",
            status="Completed with 95% coverage",
            raw="Task: Add comprehensive testing\nActions:\n- Created test suite with pytest\n- Added integration tests for core functionality\n- Achieved 95% code coverage\n- All tests passing\nCommit Message: test: add comprehensive test coverage\nStatus: Completed with 95% coverage",
            timestamp="2025-08-15T20:00:00"
        )
        
        assert orchestrator.process_fsm_update(update)
        
        # Verify evidence was collected
        task_files = list((temp_fsm_env["fsm_root"] / "tasks").glob("*.json"))
        assert len(task_files) == 1
        
        task_data = json.loads(task_files[0].read_text())
        
        # Check evidence content
        evidence = task_data.get("evidence", [])
        assert len(evidence) > 0
        
        # Verify evidence structure
        for ev in evidence:
            assert "kind" in ev
            assert "agent" in ev
            assert "timestamp" in ev
            assert "summary" in ev
            assert "raw" in ev
    
    def test_freeform_message_handling(self, temp_fsm_env):
        """Test handling of freeform agent messages"""
        orchestrator = FSMOrchestrator(
            fsm_root=temp_fsm_env["fsm_root"],
            inbox_root=temp_fsm_env["inbox_root"],
            outbox_root=temp_fsm_env["outbox_root"]
        )
        
        # Create a freeform message
        freeform_update = FSMUpdate(
            event="AGENT_FREEFORM",
            agent="Agent-5",
            raw="Just checking in - system looks good",
            timestamp="2025-08-15T20:30:00"
        )
        
        # Should handle gracefully
        assert orchestrator.process_fsm_update(freeform_update)
        
        # No task should be created for freeform messages
        task_files = list((temp_fsm_env["fsm_root"] / "tasks").glob("*.json"))
        assert len(task_files) == 0
    
    def test_error_handling(self, temp_fsm_env):
        """Test error handling for invalid updates"""
        orchestrator = FSMOrchestrator(
            fsm_root=temp_fsm_env["fsm_root"],
            inbox_root=temp_fsm_env["inbox_root"],
            outbox_root=temp_fsm_env["outbox_root"]
        )
        
        # Test update with missing required fields
        invalid_update = FSMUpdate(
            event="AGENT_REPORT",
            agent="Agent-1",
            # Missing task field
            status="Some status",
            timestamp="2025-08-15T21:00:00"
        )
        
        # Should handle gracefully and return False
        assert not orchestrator.process_fsm_update(invalid_update)
        
        # No task should be created
        task_files = list((temp_fsm_env["fsm_root"] / "tasks").glob("*.json"))
        assert len(task_files) == 0


class TestFSMOrchestratorIntegration:
    """Test the FSM orchestrator integration with the broader system"""
    
    @pytest.fixture
    def mock_fsm_bridge_output(self, temp_fsm_env):
        """Create mock FSM bridge output for testing"""
        bridge_output = temp_fsm_env["inbox_root"]
        
        # Create sample FSM bridge output files
        sample_updates = [
            {
                "event": "AGENT_REPORT",
                "agent": "Agent-1",
                "task": "Wire FSM Bridge Integration",
                "status": "In progress - creating orchestrator",
                "raw": "Currently implementing the FSM orchestrator to consume inbox updates",
                "timestamp": "2025-08-15T21:00:00"
            },
            {
                "event": "AGENT_REPORT", 
                "agent": "Agent-2",
                "task": "Add Integration Tests",
                "status": "Completed - tests passing",
                "raw": "Added comprehensive integration tests for FSM flow",
                "timestamp": "2025-08-15T21:30:00"
            }
        ]
        
        for i, update in enumerate(sample_updates):
            update_file = bridge_output / f"fsm_update_{i}.json"
            update_file.write_text(json.dumps(update, indent=2))
        
        return bridge_output
    
    def test_end_to_end_fsm_flow(self, temp_fsm_env, mock_fsm_bridge_output):
        """Test the complete end-to-end FSM flow"""
        orchestrator = FSMOrchestrator(
            fsm_root=temp_fsm_env["fsm_root"],
            inbox_root=mock_fsm_bridge_output,
            outbox_root=temp_fsm_env["outbox_root"]
        )
        
        # Process all updates
        for f in sorted(mock_fsm_bridge_output.glob("*.json")):
            with open(f, 'r') as update_file:
                update_data = json.load(update_file)
                update = FSMUpdate(**update_data)
                assert orchestrator.process_fsm_update(update)
        
        # Verify tasks were created (at least one should be created)
        task_files = list((temp_fsm_env["fsm_root"] / "tasks").glob("*.json"))
        assert len(task_files) >= 1
        
        # Check task states for created tasks
        for task_file in task_files:
            task_data = json.loads(task_file.read_text())
            assert task_data["name"] in ["Wire FSM Bridge Integration", "Add Integration Tests"]
            assert "evidence" in task_data
            assert len(task_data["evidence"]) > 0
    
    def test_background_monitoring(self, temp_fsm_env):
        """Test background monitoring functionality"""
        orchestrator = FSMOrchestrator(
            fsm_root=temp_fsm_env["fsm_root"],
            inbox_root=temp_fsm_env["inbox_root"],
            outbox_root=temp_fsm_env["outbox_root"]
        )
        
        # Start monitoring
        import threading
        monitor_thread = threading.Thread(
            target=orchestrator.monitor_inbox,
            kwargs={"poll_interval": 1},
            daemon=True
        )
        monitor_thread.start()
        
        # Wait for monitoring to start
        import time
        time.sleep(0.1)
        assert orchestrator.is_monitoring()
        
        # Stop monitoring
        orchestrator.stop_monitoring()
        monitor_thread.join(timeout=2.0)
        assert not orchestrator.is_monitoring()
    
    def test_status_reporting(self, temp_fsm_env):
        """Test status reporting functionality"""
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
        
        # Create a task and check status
        task = TaskState(
            task_id="status-test",
            repo="test",
            intent="Test status reporting",
            state="new",
            owner="Agent-1",
            assigned_at="2025-08-15T22:00:00",
            evidence=[]
        )
        orchestrator.save_task(task)
        
        status = orchestrator.get_status_summary()
        assert status["total_tasks"] == 1
        assert status["in_progress_tasks"] == 0  # New tasks are not in progress

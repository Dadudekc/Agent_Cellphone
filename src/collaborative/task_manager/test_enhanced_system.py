#!/usr/bin/env python3
"""
Test Suite for Enhanced Collaborative System

**Purpose**: Validate enhanced task breakdown and workflow optimization systems
**Coverage**: 
- Task breakdown functionality
- Workflow optimization
- System integration
- Performance metrics
- Resource allocation

This test suite ensures the enhanced collaborative system works correctly
and provides the expected optimization capabilities.
"""

import unittest
import tempfile
import shutil
import json
import time
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock

# Import systems to test
from .enhanced_task_breakdown import (
    EnhancedTaskBreakdown, TaskBreakdown, TaskComponent, 
    TaskComplexity, TaskPriority, TaskType, AgentCapability
)
from .workflow_optimizer import (
    WorkflowOptimizer, CollaborativeWorkflow, WorkflowStage,
    WorkflowMetric, WorkflowPattern, WorkflowOptimization
)
from .enhanced_collaborative_system import (
    EnhancedCollaborativeSystem, CollaborationSession, 
    CollaborationMode, SystemMetrics, OptimizationResult
)

class TestEnhancedTaskBreakdown(unittest.TestCase):
    """Test cases for Enhanced Task Breakdown system"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.task_breakdown = EnhancedTaskBreakdown(self.test_dir)

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_dir)

    def test_create_agent_capability_profile(self):
        """Test creating agent capability profile"""
        capability = self.task_breakdown.create_agent_capability_profile(
            agent_id="Agent-1",
            primary_skills=["python", "analysis"],
            secondary_skills=["documentation"],
            experience_level=0.8,
            collaboration_preference=["Agent-2", "Agent-3"]
        )
        
        self.assertEqual(capability.agent_id, "Agent-1")
        self.assertEqual(capability.primary_skills, ["python", "analysis"])
        self.assertEqual(capability.experience_level, 0.8)
        self.assertEqual(capability.collaboration_preference, ["Agent-2", "Agent-3"])

    def test_breakdown_complex_task(self):
        """Test breaking down a complex task"""
        # Create agent capabilities first
        self.task_breakdown.create_agent_capability_profile(
            agent_id="Agent-1",
            primary_skills=["python", "development"],
            secondary_skills=[],
            experience_level=0.9
        )
        
        self.task_breakdown.create_agent_capability_profile(
            agent_id="Agent-2",
            primary_skills=["testing", "analysis"],
            secondary_skills=[],
            experience_level=0.7
        )
        
        # Break down complex task
        breakdown = self.task_breakdown.breakdown_complex_task(
            task_id="TASK_001",
            title="Build Web Application",
            description="Create a full-stack web application",
            estimated_hours=12.0,
            required_skills=["python", "javascript", "testing", "analysis"]
        )
        
        self.assertEqual(breakdown.original_title, "Build Web Application")
        self.assertEqual(breakdown.total_estimated_hours, 12.0)
        self.assertGreater(len(breakdown.components), 1)
        self.assertGreater(breakdown.optimization_score, 0.0)

    def test_task_complexity_determination(self):
        """Test task complexity determination"""
        trivial = self.task_breakdown._determine_complexity(1.5)
        simple = self.task_breakdown._determine_complexity(3.0)
        moderate = self.task_breakdown._determine_complexity(6.0)
        complex_task = self.task_breakdown._determine_complexity(12.0)
        very_complex = self.task_breakdown._determine_complexity(20.0)
        
        self.assertEqual(trivial, TaskComplexity.TRIVIAL)
        self.assertEqual(simple, TaskComplexity.SIMPLE)
        self.assertEqual(moderate, TaskComplexity.MODERATE)
        self.assertEqual(complex_task, TaskComplexity.COMPLEX)
        self.assertEqual(very_complex, TaskComplexity.VERY_COMPLEX)

    def test_component_generation(self):
        """Test task component generation"""
        components = self.task_breakdown._generate_task_components(
            task_id="TASK_001",
            title="Test Task",
            description="Test description",
            estimated_hours=8.0,
            required_skills=["python", "testing"],
            complexity=TaskComplexity.MODERATE,
            priority=TaskPriority.NORMAL
        )
        
        self.assertEqual(len(components), 3)  # MODERATE complexity = 3 components
        
        for component in components:
            self.assertIsInstance(component, TaskComponent)
            self.assertEqual(component.parent_task_id, "TASK_001")
            self.assertIn(component.task_type, [TaskType.DEVELOPMENT, TaskType.TESTING])

    def test_resource_allocation_optimization(self):
        """Test resource allocation optimization"""
        # Create agent capabilities
        self.task_breakdown.create_agent_capability_profile(
            agent_id="Agent-1",
            primary_skills=["python"],
            secondary_skills=[],
            experience_level=0.9
        )
        
        self.task_breakdown.create_agent_capability_profile(
            agent_id="Agent-2",
            primary_skills=["testing"],
            secondary_skills=[],
            experience_level=0.7
        )
        
        # Create components
        components = [
            TaskComponent(
                component_id="comp1",
                parent_task_id="task1",
                title="Python Development",
                description="Develop Python code",
                task_type=TaskType.DEVELOPMENT,
                complexity=TaskComplexity.SIMPLE,
                priority=TaskPriority.NORMAL,
                estimated_hours=4.0,
                required_skills=["python"],
                dependencies=[],
                assigned_agent=None,
                status="pending",
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            ),
            TaskComponent(
                component_id="comp2",
                parent_task_id="task1",
                title="Testing",
                description="Test the application",
                task_type=TaskType.TESTING,
                complexity=TaskComplexity.SIMPLE,
                priority=TaskPriority.NORMAL,
                estimated_hours=4.0,
                required_skills=["testing"],
                dependencies=[],
                assigned_agent=None,
                status="pending",
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
        ]
        
        # Optimize resource allocation
        allocation = self.task_breakdown._optimize_resource_allocation(components)
        
        self.assertIn("Agent-1", allocation)
        self.assertIn("Agent-2", allocation)
        self.assertEqual(components[0].assigned_agent, "Agent-1")
        self.assertEqual(components[1].assigned_agent, "Agent-2")

class TestWorkflowOptimizer(unittest.TestCase):
    """Test cases for Workflow Optimizer system"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.workflow_optimizer = WorkflowOptimizer(self.test_dir)

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_dir)

    def test_create_collaborative_workflow(self):
        """Test creating collaborative workflow"""
        workflow = self.workflow_optimizer.create_collaborative_workflow(
            title="Test Workflow",
            description="Test workflow description",
            participants=["Agent-1", "Agent-2"],
            dependencies=[]
        )
        
        self.assertEqual(workflow.title, "Test Workflow")
        self.assertEqual(workflow.current_stage, WorkflowStage.INITIATION)
        self.assertEqual(workflow.participants, ["Agent-1", "Agent-2"])
        self.assertEqual(len(workflow.stages), 6)

    def test_add_workflow_metric(self):
        """Test adding workflow metrics"""
        workflow = self.workflow_optimizer.create_collaborative_workflow(
            title="Test Workflow",
            description="Test description",
            participants=["Agent-1"]
        )
        
        metric = self.workflow_optimizer.add_workflow_metric(
            workflow_id=workflow.workflow_id,
            metric_type="execution_time",
            value=2.5,
            unit="hours",
            context={"phase": "development"}
        )
        
        self.assertEqual(metric.metric_type, "execution_time")
        self.assertEqual(metric.value, 2.5)
        self.assertEqual(metric.unit, "hours")
        
        # Check that workflow was updated
        updated_workflow = self.workflow_optimizer._workflow_cache[workflow.workflow_id]
        self.assertEqual(len(updated_workflow.metrics), 1)
        self.assertGreater(updated_workflow.efficiency_score, 0.0)

    def test_workflow_stage_advancement(self):
        """Test workflow stage advancement"""
        workflow = self.workflow_optimizer.create_collaborative_workflow(
            title="Test Workflow",
            description="Test description",
            participants=["Agent-1"]
        )
        
        # Advance through stages
        self.assertTrue(self.workflow_optimizer.advance_workflow_stage(workflow.workflow_id))
        self.assertEqual(workflow.current_stage, WorkflowStage.PLANNING)
        
        self.assertTrue(self.workflow_optimizer.advance_workflow_stage(workflow.workflow_id))
        self.assertEqual(workflow.current_stage, WorkflowStage.EXECUTION)

    def test_workflow_efficiency_calculation(self):
        """Test workflow efficiency calculation"""
        workflow = self.workflow_optimizer.create_collaborative_workflow(
            title="Test Workflow",
            description="Test description",
            participants=["Agent-1"]
        )
        
        # Add metrics to improve efficiency
        self.workflow_optimizer.add_workflow_metric(
            workflow_id=workflow.workflow_id,
            metric_type="execution_time",
            value=1.0,
            unit="hours"
        )
        
        self.workflow_optimizer.add_workflow_metric(
            workflow_id=workflow.workflow_id,
            metric_type="quality_score",
            value=85.0,
            unit="percentage"
        )
        
        # Check efficiency calculation
        updated_workflow = self.workflow_optimizer._workflow_cache[workflow.workflow_id]
        self.assertGreater(updated_workflow.efficiency_score, 0.0)

    def test_optimization_recommendations(self):
        """Test optimization recommendation generation"""
        workflow = self.workflow_optimizer.create_collaborative_workflow(
            title="Test Workflow",
            description="Test description",
            participants=["Agent-1", "Agent-2", "Agent-3", "Agent-4"]
        )
        
        # Add some metrics
        self.workflow_optimizer.add_workflow_metric(
            workflow_id=workflow.workflow_id,
            metric_type="execution_time",
            value=5.0,
            unit="hours"
        )
        
        # Generate recommendations
        recommendations = self.workflow_optimizer.generate_optimization_recommendations(workflow.workflow_id)
        
        self.assertGreater(len(recommendations), 0)
        
        # Check that recommendations were added to workflow
        updated_workflow = self.workflow_optimizer._workflow_cache[workflow.workflow_id]
        self.assertEqual(len(updated_workflow.optimizations), len(recommendations))

class TestEnhancedCollaborativeSystem(unittest.TestCase):
    """Test cases for Enhanced Collaborative System integration"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.collaborative_system = EnhancedCollaborativeSystem(self.test_dir)

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_dir)

    def test_create_collaboration_session(self):
        """Test creating collaboration session"""
        session = self.collaborative_system.create_collaboration_session(
            title="Test Session",
            description="Test session description",
            participants=["Agent-1", "Agent-2", "Agent-3"],
            mode=CollaborationMode.OPTIMIZED
        )
        
        self.assertEqual(session.title, "Test Session")
        self.assertEqual(session.mode, CollaborationMode.OPTIMIZED)
        self.assertEqual(len(session.participants), 3)
        self.assertEqual(session.efficiency_score, 0.0)

    def test_add_task_to_session(self):
        """Test adding task to collaboration session"""
        session = self.collaborative_system.create_collaboration_session(
            title="Test Session",
            description="Test description",
            participants=["Agent-1", "Agent-2"]
        )
        
        # Create agent capabilities first
        self.collaborative_system.task_breakdown.create_agent_capability_profile(
            agent_id="Agent-1",
            primary_skills=["python"],
            secondary_skills=[],
            experience_level=0.8
        )
        
        self.collaborative_system.task_breakdown.create_agent_capability_profile(
            agent_id="Agent-2",
            primary_skills=["testing"],
            secondary_skills=[],
            experience_level=0.7
        )
        
        # Add task to session
        breakdown, workflow = self.collaborative_system.add_task_to_session(
            session_id=session.session_id,
            task_id="TASK_001",
            title="Build Application",
            description="Build a test application",
            estimated_hours=8.0,
            required_skills=["python", "testing"],
            priority="high"
        )
        
        self.assertIsInstance(breakdown, TaskBreakdown)
        self.assertIsInstance(workflow, CollaborativeWorkflow)
        self.assertEqual(breakdown.original_title, "Build Application")
        
        # Check session was updated
        updated_session = self.collaborative_system._session_cache[session.session_id]
        self.assertEqual(len(updated_session.task_breakdowns), 1)
        self.assertEqual(len(updated_session.workflows), 1)

    def test_session_optimization(self):
        """Test session collaboration optimization"""
        session = self.collaborative_system.create_collaboration_session(
            title="Test Session",
            description="Test description",
            participants=["Agent-1", "Agent-2"]
        )
        
        # Create agent capabilities
        self.collaborative_system.task_breakdown.create_agent_capability_profile(
            agent_id="Agent-1",
            primary_skills=["python"],
            secondary_skills=[],
            experience_level=0.8
        )
        
        self.collaborative_system.task_breakdown.create_agent_capability_profile(
            agent_id="Agent-2",
            primary_skills=["testing"],
            secondary_skills=[],
            experience_level=0.7
        )
        
        # Add task to session
        self.collaborative_system.add_task_to_session(
            session_id=session.session_id,
            task_id="TASK_001",
            title="Build Application",
            description="Build a test application",
            estimated_hours=8.0,
            required_skills=["python", "testing"],
            priority="high"
        )
        
        # Optimize session
        optimization_result = self.collaborative_system.optimize_session_collaboration(session.session_id)
        
        self.assertIsInstance(optimization_result, OptimizationResult)
        self.assertEqual(optimization_result.session_id, session.session_id)
        self.assertGreaterEqual(optimization_result.improvement, 0.0)

    def test_system_metrics(self):
        """Test system metrics functionality"""
        session = self.collaborative_system.create_collaboration_session(
            title="Test Session",
            description="Test description",
            participants=["Agent-1"]
        )
        
        # Add system metric
        metric = self.collaborative_system.add_system_metric(
            session_id=session.session_id,
            metric_type="collaboration_efficiency",
            value=0.85,
            unit="percentage",
            context={"phase": "planning"},
            impact_score=0.7
        )
        
        self.assertEqual(metric.metric_type, "collaboration_efficiency")
        self.assertEqual(metric.value, 0.85)
        self.assertEqual(metric.impact_score, 0.7)
        
        # Check session was updated
        updated_session = self.collaborative_system._session_cache[session.session_id]
        self.assertEqual(len(updated_session.performance_metrics), 1)

    def test_performance_summary(self):
        """Test performance summary generation"""
        session = self.collaborative_system.create_collaboration_session(
            title="Test Session",
            description="Test description",
            participants=["Agent-1", "Agent-2"]
        )
        
        # Create agent capabilities
        self.collaborative_system.task_breakdown.create_agent_capability_profile(
            agent_id="Agent-1",
            primary_skills=["python"],
            secondary_skills=[],
            experience_level=0.8
        )
        
        self.collaborative_system.task_breakdown.create_agent_capability_profile(
            agent_id="Agent-2",
            primary_skills=["testing"],
            secondary_skills=[],
            experience_level=0.7
        )
        
        # Add task to session
        self.collaborative_system.add_task_to_session(
            session_id=session.session_id,
            task_id="TASK_001",
            title="Build Application",
            description="Build a test application",
            estimated_hours=8.0,
            required_skills=["python", "testing"],
            priority="high"
        )
        
        # Get performance summary
        summary = self.collaborative_system.get_session_performance_summary(session.session_id)
        
        self.assertEqual(summary["session_id"], session.session_id)
        self.assertEqual(summary["title"], "Test Session")
        self.assertEqual(len(summary["workflows"]), 1)
        self.assertEqual(len(summary["task_breakdowns"]), 1)
        self.assertIn("performance_indicators", summary)
        self.assertIn("collaboration_effectiveness", summary)

    def test_system_summary(self):
        """Test system-wide summary generation"""
        # Create multiple sessions
        session1 = self.collaborative_system.create_collaboration_session(
            title="Session 1",
            description="First session",
            participants=["Agent-1"]
        )
        
        session2 = self.collaborative_system.create_collaboration_session(
            title="Session 2",
            description="Second session",
            participants=["Agent-2"]
        )
        
        # Get system summary
        system_summary = self.collaborative_system.get_system_summary()
        
        self.assertEqual(system_summary["total_sessions"], 2)
        self.assertEqual(system_summary["active_sessions"], 2)
        self.assertEqual(system_summary["completed_sessions"], 0)
        self.assertIn("performance_distribution", system_summary)
        self.assertIn("collaboration_mode_distribution", system_summary)

    def test_session_completion(self):
        """Test session completion"""
        session = self.collaborative_system.create_collaboration_session(
            title="Test Session",
            description="Test description",
            participants=["Agent-1"]
        )
        
        # Complete session
        self.assertTrue(self.collaborative_system.complete_session(session.session_id))
        
        # Check session was updated
        updated_session = self.collaborative_system._session_cache[session.session_id]
        self.assertIsNotNone(updated_session.end_time)
        self.assertIsNotNone(updated_session.efficiency_score)

def run_tests():
    """Run all tests"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_suite.addTest(unittest.makeSuite(TestEnhancedTaskBreakdown))
    test_suite.addTest(unittest.makeSuite(TestWorkflowOptimizer))
    test_suite.addTest(unittest.makeSuite(TestEnhancedCollaborativeSystem))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"TEST SUMMARY")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)

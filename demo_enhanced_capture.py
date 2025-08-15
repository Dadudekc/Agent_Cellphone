#!/usr/bin/env python3
"""
Enhanced Response Capture Demo
==============================
Demonstrates the restored advanced response capture system
with cursor database monitoring and workflow integration
"""

import sys
import time
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def demo_enhanced_capture():
    """Demonstrate the enhanced response capture system"""
    print("🚀 **ENHANCED RESPONSE CAPTURE DEMO**")
    print("=" * 50)
    
    try:
        # Import the enhanced capture system
        from services.enhanced_response_capture import (
            EnhancedResponseCapture, 
            EnhancedCaptureConfig,
            CaptureStrategy
        )
        
        print("✅ Enhanced capture system imported successfully")
        
        # Create configuration
        config = EnhancedCaptureConfig(
            primary_strategy=CaptureStrategy.CURSOR_DB,
            fallback_strategies=[
                CaptureStrategy.EXPORT_CHAT,
                CaptureStrategy.COPY_RESPONSE,
                CaptureStrategy.FILE
            ],
            workflow_inbox="agent_workspaces/Agent-5/inbox",
            fsm_inbox="runtime/agent_comms/inbox"
        )
        
        print(f"✅ Configuration created: {config.primary_strategy.value}")
        
        # Mock coordinates for demo
        coords = {
            "Agent-1": {"input_box": {"x": 100, "y": 100}},
            "Agent-2": {"input_box": {"x": 200, "y": 100}},
            "Agent-3": {"input_box": {"x": 300, "y": 100}},
            "Agent-4": {"input_box": {"x": 400, "y": 100}},
            "Agent-5": {"input_box": {"x": 500, "y": 100}}
        }
        
        # Create enhanced capture instance
        capture = EnhancedResponseCapture(coords, config)
        
        print(f"✅ Enhanced capture initialized: {capture.is_capture_enabled()}")
        print(f"📊 Available strategies: {list(capture.strategies.keys())}")
        
        # Add response callback
        def on_response(response):
            print(f"🎯 [CALLBACK] Response from {response.agent}: {response.text[:50]}...")
            print(f"   📊 Analysis: {response.analysis}")
        
        capture.add_response_callback(on_response)
        
        # Start capture for agents
        for agent in ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]:
            capture.start_for(agent)
            print(f"✅ Started capture for {agent}")
        
        print("\n🔄 **CAPTURE SYSTEM RUNNING**")
        print("The system is now monitoring:")
        print("  • Cursor database (real-time)")
        print("  • Export chat files")
        print("  • Clipboard responses") 
        print("  • Response.txt files")
        print("\n📤 **DUAL OUTPUT ROUTING**")
        print("  • Workflow Engine: agent_workspaces/Agent-5/inbox")
        print("  • FSM Bridge: runtime/agent_comms/inbox")
        
        # Let it run for a bit
        print("\n⏳ Running capture for 10 seconds...")
        time.sleep(10)
        
        # Stop capture
        capture.stop_all()
        print("✅ Capture stopped")
        
        # Show captured responses
        responses = capture.get_responses()
        print(f"\n📊 **CAPTURED RESPONSES: {len(responses)}**")
        for i, resp in enumerate(responses):
            print(f"  {i+1}. {resp.agent}: {resp.text[:100]}...")
            print(f"     Source: {resp.source} | Analysis: {resp.analysis}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure the enhanced capture system is properly installed")
        return False
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        return False

def demo_workflow_integration():
    """Demonstrate workflow engine integration"""
    print("\n🎭 **WORKFLOW ENGINE INTEGRATION DEMO**")
    print("=" * 50)
    
    try:
        from advanced_workflows.workflow_engine import WorkflowEngine, WorkflowStep
        
        print("✅ Workflow engine imported successfully")
        
        # Create a simple workflow
        engine = WorkflowEngine("demo_workflow")
        
        # Add steps
        step1 = WorkflowStep(
            id="assess_swarm",
            name="Assess SWARM Repository",
            description="Evaluate SWARM project status and identify next steps",
            agent_target="Agent-1",
            prompt_template="Assess the current state of the SWARM repository. What's the next priority?",
            expected_response_type="goal_assessment",
            timeout_seconds=300
        )
        
        step2 = WorkflowStep(
            id="implement_feature",
            name="Implement Feature",
            description="Implement the identified priority feature",
            agent_target="Agent-2", 
            prompt_template="Implement the priority feature identified by Agent-1",
            expected_response_type="task_execution",
            timeout_seconds=600,
            dependencies=["assess_swarm"]
        )
        
        engine.add_step(step1)
        engine.add_step(step2)
        
        print(f"✅ Workflow created with {len(engine.steps)} steps")
        print(f"📋 Steps: {[step.name for step in engine.steps]}")
        
        # Show workflow structure
        print("\n🔗 **WORKFLOW STRUCTURE**")
        for step in engine.steps:
            deps = ", ".join(step.dependencies) if step.dependencies else "none"
            print(f"  • {step.name} (→ {step.agent_target}) [deps: {deps}]")
        
        return True
        
    except ImportError as e:
        print(f"❌ Workflow import error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Workflow demo error: {e}")
        return False

def main():
    """Run the complete demo"""
    print("🎯 **COMPREHENSIVE ENHANCED CAPTURE DEMO**")
    print("=" * 60)
    
    # Demo 1: Enhanced Capture System
    success1 = demo_enhanced_capture()
    
    # Demo 2: Workflow Integration  
    success2 = demo_workflow_integration()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 **DEMO SUMMARY**")
    print(f"  Enhanced Capture: {'✅ SUCCESS' if success1 else '❌ FAILED'}")
    print(f"  Workflow Integration: {'✅ SUCCESS' if success2 else '❌ FAILED'}")
    
    if success1 and success2:
        print("\n🎉 **ALL SYSTEMS OPERATIONAL!**")
        print("The advanced response capture system is fully restored and integrated!")
        print("\n🚀 **WHAT'S NOW WORKING:**")
        print("  • Real-time Cursor database monitoring")
        print("  • Advanced response analysis (sentiment, tasks, conversation)")
        print("  • Dual output routing (workflow + FSM)")
        print("  • Workflow engine integration")
        print("  • Multi-strategy fallback system")
        
    else:
        print("\n⚠️ **SOME SYSTEMS NEED ATTENTION**")
        print("Check the error messages above to resolve issues")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()

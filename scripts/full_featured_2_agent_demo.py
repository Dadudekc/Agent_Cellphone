#!/usr/bin/env python3
"""
Full-Featured 2-Agent Demo for Dream.OS
=======================================
This script demonstrates all major features of the Dream.OS 2-agent mode system.
It is modular, well-commented, and guides the user through each capability step by step.

Usage:
    python scripts/full_featured_2_agent_demo.py

You can use this script for demos, onboarding, or system validation.
"""

import subprocess
import time
import sys
import os
import json
from pathlib import Path

def section(title, desc=None):
    print("\n" + "=" * 60)
    print(f"🎬 {title}")
    if desc:
        print(desc)
    print("=" * 60)
    input("Press Enter to continue...")

def run_cmd(cmd, explain=None, pause=True):
    print(f"\n$ {cmd}")
    if explain:
        print(f"# {explain}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print("--- Command Output ---")
    print(result.stdout.strip())
    if result.stderr:
        print("--- Errors ---")
        print(result.stderr.strip())
    if pause:
        input("(Press Enter to continue)")
    return result

def print_agent_status(agent_id):
    status_file = Path(f'agent_workspaces/{agent_id}/status.json')
    print(f"\n📋 {agent_id} status.json:")
    if status_file.exists():
        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                status = json.load(f)
            print(json.dumps(status, indent=2))
        except Exception as e:
            print(f"Could not read status for {agent_id}: {e}")
    else:
        print(f"No status.json found for {agent_id}")

def print_agent_log(agent_id, lines=10):
    log_dir = Path(f'agent_workspaces/{agent_id}/logs')
    if not log_dir.exists():
        print(f"No logs directory for {agent_id}")
        return
    log_files = sorted(log_dir.glob('*.log'), reverse=True)
    if not log_files:
        print(f"No log files for {agent_id}")
        return
    latest_log = log_files[0]
    print(f"\n📝 {agent_id} latest log: {latest_log.name}")
    try:
        with open(latest_log, 'r', encoding='utf-8') as f:
            log_lines = f.readlines()[-lines:]
        for line in log_lines:
            print(line.rstrip())
    except Exception as e:
        print(f"Could not read log for {agent_id}: {e}")

def print_agent_tasks(agent_id):
    tasks_dir = Path(f'agent_workspaces/{agent_id}/inbox/tasks')
    if not tasks_dir.exists():
        print(f"No tasks directory for {agent_id}")
        return
    task_files = sorted(tasks_dir.glob('*.json'))
    if not task_files:
        print(f"No tasks for {agent_id}")
        return
    print(f"\n🗂️ {agent_id} tasks:")
    for tf in task_files:
        try:
            with open(tf, 'r', encoding='utf-8') as f:
                task = json.load(f)
            print(f"- {tf.name}: {task.get('title', 'No title')}")
        except Exception as e:
            print(f"Could not read task {tf.name}: {e}")

def main():
    print("\n" + "#" * 60)
    print("FULL-FEATURED 2-AGENT DEMO - Dream.OS")
    print("#" * 60)
    print("This script will walk you through all major features of the 2-agent system.")
    print("You can observe the GUI and logs for real-time updates.")
    input("Press Enter to begin the demo...")

    # 1. System Overview
    section("SYSTEM OVERVIEW", "Dream.OS is a multi-agent system. Each agent has its own workspace, status, and capabilities. Agents communicate via structured messages and can be managed via the GUI or CLI.")
    print("Agents: Agent-1 (Coordinator), Agent-2 (Developer)")
    print("Key features: Agent management, messaging, onboarding, task assignment, system controls, document generation, monitoring, analytics.")
    input("(Observe the GUI, then press Enter to continue)")

    # 2. Agent Management
    section("AGENT MANAGEMENT", "Check status, ping, pause/resume, and show agent panels in the GUI.")
    run_cmd("python src/agent_cell_phone.py -a Agent-1 -m status -t command", "Check Agent-1 status")
    print_agent_status("Agent-1")
    run_cmd("python src/agent_cell_phone.py -a Agent-2 -m status -t command", "Check Agent-2 status")
    print_agent_status("Agent-2")
    run_cmd("python src/agent_cell_phone.py -a Agent-1 -m ping -t command", "Ping Agent-1")
    run_cmd("python src/agent_cell_phone.py -a Agent-2 -m ping -t command", "Ping Agent-2")
    print("You can also pause/resume agents from the GUI.")
    input("(Try pausing/resuming in the GUI, then press Enter)")

    # 3. Communication
    section("INTER-AGENT COMMUNICATION", "Send direct and broadcast messages between agents.")
    run_cmd("python src/agent_cell_phone.py -a Agent-2 -m 'Hello Agent-2! Ready to coordinate.' -t normal", "Agent-1 sends a message to Agent-2")
    run_cmd("python src/agent_cell_phone.py -a all -m 'System-wide broadcast: All agents, please report status.' -t broadcast", "Broadcast message to all agents")
    print_agent_status("Agent-2")
    print_agent_status("Agent-1")
    print("Observe message history in the GUI panels.")
    input("(Check the GUI for messages, then press Enter)")

    # 4. Task Management
    section("TASK MANAGEMENT", "Assign tasks, check progress, and complete tasks.")
    run_cmd("python src/agent_cell_phone.py -a Agent-1 -m 'task: Analyze requirements' -t command", "Assign a task to Agent-1")
    print_agent_tasks("Agent-1")
    run_cmd("python src/agent_cell_phone.py -a Agent-2 -m 'task: Implement feature X' -t command", "Assign a task to Agent-2")
    print_agent_tasks("Agent-2")
    print("You can view and update tasks in the agent workspaces and GUI.")
    input("(Check agent workspaces and GUI, then press Enter)")

    # 5. Onboarding
    section("ONBOARDING", "Showcase onboarding protocols: chunked vs comprehensive.")
    print("Sending comprehensive onboarding message to Agent-1...")
    run_cmd("python consolidated_onboarding.py --agent Agent-1 --style full", "Comprehensive onboarding (Agent-1)")
    print_agent_status("Agent-1")
    print("Sending chunked onboarding messages to Agent-2...")
    run_cmd("python consolidated_onboarding.py --agent Agent-2 --style ascii", "Chunked/ASCII onboarding (Agent-2)")
    print_agent_status("Agent-2")
    print("You can compare onboarding progress in the GUI and logs.")
    input("(Observe onboarding status, then press Enter)")

    # 6. System Management
    section("SYSTEM MANAGEMENT", "Restart system, coordinate mapping, and system status.")
    print("(Simulate system restart and coordinate mapping via GUI controls)")
    print("You can also run:")
    print("python src/agent_cell_phone.py -a all -m restart -t command")
    print("python src/agent_cell_phone.py -a all -m coordinates -t command")
    input("(Try these in the GUI or CLI, then press Enter)")

    # 7. Document Generation
    section("DOCUMENT GENERATION", "Generate and view resume templates and usage guides.")
    print("Resume templates and guides are available in the docs/ directory.")
    print("You can open docs/RESUME_TEMPLATES_SUMMARY.md, docs/COMPREHENSIVE_RESUME_TEMPLATE.md, etc.")
    input("(Open docs/ in your editor, then press Enter)")

    # 8. Monitoring & Analytics
    section("MONITORING & ANALYTICS", "View logs, performance metrics, and system health.")
    print_agent_log("Agent-1")
    print_agent_log("Agent-2")
    print("You can also run:")
    print("python src/agent_cell_phone.py -a Agent-1 -m 'get_metrics' -t command")
    print("python src/agent_cell_phone.py -a Agent-2 -m 'get_metrics' -t command")
    input("(Review logs and metrics, then press Enter)")

    # 9. Integration & Collaboration
    section("INTEGRATION & COLLABORATION", "Simulate a workflow: project kickoff, onboarding, task assignment, messaging, and completion.")
    print("1. Project kickoff: Agent-1 broadcasts project start.")
    run_cmd("python src/agent_cell_phone.py -a all -m 'Project kickoff: Welcome to the new sprint!' -t broadcast", "Project kickoff broadcast")
    print("2. Agent-1 assigns a task to Agent-2.")
    run_cmd("python src/agent_cell_phone.py -a Agent-2 -m 'task: Implement login feature' -t command", "Assign task to Agent-2")
    print_agent_tasks("Agent-2")
    print("3. Agent-2 sends status update.")
    run_cmd("python src/agent_cell_phone.py -a Agent-1 -m 'Status: Login feature 50% complete.' -t status", "Status update from Agent-2")
    print_agent_status("Agent-1")
    print("4. Agent-2 marks task complete.")
    run_cmd("python src/agent_cell_phone.py -a Agent-1 -m 'Status: Login feature complete.' -t status", "Task completion from Agent-2")
    print_agent_status("Agent-1")
    input("(Observe the workflow in the GUI and logs, then press Enter)")

    # 10. Final System Check
    section("FINAL SYSTEM CHECK", "Review all features and system health.")
    print("You have now seen all major features of Dream.OS 2-agent mode!")
    print("Check the GUI, logs, and docs for further exploration.")
    print("Thank you for using Dream.OS!")
    print("=" * 60)

if __name__ == "__main__":
    main()

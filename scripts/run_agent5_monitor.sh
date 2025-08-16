#!/bin/bash
# Agent-5 Monitor Runner for Linux/Mac
# ====================================
# This script runs the Agent-5 production monitor

echo "🤖 Starting Agent-5 Production Monitor..."
echo

# Set environment variables
export AGENT_STALL_SEC=1200
export AGENT_CHECK_SEC=5
export AGENT_FILE_ROOT=D:\\repos\\Dadudekc
export AGENT_FSM_ENABLED=1
export AGENT_RESCUE_COOLDOWN_SEC=300
export AGENT_ACTIVE_GRACE_SEC=300

echo "📊 Configuration:"
echo "   Stall threshold: $AGENT_STALL_SEC seconds"
echo "   Check interval: $AGENT_CHECK_SEC seconds"
echo "   File root: $AGENT_FILE_ROOT"
echo "   FSM enabled: $AGENT_FSM_ENABLED"
echo "   Rescue cooldown: $AGENT_RESCUE_COOLDOWN_SEC seconds"
echo "   Active grace: $AGENT_ACTIVE_GRACE_SEC seconds"
echo

# Run the monitor
python -m src.agent_monitors.agent5_monitor

echo
echo "✅ Agent-5 Monitor stopped."

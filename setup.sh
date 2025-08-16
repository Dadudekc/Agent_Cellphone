#!/usr/bin/env bash
# Simple setup script for Agent Cell Phone project
# Creates a virtual environment, installs dependencies, and prepares environment file

set -e

# Create virtual environment if not exists
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
  echo "Created virtual environment in .venv" 
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Copy env.example to .env if .env does not exist
if [ ! -f ".env" ] && [ -f "env.example" ]; then
  cp env.example .env
  echo "Created .env from env.example. Please review and update it." 
fi

echo "Setup complete. Activate the environment with 'source .venv/bin/activate'."

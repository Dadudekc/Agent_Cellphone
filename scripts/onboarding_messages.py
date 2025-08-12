#!/usr/bin/env python3
"""
REDIRECT: This script has been consolidated into consolidated_onboarding.py
================================================================

This file is a redirect to the new consolidated onboarding system.
The original functionality is now available in: scripts/consolidated_onboarding.py

Usage:
    python consolidated_onboarding.py --all

For more information, run:
    python consolidated_onboarding.py --help
"""

import sys
import subprocess
from pathlib import Path

# Explicit target for the consolidated script
target_script = "consolidated_onboarding.py"

def main():
    print("🔄 REDIRECTING to consolidated onboarding system...")
    print(f"📁 Original: onboarding_messages.py")
    print(f"🎯 Target: consolidated_onboarding.py")
    print("=" * 50)
    
    # Get the script directory
    script_dir = Path(__file__).parent
    target_path = script_dir / target_script
    
    if not target_path.exists():
        print(f"❌ Error: Target script consolidated_onboarding.py not found!")
        return 1
    
    # Build command (pass through original arguments unchanged)
    cmd = [sys.executable, str(target_path)] + sys.argv[1:]
    
    print("🚀 Running command...")
    print()
    
    # Execute the target script
    try:
        result = subprocess.run(cmd, cwd=script_dir.parent)
        return result.returncode
    except Exception:
        print("❌ Error executing target script")
        return 1

if __name__ == "__main__":
    sys.exit(main())

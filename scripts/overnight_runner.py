#!/usr/bin/env python3
"""
Overnight Runner – Agent Cell Phone scheduler
=============================================
Thin wrapper for overnight_runner.runner.main

Usage examples:
  python scripts/overnight_runner.py --layout 4-agent --agents Agent-1,Agent-2,Agent-3,Agent-4 \
      --interval-sec 900 --duration-min 480 --sender Agent-3

Quick test (no mouse/keyboard movement):
  python scripts/overnight_runner.py --layout 4-agent --iterations 1 --interval-sec 2 --test

Live single iteration sanity check:
  python scripts/overnight_runner.py --layout 4-agent --iterations 1 --interval-sec 2 --sender Agent-3
"""

import sys
from pathlib import Path

# Add src/ to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

if __name__ == "__main__":
    from overnight_runner.runner import main
    raise SystemExit(main())



from __future__ import annotations

import sys
from pathlib import Path

# Ensure project root and common source dirs are on sys.path so tests can import modules directly
project_root = Path(__file__).resolve().parents[1]
src_dir = project_root / "src"
src_audio_dir = src_dir / "audio"

for p in (project_root, src_dir, src_audio_dir):
    p_str = str(p)
    if p_str not in sys.path:
        sys.path.insert(0, p_str)



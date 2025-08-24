import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "harness_cli.py"


def run_cli(args):
    result = subprocess.run([sys.executable, str(SCRIPT), *args],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


def test_cli_broadcast():
    out = run_cli(["--mode", "broadcast", "--message", "hello", "--layout", "2-agent", "--test"])
    assert "Broadcast sent successfully" in out


def test_cli_individual():
    out = run_cli(["--mode", "individual", "--message", "hi", "--target", "Agent-2", "--layout", "2-agent", "--test"])
    assert "Message sent successfully" in out

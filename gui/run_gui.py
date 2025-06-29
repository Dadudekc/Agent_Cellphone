#!/usr/bin/env python3
"""
Dream.OS Cell Phone GUI Launcher
Simple launcher for the main PyQt GUI
"""

import sys
import subprocess

def main():
    """Launch the Dream.OS Cell Phone GUI."""
    print("🚀 Launching Dream.OS Cell Phone GUI...")
    print("📱 Starting PyQt interface...")
    
    try:
        # Run the main GUI
        subprocess.run([sys.executable, "dream_os_gui.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching GUI: {e}")
        print("💡 Make sure PyQt5 is installed: pip install PyQt5")
    except FileNotFoundError:
        print("❌ GUI file not found: dream_os_gui.py")
        print("💡 Make sure you're in the correct directory")
    except KeyboardInterrupt:
        print("\n👋 GUI closed by user")

if __name__ == "__main__":
    main() 
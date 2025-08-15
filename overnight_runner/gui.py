#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox


class RunnerGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Overnight Runner Control")
        self.root.geometry("560x360")

        self.listener_proc: subprocess.Popen | None = None
        self.runner_proc: subprocess.Popen | None = None

        # Controls
        row = 0

        tk.Label(root, text="Layout").grid(row=row, column=0, sticky="w")
        self.layout_var = tk.StringVar(value="5-agent")
        tk.Entry(root, textvariable=self.layout_var, width=16).grid(row=row, column=1, sticky="w")

        tk.Label(root, text="Captain").grid(row=row, column=2, sticky="w")
        self.captain_var = tk.StringVar(value="Agent-5")
        tk.Entry(root, textvariable=self.captain_var, width=16).grid(row=row, column=3, sticky="w")
        row += 1

        tk.Label(root, text="Resume Agents (comma)").grid(row=row, column=0, sticky="w")
        self.resume_var = tk.StringVar(value="Agent-1,Agent-2,Agent-3,Agent-4")
        tk.Entry(root, textvariable=self.resume_var, width=40).grid(row=row, column=1, columnspan=3, sticky="we")
        row += 1

        tk.Label(root, text="Sender").grid(row=row, column=0, sticky="w")
        self.sender_var = tk.StringVar(value="Agent-3")
        tk.Entry(root, textvariable=self.sender_var, width=16).grid(row=row, column=1, sticky="w")

        tk.Label(root, text="Plan").grid(row=row, column=2, sticky="w")
        self.plan_var = tk.StringVar(value="contracts")
        tk.Entry(root, textvariable=self.plan_var, width=16).grid(row=row, column=3, sticky="w")
        row += 1

        tk.Label(root, text="Interval (sec)").grid(row=row, column=0, sticky="w")
        self.interval_var = tk.StringVar(value="300")
        tk.Entry(root, textvariable=self.interval_var, width=16).grid(row=row, column=1, sticky="w")

        tk.Label(root, text="Duration (min)").grid(row=row, column=2, sticky="w")
        self.duration_var = tk.StringVar(value="60")
        tk.Entry(root, textvariable=self.duration_var, width=16).grid(row=row, column=3, sticky="w")
        row += 1

        tk.Label(root, text="Comms Root").grid(row=row, column=0, sticky="w")
        self.comms_var = tk.StringVar(value=self._default_comms_root())
        tk.Entry(root, textvariable=self.comms_var, width=40).grid(row=row, column=1, columnspan=3, sticky="we")
        row += 1

        # Listener controls
        tk.Label(root, text="Listener Agent").grid(row=row, column=0, sticky="w")
        self.listener_agent_var = tk.StringVar(value="Agent-5")
        tk.Entry(root, textvariable=self.listener_agent_var, width=16).grid(row=row, column=1, sticky="w")
        tk.Button(root, text="Start Listener", command=self.start_listener).grid(row=row, column=2, sticky="we")
        tk.Button(root, text="Stop Listener", command=self.stop_listener).grid(row=row, column=3, sticky="we")
        row += 1

        # Runner controls
        self.test_mode = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Test mode (no typing)", variable=self.test_mode).grid(row=row, column=0, columnspan=2, sticky="w")
        tk.Button(root, text="Start Runner", command=self.start_runner).grid(row=row, column=2, sticky="we")
        tk.Button(root, text="Stop Runner", command=self.stop_runner).grid(row=row, column=3, sticky="we")
        row += 1

        # Calibrate and onboarding
        tk.Label(root, text="Calibrate Agent").grid(row=row, column=0, sticky="w")
        self.calib_agent_var = tk.StringVar(value="Agent-5")
        tk.Entry(root, textvariable=self.calib_agent_var, width=16).grid(row=row, column=1, sticky="w")
        tk.Button(root, text="Calibrate", command=self.calibrate_agent).grid(row=row, column=2, sticky="we")
        tk.Button(root, text="Open Onboarding", command=self.open_onboarding).grid(row=row, column=3, sticky="we")
        row += 1

        # Status
        self.status_var = tk.StringVar(value="Idle")
        tk.Label(root, textvariable=self.status_var, anchor="w").grid(row=row, column=0, columnspan=4, sticky="we", pady=8)

        for c in range(4):
            root.grid_columnconfigure(c, weight=1)

    def _default_comms_root(self) -> str:
        from datetime import datetime
        d = datetime.now().strftime("%Y%m%d")
        return f"D:/repositories/communications/overnight_{d}_"

    def _python(self) -> str:
        return sys.executable or "python"

    def start_listener(self) -> None:
        if self.listener_proc and self.listener_proc.poll() is None:
            messagebox.showinfo("Listener", "Listener already running")
            return
        agent = self.listener_agent_var.get().strip() or "Agent-5"
        cmd = [self._python(), "overnight_runner/listener.py", "--agent", agent]
        self.listener_proc = subprocess.Popen(cmd, cwd=str(Path(__file__).resolve().parents[1]))
        self.status_var.set(f"Listener started for {agent}")

    def stop_listener(self) -> None:
        if self.listener_proc and self.listener_proc.poll() is None:
            self.listener_proc.terminate()
            self.listener_proc = None
            self.status_var.set("Listener stopped")
        else:
            self.status_var.set("Listener not running")

    def start_runner(self) -> None:
        if self.runner_proc and self.runner_proc.poll() is None:
            messagebox.showinfo("Runner", "Runner already running")
            return
        layout = self.layout_var.get().strip() or "5-agent"
        captain = self.captain_var.get().strip() or "Agent-5"
        resume = self.resume_var.get().strip() or "Agent-1,Agent-2,Agent-3,Agent-4"
        sender = self.sender_var.get().strip() or "Agent-3"
        plan = self.plan_var.get().strip() or "contracts"
        interval = self.interval_var.get().strip() or "300"
        duration = self.duration_var.get().strip() or "60"
        comms = self.comms_var.get().strip() or self._default_comms_root()
        Path(comms).mkdir(parents=True, exist_ok=True)
        args = [
            self._python(), "overnight_runner/runner.py",
            "--layout", layout,
            "--captain", captain,
            "--resume-agents", resume,
            "--sender", sender,
            "--interval-sec", interval,
            "--duration-min", duration,
            "--plan", plan,
            "--fsm-enabled", "--fsm-agent", captain, "--fsm-workflow", "default",
            "--initial-wait-sec", "10", "--phase-wait-sec", "5", "--stagger-ms", "1500", "--jitter-ms", "600",
            "--comm-root", comms, "--create-comm-folders",
        ]
        if self.test_mode.get():
            args.append("--test")
        self.runner_proc = subprocess.Popen(args, cwd=str(Path(__file__).resolve().parents[1]))
        self.status_var.set("Runner started")

    def stop_runner(self) -> None:
        if self.runner_proc and self.runner_proc.poll() is None:
            self.runner_proc.terminate()
            self.runner_proc = None
            self.status_var.set("Runner stopped")
        else:
            self.status_var.set("Runner not running")

    def calibrate_agent(self) -> None:
        layout = self.layout_var.get().strip() or "5-agent"
        agent = self.calib_agent_var.get().strip() or "Agent-5"
        cmd = [self._python(), "overnight_runner/tools/capture_coords.py", "--layout", layout, "--agent", agent, "--delay", "6"]
        try:
            subprocess.Popen(cmd, cwd=str(Path(__file__).resolve().parents[1]))
            self.status_var.set(f"Calibration started for {agent} ({layout})")
        except Exception as e:
            messagebox.showerror("Calibrate", str(e))

    def open_onboarding(self) -> None:
        root_dir = Path(__file__).resolve().parent / "onboarding"
        index = root_dir / "00_INDEX.md"
        try:
            if os.name == "nt":
                os.startfile(index)  # type: ignore[attr-defined]
            else:
                subprocess.Popen(["open", str(index)])
        except Exception:
            messagebox.showinfo("Onboarding", f"Open manually: {index}")


def main() -> int:
    root = tk.Tk()
    RunnerGUI(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



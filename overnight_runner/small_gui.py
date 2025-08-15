#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox


class SmallRunnerGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Overnight Runner – Quick Control")
        self.root.geometry("420x220")

        self.listener_proc: subprocess.Popen | None = None
        self.runner_proc: subprocess.Popen | None = None

        row = 0

        tk.Label(root, text="Workspace root").grid(row=row, column=0, sticky="w")
        self.ws_var = tk.StringVar(value="D:/repos/Dadudekc")
        tk.Entry(root, textvariable=self.ws_var, width=40).grid(row=row, column=1, columnspan=2, sticky="we")
        row += 1

        tk.Label(root, text="Assign root").grid(row=row, column=0, sticky="w")
        self.assign_root_var = tk.StringVar(value="D:/repos/Dadudekc")
        tk.Entry(root, textvariable=self.assign_root_var, width=40).grid(row=row, column=1, columnspan=2, sticky="we")
        row += 1

        # Listener controls
        tk.Label(root, text="Listener agent").grid(row=row, column=0, sticky="w")
        self.listener_agent_var = tk.StringVar(value="Agent-5")
        tk.Entry(root, textvariable=self.listener_agent_var, width=16).grid(row=row, column=1, sticky="w")
        tk.Button(root, text="Start Listener", command=self.start_listener).grid(row=row, column=2, sticky="we")
        row += 1
        tk.Button(root, text="Stop Listener", command=self.stop_listener).grid(row=row, column=2, sticky="we")
        row += 1

        # Runner controls
        tk.Label(root, text="Layout").grid(row=row, column=0, sticky="w")
        self.layout_var = tk.StringVar(value="5-agent")
        tk.Entry(root, textvariable=self.layout_var, width=16).grid(row=row, column=1, sticky="w")
        tk.Button(root, text="Start Runner", command=self.start_runner).grid(row=row, column=2, sticky="we")
        row += 1
        tk.Button(root, text="Stop Runner", command=self.stop_runner).grid(row=row, column=2, sticky="we")
        row += 1

        tk.Label(root, text="Agents (comma)").grid(row=row, column=0, sticky="w")
        self.agents_var = tk.StringVar(value="Agent-1,Agent-2,Agent-3,Agent-4")
        tk.Entry(root, textvariable=self.agents_var, width=40).grid(row=row, column=1, columnspan=2, sticky="we")
        row += 1

        tk.Button(root, text="Kick Prompts Now", command=self.kick_prompts).grid(row=row, column=1, sticky="we")
        tk.Button(root, text="Onboard Agents", command=self.onboard_agents).grid(row=row, column=2, sticky="we")
        row += 1

        # Control buttons
        tk.Button(root, text="Start Listener", command=self.start_listener).grid(row=row, column=0, sticky="we")
        tk.Button(root, text="Stop Listener", command=self.stop_listener).grid(row=row, column=1, sticky="we")
        tk.Button(root, text="Start Overnight Runner", command=self.start_runner).grid(row=row, column=2, sticky="we")
        row += 1
        tk.Button(root, text="Stop Runner", command=self.stop_runner).grid(row=row, column=1, sticky="we")
        row += 1

        # Logs
        tk.Button(root, text="Open Runner Log", command=self.open_runner_log).grid(row=row, column=1, sticky="we")
        tk.Button(root, text="Open Listener Log", command=self.open_listener_log).grid(row=row, column=2, sticky="we")
        row += 1

        # Status
        self.status_var = tk.StringVar(value="Idle")
        tk.Label(root, textvariable=self.status_var, anchor="w").grid(row=row, column=0, columnspan=3, sticky="we", pady=8)

        for c in range(3):
            root.grid_columnconfigure(c, weight=1)

    def _python(self) -> str:
        return sys.executable or "python"

    def start_listener(self) -> None:
        if self.listener_proc and self.listener_proc.poll() is None:
            messagebox.showinfo("Listener", "Listener already running")
            return
        agent = self.listener_agent_var.get().strip() or "Agent-5"
        # Use the forever script for resilience
        script = Path(__file__).resolve().parents[1] / "scripts" / "run_listener_forever.ps1"
        try:
            self.listener_proc = subprocess.Popen([
                "pwsh", "-NoProfile", "-File", str(script), "-Agent", agent
            ], cwd=str(Path(__file__).resolve().parents[1]))
            self.status_var.set(f"Listener loop started for {agent}")
        except Exception as e:
            messagebox.showerror("Listener", str(e))

    def stop_listener(self) -> None:
        try:
            # Best-effort: kill any python or pwsh processes running the listener scripts
            if os.name == "nt":
                subprocess.call(["powershell", "-NoProfile", "-Command",
                                  "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'listener' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"],
                                 cwd=str(Path(__file__).resolve().parents[1]))
        except Exception:
            pass
        if self.listener_proc and self.listener_proc.poll() is None:
            try:
                self.listener_proc.terminate()
            except Exception:
                pass
        self.listener_proc = None
        self.status_var.set("Listener stopped")

    def start_runner(self) -> None:
        if self.runner_proc and self.runner_proc.poll() is None:
            messagebox.showinfo("Runner", "Runner already running")
            return
        script = Path(__file__).resolve().parents[1] / "scripts" / "run_runner_forever.ps1"
        # Ensure env caps for new-chat are applied through this GUI session
        env = os.environ.copy()
        env.setdefault("ACP_MAX_NEW_CHATS_PER_AGENT", "6")
        try:
            self.runner_proc = subprocess.Popen([
                "pwsh", "-NoProfile", "-File", str(script)
            ], cwd=str(Path(__file__).resolve().parents[1]), env=env)
            self.status_var.set("Runner loop started")
        except Exception as e:
            messagebox.showerror("Runner", str(e))

    def stop_runner(self) -> None:
        try:
            if os.name == "nt":
                subprocess.call(["powershell", "-NoProfile", "-Command",
                                  "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'overnight_runner' -or $_.CommandLine -match 'run_runner_forever' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"],
                                 cwd=str(Path(__file__).resolve().parents[1]))
        except Exception:
            pass
        if self.runner_proc and self.runner_proc.poll() is None:
            try:
                self.runner_proc.terminate()
            except Exception:
                pass
        self.runner_proc = None
        self.status_var.set("Runner stopped")

    def open_runner_log(self) -> None:
        path = Path(__file__).resolve().parents[1] / "logs" / "runner.log"
        try:
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("", encoding="utf-8")
            if os.name == "nt":
                os.startfile(path)  # type: ignore[attr-defined]
        except Exception as e:
            messagebox.showinfo("Runner Log", f"Open manually: {path}\n{e}")

    def open_listener_log(self) -> None:
        path = Path(__file__).resolve().parents[1] / "logs" / "listener.log"
        try:
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("", encoding="utf-8")
            if os.name == "nt":
                os.startfile(path)  # type: ignore[attr-defined]
        except Exception as e:
            messagebox.showinfo("Listener Log", f"Open manually: {path}\n{e}")

    def kick_prompts(self) -> None:
        try:
            # Run a quick FSM-enabled runner cycle to seed tasks and send prompts
            ws = Path(self.ws_var.get().strip() or "D:/repos/Dadudekc")
            assign_root = Path(self.assign_root_var.get().strip() or "D:/repos/Dadudekc")
            agents = self.agents_var.get().strip() or "Agent-1,Agent-2,Agent-3,Agent-4"
            layout = self.layout_var.get().strip() or "5-agent"
            
            # Run runner with FSM enabled for immediate task seeding and prompting
            cmd = [
                sys.executable, "overnight_runner/runner.py",
                "--layout", layout,
                "--agents", agents,
                "--duration-min", "5",  # Quick cycle
                "--interval-sec", "10",  # Fast prompts
                "--sender", "Agent-3",
                "--plan", "contracts",  # Use contracts plan for FSM integration
                "--fsm-enabled",
                "--fsm-agent", "Agent-5",
                "--fsm-workflow", "default",
                "--seed-from-tasklists",  # Seed FSM from TASK_LIST.md files
                "--skip-assignments",  # Don't reassign, just prompt
                "--skip-captain-kickoff",
                "--skip-captain-fsm-feed",
                "--devlog-sends",
                "--devlog-embed",
                "--devlog-username", "Agent Devlog",
                "--workspace-root", str(ws),
                "--assign-root", str(assign_root)
            ]
            
            # Run in background
            subprocess.Popen(cmd, cwd=str(Path(__file__).resolve().parents[1]))
            self.status_var.set("FSM runner cycle started - seeding tasks and prompts")
        except Exception as e:
            messagebox.showerror("Kick Prompts", str(e))

    def onboard_agents(self) -> None:
        try:
            # Run runner with FSM enabled for onboarding and initial task seeding
            ws = Path(self.ws_var.get().strip() or "D:/repos/Dadudekc")
            assign_root = Path(self.assign_root_var.get().strip() or "D:/repos/Dadudekc")
            agents = self.agents_var.get().strip() or "Agent-1,Agent-2,Agent-3,Agent-4"
            layout = self.layout_var.get().strip() or "5-agent"
            
            # Run runner with FSM enabled for onboarding
            cmd = [
                sys.executable, "overnight_runner/runner.py",
                "--layout", layout,
                "--agents", agents,
                "--duration-min", "5",  # Quick cycle
                "--interval-sec", "10",  # Fast prompts
                "--sender", "Agent-3",
                "--plan", "autonomous-dev",  # Use autonomous-dev plan for onboarding
                "--fsm-enabled",
                "--fsm-agent", "Agent-5",
                "--fsm-workflow", "default",
                "--seed-from-tasklists",  # Seed FSM from TASK_LIST.md files
                "--skip-assignments",  # Don't reassign, just onboard
                "--skip-captain-kickoff",
                "--skip-captain-fsm-feed",
                "--devlog-sends",
                "--devlog-embed",
                "--devlog-username", "Agent Devlog",
                "--workspace-root", str(ws),
                "--assign-root", str(assign_root)
            ]
            
            # Run in background
            subprocess.Popen(cmd, cwd=str(Path(__file__).resolve().parents[1]))
            self.status_var.set("FSM onboarding cycle started - seeding tasks and onboarding")
        except Exception as e:
            messagebox.showerror("Onboard Agents", str(e))


def main() -> int:
    root = tk.Tk()
    SmallRunnerGUI(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



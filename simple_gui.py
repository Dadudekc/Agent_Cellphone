#!/usr/bin/env python3
"""
Simple Agent Resume System GUI
Basic interface for managing agent resume functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime

# Import our agent cell phone system
from agent_cell_phone import AgentCellPhone, MsgTag

class SimpleAgentGUI:
    """Simple GUI for the Agent Resume System."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Agent Resume System")
        self.root.geometry("800x600")
        
        # Initialize agent cell phone
        self.acp = AgentCellPhone(layout_mode="8-agent")
        self.agents = self.acp.get_available_agents()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface."""
        
        # Title
        title = tk.Label(self.root, text="🤖 Agent Resume System", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Agent selection frame
        select_frame = tk.Frame(self.root)
        select_frame.pack(pady=10)
        
        tk.Label(select_frame, text="Select Agent:").pack(side=tk.LEFT)
        self.agent_var = tk.StringVar(value=self.agents[0] if self.agents else "")
        agent_combo = ttk.Combobox(select_frame, textvariable=self.agent_var, 
                                  values=self.agents, state="readonly", width=15)
        agent_combo.pack(side=tk.LEFT, padx=10)
        
        # Control buttons frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # Individual controls
        tk.Label(button_frame, text="Individual Controls:", font=("Arial", 12, "bold")).pack()
        
        controls_frame = tk.Frame(button_frame)
        controls_frame.pack(pady=10)
        
        tk.Button(controls_frame, text="📤 Send Resume", command=self.send_resume, 
                 bg="#4CAF50", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(controls_frame, text="🔄 Sync Status", command=self.sync_status, 
                 bg="#2196F3", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(controls_frame, text="⏸️ Pause Agent", command=self.pause_agent, 
                 bg="#FF9800", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(controls_frame, text="▶️ Resume Agent", command=self.resume_agent, 
                 bg="#4CAF50", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        
        # Broadcast controls
        tk.Label(button_frame, text="Broadcast Controls:", font=("Arial", 12, "bold")).pack(pady=(20, 10))
        
        broadcast_frame = tk.Frame(button_frame)
        broadcast_frame.pack()
        
        tk.Button(broadcast_frame, text="📢 Broadcast Resume", command=self.broadcast_resume, 
                 bg="#4CAF50", fg="white", width=18).pack(side=tk.LEFT, padx=5)
        tk.Button(broadcast_frame, text="🔄 Broadcast Sync", command=self.broadcast_sync, 
                 bg="#2196F3", fg="white", width=18).pack(side=tk.LEFT, padx=5)
        tk.Button(broadcast_frame, text="⏸️ Broadcast Pause", command=self.broadcast_pause, 
                 bg="#FF9800", fg="white", width=18).pack(side=tk.LEFT, padx=5)
        
        # Custom message frame
        custom_frame = tk.Frame(self.root)
        custom_frame.pack(pady=20)
        
        tk.Label(custom_frame, text="Custom Message:", font=("Arial", 12, "bold")).pack()
        
        msg_frame = tk.Frame(custom_frame)
        msg_frame.pack(pady=10)
        
        self.custom_msg = tk.StringVar()
        tk.Entry(msg_frame, textvariable=self.custom_msg, width=40).pack(side=tk.LEFT, padx=5)
        tk.Button(msg_frame, text="📤 Send", command=self.send_custom, 
                 bg="#9C27B0", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Status display
        status_frame = tk.Frame(self.root)
        status_frame.pack(pady=20)
        
        tk.Label(status_frame, text="Agent Status:", font=("Arial", 12, "bold")).pack()
        
        self.status_text = tk.Text(status_frame, height=8, width=60)
        self.status_text.pack(pady=10)
        
        # Status controls
        status_controls = tk.Frame(status_frame)
        status_controls.pack()
        
        tk.Button(status_controls, text="🔄 Refresh Status", command=self.refresh_status, 
                 bg="#607D8B", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(status_controls, text="🗑️ Clear Status", command=self.clear_status, 
                 bg="#F44336", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Initialize status
        self.refresh_status()
    
    def log_status(self, message):
        """Add message to status display."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.status_text.insert(tk.END, log_entry)
        self.status_text.see(tk.END)
    
    def send_resume(self):
        """Send resume command to selected agent."""
        agent = self.agent_var.get()
        if agent:
            try:
                self.acp.send(agent, "Resume operation", MsgTag.RESUME)
                self.log_status(f"📤 Sent resume command to {agent}")
            except Exception as e:
                self.log_status(f"❌ Failed to send resume to {agent}: {e}")
    
    def sync_status(self):
        """Send sync command to selected agent."""
        agent = self.agent_var.get()
        if agent:
            try:
                self.acp.send(agent, "Sync status", MsgTag.SYNC)
                self.log_status(f"🔄 Sent sync command to {agent}")
            except Exception as e:
                self.log_status(f"❌ Failed to send sync to {agent}: {e}")
    
    def pause_agent(self):
        """Send pause command to selected agent."""
        agent = self.agent_var.get()
        if agent:
            try:
                self.acp.send(agent, "Pause operation", MsgTag.NORMAL)
                self.log_status(f"⏸️ Sent pause command to {agent}")
            except Exception as e:
                self.log_status(f"❌ Failed to send pause to {agent}: {e}")
    
    def resume_agent(self):
        """Send resume command to selected agent."""
        agent = self.agent_var.get()
        if agent:
            try:
                self.acp.send(agent, "Resume operation", MsgTag.RESUME)
                self.log_status(f"▶️ Sent resume command to {agent}")
            except Exception as e:
                self.log_status(f"❌ Failed to send resume to {agent}: {e}")
    
    def broadcast_resume(self):
        """Broadcast resume command to all agents."""
        try:
            self.acp.broadcast("Resume all operations", MsgTag.RESUME)
            self.log_status("📢 Broadcasted resume command to all agents")
        except Exception as e:
            self.log_status(f"❌ Broadcast resume failed: {e}")
    
    def broadcast_sync(self):
        """Broadcast sync command to all agents."""
        try:
            self.acp.broadcast("Sync all status", MsgTag.SYNC)
            self.log_status("🔄 Broadcasted sync command to all agents")
        except Exception as e:
            self.log_status(f"❌ Broadcast sync failed: {e}")
    
    def broadcast_pause(self):
        """Broadcast pause command to all agents."""
        try:
            self.acp.broadcast("Pause all operations", MsgTag.NORMAL)
            self.log_status("⏸️ Broadcasted pause command to all agents")
        except Exception as e:
            self.log_status(f"❌ Broadcast pause failed: {e}")
    
    def send_custom(self):
        """Send custom message to selected agent."""
        agent = self.agent_var.get()
        message = self.custom_msg.get()
        if agent and message:
            try:
                self.acp.send(agent, message, MsgTag.TASK)
                self.log_status(f"📤 Sent custom message to {agent}: {message}")
                self.custom_msg.set("")  # Clear input
            except Exception as e:
                self.log_status(f"❌ Failed to send custom message to {agent}: {e}")
    
    def refresh_status(self):
        """Refresh the status display."""
        self.status_text.delete(1.0, tk.END)
        self.log_status("🔄 Status refreshed")
        self.log_status(f"📋 Connected to {len(self.agents)} agents: {', '.join(self.agents)}")
        self.log_status("💡 Use the controls above to manage agents")
    
    def clear_status(self):
        """Clear the status display."""
        self.status_text.delete(1.0, tk.END)
        self.log_status("🗑️ Status cleared")
    
    def run(self):
        """Run the GUI."""
        self.root.mainloop()

def main():
    """Launch the Simple Agent GUI."""
    app = SimpleAgentGUI()
    app.run()

if __name__ == "__main__":
    main() 
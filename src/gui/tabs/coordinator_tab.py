#!/usr/bin/env python3
"""
Agent Coordinator Tab for Dream.OS GUI
Provides coordination and management functionality for agents
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict, List, Optional
import threading
import time

# Import our utilities
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

try:
    from src.gui.utils.coordination_utils import CoordinationUtils
except ImportError:
    print("Warning: coordination_utils not found")

class CoordinatorTab(ttk.Frame):
    """Agent Coordinator Tab for coordinating and managing agents"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.coordination_utils = None
        self.setup_ui()
        self.initialize_coordination()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Coordination controls
        left_panel = ttk.LabelFrame(main_frame, text="Coordination Controls", padding=10)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # System operations
        system_frame = ttk.LabelFrame(left_panel, text="System Operations", padding=5)
        system_frame.pack(fill=tk.X, pady=(0, 10))
        
        system_buttons = [
            ("Test All Agents", self.test_all_agents),
            ("Sync All Agents", self.sync_all_agents),
            ("Resume All Agents", self.resume_all_agents),
            ("Verify All Agents", self.verify_all_agents),
            ("Get System Health", self.get_system_health),
            ("Get System Metrics", self.get_system_metrics)
        ]
        
        for i, (text, command) in enumerate(system_buttons):
            btn = ttk.Button(system_frame, text=text, command=command)
            btn.grid(row=i//2, column=i%2, padx=2, pady=2, sticky="ew")
        
        # Broadcast controls
        broadcast_frame = ttk.LabelFrame(left_panel, text="Broadcast Messages", padding=5)
        broadcast_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Message tag selection
        tag_frame = ttk.Frame(broadcast_frame)
        tag_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(tag_frame, text="Tag:").pack(side=tk.LEFT)
        self.broadcast_tag_var = tk.StringVar(value="NORMAL")
        tag_combo = ttk.Combobox(tag_frame, textvariable=self.broadcast_tag_var, 
                                values=["NORMAL", "COMMAND", "STATUS", "ERROR", "CAPTAIN", "SYNC"], 
                                state="readonly")
        tag_combo.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        
        # Broadcast message
        self.broadcast_text = scrolledtext.ScrolledText(broadcast_frame, height=4, wrap=tk.WORD)
        self.broadcast_text.pack(fill=tk.X, pady=(0, 5))
        
        broadcast_buttons = ttk.Frame(broadcast_frame)
        broadcast_buttons.pack(fill=tk.X)
        
        ttk.Button(broadcast_buttons, text="Broadcast Message", 
                  command=self.broadcast_message).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(broadcast_buttons, text="Emergency Broadcast", 
                  command=self.emergency_broadcast).pack(side=tk.LEFT)
        
        # Task management
        task_frame = ttk.LabelFrame(left_panel, text="Task Management", padding=5)
        task_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Agent selection for tasks
        task_agent_frame = ttk.Frame(task_frame)
        task_agent_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(task_agent_frame, text="Agent:").pack(side=tk.LEFT)
        self.task_agent_var = tk.StringVar()
        self.task_agent_combo = ttk.Combobox(task_agent_frame, textvariable=self.task_agent_var, 
                                            state="readonly")
        self.task_agent_combo.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        
        # Task assignment
        self.task_text = scrolledtext.ScrolledText(task_frame, height=3, wrap=tk.WORD)
        self.task_text.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(task_frame, text="Assign Task", command=self.assign_task).pack(fill=tk.X)
        
        # Workload management
        workload_frame = ttk.LabelFrame(left_panel, text="Workload Management", padding=5)
        workload_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(workload_frame, text="Get Agent Workloads", 
                  command=self.get_agent_workloads).pack(fill=tk.X, pady=2)
        ttk.Button(workload_frame, text="Balance Workload", 
                  command=self.balance_workload).pack(fill=tk.X, pady=2)
        
        # Right panel - Status and monitoring
        right_panel = ttk.LabelFrame(main_frame, text="System Monitoring", padding=10)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Health status
        health_frame = ttk.LabelFrame(right_panel, text="System Health", padding=5)
        health_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.health_text = scrolledtext.ScrolledText(health_frame, height=6, wrap=tk.WORD)
        self.health_text.pack(fill=tk.BOTH, expand=True)
        
        # Coordinates display
        coords_frame = ttk.LabelFrame(right_panel, text="System Coordinates", padding=5)
        coords_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.coords_text = scrolledtext.ScrolledText(coords_frame, height=4, wrap=tk.WORD)
        self.coords_text.pack(fill=tk.BOTH, expand=True)
        
        # Log display
        log_frame = ttk.LabelFrame(right_panel, text="Coordination Log", padding=5)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Log controls
        log_controls = ttk.Frame(right_panel)
        log_controls.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(log_controls, text="Clear Log", command=self.clear_log).pack(side=tk.LEFT)
        ttk.Button(log_controls, text="Refresh All", command=self.refresh_all).pack(side=tk.RIGHT)
    
    def initialize_coordination(self):
        """Initialize the coordination utilities"""
        try:
            self.coordination_utils = CoordinationUtils(layout_mode="8-agent", test_mode=True)
            
            # Populate agent dropdowns
            agents = self.coordination_utils.acp.get_available_agents() if self.coordination_utils.acp else []
            self.task_agent_combo['values'] = agents
            
            self.log_message("Coordination system initialized successfully")
            self.refresh_all()
            
        except Exception as e:
            self.log_message(f"Error initializing coordination: {e}", error=True)
    
    def test_all_agents(self):
        """Test connectivity to all agents"""
        if not self.coordination_utils:
            messagebox.showerror("Error", "Coordination system not initialized")
            return
        
        def test_thread():
            try:
                results = self.coordination_utils.test_all_agents()
                
                # Format results
                result_text = "Agent Test Results:\n"
                result_text += "=" * 50 + "\n"
                
                for agent, result in results.items():
                    ping_success = result['ping']['success']
                    status_success = result['status']['success']
                    
                    ping_status = "✓" if ping_success else "✗"
                    status_status = "✓" if status_success else "✗"
                    
                    result_text += f"{agent}:\n"
                    result_text += f"  Ping: {ping_status} ({result['ping']['message']})\n"
                    result_text += f"  Status: {status_status} ({result['status']['message']})\n"
                    result_text += f"  Response Time: {result['ping']['response_time']}ms\n\n"
                
                self.after(0, lambda: self.log_message(result_text))
                
            except Exception as e:
                self.after(0, lambda: self.log_message(f"Error testing agents: {e}", error=True))
        
        threading.Thread(target=test_thread, daemon=True).start()
    
    def sync_all_agents(self):
        """Synchronize all agents"""
        if not self.coordination_utils:
            messagebox.showerror("Error", "Coordination system not initialized")
            return
        
        def sync_thread():
            try:
                results = self.coordination_utils.sync_all_agents()
                
                # Log results
                for agent, (success, result) in results.items():
                    status = "✓" if success else "✗"
                    self.after(0, lambda a=agent, s=status, r=result: 
                             self.log_message(f"{s} {a}: {r}"))
                
                self.after(0, lambda: messagebox.showinfo("Complete", "All agents synchronized"))
                
            except Exception as e:
                self.after(0, lambda: self.log_message(f"Error syncing agents: {e}", error=True))
        
        threading.Thread(target=sync_thread, daemon=True).start()
    
    def resume_all_agents(self):
        """Resume all agents"""
        if not self.coordination_utils:
            messagebox.showerror("Error", "Coordination system not initialized")
            return
        
        def resume_thread():
            try:
                results = self.coordination_utils.resume_all_agents()
                
                # Log results
                for agent, (success, result) in results.items():
                    status = "✓" if success else "✗"
                    self.after(0, lambda a=agent, s=status, r=result: 
                             self.log_message(f"{s} {a}: {r}"))
                
                self.after(0, lambda: messagebox.showinfo("Complete", "All agents resumed"))
                
            except Exception as e:
                self.after(0, lambda: self.log_message(f"Error resuming agents: {e}", error=True))
        
        threading.Thread(target=resume_thread, daemon=True).start()
    
    def verify_all_agents(self):
        """Verify all agents"""
        if not self.coordination_utils:
            messagebox.showerror("Error", "Coordination system not initialized")
            return
        
        def verify_thread():
            try:
                results = self.coordination_utils.verify_all_agents()
                
                # Log results
                for agent, (success, result) in results.items():
                    status = "✓" if success else "✗"
                    self.after(0, lambda a=agent, s=status, r=result: 
                             self.log_message(f"{s} {a}: {r}"))
                
                self.after(0, lambda: messagebox.showinfo("Complete", "All agents verified"))
                
            except Exception as e:
                self.after(0, lambda: self.log_message(f"Error verifying agents: {e}", error=True))
        
        threading.Thread(target=verify_thread, daemon=True).start()
    
    def get_system_health(self):
        """Get system health status"""
        if not self.coordination_utils:
            messagebox.showerror("Error", "Coordination system not initialized")
            return
        
        def health_thread():
            try:
                health = self.coordination_utils.get_system_health()
                
                # Update health display
                health_text = "System Health:\n"
                health_text += "=" * 50 + "\n"
                
                if "error" in health:
                    health_text += f"Error: {health['error']}\n"
                else:
                    health_text += f"Total Agents: {health.get('total_agents', 0)}\n"
                    health_text += f"Responsive Agents: {health.get('responsive_agents', 0)}\n"
                    health_text += f"Response Rate: {health.get('response_rate', 0):.1f}%\n"
                    health_text += f"Average Ping Time: {health.get('average_ping_time', 0)}ms\n"
                    health_text += f"System Status: {health.get('system_status', 'Unknown')}\n"
                    health_text += f"Timestamp: {health.get('timestamp', 'Unknown')}\n"
                
                self.after(0, lambda: self.update_health_display(health_text))
                
            except Exception as e:
                error_text = f"Error getting health: {e}"
                self.after(0, lambda: self.update_health_display(error_text))
        
        threading.Thread(target=health_thread, daemon=True).start()
    
    def get_system_metrics(self):
        """Get comprehensive system metrics"""
        if not self.coordination_utils:
            messagebox.showerror("Error", "Coordination system not initialized")
            return
        
        def metrics_thread():
            try:
                metrics = self.coordination_utils.get_system_metrics()
                
                # Log metrics summary
                if "error" not in metrics:
                    self.after(0, lambda: self.log_message("System metrics collected successfully"))
                    self.after(0, lambda: self.log_message(f"Total tasks: {metrics.get('total_tasks', 0)}"))
                    self.after(0, lambda: self.log_message(f"Average tasks per agent: {metrics.get('average_tasks_per_agent', 0):.1f}"))
                else:
                    self.after(0, lambda: self.log_message(f"Error getting metrics: {metrics['error']}", error=True))
                
            except Exception as e:
                self.after(0, lambda: self.log_message(f"Error getting metrics: {e}", error=True))
        
        threading.Thread(target=metrics_thread, daemon=True).start()
    
    def broadcast_message(self):
        """Broadcast a message to all agents"""
        if not self.coordination_utils:
            messagebox.showerror("Error", "Coordination system not initialized")
            return
        
        message = self.broadcast_text.get(1.0, tk.END).strip()
        tag = self.broadcast_tag_var.get()
        
        if not message:
            messagebox.showwarning("Warning", "Please enter a message")
            return
        
        def broadcast_thread():
            try:
                success, result = self.coordination_utils.broadcast_system_message(message, tag)
                self.after(0, lambda: self.handle_broadcast_result(success, result))
            except Exception as e:
                self.after(0, lambda: self.handle_broadcast_result(False, f"Error: {e}"))
        
        threading.Thread(target=broadcast_thread, daemon=True).start()
    
    def emergency_broadcast(self):
        """Send an emergency broadcast"""
        if not self.coordination_utils:
            messagebox.showerror("Error", "Coordination system not initialized")
            return
        
        message = self.broadcast_text.get(1.0, tk.END).strip()
        
        if not message:
            messagebox.showwarning("Warning", "Please enter an emergency message")
            return
        
        # Confirm emergency broadcast
        if not messagebox.askyesno("Emergency Broadcast", 
                                 "Are you sure you want to send an emergency broadcast?"):
            return
        
        def emergency_thread():
            try:
                success, result = self.coordination_utils.emergency_broadcast(message)
                self.after(0, lambda: self.handle_broadcast_result(success, result))
            except Exception as e:
                self.after(0, lambda: self.handle_broadcast_result(False, f"Error: {e}"))
        
        threading.Thread(target=emergency_thread, daemon=True).start()
    
    def handle_broadcast_result(self, success: bool, result: str):
        """Handle broadcast result"""
        if success:
            self.log_message(f"✓ Broadcast: {result}")
            messagebox.showinfo("Success", result)
        else:
            self.log_message(f"✗ Broadcast: {result}", error=True)
            messagebox.showerror("Error", result)
    
    def assign_task(self):
        """Assign a task to a specific agent"""
        if not self.coordination_utils:
            messagebox.showerror("Error", "Coordination system not initialized")
            return
        
        agent = self.task_agent_var.get()
        task = self.task_text.get(1.0, tk.END).strip()
        
        if not agent:
            messagebox.showwarning("Warning", "Please select an agent")
            return
        
        if not task:
            messagebox.showwarning("Warning", "Please enter a task")
            return
        
        def assign_thread():
            try:
                success, result = self.coordination_utils.acp.send(agent, f"task assign {task}", 
                                                                  self.coordination_utils.acp.MsgTag.COMMAND)
                self.after(0, lambda: self.handle_task_result(success, result))
            except Exception as e:
                self.after(0, lambda: self.handle_task_result(False, f"Error: {e}"))
        
        threading.Thread(target=assign_thread, daemon=True).start()
    
    def handle_task_result(self, success: bool, result: str):
        """Handle task assignment result"""
        if success:
            self.log_message(f"✓ Task assigned: {result}")
            messagebox.showinfo("Success", f"Task assigned successfully")
        else:
            self.log_message(f"✗ Task assignment failed: {result}", error=True)
            messagebox.showerror("Error", f"Task assignment failed: {result}")
    
    def get_agent_workloads(self):
        """Get workload information for all agents"""
        if not self.coordination_utils:
            messagebox.showerror("Error", "Coordination system not initialized")
            return
        
        def workload_thread():
            try:
                workloads = self.coordination_utils.get_agent_workloads()
                
                # Log workload information
                for agent, info in workloads.items():
                    if "error" not in info:
                        task_count = info.get("task_count", 0)
                        self.after(0, lambda a=agent, tc=task_count: 
                                 self.log_message(f"{a}: {tc} tasks"))
                    else:
                        self.after(0, lambda a=agent, e=info["error"]: 
                                 self.log_message(f"{a}: Error - {e}", error=True))
                
            except Exception as e:
                self.after(0, lambda: self.log_message(f"Error getting workloads: {e}", error=True))
        
        threading.Thread(target=workload_thread, daemon=True).start()
    
    def balance_workload(self):
        """Attempt to balance workload across agents"""
        if not self.coordination_utils:
            messagebox.showerror("Error", "Coordination system not initialized")
            return
        
        def balance_thread():
            try:
                result = self.coordination_utils.balance_workload()
                
                if "error" in result:
                    self.after(0, lambda: self.log_message(f"Error balancing workload: {result['error']}", error=True))
                else:
                    self.after(0, lambda: self.log_message(f"Workload balance suggestion: {result.get('suggestion', 'None')}"))
                    self.after(0, lambda: self.log_message(f"Current distribution: {result.get('current_distribution', {})}"))
                
            except Exception as e:
                self.after(0, lambda: self.log_message(f"Error balancing workload: {e}", error=True))
        
        threading.Thread(target=balance_thread, daemon=True).start()
    
    def clear_log(self):
        """Clear the log display"""
        self.log_text.delete(1.0, tk.END)
    
    def log_message(self, message: str, error: bool = False):
        """Add a message to the log"""
        timestamp = time.strftime("%H:%M:%S")
        prefix = "ERROR" if error else "INFO"
        log_entry = f"[{timestamp}] {prefix}: {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
    
    def refresh_all(self):
        """Refresh all displays"""
        self.get_system_health()
        self.get_system_coordinates()
    
    def get_system_coordinates(self):
        """Get and display system coordinates"""
        if not self.coordination_utils:
            self.coords_text.delete(1.0, tk.END)
            self.coords_text.insert(1.0, "Coordination system not initialized")
            return
        
        def coords_thread():
            try:
                coords = self.coordination_utils.get_system_coordinates()
                
                # Format coordinates for display
                coords_text = "System Coordinates:\n"
                coords_text += "=" * 50 + "\n"
                
                if "error" in coords:
                    coords_text += f"Error: {coords['error']}\n"
                else:
                    coords_text += f"Layout Mode: {coords.get('layout_mode', 'Unknown')}\n"
                    coords_text += f"Total Agents: {coords.get('total_agents', 0)}\n"
                    coords_text += f"Available Layouts: {', '.join(coords.get('available_layouts', []))}\n\n"
                    
                    # Agent coordinates
                    coordinates = coords.get('coordinates', {})
                    for agent, coord in coordinates.items():
                        coords_text += f"{agent}: {coord}\n"
                
                self.after(0, lambda: self.update_coords_display(coords_text))
                
            except Exception as e:
                error_text = f"Error getting coordinates: {e}"
                self.after(0, lambda: self.update_coords_display(error_text))
        
        threading.Thread(target=coords_thread, daemon=True).start()
    
    def update_health_display(self, health_text: str):
        """Update the health display"""
        self.health_text.delete(1.0, tk.END)
        self.health_text.insert(1.0, health_text)
    
    def update_coords_display(self, coords_text: str):
        """Update the coordinates display"""
        self.coords_text.delete(1.0, tk.END)
        self.coords_text.insert(1.0, coords_text) 
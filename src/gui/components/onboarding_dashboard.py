#!/usr/bin/env python3
"""
Enhanced Onboarding Dashboard Component for Dream.OS GUI
Provides comprehensive onboarding status, verification, and management
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict, List, Optional, Callable
import threading
import time
from datetime import datetime
from pathlib import Path
import sys
import json

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

try:
    from agent_workspaces.onboarding.onboarding_verifier import OnboardingVerifier
    from agent_workspaces.onboarding.onboarding_manager import OnboardingManager
except ImportError as e:
    print(f"Warning: onboarding modules not found: {e}")

class OnboardingDashboardWidget:
    """Enhanced onboarding dashboard widget"""
    
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.verifier = None
        self.manager = None
        self.agents_data = {}
        self.setup_widget(**kwargs)
        self.initialize_components()
    
    def setup_widget(self, **kwargs):
        """Setup the dashboard widget"""
        # Main container
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="Onboarding Dashboard", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Top control panel
        control_frame = ttk.LabelFrame(main_frame, text="Dashboard Controls", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Refresh Status", 
                  command=self.refresh_dashboard).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Run Verification", 
                  command=self.run_verification).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Generate Report", 
                  command=self.generate_report).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Auto-Onboard All", 
                  command=self.auto_onboard_all).pack(side=tk.LEFT, padx=(0, 5))
        
        # Summary panel
        summary_frame = ttk.LabelFrame(main_frame, text="System Summary", padding=10)
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Summary metrics
        metrics_frame = ttk.Frame(summary_frame)
        metrics_frame.pack(fill=tk.X)
        
        # Create metric labels
        self.total_agents_label = ttk.Label(metrics_frame, text="Total Agents: 0")
        self.total_agents_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.onboarded_agents_label = ttk.Label(metrics_frame, text="Onboarded: 0")
        self.onboarded_agents_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.verified_agents_label = ttk.Label(metrics_frame, text="Verified: 0")
        self.verified_agents_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.pending_agents_label = ttk.Label(metrics_frame, text="Pending: 0")
        self.pending_agents_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.success_rate_label = ttk.Label(metrics_frame, text="Success Rate: 0%")
        self.success_rate_label.pack(side=tk.LEFT)
        
        # Agent status panel
        status_frame = ttk.LabelFrame(main_frame, text="Agent Status", padding=10)
        status_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create treeview for agent status
        columns = ("Agent", "Status", "Progress", "Verification", "Last Updated", "Actions")
        self.agent_tree = ttk.Treeview(status_frame, columns=columns, show="headings", height=8)
        
        # Configure columns
        for col in columns:
            self.agent_tree.heading(col, text=col)
            self.agent_tree.column(col, width=100, minwidth=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=self.agent_tree.yview)
        self.agent_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.agent_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click event
        self.agent_tree.bind("<Double-1>", self.on_agent_double_click)
        
        # Details panel
        details_frame = ttk.LabelFrame(main_frame, text="Agent Details", padding=10)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        self.details_text = scrolledtext.ScrolledText(details_frame, height=8, wrap=tk.WORD)
        self.details_text.pack(fill=tk.BOTH, expand=True)
    
    def initialize_components(self):
        """Initialize verification and manager components"""
        try:
            self.verifier = OnboardingVerifier()
            self.manager = OnboardingManager()
            self.refresh_dashboard()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize components: {e}")
    
    def refresh_dashboard(self):
        """Refresh the dashboard with current data"""
        def refresh_thread():
            try:
                # Get agent directories
                agent_dirs = self.verifier.get_agent_directories()
                agents_data = {}
                
                for agent_dir in agent_dirs:
                    agent_id = agent_dir.name
                    status = self.verifier.load_agent_status(agent_dir)
                    if status:
                        agents_data[agent_id] = status
                
                self.agents_data = agents_data
                
                # Update UI in main thread
                self.parent.after(0, self.update_dashboard_ui)
                
            except Exception as e:
                self.parent.after(0, lambda: messagebox.showerror("Error", f"Refresh failed: {e}"))
        
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def update_dashboard_ui(self):
        """Update the dashboard UI with current data"""
        # Clear existing items
        for item in self.agent_tree.get_children():
            self.agent_tree.delete(item)
        
        # Calculate metrics
        total_agents = len(self.agents_data)
        onboarded_agents = 0
        verified_agents = 0
        pending_agents = 0
        
        # Add agents to treeview
        for agent_id, status in self.agents_data.items():
            onboarding = status.get("onboarding", {})
            
            # Calculate metrics
            if onboarding.get("status") == "completed":
                onboarded_agents += 1
            elif onboarding.get("status") in ["pending", "in_progress"]:
                pending_agents += 1
            
            if onboarding.get("verification_passed", False):
                verified_agents += 1
            
            # Prepare treeview item
            progress = f"{onboarding.get('progress', 0):.1f}%"
            verification = "✓" if onboarding.get("verification_passed", False) else "✗"
            last_updated = status.get("last_updated", "Unknown")
            
            item = self.agent_tree.insert("", "end", values=(
                agent_id,
                onboarding.get("status", "unknown"),
                progress,
                verification,
                last_updated,
                "View Details"
            ))
        
        # Update summary labels
        self.total_agents_label.config(text=f"Total Agents: {total_agents}")
        self.onboarded_agents_label.config(text=f"Onboarded: {onboarded_agents}")
        self.verified_agents_label.config(text=f"Verified: {verified_agents}")
        self.pending_agents_label.config(text=f"Pending: {pending_agents}")
        
        success_rate = (verified_agents / total_agents * 100) if total_agents > 0 else 0
        self.success_rate_label.config(text=f"Success Rate: {success_rate:.1f}%")
    
    def run_verification(self):
        """Run verification for all agents"""
        def verification_thread():
            try:
                self.parent.after(0, lambda: messagebox.showinfo("Verification", "Starting verification process..."))
                
                # Run verification
                results = self.verifier.verify_all_agents()
                
                # Generate report
                report = self.verifier.generate_verification_report(results)
                
                # Update verification status
                for agent_id, result in results.items():
                    self.verifier.update_verification_status(
                        agent_id,
                        result["verification_passed"],
                        f"Verification {'passed' if result['verification_passed'] else 'failed'}"
                    )
                
                # Refresh dashboard
                self.parent.after(0, self.refresh_dashboard)
                
                # Show results
                self.parent.after(0, lambda: self.show_verification_results(results, report))
                
            except Exception as e:
                self.parent.after(0, lambda: messagebox.showerror("Error", f"Verification failed: {e}"))
        
        threading.Thread(target=verification_thread, daemon=True).start()
    
    def show_verification_results(self, results: Dict, report: str):
        """Show verification results"""
        # Create results window
        results_window = tk.Toplevel(self.parent)
        results_window.title("Verification Results")
        results_window.geometry("800x600")
        
        # Add report text
        report_text = scrolledtext.ScrolledText(results_window, wrap=tk.WORD)
        report_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        report_text.insert(tk.END, report)
        report_text.config(state=tk.DISABLED)
        
        # Add close button
        ttk.Button(results_window, text="Close", 
                  command=results_window.destroy).pack(pady=10)
    
    def generate_report(self):
        """Generate and save onboarding report"""
        try:
            # Run verification first
            results = self.verifier.verify_all_agents()
            report = self.verifier.generate_verification_report(results)
            
            # Save report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = f"onboarding_report_{timestamp}.txt"
            
            with open(report_file, 'w') as f:
                f.write(report)
            
            messagebox.showinfo("Report Generated", f"Report saved to: {report_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def auto_onboard_all(self):
        """Automatically onboard all pending agents"""
        def onboard_thread():
            try:
                pending_agents = []
                for agent_id, status in self.agents_data.items():
                    onboarding = status.get("onboarding", {})
                    if onboarding.get("status") in ["pending", "in_progress"]:
                        pending_agents.append(agent_id)
                
                if not pending_agents:
                    self.parent.after(0, lambda: messagebox.showinfo("Info", "No pending agents to onboard"))
                    return
                
                self.parent.after(0, lambda: messagebox.showinfo("Onboarding", 
                    f"Starting auto-onboarding for {len(pending_agents)} agents..."))
                
                # Onboard each agent
                for agent_id in pending_agents:
                    try:
                        result = self.manager.onboard_agent(agent_id)
                        print(f"Onboarded {agent_id}: {result}")
                        time.sleep(2)  # Delay between agents
                    except Exception as e:
                        print(f"Failed to onboard {agent_id}: {e}")
                
                # Refresh dashboard
                self.parent.after(0, self.refresh_dashboard)
                self.parent.after(0, lambda: messagebox.showinfo("Complete", 
                    "Auto-onboarding completed. Check dashboard for updated status."))
                
            except Exception as e:
                self.parent.after(0, lambda: messagebox.showerror("Error", f"Auto-onboarding failed: {e}"))
        
        threading.Thread(target=onboard_thread, daemon=True).start()
    
    def on_agent_double_click(self, event):
        """Handle double-click on agent row"""
        selection = self.agent_tree.selection()
        if selection:
            item = self.agent_tree.item(selection[0])
            agent_id = item['values'][0]
            self.show_agent_details(agent_id)
    
    def show_agent_details(self, agent_id: str):
        """Show detailed information for a specific agent"""
        if agent_id not in self.agents_data:
            return
        
        status = self.agents_data[agent_id]
        onboarding = status.get("onboarding", {})
        
        # Format details
        details = f"Agent Details: {agent_id}\n"
        details += "=" * 50 + "\n\n"
        
        # Basic info
        details += f"Status: {status.get('status', 'unknown')}\n"
        details += f"Current Task: {status.get('current_task', 'none')}\n"
        details += f"Last Updated: {status.get('last_updated', 'unknown')}\n\n"
        
        # Onboarding info
        details += "ONBOARDING STATUS:\n"
        details += f"  Status: {onboarding.get('status', 'unknown')}\n"
        details += f"  Progress: {onboarding.get('progress', 0):.1f}%\n"
        details += f"  Started: {onboarding.get('started_at', 'not started')}\n"
        details += f"  Completed: {onboarding.get('completed_at', 'not completed')}\n"
        details += f"  Verification: {'✓ Passed' if onboarding.get('verification_passed', False) else '✗ Failed'}\n\n"
        
        # Checklist
        details += "CHECKLIST:\n"
        checklist = onboarding.get("checklist", {})
        for item, completed in checklist.items():
            status = "✓" if completed else "✗"
            details += f"  {status} {item.replace('_', ' ').title()}\n"
        details += "\n"
        
        # Documents read
        documents = onboarding.get("documents_read", [])
        details += f"DOCUMENTS READ ({len(documents)}):\n"
        for doc in documents:
            details += f"  ✓ {doc}\n"
        details += "\n"
        
        # Capabilities
        details += "CAPABILITIES:\n"
        capabilities = status.get("capabilities", {})
        for capability, enabled in capabilities.items():
            status = "✓" if enabled else "✗"
            details += f"  {status} {capability.replace('_', ' ').title()}\n"
        details += "\n"
        
        # Performance
        details += "PERFORMANCE:\n"
        performance = status.get("performance", {})
        details += f"  Tasks Completed: {performance.get('tasks_completed', 0)}\n"
        details += f"  Messages Sent: {performance.get('messages_sent', 0)}\n"
        details += f"  Messages Received: {performance.get('messages_received', 0)}\n"
        details += f"  Uptime Hours: {performance.get('uptime_hours', 0):.1f}\n"
        details += f"  Last Activity: {performance.get('last_activity', 'none')}\n\n"
        
        # Health
        details += "HEALTH:\n"
        health = status.get("health", {})
        details += f"  Status: {health.get('status', 'unknown')}\n"
        details += f"  Last Health Check: {health.get('last_health_check', 'none')}\n"
        
        errors = health.get("errors", [])
        if errors:
            details += f"  Errors: {len(errors)}\n"
            for error in errors:
                details += f"    - {error}\n"
        
        warnings = health.get("warnings", [])
        if warnings:
            details += f"  Warnings: {len(warnings)}\n"
            for warning in warnings:
                details += f"    - {warning}\n"
        
        # Update details text
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(1.0, details)
    
    def get_widget(self):
        """Get the main widget"""
        return self.parent 
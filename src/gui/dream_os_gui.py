#!/usr/bin/env python3
"""
Dream.OS GUI - Main Application
Comprehensive GUI for Dream.OS Autonomous Framework
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import threading
import time
from datetime import datetime
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Import tab components
try:
    from src.gui.tabs.agent_messenger_tab import AgentMessengerTab
    from src.gui.tabs.onboarding_tab import OnboardingTab
    from src.gui.tabs.coordinator_tab import CoordinatorTab
except ImportError as e:
    print(f"Warning: Could not import tab components: {e}")

class DreamOSGUI:
    """Main Dream.OS GUI Application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Dream.OS Autonomous Framework")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Initialize status variable first
        self.status_var = tk.StringVar(value="Ready")
        
        # Configure style
        self.setup_style()
        
        # Setup main interface
        self.setup_ui()
        
        # Initialize status
        self.update_status("Dream.OS GUI initialized")
    
    def setup_style(self):
        """Setup application styling"""
        style = ttk.Style()
        
        # Configure theme
        try:
            style.theme_use('clam')
        except:
            pass
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Status.TLabel', font=('Arial', 10))
        
        # Configure notebook
        style.configure('TNotebook.Tab', padding=[10, 5])
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title_label = ttk.Label(header_frame, text="Dream.OS Autonomous Framework", 
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Status bar
        status_frame = ttk.Frame(header_frame)
        status_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                                     style='Status.TLabel')
        self.status_label.pack(side=tk.RIGHT)
        
        # Main notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_tabs()
        
        # Footer
        footer_frame = ttk.Frame(main_container)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Footer controls
        controls_frame = ttk.Frame(footer_frame)
        controls_frame.pack(side=tk.RIGHT)
        
        ttk.Button(controls_frame, text="Refresh All", 
                  command=self.refresh_all).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(controls_frame, text="System Info", 
                  command=self.show_system_info).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(controls_frame, text="About", 
                  command=self.show_about).pack(side=tk.LEFT)
    
    def create_tabs(self):
        """Create all application tabs"""
        try:
            # Agent Messenger Tab
            self.messenger_tab = AgentMessengerTab(self.notebook)
            self.notebook.add(self.messenger_tab, text="Agent Messenger")
            
            # Onboarding Manager Tab
            self.onboarding_tab = OnboardingTab(self.notebook)
            self.notebook.add(self.onboarding_tab, text="Onboarding Manager")
            
            # Agent Coordinator Tab
            self.coordinator_tab = CoordinatorTab(self.notebook)
            self.notebook.add(self.coordinator_tab, text="Agent Coordinator")
            
            # Quick Actions Tab
            self.quick_actions_tab = self.create_quick_actions_tab()
            self.notebook.add(self.quick_actions_tab, text="Quick Actions")
            
            # System Monitor Tab
            self.system_monitor_tab = self.create_system_monitor_tab()
            self.notebook.add(self.system_monitor_tab, text="System Monitor")
            
        except Exception as e:
            self.show_error(f"Error creating tabs: {e}")
    
    def create_quick_actions_tab(self):
        """Create the Quick Actions tab"""
        tab = ttk.Frame(self.notebook)
        
        # Main container
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Quick action buttons
        actions_frame = ttk.LabelFrame(main_frame, text="Quick Actions", padding=10)
        actions_frame.pack(fill=tk.BOTH, expand=True)
        
        # Grid of action buttons
        actions = [
            ("Ping All Agents", self.quick_ping_all),
            ("Get System Status", self.quick_system_status),
            ("Sync All Agents", self.quick_sync_all),
            ("Resume All Agents", self.quick_resume_all),
            ("Test Connectivity", self.quick_test_connectivity),
            ("Get Agent Workloads", self.quick_get_workloads),
            ("Emergency Broadcast", self.quick_emergency_broadcast),
            ("System Health Check", self.quick_health_check),
            ("Onboard All Agents", self.quick_onboard_all),
            ("Verify All Agents", self.quick_verify_all),
            ("Balance Workload", self.quick_balance_workload),
            ("Clear All Logs", self.quick_clear_logs)
        ]
        
        for i, (text, command) in enumerate(actions):
            btn = ttk.Button(actions_frame, text=text, command=command)
            btn.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="ew")
        
        # Configure grid weights
        for i in range(3):
            actions_frame.columnconfigure(i, weight=1)
        
        # Status display
        status_frame = ttk.LabelFrame(main_frame, text="Quick Status", padding=10)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.quick_status_text = scrolledtext.ScrolledText(status_frame, height=8, wrap=tk.WORD)
        self.quick_status_text.pack(fill=tk.BOTH, expand=True)
        
        return tab
    
    def create_system_monitor_tab(self):
        """Create the System Monitor tab"""
        tab = ttk.Frame(self.notebook)
        
        # Main container
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - System info
        left_panel = ttk.LabelFrame(main_frame, text="System Information", padding=10)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.system_info_text = scrolledtext.ScrolledText(left_panel, height=15, wrap=tk.WORD)
        self.system_info_text.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Real-time monitoring
        right_panel = ttk.LabelFrame(main_frame, text="Real-time Monitoring", padding=10)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Monitoring controls
        monitor_controls = ttk.Frame(right_panel)
        monitor_controls.pack(fill=tk.X, pady=(0, 10))
        
        self.monitoring_var = tk.BooleanVar()
        self.monitoring_check = ttk.Checkbutton(monitor_controls, text="Enable Monitoring", 
                                               variable=self.monitoring_var, 
                                               command=self.toggle_monitoring)
        self.monitoring_check.pack(side=tk.LEFT)
        
        ttk.Button(monitor_controls, text="Refresh Now", 
                  command=self.refresh_monitoring).pack(side=tk.RIGHT)
        
        # Monitoring display
        self.monitoring_text = scrolledtext.ScrolledText(right_panel, height=15, wrap=tk.WORD)
        self.monitoring_text.pack(fill=tk.BOTH, expand=True)
        
        return tab
    
    def update_status(self, message: str):
        """Update the status bar"""
        timestamp = time.strftime("%H:%M:%S")
        self.status_var.set(f"[{timestamp}] {message}")
    
    def show_error(self, message: str):
        """Show an error message"""
        messagebox.showerror("Error", message)
        self.update_status(f"Error: {message}")
    
    def show_info(self, message: str):
        """Show an info message"""
        messagebox.showinfo("Information", message)
        self.update_status(f"Info: {message}")
    
    def refresh_all(self):
        """Refresh all tabs"""
        self.update_status("Refreshing all components...")
        
        try:
            # Refresh each tab
            if hasattr(self, 'messenger_tab'):
                self.messenger_tab.refresh_status()
            
            if hasattr(self, 'onboarding_tab'):
                self.onboarding_tab.refresh_status()
            
            if hasattr(self, 'coordinator_tab'):
                self.coordinator_tab.refresh_all()
            
            self.refresh_monitoring()
            self.update_status("All components refreshed")
            
        except Exception as e:
            self.show_error(f"Error refreshing: {e}")
    
    def show_system_info(self):
        """Show system information"""
        try:
            info = self.get_system_info()
            
            info_window = tk.Toplevel(self.root)
            info_window.title("System Information")
            info_window.geometry("600x400")
            
            info_text = scrolledtext.ScrolledText(info_window, wrap=tk.WORD)
            info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            info_text.insert(1.0, info)
            info_text.config(state=tk.DISABLED)
            
        except Exception as e:
            self.show_error(f"Error showing system info: {e}")
    
    def get_system_info(self) -> str:
        """Get comprehensive system information"""
        info = "Dream.OS Autonomous Framework\n"
        info += "=" * 50 + "\n\n"
        
        info += f"Version: 1.0.0\n"
        info += f"Build Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        info += f"Python Version: {sys.version}\n"
        info += f"Platform: {sys.platform}\n\n"
        
        info += "Project Structure:\n"
        info += "-" * 20 + "\n"
        
        # Check key directories
        key_dirs = [
            "agent_workspaces",
            "config",
            "core",
            "docs",
            "examples",
            "gui",
            "scripts",
            "src",
            "tests"
        ]
        
        for dir_name in key_dirs:
            dir_path = project_root / dir_name
            status = "✓" if dir_path.exists() else "✗"
            info += f"{status} {dir_name}/\n"
        
        info += "\nAgent Workspaces:\n"
        info += "-" * 20 + "\n"
        
        agent_dir = project_root / "agent_workspaces"
        if agent_dir.exists():
            agent_dirs = [d.name for d in agent_dir.iterdir() if d.is_dir() and d.name.startswith("Agent-")]
            for agent in sorted(agent_dirs):
                info += f"  {agent}/\n"
        else:
            info += "  No agent workspaces found\n"
        
        info += "\nConfiguration:\n"
        info += "-" * 20 + "\n"
        
        config_dir = project_root / "config"
        if config_dir.exists():
            config_files = [f.name for f in config_dir.rglob("*.json")]
            for config_file in sorted(config_files):
                info += f"  {config_file}\n"
        else:
            info += "  No configuration files found\n"
        
        return info
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Dream.OS Autonomous Framework

A sophisticated multi-agent system designed for autonomous development and collaboration.

Features:
• Multi-agent coordination and communication
• Real-time status monitoring and reporting
• Flexible message routing and command processing
• Comprehensive logging and audit trails
• Intuitive GUI for system management

Version: 1.0.0
Build Date: 2024

For more information, see the documentation in the docs/ directory.
"""
        
        messagebox.showinfo("About Dream.OS", about_text)
    
    # Quick action methods
    def quick_ping_all(self):
        """Quick ping all agents"""
        self.update_status("Pinging all agents...")
        if hasattr(self, 'coordinator_tab'):
            self.coordinator_tab.test_all_agents()
    
    def quick_system_status(self):
        """Quick system status check"""
        self.update_status("Getting system status...")
        if hasattr(self, 'coordinator_tab'):
            self.coordinator_tab.get_system_health()
    
    def quick_sync_all(self):
        """Quick sync all agents"""
        self.update_status("Syncing all agents...")
        if hasattr(self, 'coordinator_tab'):
            self.coordinator_tab.sync_all_agents()
    
    def quick_resume_all(self):
        """Quick resume all agents"""
        self.update_status("Resuming all agents...")
        if hasattr(self, 'coordinator_tab'):
            self.coordinator_tab.resume_all_agents()
    
    def quick_test_connectivity(self):
        """Quick connectivity test"""
        self.update_status("Testing connectivity...")
        if hasattr(self, 'messenger_tab'):
            self.messenger_tab.test_connectivity()
    
    def quick_get_workloads(self):
        """Quick get agent workloads"""
        self.update_status("Getting agent workloads...")
        if hasattr(self, 'coordinator_tab'):
            self.coordinator_tab.get_agent_workloads()
    
    def quick_emergency_broadcast(self):
        """Quick emergency broadcast"""
        message = tk.simpledialog.askstring("Emergency Broadcast", 
                                          "Enter emergency message:")
        if message:
            self.update_status("Sending emergency broadcast...")
            if hasattr(self, 'coordinator_tab'):
                self.coordinator_tab.emergency_broadcast(message)
    
    def quick_health_check(self):
        """Quick health check"""
        self.update_status("Performing health check...")
        if hasattr(self, 'coordinator_tab'):
            self.coordinator_tab.get_system_health()
    
    def quick_onboard_all(self):
        """Quick onboard all agents"""
        self.update_status("Onboarding all agents...")
        if hasattr(self, 'onboarding_tab'):
            self.onboarding_tab.onboard_all_agents()
    
    def quick_verify_all(self):
        """Quick verify all agents"""
        self.update_status("Verifying all agents...")
        if hasattr(self, 'coordinator_tab'):
            self.coordinator_tab.verify_all_agents()
    
    def quick_balance_workload(self):
        """Quick balance workload"""
        self.update_status("Balancing workload...")
        if hasattr(self, 'coordinator_tab'):
            self.coordinator_tab.balance_workload()
    
    def quick_clear_logs(self):
        """Quick clear all logs"""
        if messagebox.askyesno("Clear Logs", "Are you sure you want to clear all logs?"):
            self.update_status("Clearing all logs...")
            if hasattr(self, 'messenger_tab'):
                self.messenger_tab.clear_log()
            if hasattr(self, 'onboarding_tab'):
                self.onboarding_tab.clear_log()
            if hasattr(self, 'coordinator_tab'):
                self.coordinator_tab.clear_log()
            self.quick_status_text.delete(1.0, tk.END)
            self.monitoring_text.delete(1.0, tk.END)
    
    def toggle_monitoring(self):
        """Toggle real-time monitoring"""
        if self.monitoring_var.get():
            self.start_monitoring()
        else:
            self.stop_monitoring()
    
    def start_monitoring(self):
        """Start real-time monitoring"""
        self.update_status("Starting real-time monitoring...")
        self.monitoring_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.monitoring_thread.start()
    
    def stop_monitoring(self):
        """Stop real-time monitoring"""
        self.update_status("Stopping real-time monitoring...")
        self.monitoring_var.set(False)
    
    def monitoring_loop(self):
        """Real-time monitoring loop"""
        while self.monitoring_var.get():
            try:
                self.refresh_monitoring()
                time.sleep(30)  # Update every 30 seconds
            except Exception as e:
                self.after(0, lambda: self.update_status(f"Monitoring error: {e}"))
                break
    
    def refresh_monitoring(self):
        """Refresh monitoring display"""
        try:
            # Get current system status
            status_text = "Real-time System Status\n"
            status_text += "=" * 50 + "\n"
            status_text += f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            # Add monitoring information here
            status_text += "Monitoring active...\n"
            status_text += "Check individual tabs for detailed status.\n"
            
            self.monitoring_text.delete(1.0, tk.END)
            self.monitoring_text.insert(1.0, status_text)
            
        except Exception as e:
            self.monitoring_text.delete(1.0, tk.END)
            self.monitoring_text.insert(1.0, f"Error refreshing monitoring: {e}")

def main():
    """Main entry point"""
    root = tk.Tk()
    app = DreamOSGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Utilities Module - Common utility classes and functions
Provides consolidated functionality for the Agent Cell Phone system
"""

import os
import configparser
import logging
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import datetime

class MLRobotUtils:
    """Utility class for MLRobotmaker operations"""
    
    def __init__(self, is_debug_mode=False):
        self.is_debug_mode = is_debug_mode

    def log_message(self, message, root_window=None, log_text_widget=None):
        """Log a message to console and optionally to a text widget"""
        if self.is_debug_mode:
            print(message)  # Log to the console

        if log_text_widget and isinstance(log_text_widget, tk.Text) and root_window:
            def append_message():
                log_text_widget.config(state='normal')
                log_text_widget.insert(tk.END, message + "\n")
                log_text_widget.config(state='disabled')
                log_text_widget.see(tk.END)

            root_window.after(0, append_message)

    def get_model_types(self):
        """Return a list of supported model types."""
        return ['linear_regression', 'random_forest', 'lstm', 'neural_network', 'arima']
    
    def select_directory(self, entry):
        """Select a directory using file dialog"""
        directory = filedialog.askdirectory()
        if self.is_debug_mode:
            self.log_message(f"Debug: Selected directory - {directory}", None)
        if directory:
            entry.delete(0, tk.END)
            entry.insert(0, directory)

    def save_preferences(self, config, data_fetch_entry, data_processing_entry, model_training_entry, directory_entry):
        """Save application preferences to config file"""
        config['DataDirectories']['DataFetchDirectory'] = data_fetch_entry.get()
        config['DataDirectories']['DataProcessingDirectory'] = data_processing_entry.get()
        config['DataDirectories']['ModelTrainingDirectory'] = model_training_entry.get()
        config['DEFAULT']['LastDirectory'] = directory_entry.get()
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def browse_directory(self, entry):
        """Browse and select a directory"""
        directory = filedialog.askdirectory()
        if directory:
            entry.delete(0, tk.END)
            entry.insert(0, directory)
            if self.is_debug_mode:
                self.log_message(f"Debug: Directory selected - {directory}", None)

    def auto_generate_save_path(self, input_file_path, base_dir):
        """Generate a save path with timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        base_name, extension = os.path.splitext(os.path.basename(input_file_path))

        if extension.lower() != '.csv':
            raise ValueError("Input file is not a CSV file.")

        new_filename = f"{base_name}_processed_{timestamp}.csv"
        return os.path.join(base_dir, new_filename)

    def generate_save_path(self, file_path, config):
        """Generate a save path based on configuration"""
        directory, filename = os.path.split(file_path)
        name, extension = os.path.splitext(filename)
        save_directory = config.get('SAVE_PATH_SECTION', {}).get('save_path_dir', directory)
        new_filename = f"{name}_processed{extension}"
        save_path = os.path.join(save_directory, new_filename)
        return save_path

    def update_status(self, status_output, message):
        """Update status text widget"""
        if hasattr(status_output, 'config'):
            status_output.config(state=tk.NORMAL)
            status_output.delete(1.0, tk.END)
            status_output.insert(tk.END, message + "\n")
            status_output.config(state=tk.DISABLED)

    def browse_data_file(self, data_file_entry):
        """Browse and select a data file"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            data_file_entry.delete(0, tk.END)
            data_file_entry.insert(0, file_path)

# Convenience functions for backward compatibility
def get_ml_robot_utils(debug_mode=False):
    """Get an instance of MLRobotUtils"""
    return MLRobotUtils(debug_mode)

def log_message(message, debug_mode=False):
    """Quick logging utility"""
    utils = MLRobotUtils(debug_mode)
    utils.log_message(message)

__all__ = ['MLRobotUtils', 'get_ml_robot_utils', 'log_message']




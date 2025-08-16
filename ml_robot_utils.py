#!/usr/bin/env python3
"""
MLRobotUtils - Utility class for MLRobotmaker
Provides common functionality for data processing, configuration, and logging
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

    def load_configuration(self, config_file='config.ini'):
        """Load configuration from file"""
        config = configparser.ConfigParser()
        if not os.path.exists(config_file):
            logging.error(f"Configuration file does not exist: {config_file}")
            raise FileNotFoundError(f"Configuration file does not exist: {config_file}")
        config.read(config_file)
        logging.info("Configuration file loaded successfully.")
        return config

    def setup_logging(self, level=logging.INFO):
        """Setup logging configuration"""
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=level)

    def validate_section_keys(self, config, section, required_keys):
        """Validate that required keys exist in a config section"""
        if section not in config:
            raise ValueError(f"Config section '{section}' not found")
        missing_keys = [key for key in required_keys if key not in config[section]]
        if missing_keys:
            raise ValueError(f"Missing required config key(s) in '{section}': {', '.join(missing_keys)}")

    def save_data_to_csv(self, data_frame, ticker_symbol):
        """Save data frame to CSV file"""
        # Create output directory if it doesn't exist
        output_dir = "csv_files/output"
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{ticker_symbol}_data.csv"
        file_path = os.path.join(output_dir, filename)
        data_frame.to_csv(file_path, index=False)
        print(f"Data for {ticker_symbol} saved to {file_path}")
        return file_path

    def clear_logs(self):
        """Clear log text widget"""
        pass  # Placeholder for log clearing functionality

    def toggle_debug_mode(self, debug_mode_button):
        """Toggle debug mode on/off"""
        self.is_debug_mode = not self.is_debug_mode
        print(f"Debug mode set to: {self.is_debug_mode}")

        if self.is_debug_mode:
            debug_mode_button.config(text="Debug Mode: ON")
            print("Debug mode is now ON")
        else:
            debug_mode_button.config(text="Debug Mode: OFF")
            print("Debug mode is now OFF")

    def browse_save_directory(self):
        """Browse and select save directory"""
        save_dir = filedialog.askdirectory()
        if save_dir:
            return save_dir
        return None


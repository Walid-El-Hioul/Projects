import json
import os
from src.ui.ids_ui.errors_panel import MainErrorWindow


class Config:
    def __init__(self):
        self.script_dir = os.path.dirname(__file__)
        self.config_path = os.path.abspath(os.path.join(self.script_dir, '../../config/environment/config.json'))
        self.error_window = MainErrorWindow()

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as config_file:
                try:
                    return json.load(config_file)
                except json.JSONDecodeError as e:
                    message = "Error decoding JSON from the main configuration file."
                    self.error_window.show_error(message, e)
                except Exception as e:
                    message = "An unexpected error occurred while loading the main configuration file."
                    self.error_window.show_error(message, e)
        else:
            self.error_window.show_error("Main configuration file not found.")

    def load_db_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as config_file:
                try:
                    return json.load(config_file)
                except json.JSONDecodeError as e:
                    message = "Error decoding JSON from the database configuration file."
                    self.error_window.show_error(message, e)
                except Exception as e:
                    message = "An unexpected error occurred while loading the database configuration file."
                    self.error_window.show_error(message, e)
        else:
            self.error_window.show_error("Database configuration file not found.")

    def load_alert_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as config_file:
                try:
                    return json.load(config_file)
                except json.JSONDecodeError as e:
                    message = "Error decoding JSON from the alert configuration file."
                    self.error_window.show_error(message, e)
                except Exception as e:
                    message = "An unexpected error occurred while loading the alert configuration file."
                    self.error_window.show_error(message, e)
        else:
            self.error_window.show_error("Alert configuration file not found.")

    def load_interface_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as config_file:
                try:
                    return json.load(config_file)
                except json.JSONDecodeError as e:
                    message = "Error decoding JSON from the interface configuration file."
                    self.error_window.show_error(message, e)
                except Exception as e:
                    message = "An unexpected error occurred while loading the interface configuration file."
                    self.error_window.show_error(message, e)
        else:
            self.error_window.show_error("Interface configuration file not found.")

    def write_config_update(self, section, new_data):
        try:
            config_data = {}

            if os.path.exists(self.config_path) and os.path.getsize(self.config_path) > 0:
                with open(self.config_path, 'r') as f:
                    try:
                        config_data = json.load(f)
                    except json.JSONDecodeError:
                        config_data = {}

            if section not in config_data:
                config_data[section] = {}

            config_data[section].update(new_data)

            with open(self.config_path, 'w') as f:
                json.dump(config_data, f, indent=4)

        except Exception as e:
            self.error_window.show_error("Error writing to configuration file.", e)








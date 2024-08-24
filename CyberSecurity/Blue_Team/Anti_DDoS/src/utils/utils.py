import json
import os


class Utils:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        config_path = os.path.join('config', 'config.json')

        if os.path.exists(config_path):
            with open(config_path, 'r') as config_file:
                try:
                    return json.load(config_file)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from config file: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
        else:
            print("Config file not found.")

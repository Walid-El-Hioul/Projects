import os
import json

script_dir = os.path.dirname(__file__)
config_path = os.path.abspath(os.path.join(script_dir, '../../config/environment/config.json'))


if os.path.exists(config_path):
    try:

        with open(config_path, 'r') as config_file:
            try:
                read = json.load(config_file)
                print(read)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
    except IOError as e:
        print(f"Error opening file: {e}")
else:
    print("Configuration file not found.")

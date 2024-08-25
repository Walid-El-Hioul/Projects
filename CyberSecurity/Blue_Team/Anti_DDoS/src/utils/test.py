import os
import json

# Define the path to the configuration file
script_dir = os.path.dirname(__file__)  # Gets the directory of the current script
config_path = os.path.abspath(os.path.join(script_dir, '../../config/environment/config.json'))

# Check if the file exists before attempting to open it
if os.path.exists(config_path):
    try:
        # Open and read the JSON file
        with open(config_path, 'r') as config_file:
            try:
                read = json.load(config_file)
                print(read)  # Print the loaded JSON data
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
    except IOError as e:
        print(f"Error opening file: {e}")
else:
    print("Configuration file not found.")

import json
import os


def prompt_for_config():
    config = {}

    # Database configuration
    print("Please enter your database configuration:")
    config['db_config'] = {
        'host': input("MySQL Host: "),
        'user': input("MySQL User: "),
        'password': input("MySQL Password: "),
        'database_anomalies': input("Name of the anomalies database: "),
        'database_packets': input("Name of the packets database: ")
    }

    print("Please enter your interface configuration:")
    config['interface'] = {
        'interface': input("Interface: ")
    }

    # Save configuration to config.json
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
    print("Configuration saved to config.json")


if __name__ == "__main__":
    prompt_for_config()

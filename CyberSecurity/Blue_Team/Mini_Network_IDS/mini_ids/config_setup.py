import json
import getpass


def prompt_for_config():
    config = {}

    # Database configuration with default values
    print("Please enter your database configuration:")
    config['db_config'] = {
        'host': input("MySQL Host (default: localhost): ") or "localhost",
        'user': input("MySQL User: "),
        'password': getpass.getpass("MySQL Password (input will be hidden): ")
    }

    # Interface configuration
    print("Please enter your interface configuration:")
    config['interface'] = {
        'interface': input("Interface: ")
    }

    # Alerts configuration with email validation
    print("Please enter your alert configuration:")

    def validate_email(email):
        return '@' in email and '.' in email

    while True:
        sender_gmail = input("Sender Gmail: ")
        if validate_email(sender_gmail):
            break
        print("Invalid email format. Please try again.")

    while True:
        receiver_email = input("Receiver email: ")
        if validate_email(receiver_email):
            break
        print("Invalid email format. Please try again.")

    config['alert_config'] = {
        'sender_gmail': sender_gmail,
        'password': getpass.getpass("Gmail password (input will be hidden): "),
        'receiver_email': receiver_email
    }

    # Save configuration to config.json
    try:
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        print("Configuration saved to config.json")
    except IOError as e:
        print(f"Failed to save configuration: {e}")

import json
import getpass
import wmi


def get_network_interfaces():
    c = wmi.WMI()
    interfaces = []

    for adapter in c.Win32_NetworkAdapterConfiguration():
        description = adapter.Description
        mac_address = adapter.MACAddress
        ip_address = ", ".join(adapter.IPAddress) if adapter.IPAddress else "No IP"
        is_enabled = adapter.IPEnabled
        interfaces.append({
            'name': description,
            'mac': mac_address,
            'ip': ip_address,
            'is_enabled': is_enabled
        })

    return interfaces


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
    print("Please choose your network interface:")
    interfaces = get_network_interfaces()

    if not interfaces:
        print("No valid network interfaces found. Exiting the configuration.")
        return

    # Display interfaces in a user-friendly format
    for i, iface in enumerate(interfaces):
        iface_name = iface['name']
        iface_mac = iface['mac']
        iface_ip = iface['ip']
        iface_status = "Enabled" if iface['is_enabled'] else "Disabled"
        print(f"[{i}] {iface_name} : {iface_status}")
        print(f"  ├─ IP  : {iface_ip}")
        print(f"  └─ MAC : {iface_mac}")

    while True:
        try:
            interface_index = int(input("Select an interface by number: "))
            if 0 <= interface_index < len(interfaces):
                selected_interface = interfaces[interface_index]
                break
            else:
                print("Invalid selection. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    config['interface'] = {
        'interface': selected_interface['name'],
        'mac': selected_interface['mac'],
        'ip': selected_interface['ip'],
        'is_enabled': selected_interface['is_enabled']
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
        print(f"Configuration saved to config.json with selected interface: {config['interface']['interface']}")
    except IOError as e:
        print(f"Failed to save configuration: {e}")


prompt_for_config()
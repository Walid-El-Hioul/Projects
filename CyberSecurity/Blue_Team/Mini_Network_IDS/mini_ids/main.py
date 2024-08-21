import json
import getpass
import sys
import os
import netifaces


def get_network_interfaces():
    interfaces = []
    if sys.platform.startswith('win'):
        # Windows
        import ctypes
        from ctypes import Structure, POINTER, byref, cast
        from ctypes.wintypes import DWORD, ULONG, BYTE, WCHAR

        class IP_ADAPTER_INFO(Structure):
            _fields_ = [("Next", POINTER("IP_ADAPTER_INFO")),
                        ("ComboIndex", DWORD),
                        ("AdapterName", CHAR * 260),
                        ("Description", CHAR * 132),
                        ("AddressLength", ULONG),
                        ("Address", BYTE * 8),
                        ("Index", DWORD),
                        ("Type", DWORD),
                        ("DhcpEnabled", DWORD),
                        ("CurrentIpAddress", POINTER("IP_ADDR_STRING")),
                        ("IpAddressList", "IP_ADDR_STRING"),
                        ("GatewayList", "IP_ADDR_STRING"),
                        ("DhcpServer", "IP_ADDR_STRING"),
                        ("HaveWins", DWORD),
                        ("PrimaryWinsServer", "IP_ADDR_STRING"),
                        ("SecondaryWinsServer", "IP_ADDR_STRING"),
                        ("LeaseObtained", DWORD),
                        ("LeaseExpires", DWORD)]

        adapter_info = IP_ADAPTER_INFO()
        adapter_ptrs = POINTER(IP_ADAPTER_INFO)()
        size = ULONG(ctypes.sizeof(adapter_info))
        rc = ctypes.windll.iphlpapi.GetAdaptersInfo(cast(byref(adapter_ptrs), POINTER(IP_ADAPTER_INFO)), byref(size))
        if rc == 0:
            current_adapter = adapter_ptrs
            while current_adapter:
                interfaces.append(current_adapter.contents)
                current_adapter = current_adapter.contents.Next
    else:
        # Linux/macOS
        interfaces = [netifaces.ifaddresses(iface).get(netifaces.AF_INET, [{'addr': 'N/A'}])[0] for iface in
                      netifaces.interfaces()]
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

    # Display interfaces with human-readable names
    for i, iface in enumerate(interfaces):
        try:
            if sys.platform.startswith('win'):
                iface_name = iface.Description.decode()
                iface_ip = iface.IpAddressList.IpAddress.decode()
                iface_mac = ':'.join(f'{b:02X}' for b in iface.Address)
            else:
                iface_name = iface.get('name', 'Unknown')
                iface_ip = iface.get('addr', 'N/A')
                iface_mac = ':'.join(f'{b:02X}' for b in iface.get('addr', [0] * 6))
            print(f"[{i}] {iface_name} - IP: {iface_ip}, MAC: {iface_mac}")
        except Exception as e:
            print(f"[{i}] {iface_name} - Error retrieving details: {e}")

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

    if sys.platform.startswith('win'):
        config['interface'] = {
            'interface': selected_interface.Description.decode()
        }
    else:
        config['interface'] = {
            'interface': selected_interface.get('name', 'Unknown')
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


if __name__ == "__main__":
    prompt_for_config()
from scapy.all import *
import threading
from config_setup import prompt_for_config
import json


class BasePacketSniffer:
    def __init__(self):
        # Initialize the threading event to control sniffing
        self.stop_event = threading.Event()
        self.config = self.load_config()
        if self.config is None:
            raise ValueError("Configuration could not be loaded. Please check your config.json file.")
        self.interface = self.config['interface'][
            'interface']  # This line assumes that 'interface' exists in the config

    def start_sniffing(self, prn):
        # Start sniffing packets on the specified interface
        sniff(iface=self.interface, store=False, prn=prn, stop_filter=self.stop_check)

    def stop_check(self, packet):
        # Check if the stop event is set to halt the sniffing
        return self.stop_event.is_set()

    def stop_sniffing(self):
        # Set the stop event to signal the sniffing to stop
        self.stop_event.set()

    def load_config(self):
        config_path = 'config.json'
        if os.path.exists(config_path):
            with open(config_path, 'r') as config_file:
                try:
                    return json.load(config_file)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from config file: {e}")
                    return None
        else:
            print("Config file not found.")
            return None

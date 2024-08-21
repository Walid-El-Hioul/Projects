from scapy.all import *
import threading
import json


class BasePacketSniffer:
    def __init__(self):
        self.stop_event = threading.Event()
        self.config = self.load_config()
        if self.config is None:
            raise ValueError("Configuration could not be loaded. Please check your config.json file.")
        self.interface = self.config['interface']['interface']
        self.mini_ids = None

    def start_sniffing(self):
        if self.mini_ids is None:
            from mini_ids import MiniIDS
            self.mini_ids = MiniIDS()

        sniff(iface=self.interface, store=False, prn=self.mini_ids.packet_callback, stop_filter=self.stop_check)

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
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
        else:
            print("Config file not found.")

        # If loading the config failed, prompt the user to create a new config
        user_input = input(
            "Configuration could not be loaded. Would you like to create a new configuration? (yes/no): ").strip().lower()
        if user_input == 'yes':
            from config_setup import prompt_for_config
            prompt_for_config()
            # Try loading the config again after creating it
            return self.load_config()
        else:
            print("Exiting because configuration could not be loaded or created.")
            return None



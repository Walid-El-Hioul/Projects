from scapy.all import *
import threading
from config_setup import prompt_for_config
import json


class BasePacketSniffer:
    def __init__(self):
        # Initialize the threading event to control sniffing
        self.stop_event = threading.Event()
        self.config = self.load_config()
        self.interface = self.config['interface']

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
        if not os.path.exists('config.json'):
            prompt_for_config()

            with open('config.json') as f:
                return json.load(f)
from scapy.all import *
from anomaly_detection import PacketDetector
import threading
from logger import AnomalyLogger, PacketLogger
import json

# Global event to control sniffing
stop_event = threading.Event()

class PacketSniffer:
    def __init__(self):
        config = self.load_config()
        self.interface = config['interface']
        self.packet_detector = PacketDetector()
        self.anomaly_logger = AnomalyLogger()
        self.packet_logger = PacketLogger()

    def load_config(self):
        with open('config.json') as f:
            return json.load(f)

    def packet_callback(self, packet):
        self.packet_detector.detect(packet)
        # Log the packet data
        self.packet_logger.log_packet(
            src_ip=packet[IP].src if packet.haslayer(IP) else "N/A",
            dst_ip=packet[IP].dst if packet.haslayer(IP) else "N/A",
            protocol=packet.proto if packet.haslayer(IP) else "N/A",
            length=len(packet),
            payload=bytes(packet)[:100]  # Log first 100 bytes of the payload
        )

    def start_sniffing(self):
        sniff(iface=self.interface, store=False, prn=self.packet_callback, stop_filter=self.stop_check)

    def stop_check(self, packet):
        return stop_event.is_set()

def user_input():
    while True:
        command = input()
        if command.lower() == "exit":
            stop_event.set()  # Signal to stop sniffing
            break

# Run the config setup if config.json doesn't exist
import os
if not os.path.exists('config.json'):
    from config_setup import setup_config
    setup_config()

# Create an instance of PacketSniffer
sniffer = PacketSniffer()

# Start sniffing in a separate thread
sniff_thread = threading.Thread(target=sniffer.start_sniffing)
sniff_thread.start()

# Start listening for user input
user_input()

# Wait for sniffing thread to finish
sniff_thread.join()

# Clean up
sniffer.packet_logger.delete_old_tables()
sniffer.packet_logger.close()
sniffer.anomaly_logger.close()

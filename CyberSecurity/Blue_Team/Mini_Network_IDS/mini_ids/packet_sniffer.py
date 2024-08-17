from scapy.all import *
from anomaly_detection import PacketDetector
import threading

# Global event to control sniffing
stop_event = threading.Event()

class PacketSniffer:
    def __init__(self, interface="Ethernet"):
        self.interface = interface
        self.packet_detector = PacketDetector()

    def packet_callback(self, packet):
        self.packet_detector.detect(packet)

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

# Create an instance of PacketSniffer
sniffer = PacketSniffer(interface="Ethernet")

# Start sniffing in a separate thread
sniff_thread = threading.Thread(target=sniffer.start_sniffing)
sniff_thread.start()

# Start listening for user input
user_input()

# Wait for sniffing thread to finish
sniff_thread.join()

from scapy.all import *
import threading
from utils import Utils


class BasePacketSniffer:
    def __init__(self):
        self.stop_event = threading.Event()
        self.utils = Utils()
        self.config = self.utils.load_config()
        self.interface = self.config['interface']['interface']
        self.anomalies_detector = None

    # def load_interface_config(self):
    def start_sniffing(self):
        if self.anomalies_detector is None:
            from anomalies_detector import AnomaliesDetector
            self.anomalies_detector = AnomaliesDetector()

        sniff(iface=self.interface, store=False, prn=self.anomalies_detector.packet_callback,
              stop_filter=self.stop_check)

    def stop_check(self, packet):
        return self.stop_event.is_set()

    def stop_sniffing(self):
        self.stop_event.set()



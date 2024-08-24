from base_packet_sniffer import BasePacketSniffer
from anomaly_detection import AnomaliesDetection
from logger import AnomalyLogger, PacketLogger, Logger, PcapFileLogger
from scapy.all import rdpcap
import threading
from anomalies_detector import AnomaliesDetector


class MiniIDS:
    def __init__(self):
        self.anomalies_detector = AnomaliesDetector()
        self.packet_sniffer = BasePacketSniffer()
        self.packet_detector = AnomaliesDetection()
        self.anomaly_logger = AnomalyLogger()
        self.packet_logger = PacketLogger()
        self.stop_event = threading.Event()
        self.logger = Logger()
        self.stop_logger = self.logger.close_db()
        self.alert_enabled = True

    def start_ids(self):
        self.logger.create_db()
        self.logger.connect_to_db()

        # Start packet sniffing in a separate thread
        self.packet_sniffer.start_sniffing()

    def stop_ids(self):
        self.stop_event.set()
        self.packet_sniffer.stop_sniffing()
        self.packet_logger.close_pcap()
        self.stop_logger()
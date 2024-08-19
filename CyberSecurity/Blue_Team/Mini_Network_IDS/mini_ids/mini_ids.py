from base_packet_sniffer import BasePacketSniffer
from anomaly_detection import AnomaliesDetection
from logger import AnomalyLogger, PacketLogger, Logger
import threading


class MiniIDS:
    def __init__(self):
        self.packet_sniffer = BasePacketSniffer()
        self.packet_detector = AnomaliesDetection()
        self.anomaly_logger = AnomalyLogger()
        self.packet_logger = PacketLogger()
        self.stop_event = threading.Event()
        self.stop_logger = Logger.close_db()

    def packet_callback(self, packet):
        # Detect anomalies
        detect_anomalies = self.packet_detector.detect(packet)
        if detect_anomalies:
            self.anomaly_logger.log_anomaly(f"Anomaly detected: {detect_anomalies}")

        # Log the entire packet to the PCAP file
        try:
            self.packet_logger.log_packet(packet)
        except Exception as e:
            print(f"Error while logging packet: {e}")

    def start_ids(self, packet):
        # Start packet sniffing in a separate thread
        sniff_thread = threading.Thread(target=self.packet_sniffer.start_sniffing(prn=self.packet_callback(packet)))
        sniff_thread.start()

        # Wait for the sniffing to be stopped
        sniff_thread.join()

    def stop_ids(self):
        self.stop_event.set()  # Signal to stop sniffing
        self.packet_sniffer.stop_sniffing()
        self.packet_logger.close_pcap()
        self.stop_logger()




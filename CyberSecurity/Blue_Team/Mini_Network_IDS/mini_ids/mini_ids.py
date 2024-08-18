from base_packet_sniffer import BasePacketSniffer
from anomaly_detection import PacketDetector
from logger import AnomalyLogger, PacketLogger
import threading


class MiniIDS:
    def __init__(self):
        self.packet_sniffer = BasePacketSniffer()
        self.packet_detector = PacketDetector()
        self.anomaly_logger = AnomalyLogger()
        self.packet_logger = PacketLogger()
        self.stop_event = threading.Event()

    def packet_callback(self, packet):
        # Detect anomalies
        if self.packet_detector.detect(packet):
            # Log anomalies
            self.anomaly_logger.log_anomaly("Anomaly detected!")

        # Log packets
        self.packet_logger.log_packet(
            src_ip=packet[IP].src if packet.haslayer(IP) else "N/A",
            dst_ip=packet[IP].dst if packet.haslayer(IP) else "N/A",
            protocol=packet.proto if packet.haslayer(IP) else "N/A",
            length=len(packet),
            payload=bytes(packet)[:100]  # Log first 100 bytes of the payload
        )

    def start(self):
        # Start packet sniffing in a separate thread
        sniff_thread = threading.Thread(target=self.packet_sniffer.start_sniffing(prn="self.packet_callback()"))
        sniff_thread.start()

        # Wait for the sniffing to be stopped
        sniff_thread.join()

    def stop(self):
        self.stop_event.set()  # Signal to stop sniffing
        self.packet_sniffer.stop_sniffing()
        self.packet_logger.delete_old_tables()
        self.packet_logger.close()
        self.anomaly_logger.close()




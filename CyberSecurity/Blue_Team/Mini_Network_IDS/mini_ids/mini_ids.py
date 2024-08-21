from base_packet_sniffer import BasePacketSniffer
from anomaly_detection import AnomaliesDetection
from logger import AnomalyLogger, PacketLogger, Logger, PcapFileLogger
from scapy.all import rdpcap
import threading


class MiniIDS:
    def __init__(self):
        self.packet_sniffer = BasePacketSniffer()
        self.packet_detector = AnomaliesDetection()
        self.anomaly_logger = AnomalyLogger()
        self.packet_logger = PacketLogger()
        self.stop_event = threading.Event()
        self.logger = Logger()
        self.logger.create_db(db_name="anomalies_db")
        self.logger.connect_to_db(db_name="anomalies_db")
        self.stop_logger = self.logger.close_db

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

    def process_pcap_file(self, pcap_file_path):
        # Create a separate logger for this PCAP file
        pcap_file_logger = PcapFileLogger(pcap_file_path)

        try:
            packets = rdpcap(pcap_file_path)
            for packet in packets:
                # Process each packet using the existing detection logic
                detect_anomalies = self.packet_detector.detect(packet)
                if detect_anomalies:
                    pcap_file_logger.log_analysis(f"Anomaly detected: {detect_anomalies}")

                # Log the packet in the PCAP file logger
                pcap_file_logger.log_packet(packet)
        except Exception as e:
            print(f"Error while processing PCAP file {pcap_file_path}: {e}")
        finally:
            pcap_file_logger.close_pcap()
            print("Finished processing PCAP file.")

    def start_ids(self):
        # Start packet sniffing in a separate thread
        sniff_thread = threading.Thread(target=self.packet_sniffer.start_sniffing)
        sniff_thread.start()

        # Wait for the sniffing to be stopped
        sniff_thread.join()

    def stop_ids(self):
        self.stop_event.set()  
        self.packet_sniffer.stop_sniffing()
        self.packet_logger.close_pcap()
        self.stop_logger()

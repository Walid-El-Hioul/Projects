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
        self.stop_logger = self.logger.close_db()
        self.alert_enabled = True

    def packet_callback(self, packet):
        detect_anomalies = self.packet_detector.detect(packet)
        if detect_anomalies:
            self.anomaly_logger.log_anomaly(f"Anomaly detected: {detect_anomalies}")
            if self.alert_enabled:
                # If alerting is enabled, send an alert
                self.send_alert("Anomaly Detected", f"Anomaly detected: {detect_anomalies}")

        # Log the entire packet to the PCAP file
        try:
            self.packet_logger.log_packet(packet)
        except Exception as e:
            print(f"Error while logging packet: {e}")

    def process_pcap_file(self, pcap_file_path):
        # Disable alerts when processing PCAP files
        self.alert_enabled = False

        pcap_file_logger = PcapFileLogger(pcap_file_path)

        try:
            packets = rdpcap(pcap_file_path)
            for packet in packets:
                detect_anomalies = self.packet_detector.detect(packet)
                if detect_anomalies:
                    pcap_file_logger.log_analysis(f"Anomaly detected: {detect_anomalies}")

        except Exception as e:
            print(f"Error while processing PCAP file {pcap_file_path}: {e}")
        finally:
            pcap_file_logger.close_pcap()
            print("Finished processing PCAP file.")

    def send_alert(self, subject, message):
        try:
            # Assuming AnomalyLogger is already configured to send emails
            self.anomaly_logger.send_email_alert(subject, message)
        except Exception as e:
            print(f"Failed to send alert: {e}")

    def start_ids(self):
        self.logger.create_db()
        self.logger.connect_to_db()
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


mini_ids = MiniIDS()

mini_ids.start_ids()
#mini_ids.process_pcap_file("packet_logs_2024_08_20.pcap")

from scapy.all import *
from collections import defaultdict
import time
from base_packet_sniffer import BasePacketSniffer
from anomaly_detection import AnomaliesDetection
from logger import AnomalyLogger, PacketLogger, Logger, PcapFileLogger
from scapy.all import rdpcap
import threading


class AnomaliesDetectorLogic:
    def __init__(self):
        self.syn_count = defaultdict(int)
        self.syn_threshold = 300
        self.time_window = 60  # in second
        self.last_time = time.time()
        self.http_count = defaultdict(int)
        self.http_threshold = 500
        self.http_time_window = 60
        self.blocked_ips = set()

    def block_ip(self, ip):
        if ip not in self.blocked_ips:
            os.system(f"iptables -A INPUT -s {ip} -j DROP")
            self.blocked_ips.add(ip)
            print(f"Blocked IP: {ip}")

    def detect(self, packet):
        try:
            self.detect_syn_flood(packet)
            self.detect_http_flood(packet)
        except Exception as e:
            print(f"Error occurred: {e}")

    def detect_syn_flood(self, packet):
        current_time = time.time()
        if current_time - self.last_time > self.time_window:
            self.syn_count.clear()
            self.last_time = current_time

        if packet.haslayer(TCP) and packet[TCP].flags & 0x02:  # SYN flag
            src_ip = packet[IP].src
            self.syn_count[src_ip] += 1
            if self.syn_count[src_ip] > self.syn_threshold:
                alert_message = f"Detected SYN flood attack from {src_ip}"
                print(alert_message)

    def detect_http_flood(self, packet):
        current_time = time.time()

        if packet.haslayer(TCP) and packet.haslayer(Raw):
            payload = packet[Raw].load.decode(errors='ignore')
            if "HTTP" in payload:
                src_ip = packet[IP].src
                self.http_count[src_ip] += 1

                # Reset the count after the time window
                if current_time - self.last_time > self.http_time_window:
                    self.http_count.clear()
                    self.last_time = current_time

                if self.http_count[src_ip] > self.http_threshold:
                    alert_message = f"Detected HTTP flood attack from {src_ip}"
                    print(alert_message)


class AnomaliesDetector:
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
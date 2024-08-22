from scapy.all import *
from collections import defaultdict
import time


class AnomaliesDetection:
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

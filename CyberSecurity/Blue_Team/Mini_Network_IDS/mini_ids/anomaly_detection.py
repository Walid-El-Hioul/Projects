from scapy.all import *
from collections import defaultdict
import time

class PacketDetector:
    def __init__(self):
        self.syn_count = defaultdict(int)
        self.syn_threshold = 300  # Increased threshold
        self.time_window = 60
        self.last_time = time.time()
        self.port_scan_count = defaultdict(set)
        self.port_scan_threshold = 40  # Increased threshold
        self.dns_count = defaultdict(int)
        self.dns_threshold = 100  # Increased threshold
        self.data_threshold = 30000  # Increased threshold
        self.data_transfers = defaultdict(int)
        self.unauthorized_ports = {22, 23, 3389}
        self.ip_mac_map = {}

    def detect(self, packet):
        try:
            self.detect_syn_flood(packet)
            self.detect_port_scanning(packet)
            self.detect_dns_flooding(packet)
            self.detect_large_data_transfers(packet)
            self.detect_sql_injection(packet)
            self.detect_xss(packet)
            self.detect_unauthorized_access(packet)
            self.detect_ip_spoofing(packet)
            self.detect_packet_injection(packet)
            #self.detect_abnormal_protocol_usage(packet)
        except Exception as e:
            print(f"Error occurred: {e}")

    def detect_syn_flood(self, packet):
        current_time = time.time()
        if current_time - self.last_time > self.time_window:
            self.syn_count.clear()
            self.last_time = current_time

        if packet.haslayer(TCP) and packet[TCP].flags & 0x02:  # SYN flag
            self.syn_count[packet[IP].src] += 1
            if self.syn_count[packet[IP].src] > self.syn_threshold:
                print(f"Detected SYN flood attack from {packet[IP].src}")

    def detect_port_scanning(self, packet):
        if packet.haslayer(TCP) and packet.haslayer(IP):
            src_ip = packet[IP].src
            dst_port = packet[TCP].dport
            self.port_scan_count[src_ip].add(dst_port)
            if len(self.port_scan_count[src_ip]) > self.port_scan_threshold:
                print(f"Detected port scanning from {src_ip}")

    def detect_dns_flooding(self, packet):
        if packet.haslayer(DNSQR) and packet.haslayer(IP):
            self.dns_count[packet[IP].src] += 1
            if self.dns_count[packet[IP].src] > self.dns_threshold:
                print(f"Detected DNS query flooding from {packet[IP].src}")

    def detect_large_data_transfers(self, packet):
        if packet.haslayer(Raw) and packet.haslayer(IP):
            src_ip = packet[IP].src
            self.data_transfers[src_ip] += len(packet[Raw].load)
            if self.data_transfers[src_ip] > self.data_threshold:
                print(f"Detected large data transfer from {src_ip}")

    def detect_sql_injection(self, packet):
        if packet.haslayer(Raw):
            payload = packet[Raw].load.decode(errors='ignore')
            sql_patterns = ["SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "OR 1=1"]
            for pattern in sql_patterns:
                if pattern in payload.upper():
                    print(f"Detected SQL injection attempt with payload: {payload}")

    def detect_xss(self, packet):
        if packet.haslayer(Raw):
            payload = packet[Raw].load.decode(errors='ignore')
            xss_patterns = ["<script>", "</script>", "javascript:"]
            for pattern in xss_patterns:
                if pattern in payload:
                    print(f"Detected XSS attack with payload: {payload}")

    def detect_unauthorized_access(self, packet):
        if packet.haslayer(TCP) and packet[TCP].dport in self.unauthorized_ports:
            print(f"Detected unauthorized access attempt to port {packet[TCP].dport}")

    def detect_ip_spoofing(self, packet):
        if packet.haslayer(Ether) and packet.haslayer(IP):
            ip = packet[IP].src
            mac = packet[Ether].src
            if ip in self.ip_mac_map and self.ip_mac_map[ip] != mac:
                print(f"Detected IP spoofing: IP {ip} with MAC {mac}")
            self.ip_mac_map[ip] = mac

    def detect_packet_injection(self, packet):
        if packet.haslayer(Raw):
            payload = packet[Raw].load.decode(errors='ignore')
            if len(payload) > 1000:  # Increased threshold for large payloads
                print(f"Detected potential packet injection with payload: {payload}")

    #def detect_abnormal_protocol_usage(self, packet):
      #  if packet.haslayer(UDP) and packet.haslayer(Raw):
           # payload = packet[Raw].load.decode(errors='ignore')
         #   if "HTTP" in payload:
             #   print("Detected abnormal protocol usage: HTTP over UDP")
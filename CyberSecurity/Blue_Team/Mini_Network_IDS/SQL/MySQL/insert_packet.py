from scapy.all import sniff
import mysql.connector
from datetime import datetime

# MySQL connection configuration
db_config = {
    'user': 'Shield',
    'password': 'ELSHIELD12345@@',
    'host': 'localhost',
    'database': 'packet_data',
}

# Connect to MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()


# Function to insert packet data into the database
def insert_packet(src_ip, dst_ip, protocol, length, payload):
    query = """
    INSERT INTO packets (source_ip, destination_ip, protocol, length, payload)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (src_ip, dst_ip, protocol, length, payload))
    conn.commit()


# Callback function for packet processing
def process_packet(packet):
    if packet.haslayer('IP'):
        src_ip = packet['IP'].src
        dst_ip = packet['IP'].dst
        protocol = packet['IP'].proto
        length = len(packet)
        payload = str(packet.payload)

        insert_packet(src_ip, dst_ip, protocol, length, payload)


# Start sniffing
sniff(prn=process_packet, filter="ip", store=0, count=50)

# Close MySQL connection when done
conn.close()

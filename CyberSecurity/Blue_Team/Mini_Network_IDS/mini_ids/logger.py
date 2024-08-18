import mysql.connector
from mysql.connector import Error
import json
from config_setup import prompt_for_config
from scapy.all import *


class Logger:
    def __init__(self, db_name):
        self.config = self.load_config()
        self.connection = self.connect_to_db(db_name)

    def load_config(self):
        if not os.path.exists('config.json'):
            prompt_for_config()

            with open('config.json') as f:
                return json.load(f)

    def connect_to_db(self, db_name):
        try:
            connection = mysql.connector.connect(
                host=self.config['db_config']['host'],
                user=self.config['db_config']['user'],
                password=self.config['db_config']['password'],
                database=db_name
            )
            if connection.is_connected():
                print(f"Connected to the MySQL database: {db_name}")
            return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")


class AnomalyLogger(Logger):
    def __init__(self):
        super().__init__(db_name=self.load_config()['db_config']['database_anomalies'])

    def log_anomaly(self, message):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO anomalies_logs (message) VALUES (%s)"
            cursor.execute(query, (message,))
            self.connection.commit()
            print("Anomaly logged successfully")
        except Error as e:
            print(f"Error while logging anomaly: {e}")



class PacketLogger(Logger):
    def __init__(self):
        super().__init__()
        self.pcap_file = self.get_pcap_file_name()
        self.pcap_writer = PcapWriter(self.pcap_file, append=True, sync=True)

    def get_pcap_file_name(self):
        today_date = datetime.now().strftime('%Y_%m_%d')
        return f"packet_logs_{today_date}.pcap"

    def log_packet(self, packet: Packet):
        try:
            self.pcap_writer.write(packet)
            print(f"Packet logged successfully to {self.pcap_file}")
        except Exception as e:
            print(f"Error while logging packet: {e}")

    def import_pcap(self, file_path):
        try:
            packets = rdpcap(file_path)
            for packet in packets:
                self.log_packet(packet)
            print(f"Packets imported successfully from {file_path}")
        except Exception as e:
            print(f"Error while importing packets: {e}")

    def export_pcap(self, export_path):
        try:
            if os.path.exists(self.pcap_file):
                os.rename(self.pcap_file, export_path)
                print(f"PCAP file exported successfully to {export_path}")
            else:
                print(f"PCAP file {self.pcap_file} does not exist.")
        except Exception as e:
            print(f"Error while exporting PCAP file: {e}")

    def close(self):
        self.pcap_writer.close()
        print("PCAP writer closed.")

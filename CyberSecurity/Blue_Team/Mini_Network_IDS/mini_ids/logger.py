import mysql.connector
from mysql.connector import Error
import json
from config_setup import prompt_for_config
from scapy.all import *


class Logger:
    def __init__(self, db_name="anomalies_db"):
        self.config = self.load_config()
        self.connection = self.connect_to_db(db_name)

    def load_config(self):
        if not os.path.exists('config.json'):
            prompt_for_config()

        with open('config.json') as f:
            return json.load(f)

    def create_db(self, db_name="anomalies_db"):
        try:
            connection = mysql.connector.connect(
                host=self.config['db_config']['host'],
                user=self.config['db_config']['user'],
                password=self.config['db_config']['password']
            )
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print(f"Database {db_name} created or already exists.")
            cursor.close()
            connection.close()
        except Error as e:
            print(f"Error while creating database: {e}")

    def connect_to_db(self, db_name="anomalies_db"):
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
            print(f"Connection failed: {e}. Attempting to create database...")
            self.create_db(db_name)
            return self.retry_connect_to_db(db_name)

    def retry_connect_to_db(self, db_name="anomalies_db"):
        try:
            connection = mysql.connector.connect(
                host=self.config['db_config']['host'],
                user=self.config['db_config']['user'],
                password=self.config['db_config']['password'],
                database=db_name
            )
            if connection.is_connected():
                print(f"Connected to the MySQL database: {db_name} after creation.")
            return connection
        except Error as e:
            print(f"Retry connection failed: {e}")
            return None

    def close_db(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")


class AnomalyLogger(Logger):
    def __init__(self):
        super().__init__(db_name="anomalies_db")

    def create_anomaly_table(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS anomalies_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                message TEXT
            );
            """)
            print("Anomalies table created or already exists.")
        except Error as e:
            print(f"Error while creating anomalies table: {e}")

    def log_anomaly(self, message):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO anomalies_logs (message) VALUES (%s)"
            cursor.execute(query, (message,))
            self.connection.commit()
            print("Anomaly logged successfully")
        except Error as e:
            print(f"Error while logging anomaly: {e}")


class PacketLogger():

    def __init__(self):
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

    def close_pcap(self):
        self.pcap_writer.close()
        print("PCAP writer closed.")

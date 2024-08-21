import mysql.connector
from mysql.connector import Error
import json
from scapy.all import *
import csv


class Logger:
    def __init__(self, db_name="anomalies_db"):
        self.config = self.load_config()
        self.connection = self.connect_to_db(db_name)

    def load_config(self):
        config_path = 'config.json'

        if os.path.exists(config_path):
            with open(config_path, 'r') as config_file:
                try:
                    return json.load(config_file)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from config file: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
        else:
            print("Config file not found.")

        # If loading the config failed, prompt the user to create a new config
        user_input = input(
            "Configuration could not be loaded. Would you like to create a new configuration? (yes/no): ").strip().lower()
        if user_input == 'yes':
            from config_setup import prompt_for_config
            prompt_for_config()
            # Try loading the config again after creating it
            return self.load_config()
        else:
            print("Exiting because configuration could not be loaded or created.")
            return None

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

    def export_anomalies_to_csv(self, export_path=None):
        if export_path is None:
            today_date = datetime.now().strftime('%Y_%m_%d')
            export_path = f"anomalies_logs_{today_date}.csv"

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM anomalies_logs")
            rows = cursor.fetchall()

            with open(export_path, 'w', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)
                # Write the header
                csvwriter.writerow(['ID', 'Timestamp', 'Message'])
                # Write the data
                csvwriter.writerows(rows)

            print(f"Anomalies logs exported successfully to {export_path}")
        except Error as e:
            print(f"Error while exporting anomalies logs: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


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


class PcapFileLogger(PacketLogger):
    def __init__(self, pcap_filename):
        super().__init__()
        self.pcap_file = pcap_filename
        self.pcap_writer = PcapWriter(self.pcap_file, append=True, sync=True)
        self.log_file = f"{self.pcap_file}_analysis.log"

    def log_analysis(self, message):
        try:
            with open(self.log_file, 'a') as log:
                log.write(f"{datetime.now()} - {message}\n")
            print(f"Analysis logged successfully in {self.log_file}")
        except Exception as e:
            print(f"Error while logging analysis: {e}")
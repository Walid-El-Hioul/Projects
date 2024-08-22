import mysql.connector
from mysql.connector import Error
import json
from scapy.all import *
import smtplib
from email.mime.text import MIMEText
import os
from datetime import datetime
from config_setup import ConfigSetup


class Logger:
    def __init__(self):
        self.config_setup = ConfigSetup()
        self.config = self.load_config()
        self.connection = None

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
            "Configuration could not be loaded. "
            "Would you like to create a new database and alert configuration? (yes/no): "
        ).strip().lower()

        if user_input == 'yes':
            self.config_setup.prompt_for_db_config()
            self.config_setup.prompt_for_alert_config()
            # Try loading the config again after creating it
            return self.load_config()
        else:
            print("Exiting because configuration could not be loaded or created.")
            return None

    def create_db(self):
        try:
            connection = mysql.connector.connect(
                host=self.config['db_config']['host'],
                user=self.config['db_config']['user'],
                password=self.config['db_config']['password']
            )
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS anomalies_db")
            print(f"Database anomalies_db created or already exists.")
            cursor.close()
            connection.close()
        except Error as e:
            print(f"Error while creating database: {e}")

    def connect_to_db(self):
        try:
            connection = mysql.connector.connect(
                host=self.config['db_config']['host'],
                user=self.config['db_config']['user'],
                password=self.config['db_config']['password'],
                database="anomalies_db"
            )
            if connection.is_connected():
                print(f"Connected to the MySQL database: anomalies_db")
            return connection
        except Error as e:
            print(f"Connection failed: {e}. Attempting to create database...")
            self.config_setup.prompt_for_db_config()
            self.create_db()
            self.connect_to_db()

    def close_db(self):
        if self.connection is None:
            self.connection = self.connect_to_db()

            if self.connection and self.connection.is_connected():
                self.connection.close()
                print("MySQL connection closed.")


class AnomalyLogger(Logger):
    def __init__(self):
        super().__init__()

    def create_anomaly_table(self):
        if self.connection is None:
            self.connection = self.connect_to_db()

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
        if self.connection is None:
            self.connection = self.connect_to_db()

            try:
                cursor = self.connection.cursor()
                query = "INSERT INTO anomalies_logs (message) VALUES (%s)"
                cursor.execute(query, (message,))
                self.connection.commit()
                print("Anomaly logged successfully")
            except Error as e:
                print(f"Error while logging anomaly: {e}")

    def send_email_alert(self, subject, message):
        sender_gmail = self.config['alert_config']['sender_gmail']
        receiver_email = self.config['alert_config']['receiver_email']
        password = self.config['alert_config']['password']

        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender_gmail
        msg['To'] = receiver_email

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender_gmail, password)
            server.sendmail(sender_gmail, receiver_email, msg.as_string())
            server.quit()
            print(f"Email alert sent to {receiver_email}")
        except Exception as e:
            print(f"Failed to send email: {e}")
            self.config_setup.prompt_for_alert_config()
            print("Resending email")
            self.send_email_alert(subject, message)

    def export_anomalies_to_txt(self, export_path=None):
        if self.connection is None:
            raise ValueError("Connection could not be established.")

        if export_path is None:
            today_date = datetime.now().strftime('%Y_%m_%d')
            export_path = f"anomalies_logs_{today_date}.txt"

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM anomalies_logs")
            rows = cursor.fetchall()

            with open(export_path, 'w', encoding='utf-8') as txtfile:
                txtfile.write("ID\tTimestamp\tMessage\n")
                for row in rows:
                    txtfile.write(f"{row[0]}\t{row[1]}\t{row[2]}\n")

            print(f"Anomalies logs exported successfully to {export_path}")
        except Error as e:
            print(f"Error while exporting anomalies logs: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


class PacketLogger:
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
        self.txt_file = f"{self.pcap_file}_analysis.txt"
        self.ensure_txt_file_headers()

    def ensure_txt_file_headers(self):
        try:
            with open(self.txt_file, 'a', encoding='utf-8') as txtfile:
                # Check if the file is empty; if so, write headers
                if txtfile.tell() == 0:
                    txtfile.write("Timestamp\tMessage\n")  # Header line for text file
        except Exception as e:
            print(f"Error while ensuring TXT file headers: {e}")

    def log_analysis(self, message):
        try:
            with open(self.txt_file, 'a', encoding='utf-8') as txtfile:
                txtfile.write(f"{datetime.now()}\t{message}\n")
            print(f"Analysis logged successfully in {self.txt_file}")
        except Exception as e:
            print(f"Error while logging analysis: {e}")

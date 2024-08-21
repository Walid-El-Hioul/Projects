from scapy.all import *
from collections import defaultdict
import time
import smtplib
from email.mime.text import MIMEText
import json


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
        self.config = self.load_config()

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

    def send_email_alert(self, subject, message):
        sender_gmail = self.config['alert_config']['sender_gmail']
        receiver_email = self.config['alert_config']['receiver_email']
        password = self.config['alert_config']['password']

        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender_gmail
        msg['To'] = receiver_email


        try:
            server = smtplib.SMTP_SSL('smtp.google.com', 587)
            server.login(sender_gmail, password)
            server.sendmail(sender_gmail, receiver_email, msg.as_string())
            server.quit()
            print(f"Email alert sent to {receiver_email}")
        except Exception as e:
            print(f"Failed to send email: {e}")

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
                self.send_email_alert("SYN Flood Attack Detected", alert_message)
                self.block_ip(src_ip)

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
                    self.send_email_alert("HTTP Flood Attack Detected", alert_message)
                    self.block_ip(src_ip)
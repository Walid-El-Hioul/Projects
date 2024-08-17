import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime, timedelta

class Logger:
    def __init__(self, db_name):
        self.config = self.load_config()
        self.connection = self.connect_to_db(db_name)

    def load_config(self):
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
            query = "INSERT INTO anomaly_logs (message) VALUES (%s)"
            cursor.execute(query, (message,))
            self.connection.commit()
            print("Anomaly logged successfully")
        except Error as e:
            print(f"Error while logging anomaly: {e}")


class PacketLogger(Logger):
    def __init__(self):
        super().__init__(db_name=self.load_config()['db_config']['database_packets'])
        self.current_table = self.get_current_table_name()
        self.create_daily_table()

    def get_current_table_name(self):
        today_date = datetime.now().strftime('%Y_%m_%d')
        return f"packet_logs_{today_date}"

    def create_daily_table(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.current_table} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                src_ip VARCHAR(45),
                dst_ip VARCHAR(45),
                protocol VARCHAR(10),
                length INT,
                payload BLOB
            );
            """)
            print(f"Table {self.current_table} created or already exists.")
        except Error as e:
            print(f"Error while creating table: {e}")

    def log_packet(self, src_ip, dst_ip, protocol, length, payload):
        try:
            cursor = self.connection.cursor()
            query = f"INSERT INTO {self.current_table} (src_ip, dst_ip, protocol, length, payload) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (src_ip, dst_ip, protocol, length, payload))
            self.connection.commit()
            print("Packet logged successfully")
        except Error as e:
            print(f"Error while logging packet: {e}")

    def delete_old_tables(self):
        try:
            yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y_%m_%d')
            old_table_name = f"packet_logs_{yesterday_date}"
            cursor = self.connection.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {old_table_name};")
            print(f"Old table {old_table_name} deleted.")
        except Error as e:
            print(f"Error while deleting old table: {e}")

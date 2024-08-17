import mysql.connector
from datetime import datetime


class AnomalyLogger:
    def __init__(self, db_config):
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS anomalies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                src_ip VARCHAR(45),
                dst_ip VARCHAR(45),
                description TEXT
            )
        ''')
        self.connection.commit()

    def log_anomaly(self, src_ip, dst_ip, description):
        self.cursor.execute('''
            INSERT INTO anomalies (src_ip, dst_ip, description)
            VALUES (%s, %s, %s)
        ''', (src_ip, dst_ip, description))
        self.connection.commit()

    def close(self):
        self.connection.close()


class PacketLogger:
    def __init__(self, db_config):
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS packets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                src_ip VARCHAR(45),
                dst_ip VARCHAR(45),
                protocol VARCHAR(10),
                info TEXT
            )
        ''')
        self.connection.commit()
        self.clear_old_data()

    def clear_old_data(self):
        today = datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute('DELETE FROM packets WHERE DATE(timestamp) != %s', (today,))
        self.connection.commit()

    def log_packet(self, src_ip, dst_ip, protocol, info):
        self.cursor.execute('''
            INSERT INTO packets (src_ip, dst_ip, protocol, info)
            VALUES (%s, %s, %s, %s)
        ''', (src_ip, dst_ip, protocol, info))
        self.connection.commit()

    def close(self):
        self.connection.close()
import mysql.connector
from mysql.connector import Error
import json


def load_config():
    with open('config.json') as f:
        return json.load(f)


def create_database_and_tables():
    config = load_config()
    db_config = config['db_config']

    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Create databases
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database_anomalies']};")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database_packets']};")

            # Commit database creation
            connection.commit()

            # Create tables for anomalies
            connection.database = db_config['database_anomalies']
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS anomaly_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    message TEXT
                );
            """)

            # Create tables for packets
            connection.database = db_config['database_packets']
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS packet_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    src_ip VARCHAR(45),
                    dst_ip VARCHAR(45),
                    protocol VARCHAR(10),
                    length INT,
                    payload BLOB
                );
            """)

            # Commit table creation
            connection.commit()
            print("Databases and tables created successfully.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    create_database_and_tables()

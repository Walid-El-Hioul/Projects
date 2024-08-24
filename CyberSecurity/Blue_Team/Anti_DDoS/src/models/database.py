import mysql.connector
from mysql.connector import Error
from utils import Utils


class Logger:
    def __init__(self):
        self.utils = Utils()
        self.config = self.utils.load_config()
        self.connection = None

    #def load_db_config(self):
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
            self.create_db()
            self.connect_to_db()

    def close_db(self):
        if self.connection is None:
            self.connection = self.connect_to_db()

            if self.connection and self.connection.is_connected():
                self.connection.close()
                print("MySQL connection closed.")
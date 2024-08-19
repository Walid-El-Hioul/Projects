import os
import threading
from config_setup import prompt_for_config
from logger import AnomalyLogger, PacketLogger, Logger
from mini_ids import MiniIDS
from scapy.all import *


def main():
    # Ensure configuration exists
    config_file = 'config.json'

    if not os.path.exists(config_file):
        # If the configuration file does not exist, prompt for configuration
        prompt_for_config()
    else:
        # If the configuration file exists, ask the user if they want to skip the configuration step
        user_input = input("Configuration file already exists. Do you want to skip the configuration step? (yes/no): ").strip().lower()
        if user_input != 'yes':
            prompt_for_config()

    # Setup anomalies database
    logger = Logger(db_name="anomalies_db")
    logger.create_db(db_name="anomalies_db")
    logger.connect_to_db(db_name="anomalies_db")
    anomaly_logger = AnomalyLogger()
    anomaly_logger.create_anomaly_table()

    # Start IDS
    mini_ids = MiniIDS()
    mini_ids.start_ids(packet)


if __name__ == "__main__":
    main()

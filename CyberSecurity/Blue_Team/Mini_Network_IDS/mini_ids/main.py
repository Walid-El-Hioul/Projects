import os
import threading
from config_setup import prompt_for_config
from base_packet_sniffer import BasePacketSniffer
from logger import AnomalyLogger, PacketLogger
from mini_ids import MiniIDS


def user_input(sniffer):
    while True:
        command = input()
        if command.lower() == "exit":
            sniffer.stop_sniffing()  # Signal to stop sniffing
            break


if __name__ == "__main__":
    try:
        prompt_for_config()
    except:
        exit()


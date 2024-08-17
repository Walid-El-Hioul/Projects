import sys
import threading
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QHBoxLayout, QComboBox, QFileDialog,
    QFormLayout, QLineEdit
)
from PyQt6.QtCore import QTimer, Qt, pyqtSignal, QObject

class PacketSniffer(QObject):
    # Define custom signals for updating the GUI
    packet_logged = pyqtSignal(dict)
    anomaly_detected = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.running = False

    def start_sniffing(self):
        self.running = True
        while self.running:
            # Simulate packet logging
            packet_info = {
                "src_ip": "192.168.0.{}".format(threading.get_ident() % 255),
                "dst_ip": "192.168.0.1",
                "protocol": "TCP",
                "timestamp": "2024-08-17 12:00:00"
            }
            self.packet_logged.emit(packet_info)

            # Simulate anomaly detection
            if threading.get_ident() % 5 == 0:  # Simulate an anomaly every 5 packets
                anomaly_info = {
                    "timestamp": "2024-08-17 12:00:00",
                    "description": "Possible intrusion detected from 192.168.0.{}".format(threading.get_ident() % 255)
                }
                self.anomaly_detected.emit(anomaly_info)

            # Sleep to simulate packet arrival time
            threading.Event().wait(1)

    def stop_sniffing(self):
        self.running = False


class MiniIDS(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.packet_count = 0
        self.anomaly_count = 0

        # Initialize the sniffer and connect signals
        self.sniffer = PacketSniffer()
        self.sniffer.packet_logged.connect(self.log_packet)
        self.sniffer.anomaly_detected.connect(self.log_anomaly)

        self.sniffer_thread = None

    def init_ui(self):
        self.setWindowTitle("Mini IDS")
        self.setGeometry(300, 300, 800, 600)

        layout = QVBoxLayout()

        # Dashboard Overview
        self.dashboard_label = QLabel("Dashboard Overview")
        self.dashboard_label.setStyleSheet("font-weight: bold; font-size: 16px;")

        self.anomaly_label = QLabel("Anomalies Detected: 0")
        self.packet_label = QLabel("Packets Logged: 0")

        dashboard_layout = QHBoxLayout()
        dashboard_layout.addWidget(self.anomaly_label)
        dashboard_layout.addWidget(self.packet_label)

        # Anomaly Log
        self.anomaly_log_label = QLabel("Anomaly Log")
        self.anomaly_log_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.anomaly_log_table = QTableWidget(0, 2)
        self.anomaly_log_table.setHorizontalHeaderLabels(["Timestamp", "Description"])
        self.anomaly_log_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Packet Log
        self.packet_log_label = QLabel("Packet Log")
        self.packet_log_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.packet_log_table = QTableWidget(0, 3)
        self.packet_log_table.setHorizontalHeaderLabels(["Source IP", "Destination IP", "Protocol"])
        self.packet_log_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Controls
        controls_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Sniffing")
        self.stop_button = QPushButton("Stop Sniffing")
        self.export_button = QPushButton("Export Logs")

        # Signals
        self.start_button.clicked.connect(self.start_sniffing)
        self.stop_button.clicked.connect(self.stop_sniffing)
        self.export_button.clicked.connect(self.export_logs)

        controls_layout.addWidget(self.start_button)
        controls_layout.addWidget(self.stop_button)
        controls_layout.addWidget(self.export_button)

        # Settings
        settings_layout = QFormLayout()
        self.interface_selector = QComboBox()
        self.interface_selector.addItems(["Ethernet", "wlan0", "lo"])  # Example interfaces
        self.log_file_location = QLineEdit("C:/path/to/log/file")

        settings_layout.addRow("Network Interface:", self.interface_selector)
        settings_layout.addRow("Log File Location:", self.log_file_location)

        # Add all widgets to the main layout
        layout.addWidget(self.dashboard_label)
        layout.addLayout(dashboard_layout)
        layout.addWidget(self.anomaly_log_label)
        layout.addWidget(self.anomaly_log_table)
        layout.addWidget(self.packet_log_label)
        layout.addWidget(self.packet_log_table)
        layout.addLayout(controls_layout)
        layout.addLayout(settings_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_sniffing(self):
        if self.sniffer_thread is None or not self.sniffer_thread.is_alive():
            self.sniffer_thread = threading.Thread(target=self.sniffer.start_sniffing)
            self.sniffer_thread.start()
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)

    def stop_sniffing(self):
        if self.sniffer_thread and self.sniffer_thread.is_alive():
            self.sniffer.stop_sniffing()
            self.sniffer_thread.join()
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def log_packet(self, packet_info):
        self.packet_count += 1
        self.packet_label.setText(f"Packets Logged: {self.packet_count}")

        # Add a row to the packet log table
        row_position = self.packet_log_table.rowCount()
        self.packet_log_table.insertRow(row_position)

        self.packet_log_table.setItem(row_position, 0, QTableWidgetItem(packet_info["src_ip"]))
        self.packet_log_table.setItem(row_position, 1, QTableWidgetItem(packet_info["dst_ip"]))
        self.packet_log_table.setItem(row_position, 2, QTableWidgetItem(packet_info["protocol"]))

    def log_anomaly(self, anomaly_info):
        self.anomaly_count += 1
        self.anomaly_label.setText(f"Anomalies Detected: {self.anomaly_count}")

        # Add a row to the anomaly log table
        row_position = self.anomaly_log_table.rowCount()
        self.anomaly_log_table.insertRow(row_position)

        self.anomaly_log_table.setItem(row_position, 0, QTableWidgetItem(anomaly_info["timestamp"]))
        self.anomaly_log_table.setItem(row_position, 1, QTableWidgetItem(anomaly_info["description"]))

    def export_logs(self):
        log_file_path, _ = QFileDialog.getSaveFileName(self, "Export Logs", "",
                                                       "CSV Files (*.csv);;JSON Files (*.json)")

        if log_file_path:
            # Example logic to export logs (extend as needed)
            with open(log_file_path, 'w') as file:
                file.write("Exported logs go here.")


def main():
    app = QApplication(sys.argv)
    ids = MiniIDS()
    ids.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

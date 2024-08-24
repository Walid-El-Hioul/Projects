from PyQt5.QtWidgets import QSplitter, QTableWidget, QTextEdit, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

class PacketSnifferPanel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # Create a vertical splitter for packet list and details
        splitter = QSplitter(Qt.Vertical, self)
        layout = QVBoxLayout(self)
        layout.addWidget(splitter)

        # Packet List
        self.packet_list = QTableWidget(0, 8)
        self.packet_list.setHorizontalHeaderLabels(["No.", "Time", "Source", "Destination", "Protocol", "Length", "Info", "Payload"])
        self.packet_list.setSortingEnabled(True)
        splitter.addWidget(self.packet_list)

        # Packet Details
        self.packet_details = QTextEdit()
        self.packet_details.setPlaceholderText("Select a packet to view details...")
        splitter.addWidget(self.packet_details)

        splitter.setSizes([300, 150])

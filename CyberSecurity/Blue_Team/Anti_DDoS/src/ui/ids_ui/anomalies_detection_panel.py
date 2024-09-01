from PyQt5.QtWidgets import QTableWidget, QWidget, QVBoxLayout


class AnomaliesDetectionPanel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # Detected Logs
        self.detection_logs = QTableWidget(0, 3)
        self.detection_logs.setHorizontalHeaderLabels(["ID", "Timestamp", "Message"])
        self.detection_logs.setSortingEnabled(True)
        layout.addWidget(self.detection_logs)

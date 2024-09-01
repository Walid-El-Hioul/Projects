import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QVBoxLayout, QSplitter, QWidget, QMenuBar
from PyQt5.QtCore import Qt
from tool_bar_panel import ToolBarPanel
from packet_sniffer_panel import PacketSnifferPanel
from anomalies_detection_panel import AnomaliesDetectionPanel
from file_menu import FileMenu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Packet Sniffer")

        # Get the screen resolution
        screen_resolution = QApplication.desktop().availableGeometry()
        width = screen_resolution.width()
        height = screen_resolution.height()

        # Set the window size to the screen resolution
        self.setGeometry(0, 0, width, height)
        self.showMaximized()

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_splitter = QSplitter(Qt.Horizontal)
        central_widget.setLayout(QVBoxLayout())
        central_widget.layout().addWidget(main_splitter)

        # Left side (Packet List and Packet Details)
        self.packet_sniffer_panel = PacketSnifferPanel(main_splitter)

        # Right side (Detection Logs)
        self.anomalies_detection_panel = AnomaliesDetectionPanel(main_splitter)

        # Add Toolbar
        self.tool_bar_panel = ToolBarPanel(self)
        self.addToolBar(self.tool_bar_panel.create_toolbar())

        # Add File Menu
        self.file_menu = FileMenu(self)
        self.menuBar().addMenu(self.file_menu.create_menu())

        # Load the stylesheet
        self.setStyleSheet(open("styles.css").read())

    def open_sensor_options(self):
        # Implement the logic to open sensor options dialog
        QMessageBox.information(self, "Sensor Options", "Sensor options dialog")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
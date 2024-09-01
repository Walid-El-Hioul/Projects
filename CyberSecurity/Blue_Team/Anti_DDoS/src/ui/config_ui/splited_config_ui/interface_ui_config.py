import sys
import wmi
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QFormLayout
)
from PyQt5.QtCore import Qt
from src.utils.utils import Config


class InterfaceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Interface")
        self.setGeometry(100, 100, 800, 600)

        # Set a modern dark theme
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #2e2e2e;
                color: #ffffff;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #e0e0e0;
                margin-bottom: 5px;
            }
            QComboBox {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #444;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #007bff;
                color: #ffffff;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: #ffffff;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # Interface selection using QFormLayout for minimal spacing
        form_layout = QFormLayout()
        layout.addLayout(form_layout)

        self.interface_combo = QComboBox()
        self.interfaces = self.get_network_interfaces()
        self.interface_combo.addItem("Select Interface")
        self.interface_combo.addItems([iface['name'] for iface in self.interfaces])

        # Add the label and combo box to the form layout
        form_layout.addRow(QLabel("Interface:"), self.interface_combo)

        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedSize(120, 40)
        self.submit_button.setEnabled(False)
        self.submit_button.clicked.connect(self.submit_form)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        layout.addLayout(button_layout)

        # Connect combo box to validation function
        self.interface_combo.currentIndexChanged.connect(self.validate_selection)

    def get_network_interfaces(self):
        c = wmi.WMI()
        interfaces = []

        for adapter in c.Win32_NetworkAdapterConfiguration():
            description = adapter.Description
            mac_address = adapter.MACAddress
            ip_address = ", ".join(adapter.IPAddress) if adapter.IPAddress else "No IP"
            is_enabled = adapter.IPEnabled
            interfaces.append({
                'name': description,
                'mac': mac_address,
                'ip': ip_address,
                'is_enabled': is_enabled
            })

        return interfaces

    def validate_selection(self):
        # Check if an interface is selected
        if self.interface_combo.currentIndex() > 0:  # Index 0 is "Select Interface"
            self.submit_button.setEnabled(True)
        else:
            self.submit_button.setEnabled(False)

    def submit_form(self):

        config = Config()

        data = {
            'interface': self.host_input.text()
        }

        config.write_config_update("interface_config", data)

        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InterfaceApp()
    window.show()
    sys.exit(app.exec_())

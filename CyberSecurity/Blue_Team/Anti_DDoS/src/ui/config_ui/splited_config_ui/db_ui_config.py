import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.utils.utils import Config


class DBConfigApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Configuration")
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
            QLineEdit {
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

        # Database configuration inputs
        layout.addWidget(QLabel("Configure Database Connection"))

        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("Enter host (e.g., localhost)")
        layout.addWidget(QLabel("Host:"))
        layout.addWidget(self.host_input)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter user")
        layout.addWidget(QLabel("User:"))
        layout.addWidget(self.user_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)

        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedSize(120, 40)
        self.submit_button.setEnabled(False)
        self.submit_button.clicked.connect(self.submit_form)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        layout.addLayout(button_layout)

        # Connect input fields to validation function
        self.host_input.textChanged.connect(self.validate_inputs)
        self.user_input.textChanged.connect(self.validate_inputs)
        self.password_input.textChanged.connect(self.validate_inputs)

    def validate_inputs(self):
        # Check if all fields are filled
        if (self.host_input.text() and
                self.user_input.text() and
                self.password_input.text()):
            self.submit_button.setEnabled(True)
        else:
            self.submit_button.setEnabled(False)

    def submit_form(self):

        # Handle form submission
        print("Form Submitted!")
        print(f"Host: {self.host_input.text()}")
        print(f"User: {self.user_input.text()}")
        print(f"Password: {self.password_input.text()}")

        # Load existing JSON data
        config = Config()

        data = {}

        # Update existing data or create new data
        data['host'] = self.host_input.text()
        data['user'] = self.user_input.text()
        data['password'] = self.password_input.text()

        # Write updated data to JSON file
        config.write_config_update(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DBConfigApp()
    window.show()
    sys.exit(app.exec_())

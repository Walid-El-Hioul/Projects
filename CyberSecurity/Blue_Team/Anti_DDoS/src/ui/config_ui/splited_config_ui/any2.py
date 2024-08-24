import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class AlertConfigApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alert Configuration")
        self.setGeometry(100, 100, 800, 600)  # Set an appropriate window size

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

        # Alert configuration inputs
        layout.addWidget(QLabel("Configure Alert Settings"))

        self.sender_input = QLineEdit()
        self.sender_input.setPlaceholderText("Enter sender email (e.g., example@gmail.com)")
        layout.addWidget(QLabel("Sender Email:"))
        layout.addWidget(self.sender_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter sender email password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)

        self.receiver_input = QLineEdit()
        self.receiver_input.setPlaceholderText("Enter receiver email")
        layout.addWidget(QLabel("Receiver Email:"))
        layout.addWidget(self.receiver_input)

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
        self.sender_input.textChanged.connect(self.validate_inputs)
        self.password_input.textChanged.connect(self.validate_inputs)
        self.receiver_input.textChanged.connect(self.validate_inputs)

    def validate_inputs(self):
        # Check if all fields are filled
        if (self.sender_input.text() and
                self.password_input.text() and
                self.receiver_input.text()):
            self.submit_button.setEnabled(True)
        else:
            self.submit_button.setEnabled(False)

    def submit_form(self):
        # Handle form submission
        print("Form Submitted!")
        print(f"Sender Email: {self.sender_input.text()}")
        print(f"Password: {self.password_input.text()}")
        print(f"Receiver Email: {self.receiver_input.text()}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AlertConfigApp()
    window.show()
    sys.exit(app.exec_())

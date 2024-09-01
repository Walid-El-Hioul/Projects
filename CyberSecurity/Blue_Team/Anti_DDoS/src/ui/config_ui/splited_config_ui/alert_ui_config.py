import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt
from src.utils.utils import Config
import re
import traceback

class AlertConfigApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alert Configuration")
        self.setGeometry(100, 100, 800, 600)

        # ... (previous styling code remains the same)
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
            QLabel.error {
                color: red;
                font-size: 12px;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        layout.addWidget(QLabel("Configure Alert Settings"))

        self.sender_input = EmailLineEdit("Enter sender email (e.g., example@gmail.com)")
        layout.addWidget(QLabel("Sender Email:"))
        layout.addWidget(self.sender_input)
        layout.addWidget(self.sender_input.error_label)

        self.password_input = PasswordLineEdit("Enter sender email password")
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.password_input.error_label)

        self.receiver_input = EmailLineEdit("Enter receiver email")
        layout.addWidget(QLabel("Receiver Email:"))
        layout.addWidget(self.receiver_input)
        layout.addWidget(self.receiver_input.error_label)

        self.submit_error_label = QLabel("")
        self.submit_error_label.setStyleSheet("color: red; font-size: 14px; font-weight: bold;")
        self.submit_error_label.setAlignment(Qt.AlignCenter)
        self.submit_error_label.setVisible(False)
        layout.addWidget(self.submit_error_label)

        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedSize(120, 40)
        self.submit_button.clicked.connect(self.submit_form)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        layout.addLayout(button_layout)

    def submit_form(self):
        try:
            if self.validate_all_fields():
                config = Config()
                data = {
                    'sender_email': self.sender_input.text(),
                    'sender_password': self.password_input.text(),
                    'receiver_email': self.receiver_input.text()
                }
                config.write_config_update("alert_config", data)
                self.close()
            else:
                self.submit_error_label.setText("Please correct the errors before submitting.")
                self.submit_error_label.setVisible(True)
        except Exception as e:
            print(f"Error in submit_form: {str(e)}")
            traceback.print_exc()

    def validate_all_fields(self):
        sender_valid = self.sender_input.validate()
        password_valid = self.password_input.validate()
        receiver_valid = self.receiver_input.validate()
        return sender_valid and password_valid and receiver_valid

class EmailLineEdit(QLineEdit):
    def __init__(self, placeholder_text, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder_text)
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red; font-size: 12px;")
        self.error_label.setVisible(False)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.validate()

    def validate(self):
        try:
            email = self.text()
            if not email:
                self.error_label.setText("Email address is required.")
                self.error_label.setVisible(True)
                return False
            elif not self.is_valid_email(email):
                self.error_label.setText("Invalid email address.")
                self.error_label.setVisible(True)
                return False
            else:
                self.error_label.setVisible(False)
                return True
        except Exception as e:
            print(f"Error in EmailLineEdit.validate: {str(e)}")
            traceback.print_exc()
            return False

    def is_valid_email(self, email):
        email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return bool(email_regex.match(email))

class PasswordLineEdit(QLineEdit):
    def __init__(self, placeholder_text, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder_text)
        self.setEchoMode(QLineEdit.Password)
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red; font-size: 12px;")
        self.error_label.setVisible(False)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.validate()

    def validate(self):
        try:
            password = self.text()
            if not password:
                self.error_label.setText("Password is required.")
                self.error_label.setVisible(True)
                return False
            elif not self.is_valid_password(password):
                self.error_label.setText("Password must be at least 8 characters long and contain uppercase, lowercase, and digits.")
                self.error_label.setVisible(True)
                return False
            else:
                self.error_label.setVisible(False)
                return True
        except Exception as e:
            print(f"Error in PasswordLineEdit.validate: {str(e)}")
            traceback.print_exc()
            return False

    def is_valid_password(self, password):
        return (len(password) >= 8 and
                any(c.isupper() for c in password) and
                any(c.islower() for c in password) and
                any(c.isdigit() for c in password))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AlertConfigApp()
    window.show()
    sys.exit(app.exec_())
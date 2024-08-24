from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

class AlertConfigTab(QWidget):
    def __init__(self):
        super().__init__()
        self.alert_config_layout = QGridLayout(self)
        self.alert_config_layout.setHorizontalSpacing(20)
        self.alert_config_layout.setVerticalSpacing(15)

        self.sender_email_input = QLineEdit()
        self.sender_email_input.setPlaceholderText("Sender Gmail")
        self.sender_email_input.setToolTip("Enter the email address from which alerts will be sent.")
        self.sender_email_input.setMinimumWidth(300)

        self.alert_password_input = QLineEdit()
        self.alert_password_input.setPlaceholderText("Password")
        self.alert_password_input.setEchoMode(QLineEdit.Password)
        self.alert_password_input.setToolTip("Enter the password for the sender email.")
        self.alert_password_input.setMinimumWidth(300)

        self.receiver_email_input = QLineEdit()
        self.receiver_email_input.setPlaceholderText("Receiver Email")
        self.receiver_email_input.setToolTip("Enter the email address to receive alerts.")
        self.receiver_email_input.setMinimumWidth(300)

        self.alert_config_layout.addWidget(QLabel("Sender Email:"), 0, 0)
        self.alert_config_layout.addWidget(self.sender_email_input, 0, 1)
        self.alert_config_layout.addWidget(QLabel("Password:"), 1, 0)
        self.alert_config_layout.addWidget(self.alert_password_input, 1, 1)
        self.alert_config_layout.addWidget(QLabel("Receiver Email:"), 2, 0)
        self.alert_config_layout.addWidget(self.receiver_email_input, 2, 1)

        self.next_button_alert = QPushButton("Next")
        self.next_button_alert.setEnabled(False)
        self.next_button_alert.setToolTip("Proceed to the next step after filling in the alert configuration.")
        self.alert_config_layout.addWidget(self.next_button_alert, 3, 1, alignment=Qt.AlignRight)

        self.back_button_alert = QPushButton("Back")
        self.back_button_alert.setToolTip("Go back to the database configuration tab.")
        self.alert_config_layout.addWidget(self.back_button_alert, 3, 0, alignment=Qt.AlignLeft)

        self.alert_config_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), 4, 1)
        self.sender_email_input.textChanged.connect(self.check_alert_fields)
        self.alert_password_input.textChanged.connect(self.check_alert_fields)
        self.receiver_email_input.textChanged.connect(self.check_alert_fields)

    def check_alert_fields(self):
        if (self.sender_email_input.text() and
                self.alert_password_input.text() and
                self.receiver_email_input.text()):
            self.next_button_alert.setEnabled(True)
        else:
            self.next_button_alert.setEnabled(False)

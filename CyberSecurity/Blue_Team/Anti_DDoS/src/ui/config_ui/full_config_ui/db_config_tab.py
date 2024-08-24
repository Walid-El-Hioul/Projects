from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

class DbConfigTab(QWidget):
    def __init__(self):
        super().__init__()
        self.db_config_layout = QGridLayout(self)
        self.db_config_layout.setHorizontalSpacing(20)
        self.db_config_layout.setVerticalSpacing(15)

        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("Host (e.g., localhost)")
        self.host_input.setToolTip("Enter the host name or IP address of the database server.")
        self.host_input.setMinimumWidth(300)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("User")
        self.user_input.setToolTip("Enter the username for the database.")
        self.user_input.setMinimumWidth(300)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setToolTip("Enter the password for the database user.")
        self.password_input.setMinimumWidth(300)

        self.db_config_layout.addWidget(QLabel("Host:"), 0, 0)
        self.db_config_layout.addWidget(self.host_input, 0, 1)
        self.db_config_layout.addWidget(QLabel("User:"), 1, 0)
        self.db_config_layout.addWidget(self.user_input, 1, 1)
        self.db_config_layout.addWidget(QLabel("Password:"), 2, 0)
        self.db_config_layout.addWidget(self.password_input, 2, 1)

        self.next_button_db = QPushButton("Next")
        self.next_button_db.setEnabled(False)
        self.next_button_db.setToolTip("Proceed to the next step after filling in the database configuration.")
        self.db_config_layout.addWidget(self.next_button_db, 3, 1, alignment=Qt.AlignRight)

        self.db_config_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), 4, 1)
        self.host_input.textChanged.connect(self.check_db_fields)
        self.user_input.textChanged.connect(self.check_db_fields)
        self.password_input.textChanged.connect(self.check_db_fields)

    def check_db_fields(self):
        if (self.host_input.text() and
                self.user_input.text() and
                self.password_input.text()):
            self.next_button_db.setEnabled(True)
        else:
            self.next_button_db.setEnabled(False)

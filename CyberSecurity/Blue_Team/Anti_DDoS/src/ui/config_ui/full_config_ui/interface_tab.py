from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QSpacerItem, QSizePolicy, QMessageBox

class InterfaceTab(QWidget):
    def __init__(self):
        super().__init__()
        self.interface_layout = QVBoxLayout(self)
        self.interface_layout.setSpacing(20)

        self.interface_choice = QComboBox()
        self.interface_choice.addItems(["Select an option", "Option 1", "Option 2", "Option 3"])
        self.interface_choice.setToolTip("Select the interface to use for capturing packets.")
        self.interface_layout.addWidget(QLabel("Choose Interface:"))
        self.interface_layout.addWidget(self.interface_choice)

        self.interface_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("start_button")
        self.start_button.setEnabled(False)
        self.start_button.setToolTip("Start the process with the selected interface.")
        self.interface_layout.addWidget(self.start_button)

        self.back_button_interface = QPushButton("Back")
        self.back_button_interface.setToolTip("Go back to the alert configuration tab.")
        self.interface_layout.addWidget(self.back_button_interface)

        self.interface_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.interface_choice.currentIndexChanged.connect(self.check_interface_choice)

        self.start_button.clicked.connect(self.start_process)

    def check_interface_choice(self):
        if self.interface_choice.currentIndex() > 0:
            self.start_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)

    def start_process(self):
        selected_option = self.interface_choice.currentText()
        QMessageBox.information(self, "Process Started", f"Started process with {selected_option}")

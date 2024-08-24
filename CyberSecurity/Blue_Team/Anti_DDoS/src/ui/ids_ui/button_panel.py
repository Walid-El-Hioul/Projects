from PyQt5.QtWidgets import QPushButton


class ButtonPanel:
    def __init__(self, parent):
        self.parent = parent
        self.init_buttons()

    def init_buttons(self):
        self.start_capture_button = QPushButton("Start Capture")
        self.stop_capture_button = QPushButton("Stop Capture")
        self.refresh_capture_button = QPushButton("Refresh Capture")
        self.sensor_options_button = QPushButton("Sensor Options")

        # Assign object names for styling
        self.start_capture_button.setObjectName("start_capture_button")
        self.stop_capture_button.setObjectName("stop_capture_button")
        self.refresh_capture_button.setObjectName("refresh_capture_button")
        self.sensor_options_button.setObjectName("sensor_options_button")

        # Connect the sensor options button to a method
        self.sensor_options_button.clicked.connect(self.open_sensor_options)

    def open_sensor_options(self):
        # Implement the logic to open sensor options dialog
        self.parent.errors_panel.show_message("Opening sensor options...")

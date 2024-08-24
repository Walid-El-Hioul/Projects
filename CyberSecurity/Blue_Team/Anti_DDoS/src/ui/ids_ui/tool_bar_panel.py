from PyQt5.QtWidgets import QToolBar, QPushButton

class ToolBarPanel:
    def __init__(self, parent):
        self.parent = parent

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")

        self.start_capture_button = QPushButton("Start Capture")
        self.stop_capture_button = QPushButton("Stop Capture")
        self.refresh_capture_button = QPushButton("Refresh Capture")
        self.sensor_options_button = QPushButton("Sensor Options")

        # Assign object names for styling
        self.start_capture_button.setObjectName("start_capture_button")
        self.stop_capture_button.setObjectName("stop_capture_button")
        self.refresh_capture_button.setObjectName("refresh_capture_button")
        self.sensor_options_button.setObjectName("sensor_options_button")

        # Add buttons to toolbar
        toolbar.addWidget(self.start_capture_button)
        toolbar.addWidget(self.stop_capture_button)
        toolbar.addWidget(self.refresh_capture_button)
        toolbar.addWidget(self.sensor_options_button)

        # Connect the sensor options button to the appropriate method
        self.sensor_options_button.clicked.connect(self.parent.open_sensor_options)

        return toolbar

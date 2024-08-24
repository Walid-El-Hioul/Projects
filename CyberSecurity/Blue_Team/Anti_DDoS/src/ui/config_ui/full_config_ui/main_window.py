from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget, QApplication
from db_config_tab import DbConfigTab
from alert_config_tab import AlertConfigTab
from interface_tab import InterfaceTab
import sys

class StepDesktopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Step Desktop App")
        self.setGeometry(100, 100, 1200, 800)

        self.setStyleSheet(open("styles.css").read())

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(20)

        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)

        self.db_config_tab = DbConfigTab()
        self.alert_config_tab = AlertConfigTab()
        self.interface_tab = InterfaceTab()

        self.tab_widget.addTab(self.db_config_tab, "DB Config")
        self.tab_widget.addTab(self.alert_config_tab, "Alert Config")
        self.tab_widget.addTab(self.interface_tab, "Interface")

        self.db_config_tab.next_button_db.clicked.connect(self.go_to_alert_config)
        self.alert_config_tab.next_button_alert.clicked.connect(self.go_to_interface)
        self.alert_config_tab.back_button_alert.clicked.connect(self.go_to_db_config)
        self.interface_tab.back_button_interface.clicked.connect(self.go_to_alert_config)


    def go_to_alert_config(self):
        self.tab_widget.setCurrentIndex(1)

    def go_to_interface(self):
        self.tab_widget.setCurrentIndex(2)

    def go_to_db_config(self):
        self.tab_widget.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StepDesktopApp()
    window.show()
    sys.exit(app.exec_())

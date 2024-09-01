import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox
)
from PyQt5.QtCore import QCoreApplication


class MainErrorWindow():

    def show_error(self, message, details=None):
        # Ensure an application instance is running
        app = QApplication.instance ()
        if app is None:
            app = QApplication(sys.argv)

        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText("An error occurred.")
        error_dialog.setInformativeText(message)
        if details:
            error_dialog.setDetailedText(details)
        error_dialog.setStandardButtons(QMessageBox.Ok)
        error_dialog.finished.connect(sys.exit)  # Exit the application when the dialog is closed
        error_dialog.exec_()

        # Run the event loop if it's not already running
        if not app.quitOnLastWindowClosed():
            sys.exit(app.exec_())

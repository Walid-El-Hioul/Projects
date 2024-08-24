from PyQt5.QtWidgets import QStatusBar


class ErrorsPanel:
    def __init__(self, parent):
        self.parent = parent
        self.init_status_bar()

    def init_status_bar(self):
        self.status_bar = QStatusBar(self.parent)
        self.parent.setStatusBar(self.status_bar)

    def show_message(self, message):
        self.status_bar.showMessage(message)

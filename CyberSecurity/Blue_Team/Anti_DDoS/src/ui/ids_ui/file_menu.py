from PyQt5.QtWidgets import QAction, QFileDialog, QMessageBox


class FileMenu:
    def __init__(self, parent):
        self.parent = parent

    def create_menu(self):
        file_menu = self.parent.menuBar().addMenu('File')

        export_logs_action = QAction('Export Logs', self.parent)
        import_pcap_action = QAction('Import PCAP', self.parent)
        export_pcap_action = QAction('Export PCAP', self.parent)
        filter_packets_action = QAction('Filter Packets', self.parent)

        export_logs_action.triggered.connect(self.export_logs)
        import_pcap_action.triggered.connect(self.import_pcap)
        export_pcap_action.triggered.connect(self.export_pcap)
        filter_packets_action.triggered.connect(self.filter_packets)

        file_menu.addAction(export_logs_action)
        file_menu.addAction(import_pcap_action)
        file_menu.addAction(export_pcap_action)
        file_menu.addAction(filter_packets_action)

        return file_menu

    def export_logs(self):
        file_name, _ = QFileDialog.getSaveFileName(self.parent, "Save Logs", "", "Log Files (*.log);;All Files (*)")
        if file_name:
            try:
                with open(file_name, 'w') as file:
                    file.write("Log data...")
                self.parent.statusBar().showMessage(f"Logs exported to {file_name}")
            except Exception as e:
                QMessageBox.critical(self.parent, "Error", f"An error occurred while exporting logs: {e}")

    def import_pcap(self):
        file_name, _ = QFileDialog.getOpenFileName(self.parent, "Open PCAP File", "", "PCAP Files (*.pcap);;All Files (*)")
        if file_name:
            try:
                self.parent.statusBar().showMessage(f"PCAP file imported from {file_name}")
            except Exception as e:
                QMessageBox.critical(self.parent, "Error", f"An error occurred while importing PCAP file: {e}")

    def export_pcap(self):
        file_name, _ = QFileDialog.getSaveFileName(self.parent, "Save PCAP File", "", "PCAP Files (*.pcap);;All Files (*)")
        if file_name:
            try:
                self.parent.statusBar().showMessage(f"PCAP file exported to {file_name}")
            except Exception as e:
                QMessageBox.critical(self.parent, "Error", f"An error occurred while exporting PCAP file: {e}")

    def filter_packets(self):
        QMessageBox.information(self.parent, "Filter Packets", "Filtering packets...")

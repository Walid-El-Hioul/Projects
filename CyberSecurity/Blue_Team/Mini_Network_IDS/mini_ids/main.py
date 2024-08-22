import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette

class ColorChangingBox(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAutoFillBackground(True)
        self.default_color = QColor(255, 255, 255)  # White
        self.hover_color = QColor(0, 150, 255)  # Blue
        self.set_background_color(self.default_color)
        self.setAlignment(Qt.AlignCenter)
        self.setText("Hover Over Me")

    def set_background_color(self, color):
        palette = self.palette()
        palette.setColor(QPalette.Window, color)
        self.setPalette(palette)

    def enterEvent(self, event):
        self.set_background_color(self.hover_color)
        self.setText("Hovered!")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.set_background_color(self.default_color)
        self.setText("Hover Over Me")
        super().leaveEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Color Changing Box")
        self.setGeometry(100, 100, 400, 300)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Color-changing box
        self.color_box = ColorChangingBox(self.central_widget)
        self.color_box.setGeometry(150, 100, 100, 100)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget


class Sender(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Sender")

        self.setFixedSize(QSize(200, 80))

        self.build_ui()

    def build_ui(self):
        self.btn = QPushButton("click")
        self.btn.clicked.connect(self.on_click)

        btn_font = QFont("Arial", 24)
        self.btn.setFont(btn_font)

        btn_size = QSize(100, 50)
        self.btn.setFixedSize(btn_size)

        layout = QHBoxLayout()
        layout.addWidget(self.btn)

        layout_widget = QWidget()
        layout_widget.setLayout(layout)

        self.setCentralWidget(layout_widget)

    def on_click(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)

    sender = Sender()
    sender.show()
    
    sys.exit(app.exec_())


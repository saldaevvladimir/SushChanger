import sys
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget
import socket


class Sender(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Sender")

        window_size = QSize(200, 80)
        self.setFixedSize(window_size)

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
        client.send('1'.encode('utf-8'))


if __name__ == "__main__":
    ip = "192.168.43.230"
    passw = 1234

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, passw))

    app = QApplication(sys.argv)

    sender = Sender()
    sender.show()
    
    sys.exit(app.exec_())


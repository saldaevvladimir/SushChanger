import sys
import os
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget, QMessageBox, QDialog
import socket

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_path)

from tools.IPTools import IPDialog


class Sender(QMainWindow):
    server = None
    client = None

    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Sender")

        icon_path = "img/icons/sender.png"
        self.setWindowIcon(QIcon(icon_path))

        window_size = QSize(200, 80)
        self.setFixedSize(window_size)

        self.build_ui()

        self.ip = None
        self.port = 1234

        self.open_ip_dialog()

        self.start_server(self.ip, self.port)

        QMessageBox.information(self, "Message", "Press the <click> button once and then connect the receiver")

    def build_ui(self):
        self.send_btn = QPushButton("click")
        self.send_btn.clicked.connect(self.on_send_click)

        send_btn_font = QFont("Arial", 24)
        self.send_btn.setFont(send_btn_font)

        send_btn_size = QSize(100, 50)
        self.send_btn.setFixedSize(send_btn_size)

        layout = QHBoxLayout()
        layout.addWidget(self.send_btn)

        layout_widget = QWidget()
        layout_widget.setLayout(layout)

        self.setCentralWidget(layout_widget)

    def on_send_click(self):
        if self.client:
            self.client.sendall('1'.encode('utf-8'))
        else:
            self.connect_client()

    def start_server(self, ip, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.server.bind((ip, port))
        except socket.gaierror as e:
            QMessageBox.warning(self, "Error", "unable to connect to selected ip")
            sys.exit()
            
        self.server.listen()

    def connect_client(self):
        if not self.client:
            self.client, _ = self.server.accept()

    def open_ip_dialog(self):
        expected_serv_state = False
        dialog = IPDialog(self)
        dialog.set_expected_serv_state(expected_serv_state)

        if dialog.exec_() == QDialog.Accepted:
            if self.client:
                self.client.close()
        else:
            sys.exit()

    def closeEvent(self, event):
        if self.client:
            self.client.close()
        if self.server:
            self.server.close()

        super().closeEvent(event)


app = QApplication(sys.argv)

sender = Sender()
sender.show()

sys.exit(app.exec_())


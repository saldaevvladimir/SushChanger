import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import glob
import socket


class Receiver(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Receiver")

        self.build_ui()

        self.img_index = 0

        timer_interval = 100
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.upd_img)
        self.timer.start(timer_interval)

        self.server = None
        self.client = None

    def build_ui(self):
        self.img_label = QLabel()
        
        self.setCentralWidget(self.img_label)

    def set_img(self, path):
        self.img_label.setPixmap(QPixmap(path))
        self.adjustSize()

    def upd_img(self):
        if self.client:
            data = self.client.recv(1024).decode("utf-8").lower()

            if data:
                self.img_index = (self.img_index + 1) % img_count

                img_path = f"../img/{self.img_index}.png"
                self.set_img(img_path)
    
    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, passw))
        self.server.listen()

        self.client, _ = self.server.accept()

    def stop_server(self):
        if self.server:
            self.server.close()


if __name__ == "__main__":
    img_count = len(glob.glob("../img/*.png")) - 1

    ip = "192.168.43.230"
    passw = 1234

    app = QApplication(sys.argv)

    receiver = Receiver()
    receiver.start_server()
    receiver.show()
    
    sys.exit(app.exec_())


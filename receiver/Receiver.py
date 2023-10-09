import sys
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import glob
import socket
import threading
import time

DEFAULT_IMG_PATH = '../img/0.png'

class Receiver(QMainWindow):
    upd_img_signal = pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Receiver")

        self.build_ui()

        self.img_index = 0

        self.server = None
        self.client = None

        self.set_img(DEFAULT_IMG_PATH)

        self.upd_img_signal.connect(self.upd_img)

    def build_ui(self):
        self.img_label = QLabel()
        
        self.setCentralWidget(self.img_label)

    def set_img(self, path):
        self.img_label.setPixmap(QPixmap(path))
        self.adjustSize()

    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, passw))
        self.server.listen()

        self.client, _ = self.server.accept()

        threading.Thread(target = self.listen_for_msg).start()

    def stop_server(self):
        if self.server:
            self.server.close()

    def listen_for_msg(self):
        while True:
            data = self.client.recv(1024).decode('utf-8').lower()

            if data:
                self.img_index = (self.img_index + 1) % img_count

                self.upd_img_signal.emit()
            
    @pyqtSlot()
    def upd_img(self):
        img_path = f"../img/{self.img_index}.png"
        self.set_img(img_path)

    def closeEvent(self, event):
        self.stop_server()
        super().closeEvent(event)


if __name__ == "__main__":
    img_count = len(glob.glob("../img/*.png")) - 1

    ip = "192.168.43.230"
    passw = 1234

    app = QApplication(sys.argv)

    receiver = Receiver()
    receiver.start_server()
    receiver.show()
    
    sys.exit(app.exec_())


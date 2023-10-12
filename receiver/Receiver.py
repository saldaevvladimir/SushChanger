import sys
import os
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QMessageBox
import glob
from threading import Thread

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_path)

from tools.IPTools import IPDialog

DEFAULT_IMG_PATH = 'img/sush/0.png'


class Receiver(QMainWindow):
    upd_img_signal = pyqtSignal()
    listening_thread = None
    client = None

    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Receiver")

        icon_path = "img/icons/receiver.png"
        self.setWindowIcon(QIcon(icon_path))

        self.build_ui()

        self.img_index = 0

        self.set_img(DEFAULT_IMG_PATH)

        self.upd_img_signal.connect(self.upd_img)

        self.ip = None
        self.port = 1234

    def build_ui(self):
        self.img_label = QLabel()

        self.img_label.setToolTip("click")
        
        self.setCentralWidget(self.img_label)

    def set_img(self, path):
        self.img_label.setPixmap(QPixmap(path))
        self.adjustSize()

    def on_img_click(self):
        if self.client:
            return
        
        self.open_ip_dialog()

        self.img_label.setToolTip("")

    def start_listening(self):
        self.listening_thread = Thread(target = self.listen_for_msg)
        self.listening_thread.start()

    def stop_listening(self):
        if not self.listening_thread:
            return
        
        self.listening_thread.join(False)
        self.client.close()

    def listen_for_msg(self):
        while True:
            msg = self.client.recv(1024).decode('utf-8').lower()

            if msg:
                self.upd_img_signal.emit()
            
    @pyqtSlot()
    def upd_img(self):
        self.img_index = (self.img_index + 1) % img_count

        img_path = f"img/sush/{self.img_index}.png"
        self.set_img(img_path)

    def open_ip_dialog(self):
        expected_serv_state = True
        dialog = IPDialog(self)
        dialog.set_expected_serv_state(expected_serv_state)

        if dialog.exec_() == QDialog.Accepted:
            if self.client:
                self.start_listening()

    def mousePressEvent(self, event):
        if event.button() in (Qt.LeftButton, Qt.RightButton) and event.pos() in self.img_label.geometry():
            self.on_img_click()
        super().mousePressEvent(event)

    def closeEvent(self, event):
        if self.listening_thread:
            self.stop_listening()
        if self.client:
            self.client.close()

        super().closeEvent(event)


img_count = len(glob.glob("img/sush/*.png")) - 1

app = QApplication(sys.argv)

receiver = Receiver()
receiver.show()
QMessageBox.information(receiver, "Message", "Click on the image to select ip")

sys.exit(app.exec_())


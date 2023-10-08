import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import glob


class Receiver(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Receiver")

        self.build_ui()

        self.img_index = 0

        self.timer_interval = 100
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.upd_img)
        self.timer.start(self.timer_interval)

        self.server = None
        self.client = None

    def build_ui(self):
        self.img_label = QLabel()
        
        self.setCentralWidget(self.img_label)

    def set_img(self, path):
        self.img_label.setPixmap(QPixmap(path))
        self.adjustSize()

    def upd_img(self):
        pass


if __name__ == "__main__":
    img_count = len(glob.glob("../img/*.png")) - 1

    app = QApplication(sys.argv)

    receiver = Receiver()
    receiver.show()
    
    sys.exit(app.exec_())


import sys
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QDialog, QLineEdit, QMessageBox
import socket


def check_server_con(ip):
    try:
        port = 1234
        client = socket.create_connection((ip, port))
        return True, client
    except socket.error as e:
        return False, None
    
def get_available_ips():
    available_ips = []

    hostname = socket.gethostname()
    ip_addresses = socket.getaddrinfo(hostname, None)
    for address in ip_addresses:
        ip = address[4][0]
        if ip not in available_ips:
            available_ips.append(ip)

    return available_ips


def check_ip(ip):
        parts = ip.split('.')
        if len(parts) != 4:
            return False, None
        for part in parts:
            if not part.isdigit() or int(part) < 0 or int(part) > 255:
                return False, None
        
        return check_server_con(ip)


class IPDialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Select IP")

        self.build_ui()

    def build_ui(self):
        self.ip_line = QLineEdit(self)

        self.button = QPushButton("confirm")
        self.button.clicked.connect(self.validate_ip)
        
        layout = QVBoxLayout()
        layout.addWidget(self.ip_line)
        layout.addWidget(self.button)
        
        self.setLayout(layout)

    def set_expected_serv_state(self, state):
        self.expected_serv_state = state
        
    def validate_ip(self):
        ip = self.ip_line.text()

        serv_state, client = check_ip(ip)

        if serv_state == self.expected_serv_state:
            self.parent().ip = ip
            self.parent().client = client
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "ip unavailable")
            

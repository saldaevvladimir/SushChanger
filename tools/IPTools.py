import netifaces as ni
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QDialog, QComboBox, QLineEdit, QMessageBox
import socket


def check_server_con(ip):
    try:
        port = 1234
        client = socket.create_connection((ip, port))
        return True, client
    except socket.error as e:
        return False, None
    

def get_available_ips():
    addresses = []

    interfaces = ni.interfaces()

    for interface in interfaces:
        addrs = ni.ifaddresses(interface)

        if ni.AF_INET in addrs:
            ipv4_addrs = addrs[ni.AF_INET]

            for addr in ipv4_addrs:
                ip = addr['addr']
                if not ip.startswith('127.') and not ip.startswith('169.254.') and not ip.endswith('56.1'):
                    if ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('172.'):
                        addresses.append(ip)

    return addresses


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
        self.ip_combobox = QComboBox(self)
        self.ip_line = QLineEdit(self)

        self.fill_ips()
        
        self.button = QPushButton("confirm")
        self.button.clicked.connect(self.validate_ip)
        
        layout = QVBoxLayout()
        layout.addWidget(self.ip_combobox)
        layout.addWidget(self.ip_line)
        layout.addWidget(self.button)
        
        self.setLayout(layout)
    
    def fill_ips(self):
        ips = get_available_ips()

        for ip in ips:
            self.ip_combobox.addItem(ip)

    def set_expected_serv_state(self, state):
        self.expected_serv_state = state

        if state:
            self.ip_combobox.hide()
        else:
            self.ip_line.hide()
        
    def validate_ip(self):
        ip = None

        if self.expected_serv_state:
            ip = self.ip_line.text()
        else:
            ip = self.ip_combobox.currentText()

        serv_state, client = check_ip(ip)

        if serv_state == self.expected_serv_state:
            self.parent().ip = ip
            self.parent().client = client
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "ip unavailable")


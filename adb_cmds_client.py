import sys
from PyQt5.QtWidgets import *
import time
from threading import *
import socket

class Monitor(QWidget):
    def __init__(self,server_ip,server_port):
        super().__init__()
        self.command_string = "timer_on=False"
        self.server_ip = server_ip
        self.server_port = server_port
        self.btn = QPushButton('Start/stop')
        self.btn.clicked.connect(self.thread)
        self.textedit = QLineEdit()
        self.textedit.setText('outputfilename.txt')
        layout = QVBoxLayout()
        layout.addWidget(self.textedit)
        layout.addWidget(self.btn)
        self.setLayout(layout)
        self.setWindowTitle("client start/stop adb_cmds")

    def thread(self):
        t1 = Thread(target=self.Operation)
        t1.start()

    def Operation(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.server_ip, self.server_port))
        # if self.command_string == "timer_on=True":
        #     self.command_string = "timer_on=False"
        # else:
        #     self.command_string = "timer_on=True"
        self.command_string = str(self.textedit.text())
        client.send(bytes(self.command_string,encoding='utf-8'))
        from_server = client.recv(4096).decode('utf-8')
        client.close()
        print(from_server)
        time.sleep(1)

if __name__ == '__main__':
    server_ip = '172.31.121.80'
    server_port = 8081
    app = QApplication(sys.argv)
    ex=Monitor(server_ip, server_port)
    ex.show()
    sys.exit(app.exec_())


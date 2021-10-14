'''
adb wait-for-device && adb root && adb remount 
adb shell mfg_tool mcu raw set dev
adb shell mfg_tool mcu raw set w ConfigHallInactiveOverride 1
adb shell mfg_tool mcu reset
adb shell mfg_tool mcu raw captouch force-streaming
adb shell mfg_tool mcu raw loglevel capt trace
adb logcat -c
adb logcat -s mcuservice
'''
import sys
import datetime
from PyQt5.QtWidgets import *
import time
from threading import *
import socket
from ppadb.client import Client as AdbClient

class Monitor(QWidget):
    def __init__(self):
        super().__init__()

        self.timer_on = False
        self.btn1 = QPushButton('logcat on/off')
        self.btn1.clicked.connect(self.thread0)
        layout = QVBoxLayout()
        layout.addWidget(self.btn1)
        self.setLayout(layout)
        self.setWindowTitle("monitor")
        self.thread2()

    def server(self):
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv.bind(('0.0.0.0', 8081))
        self.serv.listen(5)
        while True:
            conn, addr = self.serv.accept()
            from_client = ''
            while True:
                from_client_msg = conn.recv(4096)
                if not from_client_msg : break
                from_client += str(from_client_msg.decode('utf-8'))
                print(from_client)
                self.filename = from_client
                self.thread0()
                timestamp = str(datetime.datetime.now())
                payload = timestamp + ';' + str(from_client_msg) + ';OK'
                conn.send(bytes(payload,encoding='utf-8'))
        conn.close()
    
    def connect(self):
        def dump_logcat(connection):
            # with open(self.filename,'w') as f:
            f = open(self.filename,'a')
            while self.timer_on:
                data = connection.read(1024)
                if not data:
                    break
                print(data.decode('utf-8'))
                f.write(data.decode('utf-8'))
                f.flush()
            connection.close()

        if self.timer_on:
            self.timer_on = False
        else:
            self.timer_on = True
        self.client = AdbClient(host="127.0.0.1", port=5037)
        self.devices = self.client.devices()
        self.device = self.devices[0]
        print(f'connected to {self.device}')
        self.device.shell("logcat -c")
        self.device.shell("logcat -s mcuservice", handler=dump_logcat)

    def thread0(self):
        t1 = Thread(target=self.connect)
        t1.start()
    
    def thread2(self):
        t2 = Thread(target=self.server)
        t2.start()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Monitor()
    ex.show()
    sys.exit(app.exec_())
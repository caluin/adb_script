import sys
import time

import numpy as np

from matplotlib.backends.qt_compat import QtCore, QtWidgets
if QtCore.qVersion() >= "5.":
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)

        size = 100
        self.t_vec = np.linspace(0,1,size+1)[0:-1]
        self.pos = np.zeros(len(self.t_vec))
        self.y0_vec = np.zeros(len(self.t_vec))
        self.b0_vec = np.zeros(len(self.t_vec))
        self.y1_vec = np.zeros(len(self.t_vec))
        self.b1_vec = np.zeros(len(self.t_vec))
        self.y2_vec = np.zeros(len(self.t_vec))
        self.b2_vec = np.zeros(len(self.t_vec))
        self.y3_vec = np.zeros(len(self.t_vec))
        self.b3_vec = np.zeros(len(self.t_vec))
        self.starttime = 0

        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(dynamic_canvas)
        self.addToolBar(QtCore.Qt.BottomToolBarArea,
                        NavigationToolbar(dynamic_canvas, self))

        self._dynamic_ax = dynamic_canvas.figure.subplots()

        self._line0,  = self._dynamic_ax.plot(self.t_vec, self.y0_vec,'-o',label='0 instant')
        self._lineb0, = self._dynamic_ax.plot(self.t_vec, self.b0_vec,'-.',label='0 baseline')
        self._line1,  = self._dynamic_ax.plot(self.t_vec, self.y1_vec,'-o',label='1 instant')
        self._lineb1, = self._dynamic_ax.plot(self.t_vec, self.b1_vec,'-.',label='1 baseline')
        self._line2,  = self._dynamic_ax.plot(self.t_vec, self.y2_vec,'-o',label='2 instant')
        self._lineb2, = self._dynamic_ax.plot(self.t_vec, self.b2_vec,'-.',label='2 baseline')
        self._line3,  = self._dynamic_ax.plot(self.t_vec, self.y3_vec,'-o',label='3 instant')
        self._lineb3, = self._dynamic_ax.plot(self.t_vec, self.b3_vec,'-.',label='3 baseline')
        self._linepos,= self._dynamic_ax.plot(self.t_vec, self.pos,   '-+',label='position')
        self._dynamic_ax.set_ylim([400,650])
        self._dynamic_ax.legend()
        self._dynamic_ax.set_title('CapTouch Sensor 1')
        self._dynamic_ax.set_xlabel('msec')
        self._dynamic_ax.set_ylabel('cap')
        self._dynamic_ax.grid()
        # self._timer = dynamic_canvas.new_timer(50)
        self._timer = dynamic_canvas.new_timer(10)
        self._timer.add_callback(self._update_canvas2)
        self._timer.start()

    def _update_canvas2(self):
        count=0
        for line in sys.stdin:
            if "module_captouch.c(933)" in line:
                slider_list = line.replace(',','').split()
                if self.starttime ==0:
                    self.starttime = int(slider_list[10])
                self.t_vec[-1]  = int(slider_list[10])-self.starttime
                self.b0_vec[-1] = int(slider_list[19])
                self.y0_vec[-1] = int(slider_list[20])
                self.b1_vec[-1] = int(slider_list[21])
                self.y1_vec[-1] = int(slider_list[22])
                self.b2_vec[-1] = int(slider_list[23])
                self.y2_vec[-1] = int(slider_list[24])
                self.b3_vec[-1] = int(slider_list[25])
                self.y3_vec[-1] = int(slider_list[26])
                self.pos[-1]    = int(slider_list[17])
                print(self.t_vec[-1],self.pos[-1],self.b0_vec[-1],self.y0_vec[-1],np.mean(self.b0_vec),np.mean(self.y0_vec))
                if count==5:
                    self._line0.set_data(self.t_vec,self.y0_vec)
                    self._lineb0.set_data(self.t_vec,self.b0_vec)
                    self._line1.set_data(self.t_vec,self.y1_vec)
                    self._lineb1.set_data(self.t_vec,self.b1_vec)
                    self._line2.set_data(self.t_vec,self.y2_vec)
                    self._lineb2.set_data(self.t_vec,self.b2_vec)
                    self._line3.set_data(self.t_vec,self.y3_vec)
                    self._lineb3.set_data(self.t_vec,self.b3_vec)
                    self._linepos.set_data(self.t_vec,self.pos)
                    self._dynamic_ax.set_xlim([self.t_vec[0],self.t_vec[-1]])
                    self._line0.figure.canvas.draw()
                    self.t_vec  = np.append(self.t_vec[1:],0.0)
                    self.y0_vec = np.append(self.y0_vec[1:],0.0)
                    self.b0_vec = np.append(self.b0_vec[1:],0.0)
                    self.y1_vec = np.append(self.y1_vec[1:],0.0)
                    self.b1_vec = np.append(self.b1_vec[1:],0.0)
                    self.y2_vec = np.append(self.y2_vec[1:],0.0)
                    self.b2_vec = np.append(self.b2_vec[1:],0.0)
                    self.y3_vec = np.append(self.y3_vec[1:],0.0)
                    self.b3_vec = np.append(self.b3_vec[1:],0.0)
                    self.pos    = np.append(self.pos[1:],0.0)
                    break
                self.t_vec  = np.append(self.t_vec[1:],0.0)
                self.y0_vec = np.append(self.y0_vec[1:],0.0)
                self.b0_vec = np.append(self.b0_vec[1:],0.0)
                self.y1_vec = np.append(self.y1_vec[1:],0.0)
                self.b1_vec = np.append(self.b1_vec[1:],0.0)
                self.y2_vec = np.append(self.y2_vec[1:],0.0)
                self.b2_vec = np.append(self.b2_vec[1:],0.0)
                self.y3_vec = np.append(self.y3_vec[1:],0.0)
                self.b3_vec = np.append(self.b3_vec[1:],0.0)
                self.pos    = np.append(self.pos[1:],0.0)
                count+=1


if __name__ == "__main__":
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec_()

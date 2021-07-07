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
        self.y_vec = np.zeros(len(self.t_vec))
        self.b_vec = np.zeros(len(self.t_vec))
        self.starttime = 0

        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(dynamic_canvas)
        self.addToolBar(QtCore.Qt.BottomToolBarArea,
                        NavigationToolbar(dynamic_canvas, self))

        self._dynamic_ax = dynamic_canvas.figure.subplots()

        self._line, = self._dynamic_ax.plot(self.t_vec, self.y_vec,'-o',label='instant')
        self._lineb, = self._dynamic_ax.plot(self.t_vec, self.b_vec,'-o',label='baseline')
        self._dynamic_ax.set_ylim([400,650])
        self._dynamic_ax.legend()
        self._dynamic_ax.set_title('CapTouch Sensor 1')
        self._dynamic_ax.set_xlabel('msec')
        self._dynamic_ax.set_ylabel('cap')
        self._dynamic_ax.grid()
        self._timer = dynamic_canvas.new_timer(50)
        self._timer.add_callback(self._update_canvas2)
        self._timer.start()

    def _update_canvas2(self):
        count=0
        for line in sys.stdin:
            if "module_captouch.c(167)" in line:
                slider_list = line.split()
                if self.starttime ==0:
                    self.starttime = int(slider_list[10])
                self.t_vec[-1] = int(slider_list[10])-self.starttime
                self.y_vec[-1] = int(slider_list[20])
                self.b_vec[-1] = int(slider_list[19])
                print(self.t_vec[-1],self.b_vec[-1],self.y_vec[-1])
                if count==5:
                    self._line.set_data(self.t_vec,self.y_vec)
                    self._lineb.set_data(self.t_vec,self.b_vec)
                    self._dynamic_ax.set_xlim([self.t_vec[0],self.t_vec[-1]])
                    self._line.figure.canvas.draw()
                    self.t_vec = np.append(self.t_vec[1:],0.0)
                    self.y_vec = np.append(self.y_vec[1:],0.0)
                    self.b_vec = np.append(self.b_vec[1:],0.0)
                    break
                self.t_vec = np.append(self.t_vec[1:],0.0)
                self.y_vec = np.append(self.y_vec[1:],0.0)
                self.b_vec = np.append(self.b_vec[1:],0.0)
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

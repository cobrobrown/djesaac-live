import random
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PyQt5 import QtCore #conda install pyqt
from PyQt5 import QtWidgets

import sounddevice as sd
import numpy as np
import time

class MatplotlibWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)

        self.axis = self.figure.add_subplot(111)

        self.layoutVertical = QtWidgets.QVBoxLayout(self)#QVBoxLayout
        self.layoutVertical.addWidget(self.canvas)

class ThreadSample(QtCore.QThread):
    newSample = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(ThreadSample, self).__init__(parent)
        self.stream = sd.InputStream(device=6,channels=1,samplerate=48484)
        self.N = int(.02*48484)

    def run(self):
        # start audio stream
        #randomSample = random.sample(range(0, 10), 10)
        print('running')
        self.stream.start()
        print('starting stream')
        time.sleep(.5)
        #while stream.active():
        y = self.stream.read(self.N)
        y = list(y.ravel())
        print(y)
        self.newSample.emit(y)
        print('end')

class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.pushButtonPlot = QtWidgets.QPushButton(self)
        self.pushButtonPlot.setText("Plot")
        self.pushButtonPlot.clicked.connect(self.on_pushButtonPlot_clicked)

        self.matplotlibWidget = MatplotlibWidget(self)

        self.layoutVertical = QtWidgets.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.pushButtonPlot)
        self.layoutVertical.addWidget(self.matplotlibWidget)

        self.threadSample = ThreadSample(self)
        
        
        ####
        # start audio thread
        ####
        #self.threadSample.start()
        
        
        self.threadSample.newSample.connect(self.on_threadSample_newSample)
        self.threadSample.finished.connect(self.on_threadSample_finished)

    @QtCore.pyqtSlot()
    def on_pushButtonPlot_clicked(self):
        self.samples = 0
        self.matplotlibWidget.axis.clear()
        self.threadSample.start()

    @QtCore.pyqtSlot(list)
    def on_threadSample_newSample(self, sample):
        self.matplotlibWidget.axis.plot(sample)
        self.matplotlibWidget.canvas.draw()

    @QtCore.pyqtSlot()
    def on_threadSample_finished(self):
        self.samples += 1
        if self.samples <= 2:
            self.threadSample.start()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = MyWindow()
    main.resize(666, 333)
    main.show()
    print('hi')
    sys.exit(app.exec_())

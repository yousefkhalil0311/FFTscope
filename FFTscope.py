import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

app = pg.mkQApp("FFTScope")

win = pg.PlotWidget()

win.resize(800, 600)

win.setWindowTitle("FFTScope")

win.setLabel('bottom', 'Frequency', units='Hz')

pg.setConfigOptions(antialias=True)

curve = pg.PlotCurveItem()

win.addItem(curve)

x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = [1, 1, 1, 1, 1, 5, 1, 1, 1, 1]

def update():
    y[np.random.randint(0, 10)] = np.random.randint(0, 10)
    curve.setData(x, y)

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)


win.show()
pg.exec()
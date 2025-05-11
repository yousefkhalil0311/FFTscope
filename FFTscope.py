#python includes
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

#project specific include
from FFTPlot import FFTPlot

app = pg.mkQApp("FFTScope")

#window is dynamically resizable. Start with small window size for compatibility
win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle("FFTScope")
win.resize(640, 480)

#set antialiasing for better looking plots
pg.setConfigOptions(antialias=True)

plot1 = FFTPlot('A0', 2048, win)
plot2 = FFTPlot('A1', 2048, win)
plot3 = FFTPlot('A2', 2048, win)
plot4 = FFTPlot('A3', 2048, win)
win.nextRow()
plot5 = FFTPlot('B0', 2048, win)
plot6 = FFTPlot('B1', 2048, win)
plot7 = FFTPlot('B2', 2048, win)
plot8 = FFTPlot('B3', 2048, win)

def updateall():
    plot1.update()
    plot2.update()
    plot3.update()
    plot4.update()
    plot5.update()
    plot6.update()
    plot7.update()
    plot8.update()


timer = QtCore.QTimer()
timer.timeout.connect(updateall)
timer.start(30)


win.show()
pg.exec()
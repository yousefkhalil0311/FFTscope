import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

class FFTPlot:

    #each FFTPlot will represent the data from one ADC channel on the connected hardware
    def __init__(self, ADCchannel : str, x_width : int, window : pg.GraphicsLayoutWidget):
        self.ADCchannel = ADCchannel
        self.x = np.arange(0, 32500000, 32500000 / x_width)
        self.y = np.zeros(x_width)
        self.plot = window.addPlot()
        self.plot.setTitle(ADCchannel)
        self.plot.setLabel('bottom', 'Frequency', units='Hz')
        self.plot.setLabel('left', 'Amplitude', units='mV')

        self.curve = self.plot.plot(self.x, self.y, pen='y')

    def update(self, newPlotData : np.ndarray) -> None :
        self.y = np.zeros(self.x.size)
        self.y[np.random.randint(0, self.x.size)] = 10
        self.curve.setData(self.x, self.y)
        
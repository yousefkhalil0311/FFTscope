import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

class FFTPlot:

    #each FFTPlot will represent the data from one ADC channel on the connected hardware
    def __init__(self, ADCchannel : str, x_width : int, window : pg.GraphicsLayoutWidget):
        self.ADCchannel : str = ADCchannel
        self.FFT_SIZE : int = x_width
        self.x : np.ndarray = np.arange(-32500000, 32500000, 65000000 / x_width)
        self.y : np.ndarray = np.zeros(x_width)
        self.plot = window.addPlot()
        self.plot.setTitle(ADCchannel)
        self.plot.setLabel('bottom', 'Frequency', units='Hz')
        self.plot.setLabel('left', 'Amplitude', units='mV')
        self.plot.enableAutoRange(axis='y', enable=True)
        #self.plot.setYRange(0, 5000)

        self.curve = self.plot.plot(self.x, self.y, pen='y')

    def update(self, newPlotData : np.ndarray) -> None :
        
        if newPlotData is None:
            return
        
        FFT_SIZE : int = self.FFT_SIZE
        
        if len(newPlotData) != FFT_SIZE:
            return 

        tempArray : np.ndarray = newPlotData.copy()


        self.y[0 : FFT_SIZE // 2] = tempArray[FFT_SIZE // 2 : FFT_SIZE]
        self.y[64 : FFT_SIZE] = tempArray[0 : FFT_SIZE // 2]

        
        if(self.y.size % 128 == 0):
            self.curve.setData(self.x, self.y)
        
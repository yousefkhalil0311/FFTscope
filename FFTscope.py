#python includes
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
import time

#project specific include
from FFTPlot import FFTPlot
from SerialTools import SerialConnection


#name of device to connect to
defaultDevice = '/dev/cu.usbserial-2140'

#FFT size the Zynq FPGA
FFTSIZE = 128

#define serial interface and connect to device with the defaultDevice name
serialCon = SerialConnection(baudRate=230400, timeout=0.08)


#Function definitions begin

#do not proceed until device connects
def autoConnect(deviceName : str = defaultDevice):
    while(serialCon.serialHandler is None):
    
        portList = serialCon.listPorts()

        for port in portList:
            if port.device == defaultDevice:
                serialCon.connect(port.device)
        
        time.sleep(1)


#requests FFT data for ADC channel from device. every 4 bytes will combine to form a 32 bit word.
def getFFTData(channel : str) -> np.ndarray: #array of 32 bit words

    serialCon.write(channel + '\n')

    readData : bytes = serialCon.read(FFTSIZE * 4)

    _32bitList : np.ndarray = np.frombuffer(readData, dtype=np.int32)

    return _32bitList
    
app = pg.mkQApp("FFTScope")

#Function definitions end

#connect to serial device in defaultDevice param
autoConnect()

#window is dynamically resizable. Start with small window size for compatibility
win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle("FFTScope")
win.resize(640, 480)

#set antialiasing for better looking plots
pg.setConfigOptions(antialias=True)

#initialize and draw all plots
plot1 = FFTPlot('A0', FFTSIZE, win)
plot2 = FFTPlot('A1', FFTSIZE, win)
plot3 = FFTPlot('A2', FFTSIZE, win)
plot4 = FFTPlot('A3', FFTSIZE, win)
win.nextRow()
#plot5 = FFTPlot('B0', FFTSIZE, win)
#plot6 = FFTPlot('B1', FFTSIZE, win)
#plot7 = FFTPlot('B2', FFTSIZE, win)
#plot8 = FFTPlot('B3', FFTSIZE, win)

#update all plots
def updateall():
    try:
        plot1.update(getFFTData('A0'))
        plot2.update(getFFTData('A1'))
        plot3.update(getFFTData('A2'))
        plot4.update(getFFTData('A3'))
        #plot5.update(getFFTData('B0'))
        #plot6.update(getFFTData('B1'))
        #plot7.update(getFFTData('B2'))
        #plot8.update(getFFTData('B3'))
    except Exception as e:

        #close window and attempt connecting to the device
        win.close()
        print(f'Communication failure...{e}\n')
        autoConnect()


timer = QtCore.QTimer()
timer.timeout.connect(updateall)
timer.start(0)


#show window and execute plot updates
win.show()
pg.exec()



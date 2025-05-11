import serial
from serial.tools.list_ports_common import ListPortInfo
from serial.tools import list_ports
import time

class SerialConnection:

    def __init__ (self, baudRate: int = 115200, timeout: int = 1):
        self.baudRate : int = baudRate
        self.timeout : int = timeout
        self.port : str = None
        self.serialHandler : serial.Serial = None

        

    #checks for all serial ports connected to device
    def listPorts(self) -> list[ListPortInfo] | None:

        print('Detecting available serial ports...\n')

        ports = list_ports.comports()

        if (not ports):
            print('No serial ports found...\n')
            return None
        
        #list all serial ports
        print(f'Found {len(ports)} devices:\n')
        for serialport in ports:
            print(f'{serialport.device}\n')

        #we will need some other information about the serial device, so return all metadata
        return ports
    
    

    #attempts connection to specified port
    def connect(self, port: str = None) -> bool:

        if str is None:
            print('no port specified...')
            return False

        print(f'Attempting connection to {self.port}...\n')

        try:
            self.serialHandler = serial.Serial(port, baudrate=self.baudRate, timeout=self.timeout)
            self.port = port
            print('Connection Successful\n')
            return True

        except Exception as e:
            print(f'Connection to port {self.port} failed: {e}\n')
            return False
            


    #read from serial port until a specified number of bytes are read
    def read(self, numBytes : int) -> bytes | None:

        if self.serialHandler and self.serialHandler.is_open:
            print(f'Reading from {self.port}...\n')
            readData = self.serialHandler.read(numBytes)
            return readData
        
        else:
            print('Port is not open.\n')
            return None



    def write(self, buffer : str | bytes) -> int | None:

        if not buffer:
            print('No data to write')
            return None

        if isinstance(buffer, str):

            data = buffer.encode()

        else:
            data = buffer

        if(self.serialHandler and self.serialHandler.is_open):
            print(f'Writing to {self.port}...\n')

            numBytesWritten : int = self.serialHandler.write(data)

            print(f'{numBytesWritten} bytes written to {self.port}\n')

            return numBytesWritten
        


    #disconnect from serial device
    def disconnect(self) -> None:

        if(not self.serialHandler and self.serialHandler.is_open):
            self.serialHandler.close()
            print(f'Successfully closed {self.port}.\n')
            self.port = None
            self.serialHandler = None
        else:
            print('Serial port already closed.\n')


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
    def read(self, startCondition : bytes = None, numBytes : int = 1) -> bytes | None:
        
        #time limit to receive start condition
        timeoutSeconds : float = 0.1

        #check is serial connection is available
        if self.serialHandler and self.serialHandler.is_open:

            #if no start condition is provided, just read specified number of bytes from serial stream and return data
            if startCondition is None:

                if numBytes is None or numBytes <= 0:
                    raise ValueError('Invalid numBytes value: Must receive at least 1 byte.')
                
                return self.serialHandler.read(numBytes)
            
            #if start condition provided, it must be 2 bytes long
            if len(startCondition) != 2:
                raise ValueError('Payload Start Condition must be 2 bytes.')
            
            #print(f'Reading from {self.port}...\n')

            #check for start condition on serial stream. return None if header not received after timeout
            startTime = time.time()

            #wait for start condition
            while True:

                #check for timeout
                if(time.time() - startTime > timeoutSeconds):
                    print('Timeout reached waiting for serial data frame start condition...')
                    return None

                #check for first start condition byte
                headerByte1 : bytes = self.serialHandler.read(1)

                if not headerByte1:
                    continue

                elif headerByte1[0] == startCondition[0]:

                    #check for second start condition byte if first byte is received
                    headerByte2 : bytes = self.serialHandler.read(1)

                    if headerByte2 and headerByte2[0] == startCondition[1]:
                        break
            
            #get payload size from received header
            payloadSizeHeader : bytes = self.serialHandler.read(2)

            #number of bytes to receive from serial stream
            payloadSizeBytes : int = (payloadSizeHeader[0] << 8) + payloadSizeHeader[1]

            #print(f'reading {payloadSizeBytes} bytes...')

            readData : bytes = self.serialHandler.read(payloadSizeBytes)

            #print warning and return None if received number of bytes is not what is expected
            if(len(readData) != payloadSizeBytes):
                print(f'Warning: Expected {payloadSizeBytes} bytes but got {len(readData)} bytes.')
                return None

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


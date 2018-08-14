import serial
import time
from serial.tools import list_ports

class serialClass:

    def __init__(self, port, baud=115200):
        self.port = port
        self.baud = baud
        self.ser = serial.Serial(
            port=port,
            baudrate=baud
        )

    def getPort(self):
        return self.port

    def write_read_serial(self, serial_command):
        encoded_command = serial_command + '\r\n'
        encoded_command = encoded_command.encode()

        self.ser.write(encoded_command)
        time.sleep(.300)

        decoded_output = ''
        while self.ser.inWaiting() > 0:
            decoded_output += self.ser.read(1).decode()

        return decoded_output
    
    def list_ports(self):
        return (list_ports.comports())
    
    def debug_loop(self):
        print('Begin Debug loop\nPlease type in your command, use \'exit\' to quit.')
        
        while 1:
            serial_command = input('>>')
            if serial_command == 'exit' or serial_command == 'eixt':
                print('Exiting Debuging loop, closing port')
                self.ser.close()
                print('Port closed, breaking from loop.')
                break
            else:
                serial_output = self.write_read_serial(serial_command)
                self.print_serial(serial_output)
                
        print('Broke from loop, goodbye.') 

    def print_serial(self,serial_output):
        if serial_output != '':
            print('+++\n' + serial_output + '\n+++\n')
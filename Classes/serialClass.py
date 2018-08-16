import serial
import time
from serial.tools import list_ports

GET_ENGINEERING_MODE_QUERY = 'AT+CENG?'
SET_ENGINEERING_MODE_QUERY = 'AT+CENG=1,1'

class serialClass:

    def __init__(self, port, baud=115200):
        self._port = port
        self._baud = baud
        self._ser = serial.Serial(
            port=port,
            baudrate=baud
        )

    def getPort(self):
        return self._port

    def write_read_serial(self, serial_command, wait_time=0.3):
        encoded_command = serial_command + '\r\n'
        encoded_command = encoded_command.encode()

        self._ser.write(encoded_command)
        time.sleep(wait_time)

        decoded_output = ''
        while self._ser.inWaiting() > 0:
            decoded_output += self._ser.read(1).decode()

        return decoded_output
    
    def collect_fingerprint(self, collection_time=20):
        start_time = time.time()
        while time.time() - start_time < collection_time:
            self._setupCollection()

            sample = self._getSample()
            self._print_serial(sample)

        print((time.time() - start_time), 'seconds has elapsed.') 
        print('Processing Fingerprint.......\n')

        fingerprint_Location = input('Input the location of the fingerprint: ')
        print('\nDone collecting and analysing fingerprint, Storing in database. Remember to backup the data base.')
    
    def debug_loop(self):
        print('Begin Debug loop\nPlease type in your command, use \'exit\' to quit.')
        
        while 1:
            serial_command = input('>>')
            if serial_command == 'exit' or serial_command == 'eixt':
                print('Exiting Debuging loop, closing port')
                self._ser.close()
                print('Port closed, breaking from loop.')
                break
            else:
                serial_output = self.write_read_serial(serial_command)
                self._print_serial(serial_output)
                
        print('Broke from loop, goodbye.') 

    # Helper functions
    def _print_serial(self,serial_output):
        if serial_output != '':
            print('+++\n\n' + serial_output + '\n+++\n')

    def _list_ports(self):
        return (list_ports.comports())

    def _setupCollection(self):
        set_eng_mode = self.write_read_serial(SET_ENGINEERING_MODE_QUERY)
        self._expect_OK(set_eng_mode)
    
    def _expect_OK(self, result):
        if result.find('OK') != -1 :
            return
        print('ERROR : EXPECTED AN OK, BUT DID NOT FIND ONE. THIS ERROR WILL SOON BECOME AN EXCEPTION.')
        exit()

    def _getSample(self): 
        return self.write_read_serial(GET_ENGINEERING_MODE_QUERY)

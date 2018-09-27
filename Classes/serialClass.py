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


    def scan_position(self, collection_time=5):
        fingerprint = self._collect_fingerprint(collection_time)
        fingerprint = self._normalise_fingerprint_ave(fingerprint)
        return fingerprint
    
    def short_scan_fingerprint(self, collection_time=20):
        fingerprint = self._collect_fingerprint(collection_time)
        print('Processing Fingerprint.......\n')

        fingerprint_location = input('Input the location of the fingerprint: ')
        print('Samples collected: ', fingerprint, 'At location', fingerprint_location)

        print('Normalising fingerprint...\n')
        fingerprint = self._normalise_fingerprint_ave(fingerprint)

        print('Averaged signal fingerprint: ', { "fingerprint": fingerprint, "location" : fingerprint_location})

        print('\nDone collecting and analysing fingerprint, Storing in database. Remember to backup the data base.\n')
        return {"fingerprint": fingerprint, "location": fingerprint_location}
    
    def deep_scan_location(self, iterations, collection_time=5):

        print('Begining fingerprint scan for', iterations, 'iterations and a', collection_time, 'second collection time.\nThis will take roughly', collection_time*iterations , 'seconds.')
        fingerprint_location = input('Please enter a location for the deep scan: ')
        fingerprints = []
        for i in range(iterations):
            fingerprint = self._collect_fingerprint(fingerprint_location, collection_time)
            print('\nIteration', i+1,'\n\nFingerprint', fingerprint)

            fingerprints.append(self._normalise_fingerprint_ave(fingerprint))
        print('\n\nFingerprints of deep scan: \n\n', fingerprints)

        print('\n\n DEEP SCAN COMPLETE. ANALYSING DATA SET.\n\n')
        normalised_print = self._normalise_deep_scan_ave(fingerprints)
        normalised_print["location"] = fingerprint_location

        return normalised_print
    
    def debug_loop(self):
        print('Begin Debug loop\nPlease type in your command, use \'exit\' to quit.')
        
        while 1:
            serial_command = input('>>')
            if serial_command == 'exit' or serial_command == 'eixt':
                print('Exiting Debuging loop')
                break
            else:
                serial_output = self.write_read_serial(serial_command)
                self._print_serial(serial_output)
                
        print('Broke from loop, goodbye.') 


    # Helper functions
    def write_read_serial(self, serial_command, wait_time=0.3):
        encoded_command = serial_command + '\r\n'
        encoded_command = encoded_command.encode()

        self._ser.write(encoded_command)
        time.sleep(wait_time)

        decoded_output = ''
        while self._ser.inWaiting() > 0:
            decoded_output += self._ser.read(1).decode()

        return decoded_output

    def debug_loop_read(self):
        print('Begin Debug loop\nPlease type in your command, use \'exit\' to quit.')
        while 1:
            serial_output = self.read_serial()
            self._print_serial(serial_output)

    def read_serial(self,wait_time=0.3):
        time.sleep(wait_time)
        decoded_output = ''
        while self._ser.inWaiting() > 0:
            decoded_output += self._ser.read(1).decode()
        
        return decoded_output

    def getPort(self):
        return self._port

    def _print_serial(self,serial_output):
        if serial_output != '':
            print('+++\n\n', serial_output, '\n+++\n')

    def _list_ports(self):
        return (list_ports.comports())

    def _setupCollection(self):
        set_eng_mode = self.write_read_serial(SET_ENGINEERING_MODE_QUERY)
        self._expect_OK(set_eng_mode)

    def _collect_fingerprint(self, location, collection_time=5):
        start_time = time.time()
        fingerprint = dict()
        while time.time() - start_time < collection_time:  
            self._setupCollection()
            sample = self._getSample()
            sample = self._organise_fingerprint(sample)

            fingerprint = self._add_to_fingerprint(sample, fingerprint)
        return fingerprint
    
    def _expect_OK(self, result):
        if result.find('OK') != -1 :
            return
        print('ERROR : EXPECTED AN OK, BUT DID NOT FIND ONE. THIS ERROR WILL SOON BECOME AN EXCEPTION.')
        exit()

    def _getSample(self): 
        return self.write_read_serial(GET_ENGINEERING_MODE_QUERY)

    def _organise_fingerprint(self, fingerprint):
        # split eng information lines into array items
        fingerprint = fingerprint.splitlines()
        print('\n',fingerprint, '\n')

        #get serving cell line
        # 3 for no echo, 4 for echo
        serving_cell_fingerprint = fingerprint[4].replace("\"", "").split(",")

        # strip away verbose serial information
        # 4 for no echo, 5 for echo
        neighbor_fingerprints = fingerprint[5:len(fingerprint)-2]

        organised_fingerprint = []

        organised_fingerprint.append([
            serving_cell_fingerprint[7], serving_cell_fingerprint[2]
        ]) 

        for line in neighbor_fingerprints:
            line = line.replace("\"", "").split(",")
            organised_fingerprint.append([
                line[4],line[2]
            ])

        return organised_fingerprint
        
    
    def _add_to_fingerprint(self, sample, fingerprint):
        for cell in sample:
            if cell[0] in fingerprint:
                fingerprint[cell[0]].append(float(cell[1]))
            else:
                fingerprint[cell[0]] = [float(cell[1])]
        return fingerprint
    
    def _add_to_deep_print(self, sample, deep_print):
        for cell in sample:
            if cell in deep_print:
                deep_print[cell].append(sample[cell])
            else:
                deep_print[cell] = [sample[cell]]
        return deep_print

    def _normalise_deep_scan_ave(self,fingerprints):
        normalised_set = dict()
        for sample_set in fingerprints:
            print('\n\n SAMPLE SET: \n',sample_set)
            normalised_set = self._add_to_deep_print(sample_set, normalised_set)

        print('This is the not normal set :\n\n', normalised_set)

        #  currently just finding the average at a location. We may want to use more than one search point. 
        primary_print = dict()
        for sample in normalised_set:
            primary_print[sample] = sum(normalised_set[sample]) / len(normalised_set[sample])

        print('This is the normalised set :\n\n', primary_print)

        return {"primary_print":primary_print, "fingerprint_set":normalised_set}

    def _normalise_fingerprint_ave(self,fingerprint):
        for loc in fingerprint:
            fingerprint[loc] = sum(fingerprint[loc]) / len(fingerprint[loc])
        return fingerprint
    
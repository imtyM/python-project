from Classes.serialClass import serialClass
from Classes.algorithms import signalClass
from serial.tools import list_ports
import time

usb_modem = None 
signalQualityObject = signalClass()

# functions.
def connect_to_port(port):
    print('Connecting to port: ' + port)
    usb_modem = serialClass(port)

# Find serial interface of the modem.
# Attach usb_modem to the serial interface of the found modem. 
for index, port in enumerate(list_ports.comports()):
    print('found device at ', port[0], '\nAttempting to connect..')
    connect_to_port(port[0])

while 1:
    print (
        'RAT: ', signalQualityObject.getRAT(usb_modem.getCOPS()),
        'Signal Quality % ', signalQualityObject.getQual(usb_modem.getCESQ())
    )

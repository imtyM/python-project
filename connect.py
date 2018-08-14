from Classes.serialClass import serialClass
from Classes.mongoDB import mongoDB
from serial.tools import list_ports

usb_modems = []
number_connected_devices = 0

for index, port in enumerate(list_ports.comports()):
    number_connected_devices += 1
    connect_to_port(port[0], index)

print('Succesfuly connected to',number_connected_devices, 'devices')
for index,usb_modem in enumerate(usb_modems):
    print('Device', index, 'at', usb_modem.getPort())



# functions.
def connect_to_port(port):
    print('Connecting to port: ' + port)
    usb_modems[index] = serialClass(port)

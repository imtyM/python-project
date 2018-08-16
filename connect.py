from Classes.serialClass import serialClass
from Classes.mongoDB import mongoDB
from serial.tools import list_ports
# functions.
def connect_to_port(port):
    print('Connecting to port: ' + port)
    usb_modems.append(serialClass(port))

usb_modems = []
number_connected_devices = 0
print('attempting to connect to devices...')
for index, port in enumerate(list_ports.comports()):
    print('found device at ', port[0], '\nAttempting to connect..')
    number_connected_devices += 1
    connect_to_port(port[0])

print('Succesfuly connected to',number_connected_devices, 'devices')
for index,usb_modem in enumerate(usb_modems):
    print('Device', index, 'at', usb_modem.getPort())

print('opening debug loop on first device')
usb_modems[0].debug_loop()
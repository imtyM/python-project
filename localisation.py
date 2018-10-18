from Classes.serialClass import serialClass
from Classes.mongoDB import mongoDB
from serial.tools import list_ports
from Classes.algorithms import algorithms
import os

myDevice = serialClass('/dev/ttyUSB0')
myDB = mongoDB('lab')
processor = algorithms(myDB)

while True:
    fingerprint = myDevice.scan_position(5)

    print(fingerprint)

    found_location = processor.debugProcess(fingerprint)
    print('THIS IS THE FOUND LOCATION: ', found_location, '\n\n\n\n\n')



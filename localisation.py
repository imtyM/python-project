from Classes.serialClass import serialClass
from Classes.mongoDB import mongoDB
from serial.tools import list_ports
from Classes.algorithms import algorithms
import os

myDevice = serialClass('/dev/ttyUSB0')
myDB = mongoDB('field_collection_170918')
processor = algorithms(myDB)

while True:
    fingerprint = myDevice.scan_position(5)

    print(fingerprint)

    processor.debugProcess(fingerprint)



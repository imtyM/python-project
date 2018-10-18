from Classes.serialClass import serialClass
from Classes.mongoDB import mongoDB
from serial.tools import list_ports
from Classes.algorithms import algorithms
import os
import requests
#  https://8pi5e8eqs7.execute-api.eu-west-1.amazonaws.com/latest
myDevice = serialClass('/dev/ttyUSB0')
myDB = mongoDB('lab')
processor = algorithms(myDB)

while True:
    fingerprint = myDevice.scan_position(5)

    print(fingerprint)

    found_location = processor.debugProcess(fingerprint)
    print('THIS IS THE FOUND LOCATION: ', found_location, '\n\n\n\n\n')
    print('POSTING REQ ------\n\n')
    r = requests.post('https://8pi5e8eqs7.execute-api.eu-west-1.amazonaws.com/latest/currentLocation', data={'currentLocation':found_location})
    print('POST STATUS: ', r.status_code, r.reason)



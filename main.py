from Classes.serialClass import serialClass
from Classes.mongoDB import mongoDB
from serial.tools import list_ports

myDevice = serialClass('/dev/ttyUSB0')
myDevice.collect_fingerprint(5)
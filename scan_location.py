from Classes.serialClass import serialClass
from Classes.mongoDB import mongoDB
from serial.tools import list_ports
import os

myDevice = serialClass('/dev/ttyUSB0')
myDB = mongoDB('lab')

# myDevice.debug_loop()
fingerprint = myDevice.deep_scan_location(10)
# fingerprint = myDevice.short_scan_fingerprint(5)
myDB.updateFingerprint(fingerprint)

print(fingerprint)
os.system('spd-say "w w w w w w w w w w w w w"')



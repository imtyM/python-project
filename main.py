from Classes.serialClass import serialClass
from Classes.mongoDB import mongoDB
from serial.tools import list_ports

myDevice = serialClass('/dev/ttyUSB0')
myDB = mongoDB()

# myDevice.debug_loop()
fingerprint = myDevice.deep_scan_location(20)
# fingerprint = myDevice.short_scan_fingerprint(5)
myDB.updateOne(fingerprint)
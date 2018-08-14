from serialClass import serialClass

serial_for_modem_1 = serialClass('/dev/ttyUSB0')
serial_for_modem_1.debug_loop()

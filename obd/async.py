import obd
import os

os.system('clear')
print("Trying to connect to CAN...")
connection = obd.Async(portstr="/dev/tty.usbserial-12345678", baudrate="500000", protocol="6") # same constructor as 'obd.OBD()'
print(connection.status())
connection.watch(obd.commands['RPM']) # keep track of the RPM

connection.start() # start the async update loop

print(connection.query(obd.commands['RPM']))
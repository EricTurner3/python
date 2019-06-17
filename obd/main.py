import obd
import os
import time

os.system('clear')
print("Trying to connect to CAN...")
connection = obd.OBD(portstr="/dev/tty.usbserial-12345678", baudrate="500000", protocol="6") # auto-connects to USB or RF port
print(connection.status())

# find the rpm
print("Querying current RPM...")
cmd = obd.commands['RPM'] # select an OBD command (sensor)

#print every second
while True:
    response = connection.query(cmd) # send the command, and parse the response
    print(response.value) # returns unit-bearing values thanks to Pint
    time.sleep(1)



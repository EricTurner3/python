import obd
import os
import time

os.system('clear')
print("Trying to connect to CAN...")
connection = obd.OBD(portstr="/dev/tty.usbserial-12345678", baudrate="500000", protocol="6") # auto-connects to USB or RF port
print(connection.status())

print("Querying ambiant air temp..")
cmd = obd.commands['AMBIANT_AIR_TEMP'] # select an OBD command (sensor)

while True:
    response = connection.query(cmd) # send the command, and parse the response
    fahrenheit = (float(str(response).split()[0]) * 9) / 5 + 32
    print(fahrenheit) # returns unit-bearing values thanks to Pint
    time.sleep(1)



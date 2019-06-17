from canard import can
from canard.hw import cantact

# CANable 1 (HS-CAN): /dev/tty.usbmodem146201
# CANable 2 (MS-CAN): 

dev = cantact.CantactDev("/dev/tty.usbmodem146201") # Connect to CANable that enumerated as ttyACM0
dev.set_bitrate(500000) # Set the bitrate to a 500kbps (for HS-CAN)
dev.start() # Go on the bus
count = 0

while True:
    print(count)
    count += 1
    frame = dev.recv() # Receive a CAN frame
    dev.send(frame) # Echo the CAN frame back out on the bus
    print(str(count) + ": " + str(frame)) # Print out the received frame
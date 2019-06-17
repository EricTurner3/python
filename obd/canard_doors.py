# # # # # # # # # # # # # # # # # #
# Project: Mustang Custom Entertainment System
# File Name: canard_doors.py
# Description: Scan the CAN bus for the status of the doors
# Date Created: 30 April 2019
# Modification History:
#   - 30 April 2019: Creation
#   - 1 May 2019: Minor updates for readability
# # # # # # # # # # # # # # # # # #


from canard import can
from canard.hw import cantact
from canard.utils.queue import CanQueue
import time
import sys
import codecs

#TODO: Sometimes when running, We get an AttributeError: 'Frame' object has no attribute 'is_extended_id'
# or AttributeError: 'NoneType' object has no attribute 'data'
# maybe do a try catch loop to only return when we get the data we need?

# 30 April 2019 - Even in the try/catch loop, we throw a lot of errors and sometimes takes 3-4 loops to finally
# get a positive result


# maybe we just need to run the fork of CANard from here with appropriate changes: https://github.com/normaldotcom/CANard/
# 1 April 2019: Merged the branch from normaldotcom into the downloaded package. Need to test to see how it performs

def get_door_status():
    #CANable USB port. Find by calling  ls /dev/tty* in the mac terminal
    usb_port = "/dev/tty.usbmodem146201"

    # init the Cantact with the usb port
    dev = cantact.CantactDev(usb_port)
    # set the bitrate to 500kbps
    dev.set_bitrate(500000)
    # wrap in a CanQueue
    cq = CanQueue(dev)
    # start scanning
    cq.start()
    # receive the packets, and filter for only the 947 (hex: 0x3B3) (door sensor) and print to console
    frame = cq.recv(filter=0x3B3, timeout=1)
    # stop searching
    cq.stop()

    # All of my analysis was done on the hexadecimal format, so we need to convert the ascii into hex for the algorithm
    byte_1 = format(frame.data[0], '02x')
    byte_8 = format(frame.data[7], '02x') 

    # print statements just to verify what the 1st and 8th bytes are (the only bytes that will ever change)
    print("Byte 1:")
    print(byte_1)
    print("Byte 8:")
    print(byte_8)
    print("===============")


    # set up the door statuses (default = False)
    trunk_ajar = False
    driver_ajar = False
    passenger_ajar = False
    hood_ajar = False

    # Algorithm as described in my notebook under Methodology > Door Ajar Status Notes
    
    # Check the second digit of the first byte
    if byte_1[1] == "1":
        trunk_ajar = True

    # Check the first digit of the last byte
    if byte_8[0] == "0":
        driver_ajar = False
        passenger_ajar = False
    if byte_8[0] == "1":
        passenger_ajar = True
    if byte_8[0] == "2":
        driver_ajar = True
    if byte_8[0] == "3":
        driver_ajar = True
        passenger_ajar = True

    # Check the second digit of the last byte
    if byte_8[1] == "a":
        hood_ajar = True


    # print out the statuses to console (as testing)
    print("Trunk Ajar? " + str(trunk_ajar))
    print("Driver Door Ajar? " + str(driver_ajar))
    print("Passenger Door Ajar? " + str(passenger_ajar))
    print("Hood Ajar? " + str(hood_ajar))

    # TODO: Once we can reliably get the data each time,  export the statuses to a JSON file so the front end
    # can pick up on the statuses and display them



connected = False
while not connected:
    try:
        get_door_status()
        connected = True
    except Exception:
        pass

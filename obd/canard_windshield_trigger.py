from canard.hw import socketcan
# create a SocketCAN 
usb_port = "/dev/tty.usbmodem146101"
dev = socketcan.SocketCanDev(usb_port)
# wrap the device in a CanQueue
cq = CanQueue(dev)
cq.start()
# create a request frame
req = can.Frame(0x083)
req.dlc = 3
req.data = [0x04, 0xE0, 0x80]
# send the request
cq.send(req)
# receive a response, timing out after 10 seconds
print(cq.recv(filter=0x083, timeout=10))
cq.stop()
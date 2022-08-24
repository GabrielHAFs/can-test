import time
import os
import sys
import can

# Setting up CAN interface
os.system("ip link set can0 down")
time.sleep(1)
os.system("ip link set can0 type can bitrate 500000 loopback on")
time.sleep(1)
os.system("ip link set can0 up")
time.sleep(1)

# Setting up CAN bus
bus = can.interface.Bus(channel="can0", bustype='socketcan')

# Our Transmission ID
tx_arb_id = 0x001
acc = 0x00000000
data_frame = [0x00, 0x00, 0x00, 0x00]

# CAN Frame
while (1):
    acc = acc + 1000
    data_frame[3] =  acc & 0x000000FF
    data_frame[2] = (acc & 0x0000FF00) >> 8
    data_frame[1] = (acc & 0x00FF0000) >> 16
    data_frame[0] = (acc & 0xFF000000) >> 24

    # Send our message in CAN 11-bit format
    msg = can.Message(arbitration_id=tx_arb_id, data=data_frame, is_extended_id=False)
    bus.send(msg)

    message = bus.recv(1.0)  # Quite a good timeout for a demonstration!
    if message is None:
        print('Timeout occurred, no message.')
        sys.exit(1)
    if acc >= 0x00FFFFFF:
        break

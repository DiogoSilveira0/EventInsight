from network import LoRa
import socket
import time
import binascii

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)

# create an OTAA authentication parameters
app_eui = binascii.unhexlify('70B3D57ED002D39B')
app_key = binascii.unhexlify('F6F0F83F982E7F359F0B55DF603A2FD4')


# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket non-blocking
s.setblocking(False)

# send some data
while True:
    try:
        print('cucu')
        s.send(bytes([0x01, 0x02, 0x03]))

        # get any data received...
        data = s.recv(64)
        if len(data) > 0:
            print(data)
    except:
        pass
    time.sleep(2.5)

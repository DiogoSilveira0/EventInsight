
from network import LoRa
import socket
import time
import binascii
import machine
from machine import Pin
import cbor

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)

# create an OTAA authentication parameters
app_eui = binascii.unhexlify('70B3D57ED002E341')
app_key = binascii.unhexlify('698B4993E83E9445B3B3174A0A546242')

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

print('Network joined!')

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket non-blocking
s.setblocking(False)

button = Pin("P9", mode=Pin.IN, pull=Pin.PULL_UP)

# initial state
is_pressed = False

def send_message():
    data = cbor.dumps(1)
    try:
        s.send(data)
        print(data)
    except:
        pass

while True:
    #initial
    if button() == 1 and not is_pressed:
        time.sleep(1)
    #when it goes from 1 to 0
    elif button() == 0 and not is_pressed:
        send_message()
        is_pressed = True
    #when it goes from 0 to 1
    elif button() == 1 and is_pressed:
        send_message()
        is_pressed = False
    else:
        pass

'''
other butoon code
while True:
    if button() == 1 and not is_pressed:
        time.sleep(1)
    elif button() == 0 and not is_pressed:
        print("Button pressed")
        send_message()
        is_pressed = True
    elif button() == 1 and is_pressed:
        print("Button released")
        is_pressed = False
    else:
        pass
'''

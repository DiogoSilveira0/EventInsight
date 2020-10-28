from machine import UART
import os
from network import WLAN
import machine

uart = UART(0, 115200)
os.dupterm(uart)

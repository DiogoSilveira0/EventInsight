from network import WLAN
import machine

wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()
for net in nets:
    if net.ssid == 'Vodafone-1D0126':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, '249155911'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

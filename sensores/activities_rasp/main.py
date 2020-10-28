import RPi.GPIO as GPIO
import time
import json
from datetime import datetime

import sys
sys.path.insert(0,'..')
from send_message import SendMessage

button = 16
publisher = SendMessage('queue16')

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def message(aux):
    #event starts
    if aux:
        status = 1
        aux = False
    #event ends
    else:
        status = 0
        aux = True
    message = json.dumps({
            "timestamp": datetime.now().isoformat(),
            "fields": {
                "status" : status
            }
        })
    publisher.send(message)
    return aux

def loop():
    pressed = False
    aux = True
    while True:
        button_state = GPIO.input(button)
        #initial state
        if button_state and not pressed:
            time.sleep(1)

        elif not button_state and not pressed:
            print('Start ')
            aux = message(aux)
            pressed = True

        elif button_state and pressed:
            print('End ')
            aux = message(aux)
            pressed = False

        else:
            pass

def endprogram():
    GPIO.cleanup()
    publisher.stop_connection()

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        print('keyboard interrupt detected')
        endprogram()

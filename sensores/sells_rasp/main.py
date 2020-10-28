import RPi.GPIO as GPIO
import time
import json
from datetime import datetime

import sys
sys.path.insert(0,'..')
from send_message import SendMessage

button = 16
publisher = SendMessage('queue15')

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def message():
    message = json.dumps({
            "timestamp": datetime.now().isoformat(),
            "fields": {
                "sell" : 1
            }
        })
    publisher.send(message)

def loop():
    pressed = False

    while True:
        button_state = GPIO.input(button)

        #initial state
        if button_state and not pressed:
            time.sleep(1)

        elif not button_state and not pressed:
            #print('Button Pressed...1')
            message()
            pressed = True

        elif button_state and pressed:
            #print('Button Pressed...2')
            message()
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

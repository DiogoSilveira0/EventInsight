
from send_message import SendMessage
import time
import json
from datetime import datetime

publisher = SendMessage("queue11") # init publish
n = 1

while True:

    message = json.dumps({
        "timestamp": datetime.now().isoformat(),
        "fields": {
            "number" : n
        }
    })

    publisher.send(message)
    n+=1

publisher.stop_connection()

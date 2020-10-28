
import time
import ttn

import json
from datetime import datetime
from send_message import SendMessage

#sells
app_id = "sensor_atividade_pi"
access_key = "ttn-account-v2.-_7tfUtY1b1TPdRep8YaprdWxCDpDtLeMy4LVak3F4E"
publisher = SendMessage('queue22')

def uplink_callback(msg, client):
  print("Received uplink from ", msg.dev_id)
  print(msg)
  print('---------------------------------------')
  if aux == 0:
      status = 1
      aux = 1
  else:
      status = 0
      aux = 0
  message = json.dumps({
          "timestamp": msg.metadata.time,
          "fields": {
              "status" : status
          }
      })
  #print(message)
  publisher.send(message)


handler = ttn.HandlerClient(app_id, access_key)

# using mqtt client
client = handler.data()
client.set_uplink_callback(uplink_callback)
client.connect()
aux = 0;
while True:
    time.sleep(20000000)

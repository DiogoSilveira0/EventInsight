
import time
import ttn

import json
from datetime import datetime
from send_message import SendMessage

#sells
app_id = "sensor_vendas_pi"
access_key = "ttn-account-v2.7p_Qll8fzeAumSjxoSF0PznQdmZ5_cKxgM0CRIxb8Bg"
publisher = SendMessage('queue21')

def uplink_callback(msg, client):
  print("Received uplink from ", msg.dev_id)
  print(msg)
  print('---------------------------------------')
  message = json.dumps({
          "timestamp": msg.metadata.time,
          "fields": {
              "sell" : 1
          }
      })
  publisher.send(message)


handler = ttn.HandlerClient(app_id, access_key)

# using mqtt client
client = handler.data()
client.set_uplink_callback(uplink_callback)
client.connect()
while True:
    time.sleep(20000000)

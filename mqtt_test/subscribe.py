import paho.mqtt.client as mqtt
import time

def on_log (client, userdata, level, buf):
    print('log: ' + buf)

def on_connect (client, userdata, flags, rc):
    if rc == 0:
        print('Connected ok')
    else:
        print('Bad connection return code=', rc)

def on_disconnect (client, userdata, flags, rc=0):
    print('Disconected result code ' + str(rc))

def on_message(client, userdata, msg):
    print("message received ", str(msg.payload.decode("utf-8")))
    print("message topic=", msg.topic)

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_log = on_log
client.on_message = on_message

broker = '192.168.1.243'
print('Conecting to broker', broker)
client.connect(broker)
client.username_pw_set("user2", "user2")

client.loop_start()
time.sleep(1)
while True:
    client.subscribe('Tutorial')
    time.sleep(15)

client.loop_stop()
'''
time.sleep(4)
client.loop_stop()
'''
client.disconnect()

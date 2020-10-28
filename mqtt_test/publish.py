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

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_log = on_log

broker = '192.168.1.243'
print('Conecting to broker', broker)
client.connect(broker)
client.username_pw_set("user1", "user1")

client.loop_start()
time.sleep(1)
while True:
    client.publish("Tutorial","Getting Started with MQTT")
    print ("Message Sent")
    time.sleep(15)

client.loop_stop()
client.disconnect()
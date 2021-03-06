import pika
import json
from datetime import datetime, timedelta 
import time


ROUTING_KEY = "SPECIAL_QUEUE"  
EXCHANGE = "" 


USER = "user"
PASSWORD = "user"


HOST = "localhost" # Dps mudar p url da VM
PORT = 5672


def send_message(message):
    credentials = pika.PlainCredentials(USER, PASSWORD)
    connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=HOST, port=PORT,credentials=credentials)
        )

    channel = connection.channel()

    channel.queue_declare(queue=ROUTING_KEY, durable=True)

    message = json.dumps({
        "timestamp": (datetime.now()).isoformat(),
        "fields": message
    })

    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=ROUTING_KEY,
        body=message,
        properties=pika.BasicProperties(
        delivery_mode=2 # torna a msg persistente
        )
    )

    print("Sent: {}".format(message)) # so p checkar

    connection.close()

def signal():
    send_message({
            "value" : True
        })

if __name__ == "__main__":
    signal()

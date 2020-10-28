import pika
import json
from datetime import datetime, timedelta
import time
import random


ROUTING_KEY = "queue18"  
EXCHANGE = "" 


USER = "user"
PASSWORD = "user"

#HOST = "localhost" 
#PORT = 5672

HOST = "193.136.92.150"
PORT = 1884


def run():
    credentials = pika.PlainCredentials(USER, PASSWORD)
    connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=HOST, port=PORT,credentials=credentials)
        )

    channel = connection.channel()

    channel.queue_declare(queue=ROUTING_KEY, durable=True)

    i = 0

    pattern = '%Y-%m-%d %H:%M:%S.%f'

    t = '2020-07-18 20:49:00.00'

    try:
        for signal in range(100):
            s = datetime.strptime(t, pattern)

            while datetime.now() < s:
                time.sleep(10)
                continue

            message = json.dumps({
                    "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
                    "fields": {
                        "lat": 40.6412 + random.randint(-1, 1) / 10,
                        "lon": -8.65362 + random.randint(-1, 1) / 10,
                    }
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
            time.sleep(3)

        message = json.dumps({
                "timestamp": datetime.now().isoformat(),
                "fields": {
                    "lat": 40.6422,
                    "lon": -8.6569,
                }
            })

        channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=ROUTING_KEY,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2 # torna a msg persistente
            )
        )

        print("Sent: {}".format(message))

    except KeyboardInterrupt:
        connection.close() # p fechar a connection mm q se interrompa a execucao antes
    except pika.exceptions.StreamLostError:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=HOST, port=PORT,credentials=credentials)
        )

        channel = connection.channel()

        channel.queue_declare(queue=ROUTING_KEY, durable=True)

        print("Connection reseted")

    connection.close()

if __name__ == "__main__":
    run()

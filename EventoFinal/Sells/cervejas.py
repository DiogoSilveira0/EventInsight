import pika
import json
from datetime import datetime
import time
import random


ROUTING_KEY = "queue14"  
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

    times = []
    for day in range(11, 22):   
        times.append('2020-07-{} 21:{}:00.01'.format(day, "{}"))
        times.append('2020-07-{} 22:{}:00.01'.format(day, "{}"))
        times.append('2020-07-{} 23:{}:00.01'.format(day, "{}"))

    ctl = 0

    for t in times:
        lim = random.randint(5, 7)
        m = 0
        for signal in range(lim):
            s = datetime.strptime(t.format(m), pattern)

            while datetime.now() < s:
                time.sleep(10)
                continue

            try:
                message = json.dumps({
                    "timestamp": s.isoformat(),
                    "fields": {
                        "value" : 1,  ### dados simulados
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
                m += 8
                time.sleep(3)

            except KeyboardInterrupt:
                connection.close() # p fechar a connection mm q se interrompa a execucao antes
            except pika.exceptions.StreamLostError:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=HOST, port=PORT,credentials=credentials)
                )

                channel = connection.channel()

                channel.queue_declare(queue=ROUTING_KEY, durable=True)

                print("Connection reseted")
        ctl += 1
    connection.close()

if __name__ == "__main__":
    run()

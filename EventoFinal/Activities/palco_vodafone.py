import pika
import json
import datetime
import time


ROUTING_KEY = "queue17"
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

    pattern = '%Y-%m-%d %H:%M:%S.%f'

    starts = []
    ends = []
    for i in range(11, 22):
        starts.append('2020-07-{} 21:00:00.02'.format(i))
        starts.append('2020-07-{} 22:00:00.02'.format(i))
        starts.append('2020-07-{} 23:00:00.02'.format(i))
        ends.append('2020-07-{} 22:00:00.01'.format(i))
        ends.append('2020-07-{} 23:00:00.01'.format(i))
        ends.append('2020-07-{} 00:00:00.01'.format(i + 1))

    for i in range(len(starts)):
        time.sleep(2)
        s = datetime.datetime.strptime(starts[i], pattern)
        e = datetime.datetime.strptime(ends[i], pattern)

        while not datetime.datetime.now() > s:
            continue

        try:
                message = json.dumps({
                        "timestamp": s.isoformat(),
                        "fields": {
                            "status" : 1  ### dados simulados
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
                if datetime.datetime.now() < e:
                    time.sleep(60*60)

                time.sleep(2)

                message = json.dumps({
                        "timestamp": e.isoformat(),
                        "fields": {
                            "status" : 0  ### dados simulados
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

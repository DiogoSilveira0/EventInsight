import pika
import time

EXCHANGE = ""
USER = "user"
PASSWORD = "user"

HOST = "193.136.92.150" #"192.168.1.88" # Dps mudar p url da VM
PORT = 1884

class SendMessage:

    def __init__(self, routing_key):
        self.credentials = pika.PlainCredentials(USER, PASSWORD)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=HOST, port=PORT,credentials=self.credentials)
        )

        self.channel = self.connection.channel()
        # queue
        self.routing_key = routing_key
        self.channel.queue_declare(queue=routing_key, durable=True)

    def send(self, message):
        try:
            self.channel.basic_publish(
                exchange=EXCHANGE,
                routing_key=self.routing_key,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2 # made msg persistent
                )
            )
            # checking
            print("Sent: {}".format(message))
            time.sleep(1)
        except pika.exceptions.StreamLostError:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=HOST, port=PORT,credentials=self.credentials)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.routing_key, durable=True)
            print("Connection reseted")
            print("Sent: {}".format(message))
            time.sleep(1)

    def stop_connection(self):
        self.connection.close()

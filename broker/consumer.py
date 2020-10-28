import pika
import json

import psycopg2
from influxdb import InfluxDBClient

# TSDB host data
TSDB_HOST = "172.18.0.3"
TSDB_PORT = 8086
TSDB_NAME = "event_insight"

# RDB host data
RDB_HOST = "172.18.0.5"
RDB_PORT = 5432
RDB_NAME = "event-insights"
RDB_USER = "user"
RDB_PASSWORD = "user"

# Connections
TSDB_CLIENT = InfluxDBClient(host=TSDB_HOST, port=TSDB_PORT, database=TSDB_NAME)

connected = False
print("Waiting for DB connection")
while not connected:
    try:
        RDB_CONN = psycopg2.connect(host=RDB_HOST, port=RDB_PORT, database=RDB_NAME,
            user=RDB_USER, password=RDB_PASSWORD)
        connected = True
    except psycopg2.OperationalError:
        continue

# user data
USER = "user"
PASSWORD = "user"

# Broker host data
HOST = "172.18.0.4"
PORT = 5672

QUEUE_NAME_START = "queue"
SPECIAL_QUEUE = "SPECIAL_QUEUE"

def run():
    credentials = pika.PlainCredentials(USER, PASSWORD) 
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST, port=PORT, credentials=credentials)
    )

    channel = init_channel(connection)

    try:
        print("Starting consuming...")
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    except ConnectionResetError:
        connection.close()
        run()
    connection.close()

def init_channel(connection):
    print("Creating channel")
    channel = connection.channel()
    create_special_queue(channel)
    create_sensor_queues(channel)
    return channel

def create_special_queue(channel):
    channel.queue_declare(queue=SPECIAL_QUEUE, durable=True)

    channel.basic_consume(
            queue=SPECIAL_QUEUE, 
            on_message_callback=special_callback, 
            auto_ack=True
        )

def create_sensor_queues(channel):
    print("Getting sensors")
    for sensor in get_sensors():
        sid = sensor[0]
        queue = QUEUE_NAME_START + str(sid)
        channel.queue_declare(queue=queue, durable=True)
        
        channel.basic_consume(
            queue=queue, 
            on_message_callback=build_callback(sid), 
            auto_ack=True
        )

def special_callback(ch, method, properties, body):
    ch.stop_consuming()
    print("Sending reset signal")
    raise ConnectionResetError()

def build_callback(sid):
    return lambda ch, method, properties, body: write_to_tsdb(body, sid)

# cria a estrutura JSON q encapsula os dados vindos do sensor e insere-a na influx
def write_to_tsdb(body, sid):
    body = build_data_struct(body, sid)
    TSDB_CLIENT.create_database(TSDB_NAME)
    TSDB_CLIENT.switch_database(TSDB_NAME)
    TSDB_CLIENT.write_points(body)
    print("Received and persisted: {} on {}".format(body, TSDB_CLIENT._database))

# constroi a estrutura de dados a gravar na tsdb
def build_data_struct(body, sid):
    sensor = get_spec_sensor(sid)[0]
    measurement = sensor[1]
    event = sensor[2]
    zone = sensor[4]
    tags = {"sid": sid, "event": event, "zone": zone}
    body = json.loads(body.decode())
    return [
        {
            "measurement": measurement,
            "tags": tags,
            "time": body['timestamp'], # timestamp vindo do sensor
            "fields": body['fields']   # vai buscar os dados independentemente do q eles sejam
        }
    ]

# obtem os sensores a serem usados
def get_sensors():
    cur = RDB_CONN.cursor()
    sql = "select * from loc_sensors;"
    cur.execute(sql, ())
    result = list(cur)
    cur.close()
    return result

# obtem info sobre um sensor especifico
def get_spec_sensor(sid):
    cur = RDB_CONN.cursor()
    sql = "select * from sensors_info where sensor = {};".format(sid)
    cur.execute(sql, ())
    result = list(cur)
    cur.close()
    return result

if __name__ == "__main__":
    print("Waiting for broker connection")
    while True:
        try:
            run()
        except pika.exceptions.AMQPConnectionError:
            continue
        break

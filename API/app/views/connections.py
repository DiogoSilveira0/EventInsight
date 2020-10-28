import psycopg2
from influxdb import InfluxDBClient

# hosts data
INFLUXDB_HOST = "172.18.0.3"
INFLUXDB_PORT = 8086
INFLUXDB_NAME = "event_insight"

RDB_HOST = "172.18.0.5"
RDB_PORT = 5432
RDB_NAME = "event-insights"
RDB_USER = "user"
RDB_PASSWORD = "user"

# connections
INFLUXDB_CLIENT = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT, database=INFLUXDB_NAME)
INFLUXDB_CLIENT.create_database(INFLUXDB_NAME)
INFLUXDB_CLIENT.switch_database(INFLUXDB_NAME)

connected = False
while not connected:
    try:
        RDB_CONN = psycopg2.connect(host=RDB_HOST, port=RDB_PORT, database=RDB_NAME,
            user=RDB_USER, password=RDB_PASSWORD)
        connected = True
    except psycopg2.OperationalError:
        continue
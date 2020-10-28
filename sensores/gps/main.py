import serial
from myGPS import MyGPS
from datetime import datetime
import json

import sys
sys.path.insert(0,'..')
from send_message import SendMessage

# convert dmt to degrees
def convert (d, m, hem):
    aux = str(m).split('.')
    m = int(aux[0])
    s = float(aux[1][0:2]+'.'+aux[1][2:])
    degrees = d + (m/60) + (s/3600)
    if hem == 'S' or hem == 'W':
        degrees = -degrees
    precision = 4
    return "{:.{}f}".format( degrees, precision )

# connect sensor
gps = serial.Serial("/dev/serial0", baudrate = 9600)
my_gps = MyGPS()
debug = 1

publisher = SendMessage('queue14')

# aux to check when localization changes
lat_aux = 0
lon_aux = 0

while True:
    # read values from sensor
    line = gps.readline().decode('ascii')

    # processing received data
    data = line.split(',')
    if data[0] == '$GPRMC':
            my_gps.upload(data)

    lat = convert(my_gps.latitude[0], my_gps.latitude[1], my_gps.latitude[2])
    lon = convert(my_gps.longitude[0], my_gps.longitude[1], my_gps.longitude[2])

    # send message when localization changes
    if (lat_aux!=lat or lon_aux!=lon):
        message = json.dumps({
                "timestamp": datetime.now().isoformat(),
                "fields": {
                "lat": lat,
                "lon": lon,
            }
        })
        publisher.send(message)
        lat_aux = lat
        lon_aux = lon

publisher.stop_connection()

from datetime import date, timedelta

from .ipma import *
from .connections import *
from .messages import *
import datetime

REF = 5 * 60

# queries TSDB
def data(event, measurement):
    query = "select * from {} where event = '{}';".format(measurement, event)
    return list(INFLUXDB_CLIENT.query(query).get_points(measurement=measurement))

# queries relational database
def query(query, args=tuple()):
    cur = RDB_CONN.cursor()
    cur.execute(query, args)
    RDB_CONN.commit()
    try:
        result = list(cur) 
    except psycopg2.ProgrammingError:
        result = {}
    cur.close()
    return result

# organizes people data by zone
def parse_by_zone_people(event):
    return parse_by_zone(event, "people")

# organizes people results by zone
def parse_by_zone(event, measurement):
    data_list = data(event, measurement)
    data_list.sort(key = lambda item: item['time'])
    result = {}
    for item in data_list:
        zone = item["zone"]
        try:
            result[zone][item["time"].split(".")[0].replace("T", "-").replace(":", "-")] = item["value"]
        except KeyError:
            result[zone] = {}
            result[zone][item["time"].split(".")[0].replace("T", "-").replace(":", "-")] = item["value"]
    return result

# last values for number of people,organized by zone
def last_values_people(event):
    data_dic = parse_by_zone(event, "people")
    result = {}
    for key in data_dic.keys():
        dic1 = data_dic[key]
        key1 = list(dic1.keys())[-1]
        result[key] = dic1[key1]
    return result

# last values for parking status
def last_values_parks(event):
    data_dic = parse_by_zone_parks(event)
    result = {}
    for key in data_dic.keys():
        dic1 = data_dic[key]
        key1 = list(dic1.keys())[-1]
        result[key] = dic1[key1]
    return result

# last values for the queues' status
def last_values_queues(event):
    data_dic = parse_by_zone_queues(event)
    result = {}
    for key in data_dic.keys():
        dic1 = data_dic[key]
        key1 = list(dic1.keys())[-1]
        result[key] = dic1[key1]
    return result

# total people in the event
def last_total_people(event):
    data_dic = parse_by_zone(event, "people")
    total = 0
    for key in data_dic.keys():
        dic1 = data_dic[key]
        total += dic1[list(dic1.keys())[-1]]
    return {"total_people": total}

# sells by hour, organized by zone
def sells_by_hour(event):
    data_dic = parse_by_zone(event, "sells")
    result = {}
    for key in list(data_dic.keys()):
        # parse by zone
        result[key] = {}
        dic1 = data_dic[key]
        keys = list(dic1.keys())
        temp = keys[0].split("-")[:4]
        temp[1] = str(int(temp[1]) - 1)  # adjust month to javascript
        temp = "-".join(temp) # hour being analyzed
        result[key][temp] = 1 # entry in the dict for the zone and the hour
        for key1 in keys[1:]:
            # parse by hour
            key1 = key1.split("-")[:4]
            key1[1] = str(int(key1[1]) - 1)
            key1 = "-".join(key1)
            # if sell was made during currently analyzed hour
            if key1 == temp:
                result[key][temp] += 1
            else:
                temp = key1
                result[key][temp] = 1
    return result

# total sells of the current day, organized by zone
def sells_sum_today(event):
    today = "total_sells_{}_today"
    result = {}
    cdate = date.today().strftime("%Y-%m-%d")
    cdate = cdate.split("-")
    cdate[1] = str(int(cdate[1]) - 1)
    cdate = "-".join(cdate)
    dic = sells_by_hour(event)
    for key in list(dic.keys()):
        total_today = 0
        dic1 = dic[key]
        for key1 in list(dic1.keys()):
            if "-".join(key1.split("-")[:3]) == cdate:
                total_today += dic1[key1]
        result[today.format(key)] = total_today
    return result

# total sales of the event organized by zone
def sells_sum_event(event):
    evnt = "total_sells_{}_event" # mal escrito para distinguir do parametro da funcao
    result = {}
    dic = sells_by_hour(event)
    for key in list(dic.keys()):
        total_event = 0
        dic1 = dic[key]
        for key1 in list(dic1.keys()):
            total_event += dic1[key1]
        result[evnt.format(key)] = total_event
    return result

# compares sales with the day before
def sells_compare(event):
    data_dic = data(event, "sells")
    result = {}
    today = date.today()
    delta = timedelta(days=-1)
    yesterday = today + delta
    today = today.strftime("%Y-%m-%d")
    yesterday = yesterday.strftime("%Y-%m-%d")
    dic = parse_by_zone(event, "sells")
    for key in list(dic.keys()):
        y_total = 0
        t_total = 0
        dic1 = dic[key]
        for key1 in list(dic1.keys()):
            if "-".join(key1.split("-")[:3]) == yesterday:
                y_total += 1
            elif "-".join(key1.split("-")[:3]) == today:
                t_total += 1
        result[key] = [y_total, t_total]
    return result

# gets parking data organized by zone
def parse_by_zone_parks(event):
    data_list = data(event, "parks")
    result = {}
    for item in data_list:
        zone = item["zone"]
        try:
            result[zone][item["time"].split(".")[0].replace("T", "-")
                .replace(":", "-")] = {"free": item["free_places"], "full": item["full_places"]}
        except KeyError:
            result[zone] = {}
            result[zone][item["time"].split(".")[0].replace("T", "-")
                .replace(":", "-")] = {"free": item["free_places"], "full": item["full_places"]}
    return result

def get_event_loc(event):
    result = query("select local from events where id = %s;", (event,))
    return result

def get_event_addr(event):
    result = query("select address from events where id = %s;", (event,))
    return {"address": result[0][0]}

def get_event_coords(event):
    result = query("select lat, lon from events where id = %s;", (event,))
    return {"entrance": [float(result[0][0]), float(result[0][1])]}

def get_event_open_close(event):
    result = query("select open_at, close_at from events where id = %s;", (event,))
    return {"open": str(result[0][0]), "close": str(result[0][1])}

def get_parade_name(event):
    result = query("select name from parades where event = %s;", (event,))
    return {"name": result[0][0]}

# weather today + 4 days
def meteo(event):
    loc = get_event_loc(event)[0][0]
    return get(loc)

def meteo_today(event):
    loc = get_event_loc(event)[0][0]
    return get_today(loc)

def all_events():
    result = query("select id, name from events;")
    result = build_list(result)
    return result

def build_list(result):
    # aux method
    new_result = []
    for item in result:
        new_result.append({"name": item[1], "id": item[0]})
    return new_result

# returns queues data by zone
def parse_by_zone_queues(event):
    data_list = data(event, "queues")
    result = {}
    for item in data_list:
        zone = item["zone"]
        try:
            result[zone][item["time"].split(".")[0].replace("T", "-")
                .replace(":", "-")] = [item["people_waiting"], item["avg_time"]]
        except KeyError:
            result[zone] = {}
            result[zone][item["time"].split(".")[0].replace("T", "-")
                .replace(":", "-")] = [item["people_waiting"], item["avg_time"]]
    return result

# gps last location
def last_value_gps(event):
    try:
        last = data(event, "gps")[-1]
        return {"lat": last['lat'], 'lon': last['lon']}
    except IndexError:
        return {}

# planned route for parade
def route(event):
    result = query("select index, street from routes where event = %s order by index;", (event,))
    result = {item[0]: item[1] for item in result}
    return result

def parade_start_data(event):
    result = query("select start_time, end_lat, end_lon from parades where event = %s;", (event,))
    return result[0]

def seconds_to_hours(seconds): 
    # aux method
    return str(datetime.timedelta(seconds=seconds)) 

# get the gps coordinates that were the last values for more than 5 minutes
def get_stop_points(event):
    status = data(1, "gps")
    init = status[0] # first point
    moving = True
    time_moving = 0 # the amount of time during which the parade moves
    stop_points = []
    for item in status[1:]:
        prev_timestamp = datetime.datetime.strptime(str(init['time']).replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S.%f')
        curr_timestamp = datetime.datetime.strptime(str(item['time']).replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S.%f')
        if moving:
            delta = (curr_timestamp - prev_timestamp).seconds
            if delta > REF: # if the interval is too large, it's considered that the parade stopped there
                time_moving = 0 # reset time_moving
                moving = False
                stop_points.append([seconds_to_hours(delta), init['lat'], init['lon']])
            else:
                time_moving += delta # the parade was moving during the interval
        else:
            moving = True
        init = item # compare current point to the next point
    return stop_points, time_moving

# gps status based on db content
def get_gps_status(event):
    WAITING = 1
    ON = 2
    TERM = 3
    status = data(event, "gps")
    start_data = parade_start_data(event)
    if not status: # if there are no data, the parade has not started yet
        return {"current": WAITING, "start_time": str(start_data[0]).replace("T", " ")}
    status = status[-1] # last value
    status = {"time": datetime.datetime.strptime(str(status['time']).replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S.%f'),
     "lat": status['lat'],
     "lon": status['lon']
    } 
    # if the ending coordinates have been reached
    if format(status['lat']) == format(start_data[1], '.4f') and format(status['lon']) == format(start_data[2], '.4f'):
        return {"current": 3, "stop_points": get_stop_points(event)[0]} 
    now = datetime.datetime.now()
    interval = (now - status['time']).seconds
    print("Interval: " + str(interval))
    if interval < REF: # the parade is moving
        return {"current": ON, 
            "time_passed": seconds_to_hours(interval + get_stop_points(event)[1]),
            "moving": "True"}
    return {"current": ON,
            "time_passed": seconds_to_hours(interval),
            "moving": "False"}

# gathers wc sensors data and groups by zone. Usually multiple sensors for the same zone
def wcs_status(event):
    ldata = data(event, "toilet")
    ldata.reverse()
    result = {}
    sids = [] # already checked sensors
    zones = [] 
    for item in ldata:
        if item['sid'] not in sids:  # if sensor not checked
            # organize data by zone of the sensor
            if item['zone'] not in zones:
                result[item['zone']] = {"free": 0, "full": 0}
                zones.append(item['zone'])
            if item['status'] == 1:
                result[item['zone']]['full'] += 1
            else:
                result[item['zone']]['free'] += 1
            sids.append(item['sid'])
    return result

def get_wcs_loc(event):
    result = query("select zone, lat, lon from wcs where event = %s;", (event,))
    result = {item[0]: [float(item[1]), float(item[2])] for item in result}
    return result

def get_parks_loc(event):
    result = query("select name, lat, lon from parks where event = %s;", (event,))
    result = {item[0]: [float(item[1]), float(item[2])] for item in result}
    return result

def get_stages_loc(event):
    result = query("select name, lat, lon from stages where event = %s;", (event,))
    result = {item[0]: [float(item[1]), float(item[2])] for item in result}
    return result

def get_artists_photo(event):
    result = query("select name, photo from artists where event = %s;", (event,))
    result = {item[0]: item[1] for item in result}
    return result

def get_artists_about(event):
    result = query("select name, about from artists where event = %s;", (event,))
    result = {item[0]: item[1] for item in result}
    return result

def stages_artists(event):
    data_list = query("select name, activity from stages_artists where event_id = %s", (event,))
    result = {}
    for item in data_list:
        zone = item[0]
        try:
            result[zone].append(item[1])
        except KeyError:
            result[zone] = []
            result[zone].append(item[1])
    return result

# checks if an user has access to an event
def get_access(user, event):
    return {"access": bool(query("select * from users_events where username = %s and event = %s", (user, event)))}

# posts_sensors
# post method for the sensors to post messages as an alternative way
def post_message(message, queue, user, password):
    send_message_to_queue(message, queue, user, password)

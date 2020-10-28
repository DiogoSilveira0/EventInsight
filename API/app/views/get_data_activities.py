import psycopg2
from influxdb import InfluxDBClient

from datetime import datetime

from .connections import *

STATUS_ON = "on"
STATUS_COMPLETED = "completed"
STATUS_NOT_STARTED = "not_started"
STATUS_LATE5 = "late5"
STATUS_LATE10 = "late10"
STATUS_LATE20 = "late20"
STATUS_LATE20P = "latePlus20"

# gets data from the relational database
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

# all activities, divided by zone
def all_activities(event):
    result = parse_acts_by_zone(query("select activity, scheduled, zone from activities where event = %s", (event,)))
    for key in result.keys():
        result[key].sort(key = lambda item: item[1])
    return result

# organizes the activities by zone
def parse_acts_by_zone(data_list):
    result = {}
    for item in data_list:
        zone = item[2]
        try:
            result[zone].append((item[0], item[1]))
        except KeyError:
            result[zone] = []
            result[zone].append((item[0], item[1]))
    return result

# organizes data by zone
def parse_status_by_zone(data_list):
    result = {}
    for item in data_list:
        zone = item['zone']
        try:
            result[zone].append({'time': datetime.strptime(item['time'].replace("Z", "").split(".")[0],
                "%Y-%m-%dT%H:%M:%S"), 'status': item['status']})
        except KeyError:
            result[zone] = []
            result[zone].append({'time': datetime.strptime(item['time'].replace("Z", "").split(".")[0],
                "%Y-%m-%dT%H:%M:%S"), 'status': item['status']})
    return result

# data from the TSDB, divided by zone
def button_signals(event):
    query = "select time, status, zone from activities where event = '{}'".format(event)
    return parse_status_by_zone(list(INFLUXDB_CLIENT.query(query).get_points()))


# relates the 1s and 0s in the TSDB to the activities in the relational DB, 
# counting all of them and comparing the numbers.
# this gives the activities that already have started as well as ended. 
def activities_status(event):
    activities = all_activities(event)
    signals = button_signals(event)
    result = {}
    for key in activities.keys():
        result[key] = {}
        count0 = 0
        count1 = 0
        # get the signals from the button
        if key in signals.keys():
            for item in signals[key]:
                if item['status'] == 0:
                    count0 += 1
                elif item['status'] == 1:
                    count1 += 1
        for i in range(count1): # count1 saves how many activities have already started
            if i < count0:
                result[key][activities[key][i][0]] = STATUS_COMPLETED # count0 saves how many activities have already finnished
            else:
                result[key][activities[key][i][0]] = STATUS_ON
        if len(activities[key]) > count1: # if some activity has not started yet
            result[key][activities[key][count1][0]] = get_delay(activities[key][count1]) # sets the status for the first one (it can be delayed)
            if len(activities[key]) > count1 + 1: # if there are even more, sets them as not started
                for i in range(count1 + 1, len(activities[key])):
                    result[key][activities[key][i][0]] = STATUS_NOT_STARTED
    return result

# gets the delay of an activity that has not started yet
def get_delay(activity):
    scheduled = activity[1]
    curr = datetime.now()
    delay = curr - scheduled
    delay =  divmod(delay.total_seconds(), 60)[0]
    return STATUS_NOT_STARTED if delay < 0 else STATUS_LATE5 if delay < 5 else STATUS_LATE10 if delay < 10 else STATUS_LATE20 if delay < 20 else STATUS_LATE20P

# all the activities that have already finnished along with their start and end times
def event_history(event): 
    activities = all_activities(event)
    signals = button_signals(event)
    result = {}
    for key in signals.keys():
        ones = []
        zeroes = []
        for signal in signals[key]:
            if signal['status'] == 0:
                zeroes.append(signal['time'])
            else:
                ones.append(signal['time'])
        for i in range(len(zeroes)):
            result[activities[key][i][0]] = [ones[i].date()
                .strftime("%Y-%m-%d"), ones[i].time()
                .strftime("%H-%M-%S"), zeroes[i].time()
                .strftime("%H-%M-%S")]
    return result

def today_plan(event):
    result = query("select activity, scheduled, zone from activities where event = %s", (event,))
    result = [item for item in result if item[1].date() == datetime.now().date()]
    result.sort(key = lambda item: item[1])
    return {item[0] : [item[1].strftime("%H-%M-%S"), item[2]] for item in result}

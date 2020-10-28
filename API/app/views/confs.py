from datetime import datetime

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .manage_data import *

OK = {"status": "ok"}
PATTERN = '%Y-%m-%d %H:%M:%S'

#Views dos Eventos
@api_view(['GET'])
def getAllEvents(request):
    result = get_events()
    responseJson = []
    for event in result:
        eventJson = {"eventID": event[0],
                    "event_name": event[1],
                    "local": event[2],
                    "lat": event[3],
                    "lon": event[4],
                    "address": event[5],
                    "open_at": event[6],
                    "close_at": event[7]}
        responseJson.append(eventJson)
    return Response(responseJson)

@api_view(['POST'])
def postEvent(request):
    json_parsed = json.loads(request.body)
    insert_event(json_parsed["event_name"], json_parsed["local"], json_parsed["lat"], json_parsed["lon"],
                 json_parsed["address"], json_parsed["open_at"], json_parsed["close_at"])
    return Response(OK)

@api_view(['DELETE'])
def deleteEvent(request):
    eventID = request.GET['event']
    delete_event(eventID)
    return Response(OK)

#Views dos Sensores

@api_view(['GET'])
def getAllSensors(request):
    result = get_sensors()
    responseJson = []
    for sensor in result:
        sensorJson = { "sensorID": sensor[0],
                       "type": sensor[1],
                       "zone": sensor[2]}
        responseJson.append(sensorJson)
    return Response(responseJson)

@api_view(['POST'])
def postSensor(request):
    insert_sensor(json.loads(request.body)['type'])
    return Response(OK)

@api_view(['POST'])
def postSensorLocation(request):
    json_parsed = json.loads(request.body)
    insert_sensor_location(json_parsed["sensorID"], json_parsed["eventID"], json_parsed["zone"])
    return Response(OK)

@api_view(['PUT'])
def editSensorLocation(request):
    json_parsed = json.loads(request.body)
    update_sensor_location(json_parsed["sensorID"], json_parsed["eventID"], json_parsed["zone"])
    return Response(OK)

@api_view(['DELETE'])
def deleteSensor(request):
    sensorID = int(request.GET['sensor'])
    delete_sensor_location(sensorID)
    delete_sensor(sensorID)
    return Response(OK)

@api_view(['GET'])
def getSensorsEvent(request):
    result = get_sensors_event(request.GET['event'])
    responseJson = []
    for sensor in result:
        sensorJson = {"sensorID": sensor[0],
                     "type": sensor[1],
                     "eventID": sensor[2],
                     "event_name": sensor[3],
                     "zone": sensor[4],
                     "address": sensor[5]}
        responseJson.append(sensorJson)
    return Response(responseJson)
# ------------------------------------/--/--------------------------------------------------
@api_view(['GET'])
def sensor_type(request):
    result = {}
    sensor = request.GET['sensor']
    data = get_sensor_type(sensor)
    result['type'] = data[0][0]
    return Response(result)

@api_view(['GET'])
def sensors_by_type(request):
    result = []
    stype = request.GET['type']
    data = get_sensors_by_type(stype)
    return Response([{
        "sensor": item[0],
        "event": {
            "id": item[1],
            "name": item[2]
        },
        "zone": item[3]
    } for item in data])

@api_view(['GET'])
def activities(request):
    event = request.GET['event']
    data = get_activities(event)
    return Response([{
        "activity": item[0],
        "scheduled": item[1].isoformat(),
        "zone": item[2]
    } for item in data])

@api_view(['POST'])
def add_activity(request):
    body = json.loads(request.body)
    insert_activity(body['event'], body['activity'], datetime.strptime(body['scheduled'], PATTERN), body['zone'])
    return(Response(OK))

@api_view(['DELETE'])
def rm_activity(request):
    event = request.GET['event']
    activity = request.GET['activity']
    delete_activity(event, activity)
    return Response(OK)

@api_view(['DELETE'])
def rm_activities(request):
    event = request.GET['event']
    delete_activities_for_event(event)
    return Response(OK)

@api_view(['GET'])
def route_nodes(request):
    event = request.GET['event']
    result = {}
    data = get_route_nodes(event)
    for node in data:
        result[node[0]] = node[1]
    return Response(result)

@api_view(['POST'])
def add_route_node(request):
    body = json.loads(request.body)
    insert_route_node(body['event'], body['index'], body['street'])
    return Response(OK)

@api_view(['DELETE'])
def rm_route_node(request):
    event = request.GET['event']
    index = request.GET['index']
    delete_route_node(event, index)
    return Response(OK)

@api_view(['DELETE'])
def rm_route(request):
    event = request.GET['event']
    delete_full_route(event)
    return Response(OK)

@api_view(['GET'])
def all_users(request):
    data = get_users()
    result = {}
    for user in data:
        try:
            result[user[0]].append(user[1])
        except KeyError:
            result[user[0]] = []
            result[user[0]].append(user[1])
    return Response(result)

@api_view(['GET'])
def event_users(request):
    event = request.GET['event']
    data = get_users_for_event(event)
    return Response([user[0] for user in data])

@api_view(['GET'])
def user_events(request):
    user = request.GET['user']
    data = get_events_for_user(user)
    return Response([user[0] for user in data])

@api_view(['POST'])
def post_user(request):
    body = json.loads(request.body)
    insert_user(body['user'], body['event'])
    return Response(OK)

@api_view(['DELETE'])
def rm_access(request):
    user = request.GET['user']
    event = request.GET['event']
    delete_access(user, event)
    return Response(OK)

@api_view(['DELETE'])
def rm_user(request):
    user = request.GET['user']
    delete_user(user)
    return Response(OK)

@api_view(['DELETE'])
def rm_users_for_event(request):
    event = request.GET['event']
    delete_users_for_event(event)
    return Response(OK)

@api_view(['POST'])
def post_parade(request):
    body = json.loads(request.body)
    insert_parade(body['name'], body['event'], datetime.strptime(body['start_time'], PATTERN),
        body['start_lat'], body['start_lon'], body['end_lat'], body['end_lon'])
    return Response(OK)

@api_view(['GET'])
def all_parades(request):
    data = get_all_parades()
    return Response([{
            "name": item[0],
            "event": item[1],
            "start_time": item[2],
            "start_coords": {
                "lat": item[3],
                "lon": item[4]
            },
            "end_coords": {
                "lat": item[5],
                "lon": item[6]
            }
        } for item in data])

@api_view(['GET'])
def parade(request):
    event = request.GET['event']
    data = get_parade_for_event(1)[0]
    result = {
        "name": data[0],
        "start_time": data[1],
        "start_coords": {
            "lat": data[2],
            "lon": data[3]
        },
        "end_coords":{
            "lat": data[4],
            "lon": data[5]
        }
    }
    return Response(result)

@api_view(['DELETE'])
def rm_parade(request):
    event = request.GET['event']
    delete_parade(event)
    return Response(OK)

@api_view(['POST'])
def post_park(request):
    body = json.loads(request.body)
    insert_park(body['name'], body['event'], body['lat'], body['lon'])
    return Response(OK)

@api_view(['GET'])
def parks(request):
    event = request.GET['event']
    data = get_parks(event)
    return Response([
        {
            "name": item[0],
            "coords": {
                "lat": item[1],
                "lon": item[2]
            }
        } for item in data])

@api_view(['DELETE'])
def rm_park(request):
    event = request.GET['event']
    name = request.GET['name']
    delete_park(name, event)
    return Response(OK)

@api_view(['DELETE'])
def rm_parks(request):
    event = request.GET['event']
    delete_parks_from_event(event)
    return Response(OK)

@api_view(['POST'])
def add_wcs(request):
    body = json.loads(request.body)
    insert_wc(body['zone'], body['event'], body['lat'], body['lon'])
    return Response(OK)

@api_view(['GET'])
def wcs(request):
    event = request.GET['event']
    data = get_wcs(event)
    return Response([{
        "name": item[0],
            "coords": {
                "lat": item[1],
                "lon": item[2]
            }
    } for item in data])    

@api_view(['DELETE'])
def rm_wcs(request):
    event = request.GET['event']
    zone = request.GET['zone']
    delete_wc(zone, event)
    return Response(OK)

@api_view(['DELETE'])
def rm_wcs_event(request):
    event = request.GET['event']
    delete_wcs_from_event(event)
    return Response(OK)

@api_view(['POST'])
def add_stage(request):
    body = json.loads(request.body)
    insert_stage(body['name'], body['event'], body['lat'], body['lon'])
    return Response(OK)

@api_view(['GET'])
def stages(request):
    event = request.GET['event']
    data = get_stages(event)
    return Response([{
            "name": item[0],
            "coords": {
                "lat": item[1],
                "lon": item[2]
            }
    } for item in data])

@api_view(['DELETE'])
def rm_stage(request):
    event = request.GET['event']
    name = request.GET['name']
    delete_stage(name, event)
    return Response(OK)

@api_view(['DELETE'])
def rm_stages_event(request):
    event = request.GET['event']
    delete_stages_from_event(event)
    return Response(OK)

@api_view(['POST'])
def post_artist(request):
    body = json.loads(request.body)
    insert_artist(body['name'], body['event'], body['photo'], body['about'])
    return Response(OK)

@api_view(['GET'])
def all_artists(request):
    event = request.GET['event']
    data = get_artists(event)
    return Response([{
        "name": item[0],
        "photo": item[1],
        "about": item[2]
    } for item in data])

@api_view(['GET'])
def single_artist(request):
    event = request.GET['event']
    name = request.GET['name']
    data = get_artist(event, name)[0]
    result = {
        "photo": data[0],
        "about": data[1]
    }
    return Response(result)

@api_view(['DELETE'])
def rm_artist(request):
    event = request.GET['event']
    name = request.GET['name']
    delete_artist(event, name)
    return Response(OK)

@api_view(['DELETE'])
def rm_all_artists(request):
    event = request.GET['event']
    delete_artists(event)
    return Response(OK)

#API
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from influxdb import InfluxDBClient

import datetime

import psycopg2
from .get_data_activities import *
from .get_data import *
import json

@api_view(['GET'])
def get_people(request):
    event = request.GET['event']
    return Response(parse_by_zone_people(event))

@api_view(['GET'])
def get_ttl_ppl(request):
    event = request.GET['event']
    return Response(last_total_people(event))

@api_view(['GET'])
def get_current_people(request):
    event = request.GET['event']
    return Response(last_values_people(event))

@api_view(['GET'])
def get_sells_hourly(request):
    event = request.GET['event']
    return Response(sells_by_hour(event))

@api_view(['GET'])
def get_sells_sum_today(request):
    event = request.GET['event']
    return Response(sells_sum_today(event))

@api_view(['GET'])
def get_sells_sum_event(request):
    event = request.GET['event']
    return Response(sells_sum_event(event))

@api_view(['GET'])
def get_parks_status(request):
    event = request.GET['event']
    return Response(last_values_parks(event))

@api_view(['GET'])
def get_meteo(request):
    event = request.GET['event']
    return Response(meteo(event))

@api_view(['GET'])
def get_meteo_today(request):
    event = request.GET['event']
    return Response(meteo_today(event))

@api_view(['GET'])
def get_all_events(request):
    return Response(all_events())

@api_view(['GET'])
def get_queues(request):
    event = request.GET['event']
    return Response(last_values_queues(event))

@api_view(['GET'])
def get_sells_compare(request):
    event = request.GET['event']
    return Response(sells_compare(event))

@api_view(['GET'])
def get_activities_status(request):
    event = request.GET['event']
    return Response(activities_status(event))

@api_view(['GET'])
def get_event_history(request):
    event = request.GET['event']
    return Response(event_history(event))

@api_view(['GET'])
def get_today_plan(request):
    event = request.GET['event']
    return Response(today_plan(event))

@api_view(['GET'])
def get_gps_coords(request):
    event = request.GET['event']
    return Response(last_value_gps(event))

@api_view(['GET'])
def get_route(request):
    event = request.GET['event']
    return Response(route(event))

@api_view(['GET'])
def get_status_gps(request):
    event = request.GET['event']
    return Response(get_gps_status(event))

@api_view(['GET'])
def get_status_wcs(request):
    event = request.GET['event']
    return Response(wcs_status(event))

@api_view(['GET'])
def get_loc_wcs(request):
    event = request.GET['event']
    return Response(get_wcs_loc(event))

@api_view(['GET'])
def get_loc_parks(request):
    event = request.GET['event']
    return Response(get_parks_loc(event))

@api_view(['GET'])
def get_loc_stages(request):
    event = request.GET['event']
    return Response(get_stages_loc(event))

@api_view(['GET'])
def get_photo_artists(request):
    event = request.GET['event']
    return Response(get_artists_photo(event))

@api_view(['GET'])
def get_about_artists(request):
    event = request.GET['event']
    return Response(get_artists_about(event))

@api_view(['GET'])
def get_event_address(request):
    event = request.GET['event']
    return Response(get_event_addr(event))

@api_view(['GET'])
def get_coords_event(request):
    event = request.GET['event']
    return Response(get_event_coords(event))

@api_view(['GET'])
def get_open_close(request):
    event = request.GET['event']
    return Response(get_event_open_close(event))

@api_view(['GET'])
def get_name_parade(request):
    event = request.GET['event']
    return Response(get_parade_name(event))

@api_view(['GET'])
def get_stages_artists(request):
    event = request.GET['event']
    return Response(stages_artists(event))

@api_view(['GET'])
def access(request):
    event = request.GET['event']
    user = request.GET['user']
    return Response(get_access(user, event))

@api_view(['POST'])
def post_data(request):
    data = json.loads(request.body)
    queue = data['queue']
    data['message']['timestamp'] = datetime.datetime.now().isoformat() # Porque alguns sensores nao conseguem enviar timestamp
    message = data['message']
    user = data['user']
    password = data['password']
    post_message(message, queue, user, password)
    return Response({"status": "ok"})

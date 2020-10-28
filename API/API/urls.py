"""API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #API
    path('dashboard/people', views.get_people),
    path('dashboard/ttl_people', views.get_ttl_ppl),
    path('dashboard/current_people', views.get_current_people),
    path('dashboard/sells', views.get_sells_hourly),
    path('dashboard/sum_sells_today', views.get_sells_sum_today),
    path('dashboard/sum_sells_event', views.get_sells_sum_event),
    path('dashboard/compare_sells', views.get_sells_compare),
    path('dashboard/parks', views.get_parks_status),
    path('dashboard/meteo', views.get_meteo),
    path('dashboard/meteo_today', views.get_meteo_today),
    path('dashboard/all_events', views.get_all_events),
    path('dashboard/queues', views.get_queues),
    path('dashboard/activities_status', views.get_activities_status),
    path('dashboard/event_history', views.get_event_history),
    path('dashboard/today_plan', views.get_today_plan),
    path('dashboard/gps_coords', views.get_gps_coords),
    path('dashboard/route', views.get_route),
    path('dashboard/gps_status', views.get_status_gps),
    path('dashboard/wcs_status', views.get_status_wcs),
    path('dashboard/wcs_loc', views.get_loc_wcs),
    path('dashboard/parks_loc', views.get_loc_parks),
    path('dashboard/stages_loc', views.get_loc_stages),
    path('dashboard/artists_photo', views.get_photo_artists),
    path('dashboard/artists_about', views.get_about_artists),
    path('dashboard/event_address', views.get_event_address),
    path('dashboard/event_coords', views.get_coords_event),
    path('dashboard/event_open_close', views.get_open_close),
    path('dashboard/event_parade_name', views.get_name_parade),
    path('dashboard/stages_artists', views.get_stages_artists),
    path('dashboard/access', views.access),

    # API - Events & Sensors
    path('dashboard/config/events/all', views.getAllEvents),
    path('dashboard/config/events/add', views.postEvent),
    path('dashboard/config/events/remove', views.deleteEvent),
    path('dashboard/config/sensors/all', views.getAllSensors),
    path('dashboard/config/sensors/add', views.postSensor),
    path('dashboard/config/sensors/add/to_location', views.postSensorLocation),
    path('dashboard/config/sensors/edit', views.editSensorLocation),
    path('dashboard/config/sensors/remove', views.deleteSensor),
    path('dashboard/config/sensors/in_event', views.getSensorsEvent),
    # ----------/--/-------------------
    path('dashboard/config/sensors/type', views.sensor_type),
    path('dashboard/config/sensors/by_type', views.sensors_by_type),
    path('dashboard/config/activities', views.activities),
    path('dashboard/config/activities/add', views.add_activity),
    path('dashboard/config/activities/rm/single', views.rm_activity),
    path('dashboard/config/activities/rm', views.rm_activities),
    path('dashboard/config/route', views.route_nodes),
    path('dashboard/config/route/nodes/add', views.add_route_node),
    path('dashboard/config/route/nodes/rm', views.rm_route_node),
    path('dashboard/config/routes/rm', views.rm_route),
    path('dashboard/config/users/all', views.all_users),
    path('dashboard/config/users/for_event', views.event_users),
    path('dashboard/config/events/for_user', views.user_events),
    path('dashboard/config/access/add', views.post_user),
    path('dashboard/config/access/rm', views.rm_access),
    path('dashboard/config/users/rm', views.rm_user),
    path('dashboard/config/users/rm_for', views.rm_users_for_event),
    path('dashboard/config/parades/add', views.post_parade),
    path('dashboard/config/parades/all', views.all_parades),
    path('dashboard/config/parades', views.parade),
    path('dashboard/config/parades/delete', views.rm_parade),
    path('dashboard/config/parks/add', views.post_park),
    path('dashboard/config/parks', views.parks),
    path('dashboard/config/parks/rm/single', views.rm_park),
    path('dashboard/config/parks/rm', views.rm_parks),
    path('dashboard/config/wcs/add', views.add_wcs),
    path('dashboard/config/wcs', views.wcs),
    path('dashboard/config/wcs/rm/single', views.rm_wcs),
    path('dashboard/config/wcs/rm', views.rm_wcs_event),
    path('dashboard/config/stages/add', views.add_stage),
    path('dashboard/config/stages/', views.stages),
    path('dashboard/config/stages/rm/single', views.rm_stage),
    path('dashboard/config/stages/rm', views.rm_stages_event),
    path('dashboard/config/artists/add', views.post_artist),
    path('dashboard/config/artists/all', views.all_artists),
    path('dashboard/config/artists/single', views.single_artist),
    path('dashboard/config/artists/rm/single', views.rm_artist),
    path('dashboard/config/artists/rm', views.rm_all_artists),

    # Posts From Sensors
    path('sensors/', views.post_data),

]

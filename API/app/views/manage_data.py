import psycopg2

from .messages import *

from .connections import *

def query(query, args=tuple()):
    cur = RDB_CONN.cursor()
    cur.execute(query, args)
    RDB_CONN.commit()
    try:
        result = list(cur) 
    except psycopg2.ProgrammingError:
        result = None
    cur.close()
    return result

### interacoes com a postgres:
#v
def get_sensors():
    return query("select * from sensor_bindings;")
#v
def get_sensors_event(event_id):
    # sensores para um evento
    return query("select * from sensor_bindings where event_id = %s;", (event_id,))

def get_sensor_type(sensor):
    return query("select type from sensors where id = %s;", (sensor,))

def get_sensors_by_type(type):
    return query("select sensor, event_id, event_name, zone from sensor_bindings where type = %s;", (type,))

def delete_sensor(sensor_id):
    query("delete from sensors where id = %s;", (sensor_id,))

def insert_sensor(sensor_type):
    query("insert into sensors (type) values (%s);", (sensor_type,))

def insert_sensor_location(sensor_id, event_id, zone):
    query("insert into loc_sensors (sensor, event, zone) values (%s, %s, %s);", (sensor_id, event_id, zone))
    signal()

def update_sensor_location(sensor_id, event_id, zone):
    query("update loc_sensors set event = %s, zone = %s where sensor = %s;", (event_id, zone, sensor_id))

def delete_sensor_location(sensor_id):
    query("delete from loc_sensors where sensor = %s", (sensor_id,))
    signal()

def delete_sensors_event(event_id):
    # em vez de apagar um unico sensor, apaga tds os associados a 1 evento
    query("delete from loc_sensors where event = %s", (event_id,))
    signal()

def get_activities(event):
    return query("select activity, scheduled, zone from activities where event = %s", (event,))

def insert_activity(event, activity, scheduled, zone):
    query("insert into activities (event, activity, scheduled, zone) values (%s, %s, %s, %s);", (event, activity, scheduled, zone))

def delete_activity(event, activity):
    query("delete from activities where event = %s and activity = %s;", (event, activity))

def delete_activities_for_event(event):
    # em vez de apagar so uma atividade apaga tdas as de um evento
    query("delete from activities where event = %s", (event,))

def get_events():
    return query("select * from events;")

def insert_event(name, local, lat, lon, address, open_at, close_at):
    query("insert into events(name, local, lat, lon, address, open_at, close_at) values (%s, %s, %s, %s, %s, %s, %s);",
        (name, local, lat, lon, address, open_at, close_at))

def delete_event(event_id):
    query("delete from events where id = %s;", (event_id,))

def get_route_nodes(event):
    return query("select index, street from routes where event = %s;", (event,))

def insert_route_node(event, index, street):
    query("insert into routes (event, index, street) values (%s, %s, %s);", (event, index, street))

def delete_route_node(event, index):
    query("delete from routes where event = %s and index = %s;", (event, index))

def delete_full_route(event):
    query("delete from routes where event = %s;", (event,))

def get_users():
    return query("select * from users_events;")

def get_users_for_event(event):
    return query("select username from users_events where event = %s", (event,))

def get_events_for_user(user):
    return query("select event from users_events where username = %s", (user,))

def insert_user(user, event):
    query("insert into users_events (username, event) values (%s, %s);", (user, event))

def delete_access(user, event):
    query("delete from users_events where username = %s and event = %s", (user, event))

def delete_user(user):
    query("delete from users_events where username = %s", (user,))

def delete_users_for_event(event):
    query("delete from users_events where event = %s", (event,))

def insert_parade(name, event, start_time, start_lat, start_lon, end_lat, end_lon):
    query("""insert into parades (name, event, start_time, start_lat, start_lon, end_lat, end_lon)
        values (%s, %s, %s, %s, %s, %s, %s);""",
        (name, event, start_time, start_lat, start_lon, end_lat, end_lon))

def get_all_parades():
    return query("select * from parades;")

def get_parade_for_event(event):
    return query("""select name, start_time, start_lat, start_lon, end_lat, end_lon
        from parades where event = %s;""", (event,))

def delete_parade(event):
    query("delete from parades where event = %s", (event,))

def insert_park(name, event, lat, lon):
    query("insert into parks (name, event, lat, lon) values (%s, %s, %s, %s);", (name, event, lat, lon))

def get_parks(event):
    return query("select name, lat, lon from parks where event = %s", (event,))

def delete_park(name, event):
    query("delete from parks where name = %s and event = %s", (name, event))

def delete_parks_from_event(event):
    query("delete from parks where event = %s", (event,))

def insert_wc(zone, event, lat, lon):
    query("insert into wcs (zone, event, lat, lon) values (%s, %s, %s, %s);", (zone, event, lat, lon))

def get_wcs(event):
    return query("select zone, lat, lon from wcs where event = %s", (event,))

def delete_wc(zone, event):
    query("delete from wcs where zone = %s and event = %s", (zone, event))

def delete_wcs_from_event(event):
    query("delete from wcs where event = %s", (event,))

def insert_stage(name, event, lat, lon):
    query("insert into stages (name, event, lat, lon) values (%s, %s, %s, %s);", (name, event, lat, lon))

def get_stages(event):
    return query("select name, lat, lon from stages where event = %s", (event,))

def delete_stage(name, event):
    query("delete from stages where name = %s and event = %s", (name, event))

def delete_stages_from_event(event):
    query("delete from stages where event = %s", (event,))

def insert_artist(name, event, photo, about):
    query("insert into artists (name, event, photo, about) values (%s, %s, %s, %s);", (name, event, photo, about))

def get_artists(event):
    return query("select name, photo, about from artists where event = %s;", (event,))

def get_artist(event, name):
    return query("select photo, about from artists where event = %s and name = %s;", (event, name))

def delete_artist(event, name):
    query("delete from artists where event = %s and name = %s;", (event, name))

def delete_artists(event):
    query("delete from artists where event = %s", (event,))

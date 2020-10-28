from django.shortcuts import render, redirect
from django.template.response import  TemplateResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserRegisterForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import requests
import json
from django.contrib.auth import authenticate
import datetime


id = "1"

def home(request,template_name="home.html"):
	#chamada feita
	artists = requests.get('http://172.18.0.6:8080/dashboard/artists_photo?event='+id)
	if artists.status_code == 200:
		artists= artists.json()
		if artists == {}:
			artists =  { "Error":"static/img/err.png" }
	else:
		artists = { "Error":"static/img/err.png" }
	
	#chamada feita
	about = requests.get('http://172.18.0.6:8080/dashboard/artists_about?event='+id)
	if about.status_code == 200:
		about= about.json()
		if about == {}:
			about =  { "Error": "Descrição do artista não definida" }
	else:
		about = { "Error": "Descrição do artista não definida" }
	
	
	'''
	today_forecast = {
		"t_max": 20,
		"t_min":12,
		"prob_rain" : 75,
		"wind": 8
	}

	'''
	#chamada feita
	today_forecast = requests.get('http://172.18.0.6:8080/dashboard/meteo_today?event='+id)
	if today_forecast.status_code == 200:
		today_forecast = today_forecast.json()
		if today_forecast == {}:
			today_forecast =  { "t_max": 20, "t_min":12, "prob_rain" : 75, "wind": 8 }
	else:
		today_forecast = { "t_max": 20, "t_min":12, "prob_rain" : 75, "wind": 8}
	

	#chamada feita
	activities = requests.get('http://172.18.0.6:8080/dashboard/activities_status?event='+id)
	if activities.status_code == 200:
		activities = activities.json()
		if activities == {}:
			activities =  { 'error': { "error":{"status":"late20"} } }
	else:
		activities = { 'error': { "error":{"status":"late20"} } }
	

	act_to_send = {}
	for palco in activities:
		p = activities[palco]
		for artist in p:
			st = p[artist]
			if(st!="not_started" and st!="completed"):
				act_to_send[palco]=[artist,st]
	
	#chamada feita
	status = requests.get('http://172.18.0.6:8080/dashboard/gps_status?event='+id)
	if status.status_code == 200:
		status = status.json()
		if status == {}:
			status = { "erro":"erro"}
	else:
		status = { "erro":"erro"}
    
	if(status["current"]==1):
		data = status["start_time"] 
		year = (data.split(" ")[0]).split("-")[0]
		month = (data.split(" ")[0]).split("-")[1]
		day = (data.split(" ")[0]).split("-")[2]
		
		if (day[0]=="0"):
			day = day[1]
		if (month=="01"):
			month="Jan"
		elif (month=="02"):
			month="Feb"
		elif (month=="03"):
			month="Mar"
		elif (month=="04"):
			month="Apr"
		elif (month=="05"):
			month="May"
		elif (month=="06"):
			month="Jun"
		elif (month=="07"):
			month="Jul"
		elif (month=="08"):
			month="Aug"
		elif (month=="09"):
			month="Sep"
		elif (month=="10"):
			month="Oct"
		elif (month=="11"):
			month="Nov"
		elif (month=="12"):
			month="Dec"
    	
		build_date = month+" "+day+", "+year+" "+data.split(" ")[1]
		status["start_time"]=build_date

	#chamada feita
	nome_desfile = requests.get('http://172.18.0.6:8080/dashboard/event_parade_name?event='+id)
	if nome_desfile.status_code == 200:
		nome_desfile = nome_desfile.json()
		if nome_desfile == {}:
			nome_desfile = { "name": "Nome não definido" }
	else:
		nome_desfile = { "name" : "Nome não definido" }


	#chamada feita
	current_pos = requests.get('http://172.18.0.6:8080/dashboard/gps_coords?event='+id)
	if current_pos.status_code == 200:
		current_pos = current_pos.json()
		if current_pos == {}:
			current_pos = { "lat": 0,"lon": 0  }
	else:
		current_pos = { "lat": 0,"lon": 0 }


	values = {}
	values['artists']=artists
	values['about']=about
	values['forecast']=today_forecast
	values['activities']=act_to_send
	values['desfile']=status
	values['nome_desfile']=nome_desfile
	values['pos']=current_pos

	return TemplateResponse(request, template_name,values)

def entrance(request,template_name="entrance.html"):
	#chamada feita
	address = requests.get('http://172.18.0.6:8080/dashboard/event_address?event='+id)
	if address.status_code == 200:
		address = address.json()
		if address == {}:
			address = { "address": "Rua não definida" }
	else:
		address = { "address" : "Rua não definida" }


	#chamada feita
	schedule = requests.get('http://172.18.0.6:8080/dashboard/event_open_close?event='+id)
	if schedule.status_code == 200:
		schedule = schedule.json()
		if schedule == {}:
			schedule = { "open":0, "close":0 }
		else:
			schedule["open"] = schedule["open"].split(":")[0]+":"+schedule["open"].split(":")[1]
			schedule["close"] = schedule["close"].split(":")[0]+":"+schedule["close"].split(":")[1]
	else:
		schedule = { "open":0, "close":0 }

	

	#chamada feita
	#queue_entrance = { "Queue" : [100,10]} # "Queue" : [pessoas,tempo]
	queue_entrance = requests.get('http://172.18.0.6:8080/dashboard/queues?event='+id)
	if queue_entrance.status_code == 200:
		queue_entrance = queue_entrance.json()
		if queue_entrance == {}:
			queue_entrance = { "entrance":[0,0] }
	else:
		queue_entrance = { "entrance":[0,0] }
	
	queue_entrance_to_send = {}
	for place in queue_entrance:
		if(place=="entrance"):
			queue_entrance_to_send["Queue"] = queue_entrance["entrance"]
	if queue_entrance_to_send=={}:
		queue_entrance_to_send["Queue"] = ["error","error"]
	

	#chamada feita
	entrance_coords = requests.get('http://172.18.0.6:8080/dashboard/event_coords?event='+id)
	if entrance_coords.status_code == 200:
		entrance_coords = entrance_coords.json()
		if entrance_coords == {}:
			entrance_coords = { "entrance":[0,0] }
	else:
		entrance_coords = { "entrance":[0,0] }


	values = {}
	values['address'] = address
	values['schedule'] = schedule
	values['queue_entrance'] = queue_entrance_to_send
	values['entrance_coords'] = entrance_coords;

	return TemplateResponse(request, template_name,values)

def toilet(request,template_name="toilet.html"):
	#chamada feita
	toilets = requests.get('http://172.18.0.6:8080/dashboard/wcs_status?event='+id)
	if toilets.status_code == 200:
		toilets = toilets.json()
		if toilets == {}:
			toilets = { "dbEmpty": {"free":0,"full":0} }
	else:
		toilets = { "error_wcs": {"free":0,"full":0} }

	cores = {} 
	for wc in toilets:
		total = toilets[wc]["free"] + toilets[wc]["full"]
		if (total!=0):
			percentagem = toilets[wc]["free"]/total
		else:
			percentagem = 0 
		percentagem = percentagem * 100 

		if percentagem>=0 and percentagem<=25:
			cores[wc] = "red"
		elif percentagem>25 and percentagem<=50:
			cores[wc] = "orange"
		elif percentagem>50 and percentagem<=75:
			cores[wc] = "yellow"
		elif percentagem>75 and percentagem<=100:
			cores[wc] = "green"

	#chamada feita
	localizacao_wcs = requests.get('http://172.18.0.6:8080/dashboard/wcs_loc?event='+id)
	if localizacao_wcs.status_code == 200:
		localizacao_wcs = localizacao_wcs.json()
		if localizacao_wcs == {}:
			localizacao_wcs = { "dbEmpty": [0,0] }
	else:
		localizacao_wcs = { "error_wcs_loc": [0,0] }
	
	#feito
	#queue_wc = { "wc1": [8,9],"wc2": [5,4],"wc": [0,0] }
	queue_wc= requests.get('http://172.18.0.6:8080/dashboard/queues?event='+id)
	if queue_wc.status_code == 200:
		queue_wc = queue_wc.json()
		if queue_wc == {}:
			queue_wc = { "wcs":[0,0] }
	else:
		queue_wc = { "wcs":[0,0] }
	
	queue_wc_to_send = {}
	for wc in queue_wc:
		if(wc=="wcs"):
			queue_wc_to_send["Queue"] = queue_wc["wcs"]
	if queue_wc_to_send=={}:
		queue_wc_to_send["Queue"] = ["error","error"]
	
	values = {'wcs':json.dumps(toilets), 'cores':cores, 'localizacao':json.dumps(localizacao_wcs),'queue': json.dumps(queue_wc_to_send)}

	return TemplateResponse(request, template_name, values)

def parking(request,template_name="parking.html"):
	
	#chamada feita
	parking = requests.get('http://172.18.0.6:8080/dashboard/parks?event='+id)
	if parking.status_code == 200:
		parking = parking.json()
		if parking == {}:
			parking = { "dbEmpty": {"free":0,"full":0} }
	else:
		parking = { "error_parking": {"free":0,"full":0} }
	cores = {} 

	for park in parking:
		total = parking[park]["free"] + parking[park]["full"]
		if (total!=0):
			percentagem = parking[park]["free"]/total
		else:
			percentagem = 0 
		percentagem = percentagem * 100 

		if percentagem>=0 and percentagem<=25:
			cores[park] = "red"
		elif percentagem>25 and percentagem<=50:
			cores[park] = "orange"
		elif percentagem>50 and percentagem<=75:
			cores[park] = "yellow"
		elif percentagem>75 and percentagem<=100:
			cores[park] = "green"
	
	#chamada feita
	localizacao_parques = requests.get('http://172.18.0.6:8080/dashboard/parks_loc?event='+id)
	if localizacao_parques.status_code == 200:
		localizacao_parques = localizacao_parques.json()
		if localizacao_parques == {}:
			localizacao_parques = { "dbEmpty": {"free":0,"full":0} }
	else:
		localizacao_parques = { "error_parking": {"free":0,"full":0} }
	

	values = {'parques':json.dumps(parking),'cores':cores, 'localizacao':json.dumps(localizacao_parques)}

	return TemplateResponse(request, template_name, values)

def stages(request, template_name="stages.html"):
	#chamada feita
	img = requests.get('http://172.18.0.6:8080/dashboard/artists_photo?event='+id)
	if img.status_code == 200:
		img = img.json()
		if img == {}:
			img =  { "Error":"static/img/err.png" }
	else:
		img = { "Error":"static/img/err.png" }
	

	#chamada feita
	stages = requests.get('http://172.18.0.6:8080/dashboard/stages_artists?event='+id)
	if stages.status_code == 200:
		stages = stages.json()
		if stages == {}:
			stages = { "Erro":["Erro","Erro","Erro"] }
	else:
		stages = { "Erro":["Erro","Erro","Erro"] }


	#chamada feita
	coords = requests.get('http://172.18.0.6:8080/dashboard/stages_loc?event='+id)
	if coords.status_code == 200:
		coords = coords.json()
		if coords == {}:
			coords = { "dbEmpty":[0,0] }
	else:
		coordss = { "error_stages_loc": [0,0] }


	values = {}
	values['stages']=stages
	values['coords']=coords
	values['img']=img

	return TemplateResponse(request, template_name, values)
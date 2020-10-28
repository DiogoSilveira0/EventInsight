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

def home(request,template_name="base_generic.html"):

    values = {}
    '''
    People part 
    '''
    people = requests.get('http://172.18.0.6:8080/dashboard/people?event='+id)

    if people.status_code == 200:
        people = people.json()
        if people == {}:
            people = {"dbEmpty":0}
    else:
        people = { "error_people": 0 }

    '''
    total = 0 #chamar a api
    '''
    total = requests.get('http://172.18.0.6:8080/dashboard/ttl_people?event='+id)
    if total.status_code == 200:
        total = total.json()
        if total == {}:
            total = 0
        else:
            total = total["total_people"]
    else:
        total = "error_total"

    '''
    at_moment = {"Entrance": 20001,"WC": 20002 , "Palco 1": 20003} #chamar a api
    '''
    at_moment = requests.get('http://172.18.0.6:8080/dashboard/current_people?event='+id)

    if at_moment.status_code == 200:
        at_moment = at_moment.json()
        if at_moment == {}:
            at_moment = { "dbEmpty" : 0}
    else:
        at_moment = { "error_at_moment": 0 }
    

    zone_more = ""
    zone_less = ""
    bigger = 0
    lower = 0

    keys = []
    for i in at_moment:
        keys.append(i)
    
    zone_more = keys[0]
    zone_less = keys[0]
    bigger = at_moment[keys[0]]
    lower = at_moment[keys[0]]
    
    for j in at_moment:
        if at_moment[j]>bigger:
            bigger = at_moment[j]
            zone_more = j
        elif at_moment[j]<lower:
            lower = at_moment[j]
            zone_less = j
        else:
            if not j in zone_more and not j in zone_less:
                zone_more += "," + j
                zone_less += "," + j
    values['total_participants'] = total
    values['more'] = zone_more
    values['less'] = zone_less
    values['atm'] = at_moment
    

    '''
    Filas Part 
    '''
    
    queue = requests.get('http://172.18.0.6:8080/dashboard/queues?event='+id)
    if queue.status_code == 200:
        queue = queue.json()
        if queue == {}:
            queue = {"dbEmpty":[0,0]}
    else:
        queue = { "error_queue": [0,0] }
    
    colors = {}
    for spot in queue:
        if spot == "error_queue":
            colors[spot]="red"
        elif queue[spot][0]!=0:
            colors[spot]="red"
        else:
            colors[spot]="green"
    
    values['queues_colors']=colors

    '''
    Parques Part
    '''

    parking = requests.get('http://172.18.0.6:8080/dashboard/parks?event='+id)
    if parking.status_code == 200:
        parking = parking.json()
        if parking == {}:
            parking =  {"dbEmpty" : {"free":0,"full":0} }
    else:
        parking = { "error_parking": {"free":0,"full":0} }
    
    colors = {} 
    for park in parking:
        total = parking[park]["free"] + parking[park]["full"]
        if (total!=0):
            percentagem = parking[park]["free"]/total
        else:
            percentagem = 0 
        percentagem = percentagem * 100 #%

        if percentagem>=0 and percentagem<=25:
            colors[park] = "red"
        elif percentagem>25 and percentagem<=50:
            colors[park] = "orange"
        elif percentagem>50 and percentagem<=75:
            colors[park] = "yellow"
        elif percentagem>75 and percentagem<=100:
            colors[park] = "green"

    values['parking_colors'] = colors

    '''
    Sales Part
    '''

    total_today = requests.get('http://172.18.0.6:8080/dashboard/sum_sells_today?event='+id)
    if total_today.status_code == 200:
        total_today = total_today.json()
        if total_today == {}:
            total_today = {"dbEmpty" : 0 }
    else:
        total_today = { "total_today_error": 0 }

    values["total_sales_today"] = total_today


    '''
    Activities Part
    '''

    activities = requests.get('http://172.18.0.6:8080/dashboard/activities_status?event='+id)
    if activities.status_code == 200:
        activities = activities.json()
        if activities == {}:
            activities = { 'dbEmpty': { 'empty_activities':{"status":"empty"} } }
    else:
        activities = {
            'error': {
                "error_activities":{"status":"error"} }
        }
    
    events_to_evaluate = {}
    possible_late = ["on","late5","late10","late20","latePlus20"]
    ctr =0
    for stage in activities:
        aux = activities[stage]
        for show in aux:
            if aux[show]in possible_late:
                if aux[show]== "on":
                    events_to_evaluate[stage] = show + "-" + "verde"
                if aux[show] == "late5":
                    events_to_evaluate[stage] = show +"-"+"verde"
                elif aux[show] == "late10":
                    events_to_evaluate[stage] = show +"-"+"amarelo"
                elif aux[show]== "late20":
                    events_to_evaluate[stage] = show +"-"+"laranja"
                elif aux[show]== "latePlus20":
                    ctr+=1
                    events_to_evaluate[stage] = show +"-"+"vermelho"
    
    values['on_stage'] = events_to_evaluate

    if request.user.is_authenticated and request.user.is_superuser:
        values['user'] = request.user
        return TemplateResponse(request, template_name, values)
    elif request.user.is_authenticated and not request.user.is_superuser:
        values['user'] = request.user
        return TemplateResponse(request, "base_generic_common.html", values)
    return TemplateResponse(request, "error.html")

def people(request, template_name="people.html"):    
    
    people = requests.get('http://172.18.0.6:8080/dashboard/people?event='+id)
    if people.status_code == 200:
        people = people.json()
        if people == {}:
            people = {"dbEmpty":0}
    else:
        people = { "error_people": 0 }
    

    '''
    total = 0 #chamar a api
    '''
    total = requests.get('http://172.18.0.6:8080/dashboard/ttl_people?event='+id)
    if total.status_code == 200:
        total = total.json()
        if total == {}:
            total = 0
        else:
            total = total["total_people"]
    else:
        total = "error_total"
    

    '''
    at_moment = {"Entrance": 20001,"WC": 20002 , "Palco 1": 20003} #chamar a api
    '''
    at_moment = requests.get('http://172.18.0.6:8080/dashboard/current_people?event='+id)
    if at_moment.status_code == 200:
        at_moment = at_moment.json()
        if at_moment == {}:
            at_moment = { "dbEmpty":0 }
    else:
        at_moment = { "error_at_moment": 0 }


    zone_more = ""
    zone_less = ""
    bigger = 0
    lower = 0

    keys = []
    for i in at_moment:
        keys.append(i)
    
    zone_more = keys[0]
    zone_less = keys[0]
    bigger = at_moment[keys[0]]
    lower = at_moment[keys[0]]
    
    for j in at_moment:
        if at_moment[j]>bigger:
            bigger = at_moment[j]
            zone_more = j
        elif at_moment[j]<lower:
            lower = at_moment[j]
            zone_less = j
        else:
            if not j in zone_more and not j in zone_less:
                zone_more += "," + j
                zone_less += "," + j

    values = {'participants':json.dumps(people),'total_participants': total , 'more':zone_more, 'less':zone_less, 'atm':at_moment} 
    
    if request.user.is_authenticated and request.user.is_superuser:
        values['user'] = request.user
        return TemplateResponse(request, template_name, values)
    elif request.user.is_authenticated and not request.user.is_superuser:
        values['user'] = request.user
        return TemplateResponse(request, "people_common.html", values)
    else:
        return TemplateResponse(request, "error.html")

def parking(request, template_name="parking.html"):
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

    values = {'parques':json.dumps(parking),'cores':cores}
    
    if request.user.is_authenticated and request.user.is_superuser:
        values['user'] = request.user
        return TemplateResponse(request, template_name, values)
    elif request.user.is_authenticated and not request.user.is_superuser:
        values['user'] = request.user
        return TemplateResponse(request, "parking_common.html", values)
    else:
        return TemplateResponse(request, "error.html")

def meteorology(request, template_name="meteorology.html"):
    forecast = requests.get('http://172.18.0.6:8080/dashboard/meteo?event='+id)
    
    if forecast.status_code == 200:
        forecast = forecast.json()
        if forecast == {}:
            forecast = {
                "temp_max": { "1970-00-00":0} , 
                "temp_min": { "1970-00-00":0} , 
                "prec" : { "1970-00-00":0} , 
                "wind_scale": { "1970-00-00":0 } 
                }
    else:
        forecast = {
        "temp_max": { "1970-00-00":0} , 
        "temp_min": { "1970-00-00":0} , 
        "prec" : { "1970-00-00":0} , 
        "wind_scale": { "1970-00-00":0 } 
        }

    x = str(datetime.datetime.now()).split(" ")
    hoje = x[0]
    

    values = {'temp_max':json.dumps(forecast["temp_max"]),
    'temp_min':json.dumps(forecast["temp_min"]),
    'prec':json.dumps(forecast["prec"]) ,
    'wind_scale':json.dumps(forecast["wind_scale"]),
    'hoje':hoje}

    if request.user.is_authenticated and request.user.is_superuser:
        values['user'] = request.user
        return TemplateResponse(request, template_name, values)
    elif request.user.is_authenticated and not request.user.is_superuser:
        values['user'] = request.user
        return TemplateResponse(request, "meteorology_common.html", values)
    else:
        return TemplateResponse(request, "error.html")

def sales(request, template_name="sales.html"):
    sales = requests.get('http://172.18.0.6:8080/dashboard/sells?event='+id)
    if sales.status_code == 200:
        sales = sales.json()
        if sales == {}:
            sales = { 'dbEmpty' : { "1970-00-00":0} }
    else:
        sales = { 'Error': { "1970-00-00":0} }
    
    #chamar api
    total_today = requests.get('http://172.18.0.6:8080/dashboard/sum_sells_today?event='+id)
    if total_today.status_code == 200:
        total_today = total_today.json()
        if total_today =={}:
            total_today = {"error_today_error":0}
    else:
        total_today = {"error_today_error":0}
    

    #chamar api
    total_event = requests.get('http://172.18.0.6:8080/dashboard/sum_sells_event?event='+id)
    if total_event.status_code == 200:
        total_event = total_event.json()
        if total_event == {}:
            total_event = {"error_event_error":0}
    else:
        total_event = {"error_event_error":0}

    #chamar api
    compare = requests.get('http://172.18.0.6:8080/dashboard/compare_sells?event='+id)
    if compare.status_code == 200:
        compare = compare.json()
        if compare == {}:
            compare = {"error_compare": [0,0] }
    else:
        compare = {"error_compare": [0,0] }

    values = {'sales': json.dumps(sales) ,'total_today': json.dumps(total_today),'total_event':json.dumps(total_event),'compare':json.dumps(compare)}
    
    if request.user.is_authenticated and request.user.is_superuser:
        values['user'] = request.user
        return TemplateResponse(request, template_name, values)
    elif request.user.is_authenticated and not request.user.is_superuser:
        values['user'] = request.user
        return TemplateResponse(request, "sales_common.html", values)
    else:
        return TemplateResponse(request, "error.html")

def gps(request, template_name="gps.html"):
    #chamar api
    coordinates  = requests.get('http://172.18.0.6:8080/dashboard/gps_coords?event='+id)

    if coordinates.status_code == 200:
        coordinates = coordinates.json()
        if coordinates == {}:
            coordinates = { "lat": "error", "lon": "error"}
    else: 
        coordinates = { "lat": "error", "lon": "error"}
    
    #chamar api
    path = requests.get('http://172.18.0.6:8080/dashboard/route?event='+id)
    
    if path.status_code == 200:
        path = path.json()
        if coordinates == {}:
            path = { "erro":"erro"}
    else:
        path = { "erro":"erro"}

    

    ######################################## FALTA ##############################################
    #Chamar API
    # 1 - Ainda não começou
    # 2 - A decorrer
    # 3 - Terminado 

    #Exemplos
    #status = {"current":1, "start_time": "Jan 5, 2021 15:37:25"} #-> Começa às 15h 37m e 25s do dia 5 de Janeiro de 2021
    #status = {"current":2, "time_passed": "10:12:30" , "moving": "True"} # -> Tempo desde que começou || Ou está em andamento ou parado (True, False)
    #status = {"current":3 , "stop_points": [ [0,0,1], [1,1,2], [2,2,3] ] } #-> Já terminou

    #status = {"current":1, "start_time": "Jan 5, 2021 15:37:25" }
    
    ##TEM QUE SER ASSIM -> COM ASPAS
    #status = {"current": 2,"time_passed": "20:00:00", "moving": "True"}
    
    #month_names_short: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # status = {"current": 1, "start_time": "2020-06-01 16:00:00" } #Testei com este. com datas que já passaram o output é "EXPIRED"

    
    
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
    


    values = {'coordinates':json.dumps(coordinates),'path':path, 'status':status}
    
    if request.user.is_authenticated and request.user.is_superuser:
        values['user'] = request.user
        return TemplateResponse(request, template_name, values)
    elif request.user.is_authenticated and not request.user.is_superuser:
        values['user'] = request.user
        return TemplateResponse(request, "gps_common.html", values)
    else:
        return TemplateResponse(request, "error.html")

def activities(request, template_name="activities.html"):
    #chamar a api
    activities = requests.get('http://172.18.0.6:8080/dashboard/activities_status?event='+id)
    
    if activities.status_code == 200:
        activities = activities.json()
        if activities == {}:
            activities = { 'dbEmpty': { 'empty_activities':{"status":"empty"} } }
    else:
        activities = {
            'error': {
                "error_activities":{"status":"error"} }
        }

    events_to_evaluate = {}
    possible_late = ["on","late5","late10","late20","latePlus20"]

    for stage in activities:
        aux = activities[stage]
        for show in aux:
            if aux[show] in possible_late:
                if aux[show] == "on":
                    events_to_evaluate[stage] = show + "-" + "verde"
                if aux[show]== "late5":
                    events_to_evaluate[stage] = show +"-"+"verde"
                elif aux[show] == "late10":
                    events_to_evaluate[stage] = show +"-"+"amarelo"
                elif aux[show]== "late20":
                    events_to_evaluate[stage] = show +"-"+"laranja"
                elif aux[show] == "latePlus20":
                    events_to_evaluate[stage] = show +"-"+"vermelho"
            

    event_history = requests.get('http://172.18.0.6:8080/dashboard/event_history?event='+id)
    
    if event_history.status_code == 200:
        event_history = event_history.json()
        if event_history == {}:
            event_history = { 'error': ["0","0","0"] }
    else:
        event_history = { 'error': ["0","0","0"] }
    
    '''

    today_plan = {
    "Carolina Deslandes": [
        "21-00-00",
        "Palco MEO"
    ],
    "Xutos & Pontapes": [
        "21-00-00",
        "Palco Vodafone"
    ],
    "Italo Brothers": [
        "22-00-00",
        "Palco Vodafone"
    ],
    "Vini Vici": [
        "22-00-00",
        "Palco MEO"
    ],
    "Quim das Remisturas": [
        "23-00-00",
        "Palco MEO"
    ],
    "Ornatos Violeta": [
        "23-00-00",
        "Palco Vodafone"
    ],
    "Mundo Segundo": [
        "23-30-00",
        "Palco Vodafone"
    ]
}
    '''
    today_plan = requests.get('http://172.18.0.6:8080/dashboard/today_plan?event='+id)
    
    if today_plan.status_code == 200:
        today_plan = today_plan.json()
        if today_plan == {}:
            today_plan = { 'dbEmpty': ["0","0"] }
    else:
        today_plan = { 'error': ["0","0"] }
    

    values =  {'events_to_evaluate':json.dumps(events_to_evaluate) , 'event_history':json.dumps(event_history) , 'today_plan':today_plan}

    if request.user.is_authenticated and request.user.is_superuser:
        values['user'] = request.user
        return TemplateResponse(request, template_name, values)
    elif request.user.is_authenticated and not request.user.is_superuser:
        values['user'] = request.user
        return TemplateResponse(request, "activities_common.html", values)
    else:
        return TemplateResponse(request, "error.html")

def wcs(request,template_name="wcs.html"):
    #chamar api
    toilets = requests.get('http://172.18.0.6:8080/dashboard/wcs_status?event='+id)
    print("-----")
    print(toilets.status_code)
    if toilets.status_code == 200:
        toilets = toilets.json()
        if toilets == {}:
            toilets = { 'dbEmpty': {'free': 0, 'full': 0} }

    #json to send
    wcs = {}
    for wc in toilets:
        wcs[wc] = [toilets[wc]["full"],toilets[wc]["free"]]

    cores = {} 

    for wc in wcs:
        total = wcs[wc][0]+wcs[wc][1]

        if (total!=0):
            percentagem = wcs[wc][0]/total
        else:
            percentagem = 0 
        percentagem = percentagem * 100 
        
        if percentagem<=50:
            cores[wc] = "green"
        elif percentagem>50 and percentagem<=70:
            cores[wc] = "yellow"
        elif percentagem>70 and percentagem<=85:
            cores[wc] = "orange"
        else:
            cores[wc] = "red"

    values = {"wcs": json.dumps(wcs),"cores": json.dumps(cores)}
    return TemplateResponse(request,template_name,values)


def queue(request,template_name="queue.html"):
    queue = requests.get('http://172.18.0.6:8080/dashboard/queues?event='+id)
    if queue.status_code == 200:
        queue = queue.json()
        if queue == {}:
            queue = { "Error": [0,0] }
    else:
        queue = { "Error": [0,0] }
    
    values = {"queue": json.dumps(queue)}
    if request.user.is_authenticated and request.user.is_superuser:
        values['user'] = request.user
        return TemplateResponse(request, template_name, values)
    elif request.user.is_authenticated and not request.user.is_superuser:
        values['user'] = request.user
        return TemplateResponse(request, "queue_common.html", values)
    else:
        return TemplateResponse(request, "error.html")
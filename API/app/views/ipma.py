import requests
import time
from datetime import date
from urllib.request import urlopen


def build_cities_code():
    '''
    O IPMA associa a cada distrito/ilhas um ID
    Por exemplo: Aveiro corresponde ao ID 1010500
    É necessário construir um dicionário com os IDs de todos os distritos e ilhas 
    '''

    #Chamada à API através do URL que retorna todos os distritos/ilhas e respectivos IDs
    text = requests.get("https://api.ipma.pt/open-data/distrits-islands.json").json()
    data = text['data']

    cities_code = {}
    ctr=0

    #Percorrer o dicionário retornado e guardar no dicionário cities_codes, na forma distrito=ID
    while ctr<len(data):
        cities_code[data[ctr]['local'].lower()]=data[ctr]['globalIdLocal']
        ctr+=1
    return cities_code

def get_forecast_by_code(city_code):
    '''
    Previsão para os próximos 5 dias (contando com o dia em que é executado)
    O que nos interessa é a previsão para o dia de hoje
    '''

    #Chamada à API através do URL que tornar a previsão meteorológica para os próximos 5 dias
    url_forecast = "https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/"+ str(city_code) +".json"
    text = requests.get(url_forecast).json()

    data = {
        "temp_max": {},
        "temp_min": {},
        "prec": {},
        "wind_scale":{}
    }

    for item in text['data']: 
        item['forecastDate'] = item['forecastDate'].split("-")
        item['forecastDate'][1] = str(int(item['forecastDate'][1]) - 1)
        item['forecastDate'] = "-".join(item['forecastDate'])
        data["temp_max"][item['forecastDate']] = item['tMax']
        data["temp_min"][item['forecastDate']] = item['tMin']
        data["prec"][item['forecastDate']] = item['precipitaProb']
        data["wind_scale"][item['forecastDate']] = item['classWindSpeed']

    return data

def get_forecast_by_code_single_day(city_code):
    '''
    Previsão para os próximos 5 dias (contando com o dia em que é executado)
    O que nos interessa é a previsão para o dia de hoje
    '''

    #Chamada à API através do URL que tornar a previsão meteorológica para os próximos 5 dias
    url_forecast = "https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/"+ str(city_code) +".json"
    text = requests.get(url_forecast).json()

    data = {}

    item = text['data'][1]
    data["t_max"] = item['tMax']
    data["t_min"] = item['tMin']
    data["prob_rain"] = item['precipitaProb']
    data["wind"] = item['classWindSpeed']

    return data

def get(city):
    '''
    Vamos ter de definir a cidade conforme o evento em que o projecto está a ser utilizado.
    Neste caso definimos "Porto" para efeitos de teste.
    Só são suportadas cidades Portuguesas.
    '''
    cities_code = build_cities_code()
    city_code = cities_code[city.lower()]
    
    #Chamada à API para obter: Temperatura mínima e máxima, probabilidade de precipitação
    return get_forecast_by_code(city_code)

def get_today(city):
    '''
    Vamos ter de definir a cidade conforme o evento em que o projecto está a ser utilizado.
    Neste caso definimos "Porto" para efeitos de teste.
    Só são suportadas cidades Portuguesas.
    '''
    cities_code = build_cities_code()
    city_code = cities_code[city.lower()]
    
    #Chamada à API para obter: Temperatura mínima e máxima, probabilidade de precipitação
    return get_forecast_by_code_single_day(city_code)

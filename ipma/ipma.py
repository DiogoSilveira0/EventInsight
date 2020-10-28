import requests
import time
import sys
import geocoder
from datetime import date
from urllib.request import urlopen


def get_city_by_lat_long():
    g = geocoder.ip('me') #Irá retornar Porto
    lat = g.latlng[0]
    lon = g.latlng[1]
    

    api_key = "2a2d8f06b0b34d039f9540481fcf99a0" #API OPEN CAGE KEY

    url = "https://api.opencagedata.com/geocode/v1/json?key="+api_key+"&q=" +str(lat) +"%2C"+str(lon)
    text = requests.get(url).json()
    
    #Obter o distrito 
    city = text['results'][0]['components']['county']
    
    return city

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

    temp_min=""
    temp_max=""
    prob_rain=""
    windSpeed=""

    for item in text['data']: 
        print("Data: "+ str(item['forecastDate']))
        print("Temperatura mínima: "+ str(item['tMin']))
        print("Temperatura máxima: "+ str(item['tMax']))
        print("Probabilidade de precipitação: "+ str(item['precipitaProb']))
        print("Velocidade do evento: "+ str(item['classWindSpeed']))
        print("-----")

def main():
    '''
    Vamos ter de definir a cidade conforme o evento em que o projecto está a ser utilizado.
    Neste caso definimos "Porto" para efeitos de teste.
    Só são suportadas cidades Portuguesas.
    '''
    cities_code = build_cities_code()
    city = "Matosinhos"
    city_code = cities_code[city.lower()]
    
    
    #Chamada à API para obter: Temperatura mínima e máxima, probabilidade de precipitação
    print('CITY NAME')
    get_forecast_by_code(city_code)

    '''
    Neste caso, obtemos a latitude e longitude do computador que executa o código e
    através da API OPENCAGE conseguimos obter a localização.
    '''
    city = get_city_by_lat_long() #Retorna a cidade 
    city_code = cities_code[city.lower()] #Retorna o ID 
    
    #Chamada à API para obter: Temperatura mínima e máxima, probabilidade de precipitação
    print("-----")
    print('LAT & LONG')
    get_forecast_by_code(city_code)
    print("-----")
    
    
if __name__ == "__main__":
    while True:
        main()
        time.sleep(20)
        #time.sleep(3600) #De hora a hora 


import requests
import json
import time
import datetime

def compare_cities(city1, city2):
    key = '986b86d5d24bbace34084b1fcda169bd'
    direct_geocoding_api_url1 = f"http://api.openweathermap.org/geo/1.0/direct?q={city1}&limit={1}&appid={key}"
    direct_geocoding_api_url2 = f"http://api.openweathermap.org/geo/1.0/direct?q={city2}&limit={1}&appid={key}"

    response1 = requests.get(direct_geocoding_api_url1)
    response_body1 = response1.text
    response_body_json1 = json.loads(response_body1)

    response2 = requests.get(direct_geocoding_api_url2)
    response_body2 = response2.text
    response_body_json2 = json.loads(response_body2)

    city_geocoding_table1 = []
    city_geocoding_table2 = []

    lat1 = response_body_json1[0]["lat"]
    city_geocoding_table1.append(lat1)
    lon1 = response_body_json1[0]["lon"]
    city_geocoding_table1.append(lon1)
    
    lat2 = response_body_json2[0]["lat"]
    city_geocoding_table2.append(lat2)
    lon2 = response_body_json2[0]["lon"]
    city_geocoding_table2.append(lon2)

    return city_geocoding_table1, city_geocoding_table2


print(compare_cities("New York", "Los Angeles"))

def get_weather(city):
    key = '986b86d5d24bbace34084b1fcda169bd'

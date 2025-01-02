import requests
import json
from CountriesDictionary import country_domain_codes as cdc

# loading the air pollution elements ant their quantity based on latitude and longitude
def load_pollution_gps_code(lat, lon):
    key = '986b86d5d24bbace34084b1fcda169bd'
    air_pollution_api_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={key}'
    response = requests.get(air_pollution_api_url)
    response_body = response.text
    response_body_json = json.loads(response_body)

    air_pollution_table = []

    air_co = float(response_body_json["list"][0]["components"]["co"])
    air_pollution_table.append(air_co)

    air_no = float(response_body_json["list"][0]["components"]["no"])
    air_pollution_table.append(air_no)

    air_no2 = float(response_body_json["list"][0]["components"]["no2"])
    air_pollution_table.append(air_no2)

    air_o3 = float(response_body_json["list"][0]["components"]["o3"])
    air_pollution_table.append(air_o3)

    air_so2 = float(response_body_json["list"][0]["components"]["so2"])
    air_pollution_table.append(air_so2)

    air_pm2_5 = float(response_body_json["list"][0]["components"]["pm2_5"])
    air_pollution_table.append(air_pm2_5)

    air_pm10 = float(response_body_json["list"][0]["components"]["pm10"])
    air_pollution_table.append(air_pm10)

    air_nh3 = float(response_body_json["list"][0]["components"]["nh3"])
    air_pollution_table.append(air_nh3)

    return air_pollution_table

# converting latitude and longitude to country and city name
def convert_gps_to_city(lat, lon):
    key = '986b86d5d24bbace34084b1fcda169bd'
    geocoding_api_url = f'http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit={5}&appid={key}'
    response = requests.get(geocoding_api_url)
    response_body = response.text
    response_body_json = json.loads(response_body)

    city_geocoding_table = []

    city_geocoding_name = response_body_json[0]["name"]
    city_geocoding_table.append(city_geocoding_name)

    city_geocoding_country = response_body_json[0]["country"]

    geocoded_country = ""
    for key, value in cdc.items():
        if key == city_geocoding_country:
            geocoded_country = value
            break
        else:
            geocoded_country = "No country found!"

    city_geocoding_table.append(geocoded_country)

    return city_geocoding_table


# Testing the code (For Poznan - Poland)
t = convert_gps_to_city(52.4053, 16.9294)
print(t)





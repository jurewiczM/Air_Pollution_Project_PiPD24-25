import requests
import json
from CountriesDictionary import country_domain_codes as cdc

# wczytywanie danych o zanieczyszczeniu powietrza z ostatniego tygodnia z godzinnym odstępem (7 dni x 24h = 168h)
def load_historical_data_1WeekBefore(lat, lon, start):
    key = '986b86d5d24bbace34084b1fcda169bd'
    historical_data = []


    for i in range(0, 7 * 24):  # 7 dni * 24 godzin
        hour_start = start - (i * 3600)
        hour_end = hour_start

        historical_api_url = f'http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={hour_start}&end={hour_end}&appid={key}'

        response = requests.get(historical_api_url)


        response_body_json = json.loads(response.text)
        historical_data.extend(response_body_json.get("list", []))


    historical_data_table = []
    for data_point in historical_data:
        components = data_point["components"]
        historical_data_table.append({
            "timestamp": data_point.get("dt", 0),
            "so2": components.get("so2", 0.0),
            "no2": components.get("no2", 0.0),
            "pm10": components.get("pm10", 0.0),
            "pm2_5": components.get("pm2_5", 0.0),
            "o3": components.get("o3", 0.0),
            "co": components.get("co", 0.0),
            "nh3": components.get("nh3", 0.0),
            "no": components.get("no", 0.0)
        })

    return historical_data_table

# wczytywanie danych o zanieczysczeniu powietrza z ostatniej doby
def load_historical_data_24hwindow(lat, lon, end):
    key = '986b86d5d24bbace34084b1fcda169bd'
    historical_data = []

    day_end = end
    day_start = day_end - 3600 * 24

    historical_api_url = f'http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={day_start}&end={day_end}&appid={key}'

    response = requests.get(historical_api_url)

    response_body_json = json.loads(response.text)
    historical_data.extend(response_body_json.get("list", []))

    historical_data_table = []
    for data_point in historical_data:
        components = data_point["components"]
        historical_data_table.append({
            "timestamp": data_point.get("dt", 0),
            "so2": components.get("so2", 0.0),
            "no2": components.get("no2", 0.0),
            "pm10": components.get("pm10", 0.0),
            "pm2_5": components.get("pm2_5", 0.0),
            "o3": components.get("o3", 0.0),
            "co": components.get("co", 0.0),
            "nh3": components.get("nh3", 0.0),
            "no": components.get("no", 0.0)
        })

    return historical_data_table

# wczytywanie obecnych danych o zanieczysczeniu powietrza (na podstawie koordynatów GPS)
def load_pollution_gps_code(lat, lon):
    key = '986b86d5d24bbace34084b1fcda169bd'

    air_pollution_api_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={key}'
    response = requests.get(air_pollution_api_url)
    response_body = response.text
    response_body_json = json.loads(response_body)

    air_pollution_table = []

    air_so2 = float(response_body_json["list"][0]["components"]["so2"])
    air_pollution_table.append(air_so2)

    air_no2 = float(response_body_json["list"][0]["components"]["no2"])
    air_pollution_table.append(air_no2)

    air_pm10 = float(response_body_json["list"][0]["components"]["pm10"])
    air_pollution_table.append(air_pm10)

    air_pm2_5 = float(response_body_json["list"][0]["components"]["pm2_5"])
    air_pollution_table.append(air_pm2_5)

    air_o3 = float(response_body_json["list"][0]["components"]["o3"])
    air_pollution_table.append(air_o3)

    air_co = float(response_body_json["list"][0]["components"]["co"])
    air_pollution_table.append(air_co)

    air_nh3 = float(response_body_json["list"][0]["components"]["nh3"])
    air_pollution_table.append(air_nh3)

    air_no = float(response_body_json["list"][0]["components"]["no"])
    air_pollution_table.append(air_no)

    return air_pollution_table

# konwersja koordynatów GPS do miasta (i innych danych)
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

# kowersja nazwy miasta to koordynatów geograficznych (i innych danych)
def convert_city_to_gps(city_name):
    key = '986b86d5d24bbace34084b1fcda169bd'
    direct_geocoding_api_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={1}&appid={key}"

    response = requests.get(direct_geocoding_api_url)
    response_body = response.text
    response_body_json = json.loads(response_body)

    city_geocoding_table = []

    lat = response_body_json[0]["lat"]
    city_geocoding_table.append(lat)
    lon = response_body_json[0]["lon"]
    city_geocoding_table.append(lon)
    country = response_body_json[0]["country"]


    geocoded_country = ""
    for key, value in cdc.items():
        if key == country:
            geocoded_country = value
            break
        else:
            geocoded_country = "No country found!"

    city_geocoding_table.append(geocoded_country)
    return city_geocoding_table

# pobieranie AQI (Air Quality Index)
def get_air_quality_index(lat, lon):
    key = '986b86d5d24bbace34084b1fcda169bd'

    air_pollution_api_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={key}'
    response = requests.get(air_pollution_api_url)
    response_body = response.text
    response_body_json = json.loads(response_body)

    air_quality_index = response_body_json["list"][0]["main"]["aqi"]

    return air_quality_index

# pobieranie kategorii AQI (Air Quality Index Category)
def get_air_quality_index_category_name(lat, lon):
    air_quality_index = get_air_quality_index(lat, lon)

    index_quantitive_name = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor",
    }

    air_quality_quantitive_name = ""
    for key, value in index_quantitive_name.items():
        if air_quality_index == key:
            air_quality_quantitive_name = value
            break
        else:
            air_quality_quantitive_name = "No index found!"

    return air_quality_quantitive_name

# przypisanie wartościom zanieczyszczeń odpowiednich kategorii
def get_air_pollutant_category(value, limits):
    categories = ['Good', 'Fair', 'Moderate', 'Poor', 'Very Poor']
    if value > limits[5]:
        value = limits[5] - 10
    for i in range(len(limits) - 1):
        if limits[i] <= value < limits[i + 1]:
            return categories[i]
    return 'Unknown'

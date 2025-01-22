import requests
import json
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CountriesDictionary import country_domain_codes as cdc
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime, timezone
from regression import get_air_quality_prediction
from PIL import Image, ImageTk


def load_historical_data_1WeekBefore(lat, lon, start):
    key = '986b86d5d24bbace34084b1fcda169bd'
    historical_data = []

    # Generate hourly timestamps for the 7 days between `start` and `end`
    for i in range(0, 7 * 24):  # 7 days * 24 hours
        hour_start = start - (i * 3600)  # Subtract i hours from start
        hour_end = hour_start # End of the hour

        historical_api_url = f'http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={hour_start}&end={hour_end}&appid={key}'

        response = requests.get(historical_api_url)


        response_body_json = json.loads(response.text)
        historical_data.extend(response_body_json.get("list", []))

    # Process the historical data
    historical_data_table = []
    for data_point in historical_data:
        components = data_point["components"]
        historical_data_table.append({
            "timestamp": data_point.get("dt", 0),  # Include timestamp
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

def load_historical_data_24hwindow(lat, lon, end):
    key = '986b86d5d24bbace34084b1fcda169bd'
    historical_data = []

    day_end = end  # Start of the day
    day_start = day_end - 3600*24    # (6 hours later)
        
    historical_api_url = f'http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={day_start}&end={day_end}&appid={key}'
        
    response = requests.get(historical_api_url)

    response_body_json = json.loads(response.text)
    historical_data.extend(response_body_json.get("list", []))


    # Process the historical data
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

# loading the air pollution elements ant their quantity based on latitude and longitude
def load_pollution_gps_code(lat, lon):
    key = '986b86d5d24bbace34084b1fcda169bd'
    # key = 'api key'
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

# converting latitude and longitude to country and city name
def convert_gps_to_city(lat, lon):
    key = '986b86d5d24bbace34084b1fcda169bd'
    # key = 'api key'
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

# converting city names to their gps-cords
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

def get_air_quality_index(lat, lon):
    key = '986b86d5d24bbace34084b1fcda169bd'
    # key = 'api key'
    air_pollution_api_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={key}'
    response = requests.get(air_pollution_api_url)
    response_body = response.text
    response_body_json = json.loads(response_body)

    air_quality_index = response_body_json["list"][0]["main"]["aqi"]

    return air_quality_index

# getting air quality index and the qir quality category
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

# displaying ranges for air quality categories for every air pollutant
def display_treshhold_values():

    categories = ['Good', 'Fair', 'Moderate', 'Poor', 'Very Poor']
    pollutants = ['SO₂', 'NO₂', 'PM10', 'PM2.5', 'O₃']
    co_pollutant = ['CO']

    ranges = {
        'SO₂': [(0, 20), (20, 80), (80, 250), (250, 350), (350, 400)],
        'NO₂': [(0, 40), (40, 70), (70, 150), (150, 200), (200, 250)],
        'PM10': [(0, 20), (20, 50), (50, 100), (100, 200), (200, 250)],
        'PM2.5': [(0, 10), (10, 25), (25, 50), (50, 75), (75, 100)],
        'O₃': [(0, 60), (60, 100), (100, 140), (140, 180), (180, 200)]
    }

    co_range = [(0, 4400), (4400, 9400), (9400, 12400), (12400, 15400), (15400, 20000)]

    colors = ['#8BC34A', '#FFEB3B', '#FF9800', '#F44336', '#9C27B0']

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12), gridspec_kw={'height_ratios': [3, 1]})

    for i, (pollutant, intervals) in enumerate(ranges.items()):
        for j, (low, high) in enumerate(intervals):
            ax1.fill_betweenx(
                [i - 0.4, i + 0.4],
                low, high,
                color=colors[j],
                edgecolor='black'
            )
            ax1.text(
                (low + high) / 2,
                i,
                f"[{low}; {high}]",
                ha='center', va='center',
                fontsize=8,
                bbox=dict(facecolor='white', alpha=0.5, edgecolor='none')
            )

    ax1.set_yticks(range(len(pollutants)))
    ax1.set_yticklabels(pollutants)
    ax1.set_xlabel('Concentration (µg/m³)')
    ax1.set_title('Air Quality Index - Threshold Ranges for Pollutants (excluding CO)')

    for j, (low, high) in enumerate(co_range):
        ax2.fill_betweenx(
            [0.6, 1.4],
            low, high,
            color=colors[j],
            edgecolor='black'
        )
        ax2.text(
            (low + high) / 2,
            1,
            f"[{low}; {high}]",
            ha='center', va='center',
            fontsize=8,
            bbox=dict(facecolor='white', alpha=0.5, edgecolor='none')
        )

    ax2.set_yticks([1])
    ax2.set_yticklabels(['CO'])
    ax2.set_xlabel('Concentration (µg/m³)')
    ax2.set_title('Air Quality Index - Threshold Ranges for CO')

    legend_patches = [mpatches.Patch(color=colors[i], label=categories[i]) for i in range(len(categories))]
    fig.legend(handles=legend_patches, title='Air Quality', bbox_to_anchor=(1.05, 0.5), loc='center left')

    plt.tight_layout()
    #plt.show()

    return fig

def get_air_pollutant_category(value, limits):
    categories = ['Good', 'Fair', 'Moderate', 'Poor', 'Very Poor']
    if value > limits[5]:
        value = limits[5] - 10
    for i in range(len(limits) - 1):
        if limits[i] <= value < limits[i + 1]:
            return categories[i]
    return 'Unknown'
# counts and displays how many pollutants belong to every air pollution category
def count_and_display_air_quality_categories(lat, lon):

    values = load_pollution_gps_code(lat, lon)

    categories_count = {
        "Good": 0,
        "Fair": 0,
        "Moderate": 0,
        "Poor": 0,
        "Very Poor": 0
    }

    categories_table = []
    so2_category = get_air_pollutant_category(values[0], [0, 20, 80, 250, 350, 400])
    categories_table.append(so2_category)
    no2_category = get_air_pollutant_category(values[1], [0, 40, 70, 150, 200, 250])
    categories_table.append(no2_category)
    pm10_category = get_air_pollutant_category(values[2], [0, 20, 50, 100, 200, 250])
    categories_table.append(pm10_category)
    pm25_category = get_air_pollutant_category(values[3], [0, 10, 25, 50, 75, 100])
    categories_table.append(pm25_category)
    o3_category = get_air_pollutant_category(values[4], [0, 60, 100, 140, 180, 220])
    categories_table.append(o3_category)
    co_category = get_air_pollutant_category(values[5], [0, 4400, 9400, 12400, 15400, 17000])
    categories_table.append(co_category)

    for key, value in categories_count.items():
        for element in categories_table:
            if element == key:
                categories_count[key] += 1

    categories = list(categories_count.keys())
    values = list(categories_count.values())
    colors = ['green', 'yellow', 'orange', 'red', 'purple']  # Kolory dla poszczególnych kategorii

    # Tworzenie wykresu słupkowego
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(categories, values, color=colors, edgecolor='black')

    # Dodanie tytułu i etykiet
    ax.set_title('Categories Count', fontsize=16)
    ax.set_xlabel('Category', fontsize=14)
    ax.set_ylabel('Count', fontsize=14)

    # Ustawienie osi Y na liczby całkowite
    ax.set_yticks(np.arange(0, max(values) + 1, 1))  # Skala osi Y tylko na liczby całkowite

    # Obrócenie etykiet na osi X dla lepszej czytelności
    ax.set_xticklabels(categories, rotation=15, fontweight="bold")

    # Wyświetlenie siatki dla osi Y
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    return fig  # Zwracamy fig, żeby można było osadzić go w nowym oknie

# a helping function to display charts for pollutants levels and their air quality category
def display_air_pollution_element_with_category_placement(value, limits, title, x_axis_limit):
    categories = ['Good', 'Fair', 'Moderate', 'Poor', 'Very Poor']
    if value > limits[5]:
        value = limits[5] - 10

    def get_category(value, limits):
        for i in range(len(limits) - 1):
            if limits[i] <= value < limits[i + 1]:
                return categories[i]
        return 'Unknown'

    category = get_category(value, limits)

    category_colors = ['green', 'yellow', 'orange', 'red', 'purple']
    category_values = [limits[i:i + 2] for i in range(len(limits) - 1)]

    fig, ax = plt.subplots(figsize=(10, 3))

    for i, (start, end) in enumerate(category_values):
        ax.barh(0, end - start, left=start, color=category_colors[i], height=1)
        ax.text((start + end) / 2, 0, categories[i], ha='center', va='center', color='black', fontweight='bold')

    ax.plot([value, value], [0, 1], color='black', linewidth=2, label=f'Value = {value} ({category})')

    ax.set_xlim(0, x_axis_limit)
    ax.set_yticks([])
    ax.set_xlabel('Value')
    ax.set_title(title)

    ax.legend()
    return fig

# displaying a chart of SO2-level and the air quality category
def display_so2_placement(lat, lon):
    value = load_pollution_gps_code(lat, lon)[0]

    limits = [0, 20, 80, 250, 350, 400]

    fig = display_air_pollution_element_with_category_placement(value, limits, "Category of sulphur dioxide (SO₂) based on value", limits[5])
    return fig

# displaying a chart of NO2-level and the air quality category
def display_no2_placement(lat, lon):
    value = load_pollution_gps_code(lat, lon)[1]

    limits = [0, 40, 70, 150, 200, 250]

    fig = display_air_pollution_element_with_category_placement(value, limits, "Category of nitrogen dioxide (NO₂) based on value", limits[5])
    return fig

# displaying a chart of PM10-level and the air quality category
def display_pm10_placement(lat, lon):
    value = load_pollution_gps_code(lat, lon)[2]

    limits = [0, 20, 50, 100, 200, 250]

    fig = display_air_pollution_element_with_category_placement(value, limits, "Category of particulates (PM10) based on value", limits[5])
    return fig

# displaying a chart of PM2.5-level and the air quality category
def display_pm25_placement(lat, lon):
    value = load_pollution_gps_code(lat, lon)[3]

    limits = [0, 10, 25, 50, 75, 100]

    fig = display_air_pollution_element_with_category_placement(value, limits, "Category of particulates (PM2.5) based on value", limits[5])
    return fig

# displaying a chart of O3-level and the air quality category
def display_o3_placement(lat, lon):
    value = load_pollution_gps_code(lat, lon)[4]

    limits = [0, 60, 100, 140, 180, 220]

    fig = display_air_pollution_element_with_category_placement(value, limits, "Category of ozone (O₃) based on value", limits[5])
    return fig

# displaying a chart of CO-level and the air quality category
def display_co_placement(lat, lon):
    value = load_pollution_gps_code(lat, lon)[5]

    limits = [0, 4400, 9400, 12400, 15400, 17000]

    fig = display_air_pollution_element_with_category_placement(value, limits, "Category of carbon monoxide (CO) based on value", limits[5])
    return fig

def display_comparison_chart(lat_c1, lon_c1, lat_c2, lon_c2, city1, city2):
    # Dane zanieczyszczeń powietrza dla dwóch miast (tabele)
    data_city1 = load_pollution_gps_code(lat_c1, lon_c1)[0:6]
    data_city2 = load_pollution_gps_code(lat_c2, lon_c2)[0:6]

    # Kategorie zanieczyszczeń
    categories = ['SO2', 'NO2', 'PM10', 'PM2.5', 'O3', 'CO']

    x = np.arange(len(categories))  # Lokalizacje dla grupy kategorii
    width = 0.35  # Szerokość słupków

    # Tworzenie wykresu
    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width / 2, data_city1, width, label=city1, color='skyblue')
    bars2 = ax.bar(x + width / 2, data_city2, width, label=city2, color='orange')

    # Dostosowanie wykresu
    ax.set_xlabel('Pollutants')
    ax.set_ylabel('Pollution level')
    ax.set_title('Pollution comparison chart')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()

    # Usunięcie kratki
    ax.grid(False)

    # Dodanie wartości na szczycie słupków
    for bar in bars1 + bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{height}', ha='center', va='bottom')

    plt.tight_layout()
    return fig

def display_pollutants_development_chart(lat, lon, data, max_ticks=10):
    # Wyciąganie wartości czasu i konwersja do formatu czytelnego
    timestamps = [datetime.fromtimestamp(item["timestamp"], tz=timezone.utc) for item in data]

    # Wyciąganie wartości dla każdego składnika powietrza
    so2 = [item["so2"] for item in data]
    no2 = [item["no2"] for item in data]
    pm10 = [item["pm10"] for item in data]
    pm2_5 = [item["pm2_5"] for item in data]
    o3 = [item["o3"] for item in data]
    co = [item["co"] for item in data]

    # Tworzenie jednej figury z dwoma osiami (jednym wykresem na każdej osi)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))

    # Wykres 1: Wszystkie składniki oprócz CO
    ax1.plot(timestamps, so2, label='SO₂', marker='o')
    ax1.plot(timestamps, no2, label='NO₂', marker='o')
    ax1.plot(timestamps, pm10, label='PM₁₀', marker='o')
    ax1.plot(timestamps, pm2_5, label='PM₂.₅', marker='o')
    ax1.plot(timestamps, o3, label='O₃', marker='o')

    ax1.set_title('Pollutants development (excluding CO)', fontsize=16)
    ax1.set_xlabel('Time', fontsize=12)
    ax1.set_ylabel('Concentration', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Ustawienie etykiet na osi X: tylko co n-ty punkt
    if len(timestamps) > max_ticks:
        step = len(timestamps) // max_ticks
    else:
        step = 1
    xticks = [timestamps[i] for i in range(0, len(timestamps), step)]

    # Ustawianie etykiet na osi X
    ax1.set_xticks(xticks)
    ax1.set_xticklabels([ts.strftime('%Y-%m-%d %H:%M') for ts in xticks], rotation=45, ha="right", fontsize=6.5)

    ax1.legend(loc='upper left', fontsize=10)

    # Wykres 2: Tylko CO
    ax2.plot(timestamps, co, label='CO', color='red', marker='o')

    ax2.set_xlabel('Time', fontsize=12)
    ax2.set_ylabel('Concentration (CO)', fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.6)

    # Ustawienie etykiet na osi X: tylko co n-ty punkt
    ax2.set_xticks(xticks)
    ax2.set_xticklabels([ts.strftime('%Y-%m-%d %H:%M') for ts in xticks], rotation=45, ha="right")

    ax2.legend(loc='upper left', fontsize=10)

    # Zwracanie jednej figury, która zawiera oba wykresy
    return fig


def display_pollutants_development_chart_24h(lat, lon):
    now = datetime.now(timezone.utc)
    rounded_time = now.replace(minute=0, second=0, microsecond=0)
    unix_time = int(rounded_time.timestamp())
    data = load_historical_data_24hwindow(lat, lon, unix_time)

    fig = display_pollutants_development_chart(lat, lon, data)

    return fig

def display_pollutants_development_chart_7days(lat, lon):
    now = datetime.now(timezone.utc)
    rounded_time = now.replace(minute=0, second=0, microsecond=0)
    unix_time = int(rounded_time.timestamp())
    data = load_historical_data_1WeekBefore(lat, lon, unix_time)
    fig = display_pollutants_development_chart(lat, lon, data)

    return fig

# Toggling the input fields
def toggle_search_mode():
    if search_mode.get() == 'coordinates':
        latitude_entry.config(state='normal')
        longitude_entry.config(state='normal')
        city_entry.config(state='disabled')
    elif search_mode.get() == 'city':
        latitude_entry.config(state='disabled')
        longitude_entry.config(state='disabled')
        city_entry.config(state='normal')

# Toggling the input fields
def toggle_compare_mode():
    if compare_mode.get() == 'city':
        for widget in [entry1, entry2]:
            widget.config(state='normal')
        for widget in [entry_gps1_lat, entry_gps1_long, entry_gps2_lat, entry_gps2_long]:
            widget.config(state='disabled')
    elif compare_mode.get() == 'gps':
        for widget in [entry1, entry2]:
            widget.config(state='disabled')
        for widget in [entry_gps1_lat, entry_gps1_long, entry_gps2_lat, entry_gps2_long]:
            widget.config(state='normal')

def toggle_historical_mode():
    if historical_chosen_mode.get() == 'city':
        entry1_t2.config(state='normal')
        for widget in [entry_gps1_lat_t2, entry_gps1_long_t2]:
            widget.config(state='disabled')
    elif historical_chosen_mode.get() == 'gps':
        entry1_t2.config(state='disabled')
        for widget in [entry_gps1_lat_t2, entry_gps1_long_t2]:
            widget.config(state='normal')

def toggle_forecast_mode():
    if forecast_chosen_mode.get() == 'city':
        entry1_forecast.config(state='normal')
        for widget in [entry_gps1_lat_forecast, entry_gps1_long_forecast]:
            widget.config(state='disabled')
    elif forecast_chosen_mode.get() == 'gps':
        entry1_forecast.config(state='disabled')
        for widget in [entry_gps1_lat_forecast, entry_gps1_long_forecast]:
            widget.config(state='normal')

# displaying the basic pollution data
def display_data():

    # Sprawdzenie trybu wyszukiwania
    try:
        if search_mode.get() == 'coordinates':
            lat = latitude_entry.get()
            lon = longitude_entry.get()
            city = convert_gps_to_city(lat, lon)[0]
            country = convert_gps_to_city(lat, lon)[1]
            pollutant_values = load_pollution_gps_code(lat, lon)
            aqi = get_air_quality_index_category_name(lat, lon)

            aqi_value_label.config(text=f"Air Quality Index: {aqi}")


            so2_category = get_air_pollutant_category(pollutant_values[0], [0, 20, 80, 250, 350, 400])
            no2_category = get_air_pollutant_category(pollutant_values[1], [0, 40, 70, 150, 200, 250])
            pm10_category = get_air_pollutant_category(pollutant_values[2], [0, 20, 50, 100, 200, 250])
            pm25_category = get_air_pollutant_category(pollutant_values[3], [0, 10, 25, 50, 75, 100])
            o3_category = get_air_pollutant_category(pollutant_values[4], [0, 60, 100, 140, 180, 220])
            co_category = get_air_pollutant_category(pollutant_values[5], [0, 4400, 9400, 12400, 15400, 17000])



            data_display.config(text=f"Searching by Coordinates:\nGPS: ({lat}, {lon})\n"
                                     f"City found: {city}\n"
                                     f"Country: {country}\n"
                                     f"Sulphur dioxide (SO₂) level: {pollutant_values[0]} µg/m³ ({so2_category})\n"
                                     f"Nitrogen dioxide (NO₂) level: {pollutant_values[1]} µg/m³ ({no2_category})\n"
                                     f"Particulates (PM10) level: {pollutant_values[2]} µg/m³ ({pm10_category})\n"
                                     f"Particulates (PM2.5) level: {pollutant_values[3]} µg/m³ ({pm25_category})\n"
                                     f"Ozone (O₃) level: {pollutant_values[4]} µg/m³ ({o3_category})\n"
                                     f"Carbon monoxide (CO) level: {pollutant_values[5]} µg/m³ ({co_category})\n"
                                     f"Additional pollutants:\n"
                                     f"Ammonia (NH₃) level: {pollutant_values[6]} µg/m³\n"
                                     f"Nitrogen oxide (NO) level: {pollutant_values[7]} µg/m³"   )

        elif search_mode.get() == 'city':
            city = city_entry.get()
            lat = convert_city_to_gps(city)[0]
            lon = convert_city_to_gps(city)[1]
            country = convert_gps_to_city(lat, lon)[1]
            pollutant_values = load_pollution_gps_code(lat, lon)
            aqi = get_air_quality_index_category_name(lat, lon)

            so2_category = get_air_pollutant_category(pollutant_values[0], [0, 20, 80, 250, 350, 400])
            no2_category = get_air_pollutant_category(pollutant_values[1], [0, 40, 70, 150, 200, 250])
            pm10_category = get_air_pollutant_category(pollutant_values[2], [0, 20, 50, 100, 200, 250])
            pm25_category = get_air_pollutant_category(pollutant_values[3], [0, 10, 25, 50, 75, 100])
            o3_category = get_air_pollutant_category(pollutant_values[4], [0, 60, 100, 140, 180, 220])
            co_category = get_air_pollutant_category(pollutant_values[5], [0, 4400, 9400, 12400, 15400, 17000])

            aqi_value_label.config(text=f"Air Quality Index: {aqi}")

            data_display.config(text=f"Searching by City:\nCity: {city}\n"
                                f"Country: {country}\n"
                                f"GPS: ({lat}, {lon})\n"
                                f"Sulphur dioxide (SO₂) level: {pollutant_values[0]} µg/m³ ({so2_category})\n"
                                f"Nitrogen dioxide (NO₂) level: {pollutant_values[1]} µg/m³ ({no2_category})\n"
                                f"Particulates (PM10) level: {pollutant_values[2]} µg/m³ ({pm10_category})\n"
                                f"Particulates (PM2.5) level: {pollutant_values[3]} µg/m³ ({pm25_category})\n"
                                f"Ozone (O₃) level: {pollutant_values[4]} µg/m³ ({o3_category})\n"
                                f"Carbon monoxide (CO) level: {pollutant_values[5]} µg/m³ ({co_category})\n"
                                f"Additional pollutants:\n"
                                f"Ammonia (NH₃) level: {pollutant_values[6]} µg/m³\n"
                                f"Nitrogen oxide (NO) level: {pollutant_values[7]} µg/m³"
                                )

        # Pokaż dodatkowe przyciski oraz listę rozwijaną po naciśnięciu Display Data
        additional_buttons_frame.pack(pady=10)
        analysis_combobox.pack(pady=5)
        analysis_button.pack(pady=5)
    except Exception as e:
        data_display.config(text="Cannot display data for this input. Change the data and try again!")

def adjust_search_mode_return_tab1():
    return_table = []
    if search_mode.get() == 'city':
        city = city_entry.get()
        lat = convert_city_to_gps(city)[0]
        lon = convert_city_to_gps(city)[1]
        country = convert_gps_to_city(lat, lon)[1]
        return_table.append(lat)
        return_table.append(lon)
        return_table.append(city)
        return_table.append(country)

    elif search_mode.get() == 'coordinates':
        lat = latitude_entry.get()
        lon = longitude_entry.get()
        city = convert_gps_to_city(lat, lon)[0]
        country = convert_gps_to_city(lat, lon)[1]
        return_table.append(lat)
        return_table.append(lon)
        return_table.append(city)
        return_table.append(country)
    return return_table

def adjust_comparison_mode_return_tab3():
    return_table = []
    if compare_mode.get() == 'city':
        city1 = entry1.get()
        city2 = entry2.get()
        lat_c1 = convert_city_to_gps(city1)[0]
        lon_c1 = convert_city_to_gps(city1)[1]
        lat_c2 = convert_city_to_gps(city2)[0]
        lon_c2 = convert_city_to_gps(city2)[1]
        country1 = convert_gps_to_city(lat_c1, lon_c1)[1]
        country2 = convert_gps_to_city(lat_c2, lon_c2)[1]
        return_table.append(lat_c1)
        return_table.append(lon_c1)
        return_table.append(city1)
        return_table.append(country1)
        return_table.append(lat_c2)
        return_table.append(lon_c2)
        return_table.append(city2)
        return_table.append(country2)


    elif compare_mode.get() == 'gps':
        lat_c1 = entry_gps1_lat.get()
        lon_c1 = entry_gps1_long.get()
        lat_c2 = entry_gps2_lat.get()
        lon_c2 = entry_gps2_long.get()
        city1 = convert_gps_to_city(lat_c1, lon_c1)[0]
        country1 = convert_gps_to_city(lat_c1, lon_c1)[1]
        city2 = convert_gps_to_city(lat_c2, lon_c2)[0]
        country2 = convert_gps_to_city(lat_c2, lon_c2)[1]
        return_table.append(lat_c1)
        return_table.append(lon_c1)
        return_table.append(city1)
        return_table.append(country1)
        return_table.append(lat_c2)
        return_table.append(lon_c2)
        return_table.append(city2)
        return_table.append(country2)
    return return_table

def adjust_historical_data_mode():
    return_table = []
    if historical_chosen_mode.get() == 'city':
        city = entry1_t2.get()
        lat = convert_city_to_gps(city)[0]
        lon = convert_city_to_gps(city)[1]
        country = convert_gps_to_city(lat, lon)[1]
        return_table.append(lat)
        return_table.append(lon)
        return_table.append(city)
        return_table.append(country)
    elif historical_chosen_mode.get() == 'gps':
        lat = entry_gps1_lat_t2.get()
        lon = entry_gps1_long_t2.get()
        city = convert_gps_to_city(lat, lon)[0]
        country = convert_gps_to_city(lat, lon)[1]
        return_table.append(lat)
        return_table.append(lon)
        return_table.append(city)
        return_table.append(country)
    return return_table

#displaying a new window with trehhold chart
def show_thresholds_window():
    # Tworzymy nowe okno do wyświetlenia wykresu
    thresholds_window = tk.Toplevel(root)
    thresholds_window.title("Thresholds Chart")
    thresholds_window.geometry('1100x950')

    # Wywołaj funkcję do rysowania wykresu w tym nowym oknie
    fig = display_treshhold_values()

    # Osadzamy wykres w oknie tkinter
    canvas = FigureCanvasTkAgg(fig, master=thresholds_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

#displaying a new window with category count chart
def show_category_count_window():
    try:
        data = adjust_search_mode_return_tab1()
        # Tworzymy nowe okno do wyświetlenia wykresu
        category_count_window = tk.Toplevel(root)
        category_count_window.title("Category Count Chart")
        category_count_window.geometry('800x600')
        lat = data[0]
        lon = data[1]
        # Wywołaj funkcję do rysowania wykresu w tym nowym oknie
        fig = count_and_display_air_quality_categories(lat, lon)

        # Osadzamy wykres w oknie tkinter
        canvas = FigureCanvasTkAgg(fig, master=category_count_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    except Exception as e:
        data_display.config(text="Cannot display data for this input. Change the data and try again!")

def show_pollutants_development_window_24h():
    try:
        data = adjust_historical_data_mode()
        pollutants_development_window = tk.Toplevel(root)
        pollutants_development_window.title("Pollutants Development Chart")
        pollutants_development_window.geometry('900x1000')
        lat = data[0]
        lon = data[1]

        fig = display_pollutants_development_chart_24h(lat, lon)
        canvas = FigureCanvasTkAgg(fig, master=pollutants_development_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    except Exception as e:
        label_area_t2.config(text="Cannot display data for this input. Change the data and try again!")

def show_pollutants_development_widnow_7days():
    try:
        data = adjust_historical_data_mode()
        pollutants_development_window = tk.Toplevel(root)
        pollutants_development_window.title("Pollutants Development Chart")
        pollutants_development_window.geometry('900x1000')
        lat = data[0]
        lon = data[1]
        fig = display_pollutants_development_chart_7days(lat, lon)
        canvas = FigureCanvasTkAgg(fig, master=pollutants_development_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    except Exception as e:
        label_area_t2.config(text="Cannot display data for this input. Change the data and try again!")


#displaying category chart with pollutant value for selected pollutant
def display_analysis():
    try:
        data = adjust_search_mode_return_tab1()
        lat = data[0]
        lon = data[1]
        selected_option = analysis_combobox.get()
        analysis_window = tk.Toplevel(root)
        analysis_window.title(f"Analysis: {selected_option}")
        analysis_window.geometry('900x750')
        fig_so2 = display_so2_placement(lat, lon)
        fig_no2 = display_no2_placement(lat, lon)
        fig_pm10 = display_pm10_placement(lat, lon)
        fig_pm25 = display_pm25_placement(lat, lon)
        fig_o3 = display_o3_placement(lat, lon)
        fig_co = display_co_placement(lat, lon)

        if selected_option == 'Sulphur dioxide (SO₂)':
            canvas = FigureCanvasTkAgg(fig_so2, master=analysis_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        elif selected_option == 'Nitrogen dioxide (NO₂)':
            canvas = FigureCanvasTkAgg(fig_no2, master=analysis_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        elif selected_option == 'Particulates (PM10)':
            canvas = FigureCanvasTkAgg(fig_pm10, master=analysis_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        elif selected_option == 'Particulates (PM2.5)':
            canvas = FigureCanvasTkAgg(fig_pm25, master=analysis_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        elif selected_option == 'Ozone (O₃)':
            canvas = FigureCanvasTkAgg(fig_o3, master=analysis_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        elif selected_option == 'Carbon monoxide (CO)':
            canvas = FigureCanvasTkAgg(fig_co, master=analysis_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    except Exception as e:
        data_display.config(text="Cannot display data for this input. Change the data and try again!")

def on_click_comparison_chart():
    try:
        data = adjust_comparison_mode_return_tab3()
        comparison_window = tk.Toplevel(root)
        comparison_window.title("Comparison Chart")
        comparison_window.geometry('800x600')
        lat_c1 = data[0]
        lon_c1 = data[1]
        lat_c2 = data[4]
        lon_c2 = data[5]
        city1 = data[2]
        city2 = data[6]

        fig = display_comparison_chart(lat_c1, lon_c1, lat_c2, lon_c2, city1, city2)

        canvas = FigureCanvasTkAgg(fig, master=comparison_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    except Exception as e:
        label_area1.config(text = "Cannot display data for this input\n. Change the data and try again!")
        label_area2.config(text = "Cannot display data for this input\n. Change the data and try again!")

# Function to fetch input and compare cities
def fetch_input_comparison():
    try:
            if compare_mode.get() == "city":
                city1 = entry1.get()
                city2 = entry2.get()

                lat_and_lon_c1 = convert_city_to_gps(city1)
                lat_and_lon_c2 = convert_city_to_gps(city2)

                pol_data_c1 = load_pollution_gps_code(lat_and_lon_c1[0], lat_and_lon_c1[1])
                pol_data_c2 = load_pollution_gps_code(lat_and_lon_c2[0], lat_and_lon_c2[1])

                country1 = convert_gps_to_city(lat_and_lon_c1[0], lat_and_lon_c1[1])[1]
                country2 = convert_gps_to_city(lat_and_lon_c2[0], lat_and_lon_c2[1])[1]

                aqi1 = get_air_quality_index_category_name(lat_and_lon_c1[0], lat_and_lon_c1[1])
                aqi2 = get_air_quality_index_category_name(lat_and_lon_c2[0], lat_and_lon_c2[1])

                so2_category1 = get_air_pollutant_category(pol_data_c1[0], [0, 20, 80, 250, 350, 400])
                no2_category1= get_air_pollutant_category(pol_data_c1[1], [0, 40, 70, 150, 200, 250])
                pm10_category1 = get_air_pollutant_category(pol_data_c1[2], [0, 20, 50, 100, 200, 250])
                pm25_category1= get_air_pollutant_category(pol_data_c1[3], [0, 10, 25, 50, 75, 100])
                o3_category1 = get_air_pollutant_category(pol_data_c1[4], [0, 60, 100, 140, 180, 220])
                co_category1 = get_air_pollutant_category(pol_data_c1[5], [0, 4400, 9400, 12400, 15400, 17000])

                so2_category2 = get_air_pollutant_category(pol_data_c2[0], [0, 20, 80, 250, 350, 400])
                no2_category2 = get_air_pollutant_category(pol_data_c2[1], [0, 40, 70, 150, 200, 250])
                pm10_category2 = get_air_pollutant_category(pol_data_c2[2], [0, 20, 50, 100, 200, 250])
                pm25_category2 = get_air_pollutant_category(pol_data_c2[3], [0, 10, 25, 50, 75, 100])
                o3_category2 = get_air_pollutant_category(pol_data_c2[4], [0, 60, 100, 140, 180, 220])
                co_category2 = get_air_pollutant_category(pol_data_c2[5], [0, 4400, 9400, 12400, 15400, 17000])

                label_area1.config(text=f"Comparing by City:\n"
                                        f"City: {city1}\n"
                                        f"Country: {country1}\n"
                                        f"GPS: ({round(lat_and_lon_c1[0], 4)}, {round(lat_and_lon_c1[1], 4)})\n"
                                        f"----------------------------------------------------------------\n"
                                        f"AQI index: {aqi1}\n"
                                        f"----------------------------------------------------------------\n"
                                        f"SO₂ level: {pol_data_c1[0]} µg/m³ ({so2_category1})\n"
                                        f"NO₂ level: {pol_data_c1[1]} µg/m³ ({no2_category1})\n"
                                        f"PM10 level: {pol_data_c1[2]} µg/m³ ({pm10_category1})\n"
                                        f"PM2.5 level: {pol_data_c1[3]} µg/m³ ({pm25_category1})\n"
                                        f"O₃ level: {pol_data_c1[4]} µg/m³ ({o3_category1})\n"
                                        f"CO level: {pol_data_c1[5]} µg/m³ ({co_category1})\n"
                                        f"----------------------------------------------------------------\n"
                                        f"Additional pollutants:\n"
                                        f"----------------------------------------------------------------\n"
                                        f"NH₃ level: {pol_data_c1[6]} µg/m³\n"
                                        f"NO level: {pol_data_c1[7]} µg/m³"
                                   )

                label_area2.config(text=f"Comparing by City:\n"
                                        f"City: {city2}\n"
                                        f"Country: {country2}\n"
                                        f"GPS: ({round(lat_and_lon_c2[0], 4)}, {round(lat_and_lon_c2[1], 4)})\n"
                                        f"----------------------------------------------------------------\n"
                                        f"AQI index: {aqi2}\n"
                                        f"----------------------------------------------------------------\n"
                                        f"SO₂ level: {pol_data_c2[0]} µg/m³ ({so2_category2})\n"
                                        f"NO₂ level: {pol_data_c2[1]} µg/m³ ({no2_category2})\n"
                                        f"PM10 level: {pol_data_c2[2]} µg/m³ ({pm10_category2})\n"
                                        f"PM2.5 level: {pol_data_c2[3]} µg/m³ ({pm25_category2})\n"
                                        f"O₃ level: {pol_data_c2[4]} µg/m³ ({o3_category2})\n"
                                        f"CO level: {pol_data_c2[5]} µg/m³ ({co_category2})\n"
                                        f"----------------------------------------------------------------\n"
                                        f"Additional pollutants:\n"
                                        f"----------------------------------------------------------------\n"
                                        f"NH₃ level: {pol_data_c2[6]} µg/m³\n"
                                        f"NO level: {pol_data_c2[7]} µg/m³"
                                   )

            elif compare_mode.get() == "gps":
                lat_c1 = float(entry_gps1_lat.get())
                lon_c1 = float(entry_gps1_long.get())
                city1 = convert_gps_to_city(lat_c1, lon_c1)[0]
                country1 = convert_gps_to_city(lat_c1, lon_c1)[1]
                pollution_city1 = load_pollution_gps_code(lat_c1, lon_c1)
                aqi_cty1 = get_air_quality_index_category_name(lat_c1, lon_c1)

                lat_c2 = float(entry_gps2_lat.get())
                lon_c2 = float(entry_gps2_long.get())
                city2 = convert_gps_to_city(lat_c2, lon_c2)[0]
                country2 = convert_gps_to_city(lat_c2, lon_c2)[1]
                pollution_city2 = load_pollution_gps_code(lat_c2, lon_c2)
                aqi_cty2 = get_air_quality_index_category_name(lat_c2, lon_c2)

                so2_category1 = get_air_pollutant_category(pollution_city1[0], [0, 20, 80, 250, 350, 400])
                no2_category1 = get_air_pollutant_category(pollution_city1[1], [0, 40, 70, 150, 200, 250])
                pm10_category1 = get_air_pollutant_category(pollution_city1[2], [0, 20, 50, 100, 200, 250])
                pm25_category1 = get_air_pollutant_category(pollution_city1[3], [0, 10, 25, 50, 75, 100])
                o3_category1 = get_air_pollutant_category(pollution_city1[4], [0, 60, 100, 140, 180, 220])
                co_category1 = get_air_pollutant_category(pollution_city1[5], [0, 4400, 9400, 12400, 15400, 17000])

                so2_category2 = get_air_pollutant_category(pollution_city2[0], [0, 20, 80, 250, 350, 400])
                no2_category2 = get_air_pollutant_category(pollution_city2[1], [0, 40, 70, 150, 200, 250])
                pm10_category2 = get_air_pollutant_category(pollution_city2[2], [0, 20, 50, 100, 200, 250])
                pm25_category2= get_air_pollutant_category(pollution_city2[3], [0, 10, 25, 50, 75, 100])
                o3_category2 = get_air_pollutant_category(pollution_city2[4], [0, 60, 100, 140, 180, 220])
                co_category2 = get_air_pollutant_category(pollution_city2[5], [0, 4400, 9400, 12400, 15400, 17000])

                label_area1.config(text=f"Comparing by Coordinates:\nGPS: ({round(lat_c1, 4)}, {round(lon_c1, 4)})\n"
                                         f"City found: {city1}\n"
                                         f"Country: {country1}\n"
                                         f"----------------------------------------------------------------\n"
                                         f"AQI index: {aqi_cty1}\n"
                                         f"----------------------------------------------------------------\n"
                                         f"SO₂ level: {pollution_city1[0]} µg/m³ ({so2_category1})\n"
                                         f"NO₂ level: {pollution_city1[1]} µg/m³ ({no2_category1})\n"
                                         f"PM10 level: {pollution_city1[2]} µg/m³ ({pm10_category1})\n"
                                         f"PM2.5 level: {pollution_city1[3]} µg/m³ ({pm25_category1})\n"
                                         f"O₃ level: {pollution_city1[4]} µg/m³ ({o3_category1})\n"
                                         f"CO level: {pollution_city1[5]} µg/m³ ({co_category1})\n"
                                         f"----------------------------------------------------------------\n"
                                         f"Additional pollutants:\n"
                                         f"----------------------------------------------------------------\n"
                                         f"NH₃ level: {pollution_city1[6]} µg/m³\n"
                                         f"NO level: {pollution_city1[7]} µg/m³")

                label_area2.config(text=f"Comparing by Coordinates:\nGPS: ({round(lat_c2, 4)}, {round(lon_c2, 4)})\n"
                                        f"City found: {city2}\n"
                                        f"Country: {country2}\n"
                                        f"----------------------------------------------------------------\n"
                                        f"AQI index: {aqi_cty2}\n"
                                        f"----------------------------------------------------------------\n"
                                        f"SO₂ level: {pollution_city2[0]} µg/m³ ({so2_category2})\n"
                                        f"NO₂ level: {pollution_city2[1]} µg/m³ ({no2_category2})\n"
                                        f"PM10 level: {pollution_city2[2]} µg/m³ ({pm10_category2})\n"
                                        f"PM2.5 level: {pollution_city2[3]} µg/m³ ({pm25_category2})\n"
                                        f"O₃ level: {pollution_city2[4]} µg/m³ ({o3_category2})\n"
                                        f"CO level: {pollution_city2[5]} µg/m³ ({co_category2})\n"
                                        f"----------------------------------------------------------------\n"
                                        f"Additional pollutants:\n"
                                        f"----------------------------------------------------------------\n"
                                        f"NH₃ level: {pollution_city2[6]} µg/m³\n"
                                        f"NO level: {pollution_city2[7]} µg/m³")

            show_chart_button.grid(row=11, column=0, columnspan=2, pady=10)
    except Exception as e:
        label_area1.config(text="Input data is invalid\n"
                                "or no data found!")
        label_area2.config(text="Input data is invalid\n"
                                "or no data found for this input!")

def fetch_input_historical_data():
    try:
        if historical_chosen_mode.get() == 'city':
            city = entry1_t2.get()
            lat = convert_city_to_gps(city)[0]
            lon = convert_city_to_gps(city)[1]
            country = convert_gps_to_city(lat, lon)[1]


            label_area_t2.config(text=f"Loading historical data by city name: {city}....\n"
                                      f"\n"
                                      f"......................................................................................................................................................\n"
                                      f"\n"
                                      f"Data found!\n"
                                      f"\n"
                                      f"Country: {country}\n"
                                      f"GPS: ({lat}, {lon})\n"
                                      f"\n"
                                      f"Click 'Last 24h' button to display pollution chart\n"
                                      f"for the last 24 hours for input location with hourly step\n"
                                      f"\n"
                                      f".......................................................................................................................................................\n"
                                      f"\n"
                                      f"Click 'Last Week' button to display pollution chart\n"
                                      f"for the last 168 hours for input location with hourly step\n"
                                      f".......................................................................................................................................................\n"
                                                                )
        elif historical_chosen_mode.get() == 'gps':
            lat = entry_gps1_lat_t2.get()
            lon = entry_gps1_long_t2.get()
            city = convert_gps_to_city(lat, lon)[0]
            country = convert_gps_to_city(lat, lon)[1]


            label_area_t2.config(text=f"Loading historical data by GPS: ({lat}, {lon})....\n"
                                      f"\n"
                                      f"......................................................................................................................................................\n"
                                      f"\n"
                                      f"Data found!\n"
                                      f"\n"
                                      f"City: {city}\n"
                                      f"Country: {country}\n"
                                      f"\n"
                                      f"Click 'Last 24h' button to display pollution chart\n"
                                      f"for the last 24 hours for input location with hourly step\n"
                                      f"\n"
                                      f".......................................................................................................................................................\n"
                                      f"\n"
                                      f"Click 'Last Week' button to display pollution chart\n"
                                      f"for the last 168 hours for input location with hourly step\n"
                                      f".......................................................................................................................................................\n"


                                                                )
        last_24_hours_button.grid(row=11, column=1, padx=10, pady=20, sticky="w")
        last_7_days_button.grid(row=11, column=0, padx=10, pady=20, sticky="e")
    except Exception as e:
        label_area_t2.config(text="Input data is invalid or no data found!")

def fetch_input_regression_data():
    try:
        if forecast_chosen_mode.get() == 'city':
            city = entry1_forecast.get()
            lat = convert_city_to_gps(city)[0]
            lon = convert_city_to_gps(city)[1]
            country = convert_gps_to_city(lat, lon)[1]
            aqi = get_air_quality_index(lat, lon)
            location = {'lat': lat, 'lon': lon}
            predicted_values = get_air_quality_prediction(location)
            predicted_aqi = predicted_values['predicted_aqi']
            r2_score = predicted_values['r2_score']
            mean_squared_error = predicted_values['mean_squared_error']
            mean_absolute_error = predicted_values['mean_absolute_error']

            label_area_forecast.config(text = f"Loading regression model based on city name: {city}....\n"
                                              
                                              f"..........................................................................................................................................................\n"
                                              
                                              f"Data found!\n"
                                              f"Country: {country}\n"
                                              f"GPS: ({lat}, {lon})\n"
                                              f"Current AQI level: {aqi}\n"
                                              f"..........................................................................................................................................................\n"
                                              f"Using Reression model to calculate predicet AQI Value......\n"
                                              f"..........................................................................................................................................................\n"
                                              f"Predicted AQI value: {predicted_aqi}\n"
                                              f"..........................................................................................................................................................\n"
                                              f"Model quality:\n"
                                              f"..........................................................................................................................................................\n"
                                              f"R2: {r2_score}\n"
                                              f"Mean Squared Error: {mean_squared_error}\n"
                                              f"Mean absolute Error: {mean_absolute_error}\n"
                                              f"Calculation based on data from the last 7 days\n"
                                              f"..........................................................................................................................................................\n"
                                              f"AQ Categories: 1 - Good, 2 - Fair, 3 - Moderate, 4 - Poor, 5 - Very Poor")
        elif forecast_chosen_mode.get() == 'gps':
            lat = entry_gps1_lat_forecast.get()
            lon = entry_gps1_long_forecast.get()
            city = convert_gps_to_city(lat, lon)[0]
            country = convert_gps_to_city(lat, lon)[1]
            aqi = get_air_quality_index(lat, lon)
            location = {'lat': lat, 'lon': lon}
            predicted_values = get_air_quality_prediction(location)
            predicted_aqi = predicted_values['predicted_aqi']
            r2_score = predicted_values['r2_score']
            mean_squared_error = predicted_values['mean_squared_error']
            mean_absolute_error = predicted_values['mean_absolute_error']

            label_area_forecast.config(text=f"Loading regression model based on city name: {city}....\n"

                                            f"..........................................................................................................................................................\n"

                                            f"Data found!\n"
                                            f"Country: {country}\n"
                                            f"GPS: ({lat}, {lon})\n"
                                            f"Current AQI level: {aqi}\n"
                                            f"..........................................................................................................................................................\n"
                                            f"Using Reression model to calculate predicet AQI Value......\n"
                                            f"..........................................................................................................................................................\n"
                                            f"Predicted AQI value: {predicted_aqi}\n"
                                            f"..........................................................................................................................................................\n"
                                            f"Model quality:\n"
                                            f"..........................................................................................................................................................\n"
                                            f"R2: {r2_score}\n"
                                            f"Mean Squared Error: {mean_squared_error}\n"
                                            f"Mean absolute Error: {mean_absolute_error}\n"
                                            f"Calculation based on data from the last 7 days\n"
                                            f"..........................................................................................................................................................\n"
                                            f"AQ Categories: 1 - Good, 2 - Fair, 3 - Moderate, 4 - Poor, 5 - Very Poor")
    except Exception as e:
        label_area_forecast.config(text="Input data is invalid or no data found!")


def update_mode_label():
    if compare_mode.get() == 'city':
        mode_label.set('Comparing by City')
    elif compare_mode.get() == 'gps':
        mode_label.set('Comparing by GPS')

def update_historical_mode_label():
    if historical_chosen_mode.get() == 'city':
        mode_label_t2.set('Load historical data by City')
    elif historical_chosen_mode.get() == 'gps':
        mode_label_t2.set('Load historical data by GPS')

def update_forecast_mode_label():
    if forecast_chosen_mode.get() == 'city':
        mode_label_forecast.set('Load regression data by City')
    elif forecast_chosen_mode.get() == 'gps':
        mode_label_forecast.set('Load regression data by GPS')




root = tk.Tk()
root.title('Check the air pollution in your area!')
root.geometry('555x790')


# Zakładki
tab_control = ttk.Notebook(root)
tab_control.pack(expand=1, fill='both')

# Zakładka 1
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='GPS- and name-based search')

# Górna sekcja z opcjami
options_frame = ttk.Frame(tab1)
options_frame.pack(fill='x', padx=10, pady=10)

# Kontenery dla opcji
left_frame = ttk.Frame(options_frame)
left_frame.pack(side='left', expand=True, fill='both', padx=10, pady=10)

right_frame = ttk.Frame(options_frame)
right_frame.pack(side='right', expand=True, fill='both', padx=10, pady=10)

# Wybór metody wyszukiwania (lewa strona)
search_mode = tk.StringVar(value='coordinates')

coordinates_radio = ttk.Radiobutton(left_frame, text='Search by Coordinates', variable=search_mode, value='coordinates',
                                    command=toggle_search_mode)
coordinates_radio.pack(anchor='w', pady=5)

latitude_label = ttk.Label(left_frame, text='Latitude:')
latitude_label.pack(anchor='w')
latitude_entry = ttk.Entry(left_frame)
latitude_entry.pack(anchor='w', fill='x', pady=2)

longitude_label = ttk.Label(left_frame, text='Longitude:')
longitude_label.pack(anchor='w')
longitude_entry = ttk.Entry(left_frame)
longitude_entry.pack(anchor='w', fill='x', pady=2)

# Wybór metody wyszukiwania (prawa strona)
city_radio = ttk.Radiobutton(right_frame, text='Search by City Name', variable=search_mode, value='city',
                             command=toggle_search_mode)
city_radio.pack(anchor='w', pady=5)

city_label = ttk.Label(right_frame, text='City:')
city_label.pack(anchor='w')
city_entry = ttk.Entry(right_frame)
city_entry.pack(anchor='w', fill='x', pady=2)

# Ustawienie domyślnego stanu pól
toggle_search_mode()


# Przycisk do wyświetlania danych
display_button = ttk.Button(tab1, text='Display Data', command=display_data, width=20, padding=10)
display_button.pack(pady=10)

aqi_value_label = ttk.Label(tab1, text='Air Quality Index: N/A', anchor='center', font=('Arial', 12, 'bold'))
aqi_value_label.pack(pady=(10, 10))

# Duże pole do wyświetlania danych
data_display = ttk.Label(tab1, text='Data will be displayed here....', anchor='nw', justify='left', background='white',
                         relief='solid', font=('Arial', 11))
data_display.pack(expand=True, fill='both', padx=10, pady=10)


# Kontener na dodatkowe przyciski (Display Thresholds i Display Category Count)
additional_buttons_frame = ttk.Frame(tab1)

threshold_button = ttk.Button(additional_buttons_frame, text="Display Thresholds", width=20, padding=10,
                              command=show_thresholds_window)
threshold_button.pack(side="left", padx=5)  # Przycisk obok przycisku "Display Category Count"

category_count_button = ttk.Button(additional_buttons_frame, text="Display Category Count", width=21, padding=10, command=show_category_count_window)
category_count_button.pack(side="left", padx=5)

# Lista rozwijana i przycisk do wyświetlania analizy
analysis_label = ttk.Label(tab1, text="Select an analysis option:")

# Kombinacja opcji do analizy
analysis_combobox = ttk.Combobox(tab1, values=["Sulphur dioxide (SO₂)", "Nitrogen dioxide (NO₂)", "Particulates (PM10)", "Particulates (PM2.5)", "Ozone (O₃)", "Carbon monoxide (CO)"],
                                 width=20)

# Przycisk "Display Analysis"
analysis_button = ttk.Button(tab1, text="Display Analysis", command=display_analysis, width=20, padding=10)





tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='Historical Data')
tab2.columnconfigure(0, weight=1)
tab2.columnconfigure(1, weight=1)

# Selection Mode with Radio Buttons
historical_chosen_mode = tk.StringVar(value='city')
mode_label_t2 = tk.StringVar(value='Loading historical data by City')

radio_city_t2 = ttk.Radiobutton(tab2, text='Load historical data by City', variable=historical_chosen_mode, value='city', command=lambda: [toggle_historical_mode(), update_historical_mode_label()])
radio_city_t2.grid(row=0, column=0, columnspan=2, pady=5)

radio_gps_t2 = ttk.Radiobutton(tab2, text='Load historical data by GPS', variable=historical_chosen_mode, value='gps', command=lambda: [toggle_historical_mode(), update_historical_mode_label()])
radio_gps_t2.grid(row=1, column=0, columnspan=2, pady=5)

mode_display_label_t2 = ttk.Label(tab2, textvariable=mode_label_t2, font=('Arial', 12, 'bold'))
mode_display_label_t2.grid(row=2, column=0, columnspan=2, pady=5)

# --- Column 1: City 1 ---
label1_t2 = tk.Label(tab2, text="Enter city name:")
label1_t2.grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry1_t2 = tk.Entry(tab2)
entry1_t2.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

label_gps1_lat_t2 = tk.Label(tab2, text="Latitude:")
label_gps1_lat_t2.grid(row=5, column=0, padx=10, pady=2, sticky="w")
entry_gps1_lat_t2 = tk.Entry(tab2)
entry_gps1_lat_t2.grid(row=6, column=0, columnspan=2, padx=10, pady=2, sticky="ew")

label_gps1_long_t2 = tk.Label(tab2, text="Longitude:")
label_gps1_long_t2.grid(row=7, column=0, padx=10, pady=2, sticky="w")
entry_gps1_long_t2 = tk.Entry(tab2)
entry_gps1_long_t2.grid(row=8, column=0, columnspan=2, padx=10, pady=2, sticky="ew")

# --- Data Display Areas ---
label_area_t2 = tk.Label(tab2, text="data....", height=20, width=70, relief="solid", anchor="nw", justify="left", background='white', font=('Arial', 11))
label_area_t2.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

fetch_input_button = ttk.Button(tab2, text='Fetch Input', command=fetch_input_historical_data, width=30)
fetch_input_button.grid(row=10, column=0, columnspan=2, pady=10)

# --- Last Week and Last 24h Buttons (initially hidden) ---
last_7_days_button = ttk.Button(tab2, text='Last Week', command = show_pollutants_development_widnow_7days, width=30, padding=10)
last_24_hours_button = ttk.Button(tab2, text='Last 24h', command=show_pollutants_development_window_24h, width=30, padding=10)

toggle_historical_mode()




tab3 = ttk.Frame(tab_control)
tab_control.add(tab3, text='Pollution Compare')

# Grid Configuration
tab3.columnconfigure(0, weight=1)
tab3.columnconfigure(1, weight=1)

# Selection Mode with Radio Buttons
compare_mode = tk.StringVar(value='city')
mode_label = tk.StringVar(value='Comparing by City')




radio_city = ttk.Radiobutton(tab3, text='Compare by City', variable=compare_mode, value='city', command=lambda: [toggle_compare_mode(), update_mode_label()])
radio_city.grid(row=0, column=0, columnspan=2, pady=5)

radio_gps = ttk.Radiobutton(tab3, text='Compare by GPS', variable=compare_mode, value='gps', command=lambda: [toggle_compare_mode(), update_mode_label()])
radio_gps.grid(row=1, column=0, columnspan=2, pady=5)

mode_display_label = ttk.Label(tab3, textvariable=mode_label, font=('Arial', 12, 'bold'))
mode_display_label.grid(row=2, column=0, columnspan=2, pady=5)

# --- Column 1: City 1 ---
label1 = tk.Label(tab3, text="Enter City 1:")
label1.grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry1 = tk.Entry(tab3)
entry1.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

label_gps1_lat = tk.Label(tab3, text="Latitude:")
label_gps1_lat.grid(row=5, column=0, padx=10, pady=2, sticky="w")
entry_gps1_lat = tk.Entry(tab3)
entry_gps1_lat.grid(row=6, column=0, padx=10, pady=2, sticky="ew")

label_gps1_long = tk.Label(tab3, text="Longitude:")
label_gps1_long.grid(row=7, column=0, padx=10, pady=2, sticky="w")
entry_gps1_long = tk.Entry(tab3)
entry_gps1_long.grid(row=8, column=0, padx=10, pady=2, sticky="ew")

# --- Column 2: City 2 ---
label2 = tk.Label(tab3, text="Enter City 2:")
label2.grid(row=3, column=1, padx=10, pady=5, sticky="w")
entry2 = tk.Entry(tab3)
entry2.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

label_gps2_lat = tk.Label(tab3, text="Latitude:")
label_gps2_lat.grid(row=5, column=1, padx=10, pady=2, sticky="w")
entry_gps2_lat = tk.Entry(tab3)
entry_gps2_lat.grid(row=6, column=1, padx=10, pady=2, sticky="ew")

label_gps2_long = tk.Label(tab3, text="Longitude:")
label_gps2_long.grid(row=7, column=1, padx=10, pady=2, sticky="w")
entry_gps2_long = tk.Entry(tab3)
entry_gps2_long.grid(row=8, column=1, padx=10, pady=2, sticky="ew")

# --- Data Display Areas ---
label_area1 = tk.Label(tab3, text="City 1 data....", height=20, width=70, relief="solid", anchor="nw", justify="left", background='white', font=('Arial', 11))
label_area1.grid(row=9, column=0, padx=10, pady=10, sticky="nsew")

label_area2 = tk.Label(tab3, text="City 2 data....", height=20, width=70, relief="solid", anchor="nw", justify="left", background='white', font=('Arial', 11))
label_area2.grid(row=9, column=1, padx=10, pady=10, sticky="nsew")

# Compare Button
compare_button = ttk.Button(tab3, text='Compare', command=fetch_input_comparison, width=20)
compare_button.grid(row=10, column=0, columnspan=2, pady=20)

show_chart_button = ttk.Button(tab3, text='Show Chart', command=on_click_comparison_chart, width=20)
show_chart_button.grid(row=11, column=0, columnspan=2, pady=7)
show_chart_button.grid_remove()  # Initially hidden

toggle_compare_mode()

tab4 = ttk.Frame(tab_control)
tab_control.add(tab4, text='Pollution forecast')
tab4.columnconfigure(0, weight=1)
tab4.columnconfigure(1, weight=1)

# Selection Mode with Radio Buttons
forecast_chosen_mode = tk.StringVar(value='city')
mode_label_forecast = tk.StringVar(value='Load regression data by City')

radio_city_forecast = ttk.Radiobutton(tab4, text='Regression based on city-name search', variable=forecast_chosen_mode, value='city', command=lambda: [toggle_forecast_mode(), update_forecast_mode_label()])
radio_city_forecast.grid(row=0, column=0, columnspan=2, pady=5)

radio_gps_forecast = ttk.Radiobutton(tab4, text='Regression based on GPS search', variable=forecast_chosen_mode, value='gps', command=lambda: [toggle_forecast_mode(), update_forecast_mode_label()])
radio_gps_forecast.grid(row=1, column=0, columnspan=2, pady=5)

mode_display_label_forecast = ttk.Label(tab4, textvariable=mode_label_forecast, font=('Arial', 12, 'bold'))
mode_display_label_forecast.grid(row=2, column=0, columnspan=2, pady=5)

# --- Column 1: City 1 ---
label1_forecast= tk.Label(tab4, text="Enter city name:")
label1_forecast.grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry1_forecast = tk.Entry(tab4)
entry1_forecast.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

label_gps1_lat_forecast = tk.Label(tab4, text="Latitude:")
label_gps1_lat_forecast.grid(row=5, column=0, padx=10, pady=2, sticky="w")
entry_gps1_lat_forecast = tk.Entry(tab4)
entry_gps1_lat_forecast.grid(row=6, column=0, columnspan=2, padx=10, pady=2, sticky="ew")

label_gps1_long_forecast = tk.Label(tab4, text="Longitude:")
label_gps1_long_forecast.grid(row=7, column=0, padx=10, pady=2, sticky="w")
entry_gps1_long_forecast= tk.Entry(tab4)
entry_gps1_long_forecast.grid(row=8, column=0, columnspan=2, padx=10, pady=2, sticky="ew")

# --- Data Display Areas ---
label_area_forecast= tk.Label(tab4, text="data....", height=20, width=70, relief="solid", anchor="nw", justify="left", background='white', font=('Arial', 11))
label_area_forecast.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

fetch_regression_input_button = ttk.Button(tab4, text='Fetch Input', command = fetch_input_regression_data, width=30, padding = 15)
fetch_regression_input_button.grid(row=10, column=0, columnspan=2, pady=10)


toggle_forecast_mode()



# Zakładka 5 (credits)
tab5 = ttk.Frame(tab_control)
tab_control.add(tab5, text='Project credits')

# Główna ramka na zawartość
credits_frame = ttk.Frame(tab5, padding=20)
credits_frame.pack(expand=1, fill='both')

# Tytuł projektu
title_label = ttk.Label(credits_frame, text="Project Credits", font=('Arial', 18, 'bold'))
title_label.pack(pady=(10, 20))

# Lista informacji o projekcie
credits_text = [
    "Project authors: Krzysztof Drobnik, Maksymilian Jurewicz",
    "Project name: Calculating air quality based on few basic pollutants using Open Weather API and basic GUI",
    "University: University of Economics in Poznań",
    "Subject: Programming and Data Processing",
    "Supervisor: mgr. Adam Gałązkiewicz",
    "Field of study: Industry 4.0",
    "Study year: 1"
]

# Wyświetlanie informacji w pętli
for text in credits_text:
    label = ttk.Label(credits_frame, text=text, font=('Arial', 12), anchor='w', justify='left')
    label.pack(anchor='w', pady=5)

# Separator na końcu
separator = ttk.Separator(credits_frame, orient='horizontal')
separator.pack(fill='x', pady=(20, 10))

# Wczytywanie i wyświetlanie obrazków
def load_and_display_image(frame, path):
    try:
        image = Image.open(path)
        image = image.resize((200, 150), Image.Resampling.LANCZOS)  # Zmiana metody resamplingu
        photo = ImageTk.PhotoImage(image)
        label = ttk.Label(frame, image=photo)
        label.image = photo  # Zapisywanie referencji, aby nie zostało usunięte przez garbage collector
        label.pack(pady=10)
    except Exception as e:
        error_label = ttk.Label(frame, text=f"Error loading image: {path}", font=('Arial', 10), foreground='red')
        error_label.pack(pady=5)

# Wyświetlenie pierwszego obrazka
load_and_display_image(credits_frame, 'jpg1.jpg')

# Wyświetlenie drugiego obrazka
load_and_display_image(credits_frame, 'jpg2.jpg')

root.mainloop()












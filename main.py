import requests
import json
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CountriesDictionary import country_domain_codes as cdc
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

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

# getting air quality index and the qir quality category
def get_air_quality_index(lat, lon):
    key = '986b86d5d24bbace34084b1fcda169bd'
    # key = 'api key'
    air_pollution_api_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={key}'
    response = requests.get(air_pollution_api_url)
    response_body = response.text
    response_body_json = json.loads(response_body)

    air_quality_index = response_body_json["list"][0]["main"]["aqi"]

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

# displaying the basic pollution data
def display_data():

    # Sprawdzenie trybu wyszukiwania
    try:
        global lat, lon
        if search_mode.get() == 'coordinates':
            lat = latitude_entry.get()
            lon = longitude_entry.get()
            city = convert_gps_to_city(lat, lon)[0]
            country = convert_gps_to_city(lat, lon)[1]
            pollutant_values = load_pollution_gps_code(lat, lon)
            aqi = get_air_quality_index(lat, lon)

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
            aqi = get_air_quality_index(lat, lon)

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
        # Tworzymy nowe okno do wyświetlenia wykresu
        category_count_window = tk.Toplevel(root)
        category_count_window.title("Category Count Chart")
        category_count_window.geometry('800x600')

        # Wywołaj funkcję do rysowania wykresu w tym nowym oknie
        fig = count_and_display_air_quality_categories(lat, lon)

        # Osadzamy wykres w oknie tkinter
        canvas = FigureCanvasTkAgg(fig, master=category_count_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    except Exception as e:
        data_display.config(text="Cannot display data for this input. Change the data and try again!")

#displaying category chart with pollutant value for selected pollutant
def display_analysis():
    try:
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



root = tk.Tk()
root.title('Check the air pollution in your area!')
root.geometry('555x700')


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

# Zakładka 2
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='Historical data')
label2 = ttk.Label(tab2, text='To jest zawartość zakładki 2', font=('Arial', 14))
label2.pack(expand=1, fill='both')

# Zakładka 3
tab3 = ttk.Frame(tab_control)
tab_control.add(tab3, text='Pollution comparison')
label3 = ttk.Label(tab3, text='To jest zawartość zakładki 3', font=('Arial', 14))
label3.pack(expand=1, fill='both')

# Zakładka 4
tab4 = ttk.Frame(tab_control)
tab_control.add(tab4, text='Pollution forecast')
label4 = ttk.Label(tab4, text='To jest zawartość zakładki 4', font=('Arial', 14))
label4.pack(expand=1, fill='both')

# Zakładka 5
tab5 = ttk.Frame(tab_control)
tab_control.add(tab5, text='Project credits')
label5 = ttk.Label(tab5, text='To jest zawartość zakładki 5', font=('Arial', 14))
label5.pack(expand=1, fill='both')

root.mainloop()











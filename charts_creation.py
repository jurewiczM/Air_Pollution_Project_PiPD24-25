import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from data_processing import *
import numpy as np
from datetime import datetime, timezone

# wykres wartości granicznych dla składników powietrza i kategorii
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

# wykres liczności kategorii (ile razy składniki powietrza znalazły się w danej kategorii)
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
    colors = ['green', 'yellow', 'orange', 'red', 'purple']


    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(categories, values, color=colors, edgecolor='black')


    ax.set_title('Categories Count', fontsize=16)
    ax.set_xlabel('Category', fontsize=14)
    ax.set_ylabel('Count', fontsize=14)


    ax.set_yticks(np.arange(0, max(values) + 1, 1))


    ax.set_xticklabels(categories, rotation=15, fontweight="bold")


    ax.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    return fig

# funkcja pomocnicza do wyświetlania wartości składnika powietrza wraz z przypisaniem wartości do odpowiedniej kategorii zanieczyszczenia
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

# wykres wartości so2 i kategorii
def display_so2_placement(lat, lon):
    value = load_pollution_gps_code(lat, lon)[0]

    limits = [0, 20, 80, 250, 350, 400]

    fig = display_air_pollution_element_with_category_placement(value, limits, "Category of sulphur dioxide (SO₂) based on value", limits[5])
    return fig

# wykres wartości no2 i kategorii
def display_no2_placement(lat, lon):
    value = load_pollution_gps_code(lat, lon)[1]

    limits = [0, 40, 70, 150, 200, 250]

    fig = display_air_pollution_element_with_category_placement(value, limits, "Category of nitrogen dioxide (NO₂) based on value", limits[5])
    return fig

# wykres wartości pm10 i kategorii
def display_pm10_placement(lat, lon):
    value = load_pollution_gps_code(lat, lon)[2]

    limits = [0, 20, 50, 100, 200, 250]

    fig = display_air_pollution_element_with_category_placement(value, limits, "Category of particulates (PM10) based on value", limits[5])
    return fig

# wykres wartości pm25 i kategorii
def display_pm25_placement(lat, lon):
    value = load_pollution_gps_code(lat, lon)[3]

    limits = [0, 10, 25, 50, 75, 100]

    fig = display_air_pollution_element_with_category_placement(value, limits, "Category of particulates (PM2.5) based on value", limits[5])
    return fig

# wykres wartości o3 i kategorii
def display_o3_placement(lat, lon):
    value = load_pollution_gps_code(lat, lon)[4]

    limits = [0, 60, 100, 140, 180, 220]

    fig = display_air_pollution_element_with_category_placement(value, limits, "Category of ozone (O₃) based on value", limits[5])
    return fig

# wykres wartości co i kategorii
def display_co_placement(lat, lon):
    value = load_pollution_gps_code(lat, lon)[5]

    limits = [0, 4400, 9400, 12400, 15400, 17000]

    fig = display_air_pollution_element_with_category_placement(value, limits, "Category of carbon monoxide (CO) based on value", limits[5])
    return fig

# wykres porównania wartości zanieczysczeń dla dwóch miast
def display_comparison_chart(lat_c1, lon_c1, lat_c2, lon_c2, city1, city2):

    data_city1 = load_pollution_gps_code(lat_c1, lon_c1)[0:6]
    data_city2 = load_pollution_gps_code(lat_c2, lon_c2)[0:6]


    categories = ['SO2', 'NO2', 'PM10', 'PM2.5', 'O3', 'CO']

    x = np.arange(len(categories))
    width = 0.35


    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width / 2, data_city1, width, label=city1, color='skyblue')
    bars2 = ax.bar(x + width / 2, data_city2, width, label=city2, color='orange')


    ax.set_xlabel('Pollutants')
    ax.set_ylabel('Pollution level')
    ax.set_title('Pollution comparison chart')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()


    ax.grid(False)


    for bar in bars1 + bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{height}', ha='center', va='bottom')

    plt.tight_layout()
    return fig

#funkcja pomocznicza to wyświetlania wykresu zmian wartości składników powietrza w czasie
def display_pollutants_development_chart(lat, lon, data, max_ticks=10):

    timestamps = [datetime.fromtimestamp(item["timestamp"], tz=timezone.utc) for item in data]


    so2 = [item["so2"] for item in data]
    no2 = [item["no2"] for item in data]
    pm10 = [item["pm10"] for item in data]
    pm2_5 = [item["pm2_5"] for item in data]
    o3 = [item["o3"] for item in data]
    co = [item["co"] for item in data]


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


    if len(timestamps) > max_ticks:
        step = len(timestamps) // max_ticks
    else:
        step = 1
    xticks = [timestamps[i] for i in range(0, len(timestamps), step)]


    ax1.set_xticks(xticks)
    ax1.set_xticklabels([ts.strftime('%Y-%m-%d %H:%M') for ts in xticks], rotation=45, ha="right", fontsize=6.5)

    ax1.legend(loc='upper left', fontsize=10)

    # Wykres 2: Tylko CO
    ax2.plot(timestamps, co, label='CO', color='red', marker='o')

    ax2.set_xlabel('Time', fontsize=12)
    ax2.set_ylabel('Concentration (CO)', fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.6)


    ax2.set_xticks(xticks)
    ax2.set_xticklabels([ts.strftime('%Y-%m-%d %H:%M') for ts in xticks], rotation=45, ha="right")

    ax2.legend(loc='upper left', fontsize=10)


    return fig

# wykres zmian wartości składników powietrza w ciągu ostatnich 24 godzin
def display_pollutants_development_chart_24h(lat, lon):
    now = datetime.now(timezone.utc)
    rounded_time = now.replace(minute=0, second=0, microsecond=0)
    unix_time = int(rounded_time.timestamp())
    data = load_historical_data_24hwindow(lat, lon, unix_time)

    fig = display_pollutants_development_chart(lat, lon, data)

    return fig

#wykres zmian wartości składników powietrza w ciągu ostatnich 168h
def display_pollutants_development_chart_7days(lat, lon):
    now = datetime.now(timezone.utc)
    rounded_time = now.replace(minute=0, second=0, microsecond=0)
    unix_time = int(rounded_time.timestamp())
    data = load_historical_data_1WeekBefore(lat, lon, unix_time)
    fig = display_pollutants_development_chart(lat, lon, data)

    return fig
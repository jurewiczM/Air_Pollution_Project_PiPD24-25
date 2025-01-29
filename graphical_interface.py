
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from tab_4_regression import get_air_quality_prediction
from PIL import Image, ImageTk
from charts_creation import *



# wybieranie trybu wyszkuiwania (1 zakładka - GPS/nazwa miasta)
def toggle_search_mode():
    if search_mode.get() == 'coordinates':
        latitude_entry.config(state='normal')
        longitude_entry.config(state='normal')
        city_entry.config(state='disabled')
    elif search_mode.get() == 'city':
        latitude_entry.config(state='disabled')
        longitude_entry.config(state='disabled')
        city_entry.config(state='normal')

# wybieranie trybu wyszukiwania (3 zakładka - porównywanie - GPS/nazwa miasta)
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

# wybieranie trybu wyszukiwania (2 zakładka - dane historyczne - GPS/nazwa miasta)
def toggle_historical_mode():
    if historical_chosen_mode.get() == 'city':
        entry1_t2.config(state='normal')
        for widget in [entry_gps1_lat_t2, entry_gps1_long_t2]:
            widget.config(state='disabled')
    elif historical_chosen_mode.get() == 'gps':
        entry1_t2.config(state='disabled')
        for widget in [entry_gps1_lat_t2, entry_gps1_long_t2]:
            widget.config(state='normal')

# wybieranie trybu wyszukiwania (4 zakładka - regresja - GPS/nazwa miasta)
def toggle_forecast_mode():
    if forecast_chosen_mode.get() == 'city':
        entry1_forecast.config(state='normal')
        for widget in [entry_gps1_lat_forecast, entry_gps1_long_forecast]:
            widget.config(state='disabled')
    elif forecast_chosen_mode.get() == 'gps':
        entry1_forecast.config(state='disabled')
        for widget in [entry_gps1_lat_forecast, entry_gps1_long_forecast]:
            widget.config(state='normal')

# wyświetlenie ogólnych danych zanieczyszczenia (1 zakładka)
def display_data():


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

# zwrócenie danych zależnie od wybranej metody wyszukiwania (zakładka 1)
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

# zwrócenie danych zależnie od wybranej metody wyszukiwania (zakładka 3)
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

# zwrócenie danych zależnie od wybranej metody wyszukiwania (zakładka 2)
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

# wyświetlenie wykresu w nowym oknie z wartościami granicznymi kategorii
def show_thresholds_window():

    thresholds_window = tk.Toplevel(root)
    thresholds_window.title("Thresholds Chart")
    thresholds_window.geometry('1100x950')


    fig = display_treshhold_values()


    canvas = FigureCanvasTkAgg(fig, master=thresholds_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# wyświetlenie wykresu w nowym oknie ze zliczeniem kategorii
def show_category_count_window():
    try:
        data = adjust_search_mode_return_tab1()

        category_count_window = tk.Toplevel(root)
        category_count_window.title("Category Count Chart")
        category_count_window.geometry('800x600')
        lat = data[0]
        lon = data[1]

        fig = count_and_display_air_quality_categories(lat, lon)


        canvas = FigureCanvasTkAgg(fig, master=category_count_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    except Exception as e:
        data_display.config(text="Cannot display data for this input. Change the data and try again!")

# wyświetlenie wykresu w nowym oknie ze zmianą wartości składników w ciągu ostatniej doby
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

# wyświetlenie wykresu w nowym oknie ze zmianą wartości składników w ciągu ostatniego tygodnia
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

# wyświetlenie wykresu w nowym oknie z wartościa oraz kategorią w zależności od wybranego składnika w rozwijanej liście
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

# wyświetlenie wykresu w nowym oknie z porównaniem 2 miast
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

# wyświetlenie danych porównawczych w polu do wyświetlania danych
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

# wyświetlenie danych historycznych w polu do wyświetlania danych
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

# wyświetlenie danych regresji w polu do wyświetlania danych
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

# zmienienie etykiety o sposobie wyszukiwania danych (zakładka 3 - porównanie)
def update_mode_label():
    if compare_mode.get() == 'city':
        mode_label.set('Comparing by City')
    elif compare_mode.get() == 'gps':
        mode_label.set('Comparing by GPS')

# zmienienie etykiety o sposobie wyszukiwania danych (zakładka 2 - dane historyczne)
def update_historical_mode_label():
    if historical_chosen_mode.get() == 'city':
        mode_label_t2.set('Load historical data by City')
    elif historical_chosen_mode.get() == 'gps':
        mode_label_t2.set('Load historical data by GPS')

# zmienienie etykiety o sposobie wyszukiwania danych (zakładka 4 - regresja)
def update_forecast_mode_label():
    if forecast_chosen_mode.get() == 'city':
        mode_label_forecast.set('Load regression data by City')
    elif forecast_chosen_mode.get() == 'gps':
        mode_label_forecast.set('Load regression data by GPS')

# ładowanie zdjęć do zakładki nr. 5
def load_and_display_image(frame, path):
    try:
        image = Image.open(path)
        image = image.resize((200, 150), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        label = ttk.Label(frame, image=photo)
        label.image = photo
        label.pack(pady=10)
    except Exception as e:
        error_label = ttk.Label(frame, text=f"Error loading image: {path}", font=('Arial', 10), foreground='red')
        error_label.pack(pady=5)



root = tk.Tk()
root.title('Check the air pollution in your area!')
root.geometry('555x790')


# Zakładki
tab_control = ttk.Notebook(root)
tab_control.pack(expand=1, fill='both')

# Zakładka 1 --------------------------------------------------------------------------------------------
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='GPS- and name-based search')


options_frame = ttk.Frame(tab1)
options_frame.pack(fill='x', padx=10, pady=10)


left_frame = ttk.Frame(options_frame)
left_frame.pack(side='left', expand=True, fill='both', padx=10, pady=10)

right_frame = ttk.Frame(options_frame)
right_frame.pack(side='right', expand=True, fill='both', padx=10, pady=10)

# Wybór metody wyszukiwania
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

# Wybór metody wyszukiwania
city_radio = ttk.Radiobutton(right_frame, text='Search by City Name', variable=search_mode, value='city',
                             command=toggle_search_mode)
city_radio.pack(anchor='w', pady=5)

city_label = ttk.Label(right_frame, text='City:')
city_label.pack(anchor='w')
city_entry = ttk.Entry(right_frame)
city_entry.pack(anchor='w', fill='x', pady=2)

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



# zakładka 2 --------------------------------------------------------------------------------------------------

tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='Historical Data')
tab2.columnconfigure(0, weight=1)
tab2.columnconfigure(1, weight=1)

# wybór metody wyszukiwania
historical_chosen_mode = tk.StringVar(value='city')
mode_label_t2 = tk.StringVar(value='Loading historical data by City')

radio_city_t2 = ttk.Radiobutton(tab2, text='Load historical data by City', variable=historical_chosen_mode, value='city', command=lambda: [toggle_historical_mode(), update_historical_mode_label()])
radio_city_t2.grid(row=0, column=0, columnspan=2, pady=5)

radio_gps_t2 = ttk.Radiobutton(tab2, text='Load historical data by GPS', variable=historical_chosen_mode, value='gps', command=lambda: [toggle_historical_mode(), update_historical_mode_label()])
radio_gps_t2.grid(row=1, column=0, columnspan=2, pady=5)

mode_display_label_t2 = ttk.Label(tab2, textvariable=mode_label_t2, font=('Arial', 12, 'bold'))
mode_display_label_t2.grid(row=2, column=0, columnspan=2, pady=5)

# --- Kolumna 1: Miasto 1 ---
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

# wyświetlanie danych
label_area_t2 = tk.Label(tab2, text="data....", height=20, width=70, relief="solid", anchor="nw", justify="left", background='white', font=('Arial', 11))
label_area_t2.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

fetch_input_button = ttk.Button(tab2, text='Fetch Input', command=fetch_input_historical_data, width=30)
fetch_input_button.grid(row=10, column=0, columnspan=2, pady=10)

# przycisk ostatnie 24h wstępnie schowany-
last_7_days_button = ttk.Button(tab2, text='Last Week', command = show_pollutants_development_widnow_7days, width=30, padding=10)
last_24_hours_button = ttk.Button(tab2, text='Last 24h', command=show_pollutants_development_window_24h, width=30, padding=10)

toggle_historical_mode()


# zakładka 3 ------------------------------------------------------------------------------------------------------------

tab3 = ttk.Frame(tab_control)
tab_control.add(tab3, text='Pollution Compare')


tab3.columnconfigure(0, weight=1)
tab3.columnconfigure(1, weight=1)

# wybór metody wyszukiwania
compare_mode = tk.StringVar(value='city')
mode_label = tk.StringVar(value='Comparing by City')


radio_city = ttk.Radiobutton(tab3, text='Compare by City', variable=compare_mode, value='city', command=lambda: [toggle_compare_mode(), update_mode_label()])
radio_city.grid(row=0, column=0, columnspan=2, pady=5)

radio_gps = ttk.Radiobutton(tab3, text='Compare by GPS', variable=compare_mode, value='gps', command=lambda: [toggle_compare_mode(), update_mode_label()])
radio_gps.grid(row=1, column=0, columnspan=2, pady=5)

mode_display_label = ttk.Label(tab3, textvariable=mode_label, font=('Arial', 12, 'bold'))
mode_display_label.grid(row=2, column=0, columnspan=2, pady=5)

# --- Kolumna1: Miasto 1 ---
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

# --- Kolumna 2: Miasto 2 ---
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

# Wyświetlanie danych
label_area1 = tk.Label(tab3, text="City 1 data....", height=20, width=70, relief="solid", anchor="nw", justify="left", background='white', font=('Arial', 11))
label_area1.grid(row=9, column=0, padx=10, pady=10, sticky="nsew")

label_area2 = tk.Label(tab3, text="City 2 data....", height=20, width=70, relief="solid", anchor="nw", justify="left", background='white', font=('Arial', 11))
label_area2.grid(row=9, column=1, padx=10, pady=10, sticky="nsew")

# Przycisk porównania
compare_button = ttk.Button(tab3, text='Compare', command=fetch_input_comparison, width=20)
compare_button.grid(row=10, column=0, columnspan=2, pady=20)

show_chart_button = ttk.Button(tab3, text='Show Chart', command=on_click_comparison_chart, width=20)
show_chart_button.grid(row=11, column=0, columnspan=2, pady=7)
show_chart_button.grid_remove()

toggle_compare_mode()


# zakładka 4 ------------------------------------------------------------------------------------------------------------------------
tab4 = ttk.Frame(tab_control)
tab_control.add(tab4, text='Pollution forecast')
tab4.columnconfigure(0, weight=1)
tab4.columnconfigure(1, weight=1)

# wybór metody wyszukiwania
forecast_chosen_mode = tk.StringVar(value='city')
mode_label_forecast = tk.StringVar(value='Load regression data by City')

radio_city_forecast = ttk.Radiobutton(tab4, text='Regression based on city-name search', variable=forecast_chosen_mode, value='city', command=lambda: [toggle_forecast_mode(), update_forecast_mode_label()])
radio_city_forecast.grid(row=0, column=0, columnspan=2, pady=5)

radio_gps_forecast = ttk.Radiobutton(tab4, text='Regression based on GPS search', variable=forecast_chosen_mode, value='gps', command=lambda: [toggle_forecast_mode(), update_forecast_mode_label()])
radio_gps_forecast.grid(row=1, column=0, columnspan=2, pady=5)

mode_display_label_forecast = ttk.Label(tab4, textvariable=mode_label_forecast, font=('Arial', 12, 'bold'))
mode_display_label_forecast.grid(row=2, column=0, columnspan=2, pady=5)

# --- Kolumna1: Miasto 1 ---
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

# --- Wyświetlanie danych
label_area_forecast= tk.Label(tab4, text="data....", height=20, width=70, relief="solid", anchor="nw", justify="left", background='white', font=('Arial', 11))
label_area_forecast.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

fetch_regression_input_button = ttk.Button(tab4, text='Fetch Input', command = fetch_input_regression_data, width=30, padding = 15)
fetch_regression_input_button.grid(row=10, column=0, columnspan=2, pady=10)


toggle_forecast_mode()



# Zakładka 5 ---------------------------------------------------------------------------------------------------------------------
tab5 = ttk.Frame(tab_control)
tab_control.add(tab5, text='Project credits')


credits_frame = ttk.Frame(tab5, padding=20)
credits_frame.pack(expand=1, fill='both')


title_label = ttk.Label(credits_frame, text="Project Credits", font=('Arial', 18, 'bold'))
title_label.pack(pady=(10, 20))


credits_text = [
    "Project authors: Krzysztof Drobnik, Maksymilian Jurewicz",
    "Project name: Calculating air quality based on few basic pollutants\nusing Open Weather API and basic GUI",
    "University: University of Economics in Poznań",
    "Subject: Programming and Data Processing",
    "Supervisor: mgr. Adam Gałązkiewicz",
    "Field of study: Industry 4.0",
    "Study year: 1"
]


for text in credits_text:
    label = ttk.Label(credits_frame, text=text, font=('Arial', 12), anchor='w', justify='left')
    label.pack(anchor='w', pady=5)


separator = ttk.Separator(credits_frame, orient='horizontal')
separator.pack(fill='x', pady=(20, 10))



load_and_display_image(credits_frame, 'jpg1.jpg')


load_and_display_image(credits_frame, 'jpg2.jpg')

root.mainloop()












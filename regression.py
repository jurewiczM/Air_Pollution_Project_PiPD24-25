import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Zaciagnij dane 
def get_air_quality_data(api_key, location):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    historical_data = []

    for day in range(8):
        date = start_date + timedelta(days=day)
        timestamp = int(date.timestamp())
        url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={location['lat']}&lon={location['lon']}&start={timestamp}&end={timestamp + 86400}&appid={api_key}"
        response = requests.get(url)
        data = response.json()

        # Error handling
        if response.status_code != 200 or 'list' not in data:
            print(f"Error fetching data for date: {date}. Status code: {response.status_code}")
            continue

        historical_data.extend(data['list'])

    return historical_data

# API klucz
api_key = 'API_KEY'
location = {'lat': 40.7128, 'lon': -74.0060}

components_list = get_air_quality_data(api_key, location)   

# Dane dla regresji
data_x = pd.DataFrame([item['components'] for item in components_list])
data_y = pd.DataFrame([item['main']['aqi'] for item in components_list], columns=['aqi'])
X = data_x[['co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3']]
y = data_y['aqi']

# Skalary
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# podzial na dane treningowe i testowe
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# model gradient boosting
xgboost_model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)


xgboost_model.fit(X_train, y_train)


single_instance = X_test[0].reshape(1, -1) 
predicted_aqi = xgboost_model.predict(single_instance)

# Print the predicted AQI value
print(f"Predicted AQI for the selected instance: {predicted_aqi[0]}")




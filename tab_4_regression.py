import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
from datetime import datetime, timedelta, timezone


def get_air_quality_prediction(location):
    api_key = 'API'

    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=7)
    historical_data = []

    for day in range(8):
        date = start_date + timedelta(days=day)
        timestamp = int(date.timestamp())
        url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={location['lat']}&lon={location['lon']}&start={timestamp}&end={timestamp + 86400}&appid={api_key}"
        response = requests.get(url)
        data = response.json()


        if response.status_code != 200 or 'list' not in data:
            print(f"Error fetching data for date: {date}. Status code: {response.status_code}")
            continue

        historical_data.extend(data['list'])

    # Przygotowanie danych do regresji
    data_x = pd.DataFrame([item['components'] for item in historical_data])
    data_y = pd.DataFrame([item['main']['aqi'] for item in historical_data], columns=['aqi'])
    X = data_x[['co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3']]
    y = data_y['aqi']

    # Normalizacja danych
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Podział na dane treningowe i testowe
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Trening modelu gradient boosting
    xgboost_model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)
    xgboost_model.fit(X_train, y_train)

    # Ocena modelu
    y_pred = xgboost_model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    # Przewidywanie dla wybranego przykładu
    single_instance = X_test[0].reshape(1, -1)
    predicted_aqi = xgboost_model.predict(single_instance)


    results = {
        "predicted_aqi": predicted_aqi[0],
        "r2_score": r2,
        "mean_squared_error": mse,
        "mean_absolute_error": mae
    }


    return results

# API klucz i lokalizacja

location = {'lat': 40.7128, 'lon': -74.0060}


results = get_air_quality_prediction(location)
#print(results)

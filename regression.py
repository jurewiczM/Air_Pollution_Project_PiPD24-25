import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np


def get_air_quality_data(api_key, location):
  url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={location['lat']}&lon={location['lon']}&appid={api_key}"
  response = requests.get(url)
  data = response.json()
  return data['list'][0]['components']

def calculate_aqi(components):
  aqi = (components['pm2_5'] + components['pm10'] + components['no2'] + components['so2'] + components['o3'] + components['co']) / 6
  return aqi


api_key = 'your_api_key_here'
location = {'lat': 40.7128, 'lon': -74.0060}  


components = get_air_quality_data(api_key, location)


data = pd.DataFrame([components])
X = data[['pm2_5', 'pm10', 'no2', 'so2', 'o3', 'co']]
y = np.array([calculate_aqi(components)])


model = LinearRegression()
model.fit(X, y)


predicted_aqi = model.predict(X)
print(f"Predicted AQI: {predicted_aqi[0]}")
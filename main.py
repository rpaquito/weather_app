from fastapi import FastAPI
import requests

app = FastAPI()
api_key = "6c0f892c6761c4e5f56e534c36075e9f"  # openweathermap API key


@app.get("/")
async def root():
    return {"message": "Hello, please use /temperature or /rain paths"}


# Function to fetch weather forecast
def get_weather_forecast(city: str, days: int, api_key: str):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"
    response = requests.get(url)
    forecast = []

    if response.status_code != 200:
        print("Error connecting to Openweatherapi")
        print(f"Error message: {response.text}")
    else:
        data = response.json()
        forecast = data['list'][days - 1]  # Weather forecast for the specified day

    return forecast


# Endpoint to get the temperature
@app.get("/temperature")
def get_temperature(city: str = "Lisbon", days: int = 3):
    forecast = get_weather_forecast(city, days, api_key)
    if not forecast:
        return {"temperature_celsius": "Unable to fetch data from openweathermap"}
    else:
        temperature_kelvin = forecast['main']['temp']
        temperature_celsius = temperature_kelvin - 273.15
        return {"temperature_celsius": temperature_celsius}


# Endpoint to get the rain
@app.get("/rain")
def check_rain(city: str = "Lisbon", days: int = 3):
    forecast = get_weather_forecast(city, days, api_key)
    if not forecast:
        return {"temperature_celsius": "Unable to fetch data from openweathermap"}
    else:
        weather = forecast['weather'][0]['main']
        return {"will_it_rain": weather.lower() == 'rain'}

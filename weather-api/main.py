from fastapi import FastAPI
import httpx

app = FastAPI(title="Weather API")

WEATHER_API_KEY = "YOUR_API_KEY"
WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"


@app.get("/")
def home():
    return {
        "message": "Weather API is running"
    }


@app.get("/weather")
def get_weather(city: str):
    params = {
        "key": WEATHER_API_KEY,
        "q": city
    }

    response = httpx.get(WEATHER_API_URL, params=params)

    return response.json()
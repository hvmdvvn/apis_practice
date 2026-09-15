from fastapi import FastAPI
from pydantic import BaseModel
import httpx

app = FastAPI(title="Weather API")

WEATHER_API_KEY = "YOUR_API_KEY"
WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"


class WeatherResponse(BaseModel):
    city: str
    country: str
    temperature_c: float
    condition: str
    humidity: int


@app.get("/")
def home():
    return {
        "message": "Weather API is running"
    }


@app.get("/weather", response_model=WeatherResponse)
def get_weather(city: str):
    params = {
        "key": WEATHER_API_KEY,
        "q": city
    }

    response = httpx.get(WEATHER_API_URL, params=params)
    data = response.json()

    return {
        "city": data["location"]["name"],
        "country": data["location"]["country"],
        "temperature_c": data["current"]["temp_c"],
        "condition": data["current"]["condition"]["text"],
        "humidity": data["current"]["humidity"]
    }
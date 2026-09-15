from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx
import os

load_dotenv()

app = FastAPI(title="Weather API")

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
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
def get_weather(
    city: str = Query(..., min_length=2, max_length=100)
):
    params = {
        "key": WEATHER_API_KEY,
        "q": city
    }

    try:
        response = httpx.get(
            WEATHER_API_URL,
            params=params,
            timeout=10
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Unable to connect to weather service"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Weather service returned an error"
        )

    data = response.json()

    if "error" in data:
        error_code = data["error"]["code"]

        if error_code == 1006:
            raise HTTPException(
                status_code=404,
                detail="City not found"
            )

        raise HTTPException(
            status_code=502,
            detail="Weather service returned an error"
        )

    return {
        "city": data["location"]["name"],
        "country": data["location"]["country"],
        "temperature_c": data["current"]["temp_c"],
        "condition": data["current"]["condition"]["text"],
        "humidity": data["current"]["humidity"]
    }
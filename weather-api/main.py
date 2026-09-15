from fastapi import FastAPI

app = FastAPI(title="Weather API")


@app.get("/")
def home():
    return {
        "message": "Weather API is running"
    }


@app.get("/weather")
def get_weather(city: str):
    return {
        "city": city
    }
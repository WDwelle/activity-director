import os
import requests
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()
OWM_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

@tool(
    description="Given a 'lat,lng' string, returns the current weather description and temperature in °F."
)
def get_weather(location: str) -> str:
    lat, lng = [s.strip() for s in location.split(",")]
    endpoint = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lng,
        "appid": OWM_KEY,
        "units": "imperial"  # Fahrenheit
    }
    resp = requests.get(endpoint, params=params).json()
    desc = resp["weather"][0]["description"].capitalize()
    temp = resp["main"]["temp"]
    return f"{desc}, {temp}°F"

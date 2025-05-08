import os
import requests
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

@tool
def find_activities_nearby(location: str, keyword: str = "things to do", radius: int = 5000) -> str:
    """Finds nearby activities based on a location string (lat,lng)."""
    endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": location,
        "radius": radius,
        "keyword": keyword,
        "key": GOOGLE_MAPS_API_KEY
    }

    response = requests.get(endpoint, params=params)
    results = response.json().get("results", [])

    if not results:
        return "No activities found nearby."

    suggestions = []
    for place in results[:10]:
        name = place.get("name")
        address = place.get("vicinity")
        rating = place.get("rating", "N/A")
        suggestions.append(f"{name} — {address} (⭐ {rating})")

    return "\n".join(suggestions)
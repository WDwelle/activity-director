import os
import requests
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

@tool(
    description="Finds nearby activities based on a location string (lat,lng). "
                "Returns up to 10 places with name, address, and rating."
)
def find_activities_nearby(location: str, keyword: str = "things to do", radius: int = 5000) -> str:
    endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": location,
        "radius": radius,
        "keyword": keyword,
        "key": GOOGLE_MAPS_API_KEY
    }
    resp = requests.get(endpoint, params=params).json()
    places = resp.get("results", [])
    if not places:
        return "No activities found nearby."
    out = []
    for p in places[:10]:
        out.append(f"{p['name']} — {p.get('vicinity','')} (⭐ {p.get('rating','N/A')})")
    return "\n".join(out)

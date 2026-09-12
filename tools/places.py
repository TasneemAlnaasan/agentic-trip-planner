import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEOAPIFY_API_KEY")


def get_places(latitude, longitude, radius=5000, limit=10):
    """
    Fetches nearby tourist places for a location, cleaned up and ready for the model
    """
    url = "https://api.geoapify.com/v2/places"

 
    # a fixed value 
    categories = "tourism.sights"

    # build the filter string first
    filter_string = f"circle:{longitude},{latitude},{radius}"

    params = {
        "categories": categories,
        "filter": filter_string,
        "limit": limit,
        "apiKey": api_key,
    }

    response = requests.get(url, params=params)
    data = response.json()

    # build a clean list, one entry per place
    result = []
    for feature in data["features"]:
        props = feature["properties"]

        result.append({
            "name": props.get("name", "unknown"),
            "formatted": props.get("formatted", ""),
            "category": props["categories"][-1].split(".")[-1],
            "lat": props["lat"],
            "lon": props["lon"],
        })

    return result

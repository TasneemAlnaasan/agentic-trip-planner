import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEOAPIFY_API_KEY")


def get_coordinates(place_name):
    """
    Converts a place name string into precise coordinates (lat/lon)
    """
    url = "https://api.geoapify.com/v1/geocode/search"
    params = {"text": place_name, "apiKey": api_key}

    response = requests.get(url, params=params)
    data = response.json()

    if len(data["features"]) > 0:
        properties = data["features"][0]["properties"]
        result = {
            "lat": properties["lat"],
            "lon": properties["lon"],
            "formatted": properties["formatted"],
        }
        return result
    else:
        return None

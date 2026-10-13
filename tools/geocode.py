
import requests
from config import settings

api_key=settings.geoapify_api_key


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

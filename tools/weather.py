import requests

def code_to_condition(code):
 
    if code == 0:
        return "clear"
    elif code in [1, 2, 3]:
        return "partly cloudy"
    elif code in [45, 48]:
        return "fog"
    elif 51 <= code <= 67:
        return "rain"
    elif 71 <= code <= 77:
        return "snow"
    elif 80 <= code <= 82:
        return "rain showers"
    elif code >= 95:
        return "storm"
    else:
        return "unknown"


def get_weather(latitude, longitude, days=3):
 
    url = "https://api.open-meteo.com/v1/forecast"

    max_forecast_days = 16
    days = min(days, max_forecast_days)

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,weathercode",
        "timezone": "auto",
        "forecast_days": days,
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "daily" not in data:
        return []

    daily = data["daily"]

   
    
    result = [ ]
    for date, temp_max, temp_min, code in zip(
        daily["time"], daily["temperature_2m_max"], daily["temperature_2m_min"], daily["weathercode"]
    ):
        result.append({
            "date": date,
            "temp_max": temp_max,
            "temp_min": temp_min,
            "condition": code_to_condition(code),
        })

    return result

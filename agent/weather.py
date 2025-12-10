# agent/weather.py
import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv, find_dotenv

# load .env from the repository root (find_dotenv searches parent dirs)
load_dotenv(find_dotenv())

# support both names in case .env uses WEATHER_API_KEY
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY") or os.getenv("WEATHER_API_KEY")


def get_weather(city: str) -> Dict[str, Any]:
    """Return structured weather info for `city`.

    Returns a dict with keys: city, temp_c, description, feels_like, humidity, raw
    Raises RuntimeError if API key missing, ValueError for API-level errors.
    """
    if not OPENWEATHER_API_KEY:
        raise RuntimeError("OPENWEATHER_API_KEY (or WEATHER_API_KEY) not set in environment")

    city_input = city.strip() if city is not None else ""
    if not city_input:
        raise ValueError("Empty city name provided")

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_input, "units": "metric", "appid": OPENWEATHER_API_KEY}

    try:
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        # Try to provide a friendly API error message
        try:
            data = resp.json()
            code = data.get("cod", "")
            message = data.get("message", "")
            raise ValueError(f"OpenWeather error: {code} {message}")
        except Exception:
            raise
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network error when calling OpenWeather: {e}")

    # parse JSON response
    data = resp.json()

    weather_desc = (data.get("weather") or [{}])[0].get("description")
    temp = data.get("main", {}).get("temp")
    feels_like = data.get("main", {}).get("feels_like")
    humidity = data.get("main", {}).get("humidity")

    result = {
        "city": data.get("name") or city_input,
        "temp_c": temp,
        "description": weather_desc,
        "feels_like": feels_like,
        "humidity": humidity,
        "raw": data,
    }
    return result
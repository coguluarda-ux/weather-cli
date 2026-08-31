#!/usr/bin/env python3
"""
Weather CLI - A simple command-line weather tool.
Fetches live weather for any city using the free Open-Meteo API.
No API key required.

Usage:
    python weather.py                 # shows weather for Istanbul (default)
    python weather.py London          # shows weather for London
    python weather.py "New York"      # city names with spaces need quotes
"""

import sys
import json
import urllib.request
import urllib.parse

# Default city if the user doesn't type one
DEFAULT_CITY = "Istanbul"


def geocode_city(city_name):
    """Convert a city name into latitude and longitude using Open-Meteo's geocoding API."""
    encoded_city = urllib.parse.quote(city_name)
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_city}&count=1&language=en&format=json"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception:
        print(f"Could not find city: {city_name}")
        sys.exit(1)

    results = data.get("results", [])
    if not results:
        print(f"Could not find city: {city_name}")
        sys.exit(1)

    first = results[0]
    return first["latitude"], first["longitude"], first["name"], first.get("country", "")


def fetch_weather(lat, lon):
    """Fetch current weather and a 5-day forecast from Open-Meteo."""
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
        f"weather_code,wind_speed_10m,wind_direction_10m"
        f"&daily=weather_code,temperature_2m_max,temperature_2m_min"
        f"&timezone=auto&forecast_days=5"
    )
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception:
        print("Could not fetch weather data. Check your internet connection.")
        sys.exit(1)


# Map Open-Meteo weather codes to human-readable descriptions
WEATHER_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Rain showers",
    81: "Heavy rain showers",
    82: "Violent rain showers",
    85: "Snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Heavy thunderstorm with hail",
}


def describe_weather(code):
    """Turn a weather code into a readable description."""
    return WEATHER_DESCRIPTIONS.get(code, f"Unknown (code {code})")


def wind_direction(degrees):
    """Convert wind degrees to a compass direction."""
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(degrees / 45) % 8
    return directions[index]


def print_current(city, country, data):
    """Print the current weather block."""
    current = data["current"]
    temp = current["temperature_2m"]
    feels = current["apparent_temperature"]
    humidity = current["relative_humidity_2m"]
    code = current["weather_code"]
    wind_speed = current["wind_speed_10m"]
    wind_dir = wind_direction(current["wind_direction_10m"])

    print()
    print(f"  {"=" * 40}")
    print(f"   Current Weather - {city}, {country}")
    print(f"  {"=" * 40}")
    print(f"   Conditions : {describe_weather(code)}")
    print(f"   Temperature: {temp}C (feels like {feels}C)")
    print(f"   Humidity   : {humidity}%")
    print(f"   Wind       : {wind_speed} km/h {wind_dir}")
    print()


def print_forecast(data):
    """Print the 5-day forecast block."""
    daily = data["daily"]
    dates = daily["time"]
    codes = daily["weather_code"]
    highs = daily["temperature_2m_max"]
    lows = daily["temperature_2m_min"]

    print(f"  {"=" * 40}")
    print(f"   5-Day Forecast")
    print(f"  {"=" * 40}")
    for i in range(len(dates)):
        print(f"   {dates[i]}  {describe_weather(codes[i]):<22}  {lows[i]}C - {highs[i]}C")
    print()


def main():
    # Get the city from command-line arguments, or use the default
    city = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else DEFAULT_CITY

    # Step 1: Turn the city name into coordinates
    lat, lon, resolved_name, country = geocode_city(city)

    # Step 2: Fetch weather data for those coordinates
    data = fetch_weather(lat, lon)

    # Step 3: Show the results
    print_current(resolved_name, country, data)
    print_forecast(data)


if __name__ == "__main__":
    main()

# Weather CLI

A simple command-line weather tool that fetches live weather and a 5-day forecast for any city. No API key required — it uses the free [Open-Meteo](https://open-meteo.com/) API.

## Features

- Current temperature, "feels like" temperature, and humidity
- Wind speed and direction
- Human-readable weather conditions (clear, rain, snow, thunderstorm, etc.)
- 5-day forecast with daily highs and lows
- Works for any city in the world
- Default city: Istanbul
- No external dependencies — runs on pure Python

## Requirements

- Python 3.6 or newer
- An internet connection

That's it. No `pip install` needed.

## Usage

```bash
# Default city (Istanbul)
python weather.py

# Any city
python weather.py London
python weather.py Tokyo
python weather.py "New York"
```

### Example output

```
========================================
 Current Weather - Istanbul, Turkey
========================================
 Conditions : Clear sky
 Temperature: 24C (feels like 25C)
 Humidity   : 45%
 Wind       : 12 km/h NE

========================================
 5-Day Forecast
========================================
 2026-08-31  Clear sky             18C - 27C
 2026-09-01  Partly cloudy         19C - 28C
 2026-09-02  Slight rain           17C - 24C
 2026-09-03  Moderate rain         16C - 22C
 2026-09-04  Mainly clear          18C - 26C
```

## How it works

1. **Geocoding** — The city name is sent to Open-Meteo's geocoding API, which returns latitude and longitude.
2. **Forecast** — Those coordinates are sent to the forecast API to get current conditions and daily forecasts.
3. **Display** — The results are formatted and printed to the terminal.

All communication uses Python's built-in `urllib` module — no third-party libraries.

## Customization

Change the default city by editing this line in `weather.py`:

```python
DEFAULT_CITY = "Istanbul"
```

## License

MIT — free to use, modify, and share.

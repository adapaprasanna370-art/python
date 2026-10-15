
from flask import Flask, request, render_template_string
import urllib.request
import urllib.parse
import json

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WeatherNow</title>
<style>
* { box-sizing: border-box; }
body {
    margin: 0; padding: 30px 15px; min-height: 100vh;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #dbeafe, #e0e7ff);
    color: #172554;
}
.container { max-width: 700px; margin: auto; }
header { text-align: center; margin-bottom: 25px; }
header .icon { font-size: 48px; }
h1 { margin: 8px 0; }
.subtitle { color: #64748b; }
.card {
    background: white; padding: 25px; border-radius: 20px;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px #1e40af12;
}
label { display: block; font-weight: bold; margin-bottom: 10px; }
.search { display: flex; gap: 10px; }
input {
    flex: 1; min-width: 0; padding: 14px;
    border: 1px solid #cbd5e1; border-radius: 10px;
    font-size: 16px;
}
button {
    border: 0; border-radius: 10px; padding: 14px 18px;
    background: #2563eb; color: white; font-weight: bold;
    cursor: pointer;
}
button:hover { background: #1d4ed8; }
.error {
    background: #fee2e2; color: #991b1b;
    padding: 12px; border-radius: 10px; margin-top: 15px;
}
.weather { text-align: center; }
.city { font-size: 26px; margin-bottom: 8px; }
.condition { color: #2563eb; font-size: 19px; margin-top: 20px; }
.temp { font-size: 65px; font-weight: bold; margin: 10px; }
.muted { color: #64748b; font-size: 14px; }
.grid {
    display: grid; grid-template-columns: repeat(2, 1fr);
    gap: 12px; margin-top: 25px; text-align: left;
}
.detail { background: #eff6ff; padding: 17px; border-radius: 13px; }
.detail p { color: #64748b; font-size: 13px; margin: 8px 0; }
.detail strong { font-size: 19px; }
footer { text-align: center; color: #64748b; font-size: 13px; }
a { color: #2563eb; }
@media(max-width: 480px) {
    .search { flex-direction: column; }
    button { width: 100%; }
    .card { padding: 18px; }
    .temp { font-size: 52px; }
}
</style>
</head>
<body>
<div class="container">
    <header>
        <div class="icon">🌤️</div>
        <h1>WeatherNow</h1>
        <p class="subtitle">Live weather for any city in the world</p>
    </header>

    <section class="card">
        <form method="POST">
            <label for="city">Enter city name</label>
            <div class="search">
                <input id="city" name="city" placeholder="e.g. Hyderabad, London"
                       value="{{ city }}" required>
                <button type="submit">🔍 Get Weather</button>
            </div>
        </form>
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
    </section>

    {% if weather %}
    <section class="card weather">
        <div class="city">📍 {{ weather.city }}</div>
        <div class="muted">{{ weather.region }} {{ weather.country }}</div>
        <div class="condition">{{ weather.condition }}</div>
        <div class="temp">{{ weather.temp }}°C</div>
        <div class="muted">Feels like {{ weather.feels }}°C</div>
        <p class="muted">Local time: {{ weather.time }}</p>

        <div class="grid">
            <div class="detail">
                <div>💧 Humidity</div>
                <p>Relative humidity</p>
                <strong>{{ weather.humidity }}%</strong>
            </div>
            <div class="detail">
                <div>💨 Wind speed</div>
                <p>Current wind</p>
                <strong>{{ weather.wind }} km/h</strong>
            </div>
            <div class="detail">
                <div>🌧️ Precipitation</div>
                <p>Current precipitation</p>
                <strong>{{ weather.rain }} mm</strong>
            </div>
            <div class="detail">
                <div>🌡️ Temperature</div>
                <p>Current temperature</p>
                <strong>{{ weather.temp }}°C</strong>
            </div>
        </div>
    </section>
    {% endif %}

    <footer>
        Weather data by
        <a href="https://open-meteo.com/" target="_blank"
           rel="noopener noreferrer">Open-Meteo</a> · Free API, no key needed
    </footer>
</div>
</body>
</html>
"""

CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy",
    3: "Overcast", 45: "Fog", 48: "Fog",
    51: "Light drizzle", 53: "Moderate drizzle",
    55: "Heavy drizzle", 61: "Light rain",
    63: "Moderate rain", 65: "Heavy rain",
    71: "Light snow", 73: "Moderate snow",
    75: "Heavy snow", 80: "Rain showers",
    81: "Moderate rain showers", 82: "Heavy rain showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail",
    99: "Thunderstorm with heavy hail"
}

def fetch_json(url, params):
    query = urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url + "?" + query,
        headers={"User-Agent": "WeatherNow/1.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))

def get_weather(city):
    places = fetch_json(
        "https://geocoding-api.open-meteo.com/v1/search",
        {"name": city, "count": 1, "language": "en", "format": "json"}
    ).get("results", [])

    if not places:
        return None

    place = places[0]
    data = fetch_json(
        "https://api.open-meteo.com/v1/forecast",
        {
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": (
                "temperature_2m,relative_humidity_2m,"
                "apparent_temperature,precipitation,"
                "weather_code,wind_speed_10m"
            ),
            "timezone": "auto"
        }
    )

    current = data["current"]
    return {
        "city": place["name"],
        "region": place.get("admin1", ""),
        "country": place.get("country", ""),
        "time": current.get("time", ""),
        "condition": CODES.get(
            current["weather_code"], "Other conditions"
        ),
        "temp": current["temperature_2m"],
        "feels": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "wind": current["wind_speed_10m"],
        "rain": current["precipitation"]
    }

@app.route("/", methods=["GET", "POST"])
def home():
    city = ""
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if not city:
            error = "Please enter a city name."
        else:
            try:
                weather = get_weather(city)
                if weather is None:
                    error = "City not found. Please try another name."
            except Exception:
                error = "Could not fetch weather. Check your internet connection."

    return render_template_string(
        HTML, city=city, weather=weather, error=error
    )

if __name__ == "__main__":
    app.run(debug=True)

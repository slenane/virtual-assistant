import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# OpenWeatherMap API Key
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(coords):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={coords['lat']}&lon={coords['lon']}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data['cod'] != 200:
            return f"Sorry, I could not find weather for your location."
        
        return {
            "name": data["name"],
            "icon": data["weather"][0]["icon"],
            "description": data["weather"][0]["description"],
            "temp": round(data["main"]["temp"]),
            "temp_max": round(data["main"]["temp_max"]),
            "temp_min": round(data["main"]["temp_min"]),
            "wind":  data["wind"]["speed"],
            "humidity":  data["main"]["humidity"],
            "visibility":  data["visibility"] / 1000, 

        }
    except Exception as e:
        return f"Something went wrong: {e}"
    
def save_city_preference(city):
    with open("config.txt", "w") as f:
        f.write(city.strip())

def load_city_preference():
    try:
        with open("config.txt", 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""
    
def get_city_preference():
    city = load_city_preference()
    if not city:
        city = input("🌆 What city should I use for your weather updates? ").strip()
        save_city_preference(city)
    return city

# Weather example
# {'coord': {'lon': 9.1922, 'lat': 45.4722}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 17.84, 'feels_like': 17.9, 'temp_min': 16.64, 'temp_max': 18.77, 'pressure': 1001, 'humidity': 85, 'sea_level': 1001, 'grnd_level': 987}, 'visibility': 10000, 'wind': {'speed': 3.6, 'deg': 100}, 'clouds': {'all': 40}, 'dt': 1746429760, 'sys': {'type': 2, 'id': 2012644, 'country': 'IT', 'sunrise': 1746417932, 'sunset': 1746470054}, 'timezone': 7200, 'id': 6542283, 'name': 'Milan', 'cod': 200}
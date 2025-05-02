import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# OpenWeatherMap API Key
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data['cod'] != 200:
            return f"Sorry, I could not find weather for '{city}'."
        
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]

        return f"In {city.title()}, it's currently {weather} with a temperature of {temp}°C (feels like {feels_like}°C)."
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
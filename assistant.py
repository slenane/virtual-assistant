import os
from dotenv import load_dotenv
import requests
from datetime import datetime

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
        return f"Something wen wrong: {e}"


def get_response(command):
    command = command.lower()
    
    if "hello" in command:
        return "Hi there! How can I help you?"
    elif "time" in command:
        now = datetime.now().strftime("%H:%M")
        return f"The time is {now}."
    elif "weather in" in command:
        city = command.split("weather in")[-1].strip()
        if city:
            return get_weather(city)
        else:
            return "Please specify a city."
    elif command in ["bye", "exit", "quit"]:
        return "Goodbye! Have a great day!"
    else:
        return "I'm not sure how to respond to that."

def main():
    print("👋 Hello! I'm your assistant. Type something:")
    
    while True:
        user_input = input("> ")
        response = get_response(user_input)
        print(response)
        
        if response.startswith("Goodbye"):
            break

if __name__ == "__main__":
    main()


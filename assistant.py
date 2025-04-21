import os
from dotenv import load_dotenv
import requests
from datetime import datetime
import dateparser
import re

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
    
def add_to_todo(task, date_str=None):
    # Create todos folder if it doesn't exist
    todo_dir = "todos"
    os.makedirs(todo_dir, exist_ok=True)

    # Default to today if no date provided
    if date_str:
        parsed_date = dateparser.parse(date_str)
    else:
        parsed_date = datetime.now()

    if not parsed_date:
        return "Sorry, I couldn't understand the date you mentioned."

    date_str_formatted = parsed_date.strftime("%Y-%m-%d")
    todo_file = os.path.join(todo_dir, f"{date_str_formatted}.txt")

    # Append the task to the file
    with open(todo_file, "a") as f:
        f.write(f"- {task}\n")

    return f"Task added to your todo list for {date_str_formatted}."

def get_todays_todo():
    todo_dir = "todos"
    today = datetime.now().strftime("%Y-%m-%d")
    todo_file = os.path.join(todo_dir, f"{today}.txt")

    if not os.path.exists(todo_file):
        return "You have no tasks on you todo list for today."
    
    with open(todo_file, 'r') as f:
        tasks = f.readlines()

    if not tasks:
        return "Your todo list is empty for today"
    
    formatted_tasks = "\n".join(task.strip() for task in tasks)
    return f"Here's your todo list for today ({today}):\n{formatted_tasks}"


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
    elif command.lower().startswith("add "):
        match = re.match(r"add (.+) to my todo list(?: for (.+))?", command.lower())

        if match:
            task = match.group(1).strip()
            date_str = match.group(2).strip() if match.group(2) else None
            return add_to_todo(task, date_str)
        else:
            return "Sorry, I couldn't understand that task"
    elif "what's on my todo list" in command.lower() or "show my todo list" in command.lower():
        return get_todays_todo()
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


import os
from dotenv import load_dotenv
import requests
from datetime import datetime
import dateparser
import re
import argparse
import ollama

# Load environment variables
load_dotenv()

# OpenWeatherMap API Key
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def ask_llm_local(prompt, history=[]):
    response = ollama.chat(
        model='llama3',
        messages=history + [{'role': "user", "content": prompt}]
    )
    answer = response['message']['content']
    return answer, history + [{"role": "assistant", "content": answer}]

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

def get_daily_briefing(city=""):
    print("\n🌅 Daily Briefing 🌅")
    print("--------------------")

    # Show weather
    if city: 
        weather = get_weather(city)
        print(f"\nWeather today in {city.title()}: \n{weather}")
    else:
        print("Weather not set")

    # Show today's todo list
    todo = get_todays_todo()
    print(f"\nToday's To-Do List: \n{todo}\n")

def save_city_preference(city):
    with open("config.txt", "w") as f:
        f.write(city.strip())

def load_city_preference():
    try:
        with open("config.txt", 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""
        

def handle_custom_commands(command):
    command = command.lower()
    
    if "weather in" in command:
        city = command.split("weather in")[-1].strip()
        if city:
            return get_weather(city)
        else:
            return "Please specify a city."
        
    elif command.lower().startswith("add ") and "todo list" in command.lower():
        match = re.match(r"add (.+) to my todo list(?: for (.+))?", command.lower())

        if match:
            task = match.group(1).strip()
            date_str = match.group(2).strip() if match.group(2) else None
            return add_to_todo(task, date_str)
        else:
            return "Sorry, I couldn't understand that task"
        
    elif "what's on my todo list" in command.lower() or "show my todo list" in command.lower():
        return get_todays_todo()
    
    # Fallback - trigger LLM chat
    return None
    

def print_help():
    help_text = """
Virtual Assistant Help Guide
----------------------------

You can interact with the assistant using natural language. Here are some things you can do:

🗣️ General Commands:
  - What's the weather in <city>?
  - Tell me the weather for today in <city>

📝 To-Do List Commands:
  - Add <task> to my todo list
    (e.g., add walk the dog to my todo list)

More features coming soon...

To display this help guide:
  python assistant.py --help
"""

    print(help_text)

def main():
    city = load_city_preference()
    if not city:
        city = input("🌆 What city should I use for your weather updates? ").strip()
        save_city_preference(city)

    get_daily_briefing(city)

    print("Assistant:👋 Hello! I'm your assistant. How can I help you today?")
    
    chat_history = []

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            break

        response = handle_custom_commands(user_input)

        if response is None:
            # Let LLM handle it
            response, chat_history = ask_llm_local(user_input, chat_history)

        print(f"\nAssistant: {response}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--help", action="store_true")
    args = parser.parse_args()

    if args.help:
        print_help()
        exit()

    main()


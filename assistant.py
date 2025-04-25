import re
import argparse

from core import get_weather, get_city_preference,get_todays_todo, add_to_todo, ask_llm_local

def get_daily_briefing(city=""):
    briefing = ""
    briefing += "\n🌅 Daily Briefing 🌅"
    briefing += "\n--------------------"

    # Show weather
    if city: 
        weather = get_weather(city)
        briefing += f"\n\nWeather today in {city.title()}: \n{weather}"
    else:
        briefing += "\nWeather not set"

    # Show today's todo list
    todo = get_todays_todo()
    briefing += f"\n\nToday's To-Do List: \n{todo}\n"

    return briefing

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


def get_greeting():
    briefing = get_daily_briefing(get_city_preference())
    initial_message = "\nAssistant:👋 Hello! I'm your assistant. How can I help you today?"
    return briefing + initial_message

def main():
    print(get_greeting())
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


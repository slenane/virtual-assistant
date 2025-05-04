import argparse
from .core import get_weather, get_city_preference, ensure_ollama_running, ask_llm_local, get_todays_events


# Run ollama in the background
ensure_ollama_running()


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

    # Show google calendar events
    events = get_todays_events()
    briefing += "\n\nToday's Google Calendar Events:"
    if len(events): 
        for event in events:
            briefing += f"\n{event}"
    else: 
        briefing += f"\n\nNo calendar events today"


    briefing += "\n--------------------"

    return briefing

def handle_custom_commands(command):
    command = command.lower()
    if "weather in" in command:
        city = command.split("weather in")[-1].strip()
        if city:
            return get_weather(city)
        else:
            return "Please specify a city."
    
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

def initialize_assistant(): 
    weather = get_weather(get_city_preference())
    events = get_todays_events()

    return {"weather": weather, "events": events}


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


from .core import get_weather, load_chat_history, ensure_ollama_running, ask_llm_local, get_todays_events, log_chat

# Run ollama in the background
ensure_ollama_running()

chat_history = []

def initialize_assistant(coords): 
    global chat_history
    weather = get_weather(coords)
    events = get_todays_events()
    chat_history = load_chat_history()

    return {"weather": weather, "events": events, "chat": chat_history}

def handle_user_input(user_input):
    global chat_history

    log_chat("you", user_input)

    response, chat_history = ask_llm_local(user_input, load_chat_history())

    print(response, chat_history)
    response = log_chat("assistant", response)

    return response


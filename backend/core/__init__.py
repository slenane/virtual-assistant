# core/__init__.py
from .chat_history import log_chat, load_chat_history
from .google_integration import get_todays_events, create_calendar_event
from .llm import ask_llm_local, ensure_ollama_running, local_llm_event_parse
from .todo import get_todays_todo, add_to_todo
from .weather import get_weather, get_city_preference
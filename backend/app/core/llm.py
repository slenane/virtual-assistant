import ollama
import subprocess
import markdown
import datetime
from zoneinfo import ZoneInfo
import re
import json
from .google_integration import create_calendar_event

# Check if Ollama is running; if not, start it
def ensure_ollama_running():
    try:
        subprocess.run(["ollama", "list"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        subprocess.Popen(["ollama", "serve"])

def ask_llm_local(prompt, history=[]):
    now = datetime.datetime.now(ZoneInfo("Europe/Rome"))
    today_date_time = now.strftime("%Y-%m-%d %H:%M:%S %Z%z")

    prompt = f"""
    You are a smart assistant. Your task is to decide if the user is trying to create a calendar event. If they are, extract the event details. Otherwise, respond normally.

    Return a JSON object in **one** of the following formats:

    If the user **is creating a calendar event**, respond like this:
    {{
        "is_event": true,
        "title": "Event Title",
        "start_time": "YYYY-MM-DDTHH:MM:SS+TZ",
        "end_time": "YYYY-MM-DDTHH:MM:SS+TZ"
    }}

    If the user is **not** creating a calendar event, respond like this:
    {{
        "is_event": false,
        "response": "Your normal assistant response here."
    }}

    Assume today's date and time is: {today_date_time}

    User input: "{prompt}"
    """

    response = ollama.chat(
        model='llama3',
        messages=history + [{'role': "user", "content": prompt}]
    )

    answer = response['message']['content']
    match = re.search(r'({.*})', answer, re.DOTALL)


    print(match)
    if match:
        # Get the matched JSON string
        json_str = match.group(1)

        # Now parse the JSON string into a Python dictionary
        parsed = json.loads(json_str)

        if parsed.get("is_event"):
            # Extract required data
            title = parsed.get("title")
            start_time = parsed.get("start_time")
            end_time = parsed.get("end_time")
            answer = markdown.markdown(create_calendar_event(title, start_time, end_time))
        
        else:
            answer = markdown.markdown(parsed.get("response"))
            
    else:
        print("No JSON found in the response.")

    return answer, history + [{"role": "assistant", "content": answer}]

# No longer used but will keep for now
def local_llm_event_parse(prompt, history=[]):
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    prompt = f"""
    Please parse my prompt and return a json object in the following format.

    Example: 'Remind me to work on my "Personal Project" today at 9am' should return:
    {{
        "title": "Personal Project",
        "start_time": "2025-05-01T09:00:00+02:00",
        "end_time": "2025-05-01T10:00:00+02:00"
    }}

    If no end time is specified, then use 1 hour as the default value.

    For all dates/times should be considered based on today's date: {today_date}.

    Prompt: "{prompt}"
    """

    response = ollama.chat(
        model='llama3',
        messages=history + [{'role': "user", "content": prompt}]
    )

    match = re.search(r'({.*})', response['message']['content'], re.DOTALL)

    if match:
        # Get the matched JSON string
        json_str = match.group(1)

        # Now parse the JSON string into a Python dictionary
        parsed_event = json.loads(json_str)

        # Extract required data
        title = parsed_event.get("title")
        start_time = parsed_event.get("start_time")
        end_time = parsed_event.get("end_time")

        return title, start_time,end_time
    else:
        print("No JSON found in the response.")
import os
import re
from datetime import datetime

def log_chat(role,message):
    # Ensure directory exists
    os.makedirs("logs", exist_ok=True)

    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join("logs", f"{today}.txt")

    # Timestamp the message
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_line = f"[{timestamp}] {role.upper()}: {message}\n"

    # Append message to the daily log file
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_line)

def load_chat_history():
    messages = []
    # Get today's date in YYYY-MM-DD format
    today_date = datetime.now().strftime("%Y-%m-%d")
    # Build the file path for today's log
    file_path = f"logs/{today_date}.txt"

    if os.path.exists(file_path):
        date = os.path.basename(file_path).split('.')[0] # Extract the date part from the filename (e.g., 2025-04-25)

        with open(file_path, "r") as file:
            log_data = file.read()

            # Regex pattern to match time and the message
            pattern = r"\[(\d{2}:\d{2}:\d{2})\] (.*?)(?=\[\d{2}:\d{2}:\d{2}\]|$)"
            matches = re.findall(pattern, log_data, re.DOTALL)

            for time, message in matches:
                # Combine the date from the file with the time from the message to create a full timestamp
                timestamp = f"{date} {time}"
                messages.append({"timestamp": timestamp, "message": message.strip()})
    
    
    return messages

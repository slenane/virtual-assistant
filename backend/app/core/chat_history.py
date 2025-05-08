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
    log_line = f"[{timestamp}] {role}: {message}\n"

    # Append message to the daily log file
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_line)

    return {
        "timestamp": timestamp,
        "role": role,
        "message": message
    }

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

            # Regex pattern to match [HH:MM:SS] Role: message
            pattern = r"\[(\d{2}:\d{2}:\d{2})\] (.*?): (.*?)(?=\[\d{2}:\d{2}:\d{2}\]|$)"
            matches = re.findall(pattern, log_data, re.DOTALL)

            for time, role, content in matches:
                timestamp = time
                role = role.lower().strip()
                content = content.strip()

                messages.append({
                    "timestamp": timestamp,
                    "role": role,
                    "message": content
                })
    
    return messages

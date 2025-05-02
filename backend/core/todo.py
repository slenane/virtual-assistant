import os
from datetime import datetime
import dateparser

def get_todays_todo():
    todo_dir = "todos"
    today = datetime.now().strftime("%Y-%m-%d")
    todo_file = os.path.join(todo_dir, f"{today}.txt")

    if not os.path.exists(todo_file):
        return "\nYou have no tasks on you todo list for today."
    
    with open(todo_file, 'r') as f:
        tasks = f.readlines()

    if not tasks:
        return "\nYour todo list is empty for today"
    
    formatted_tasks = "\n".join(task.strip() for task in tasks)
    return f"Here's your todo list for today ({today}):\n{formatted_tasks}"

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
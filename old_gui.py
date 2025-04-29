import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
from assistant import handle_custom_commands, get_greeting
from core import log_chat, load_chat_history, ask_llm_local, ensure_ollama_running

chat_history = []

# Run ollama in the background
ensure_ollama_running()

def run_gui():
    def send():
        user_input = entry.get()
        if not user_input.strip():
            return
        
        entry.delete(0, tk.END)
        chat_log.insert(tk.END, f"\n\nYou: {user_input}\n")
        log_chat("user", user_input)
    
        def handle_response():
            global chat_history
            response = handle_custom_commands(user_input)
            if response is None:
                response, chat_history = ask_llm_local(user_input, chat_history)

            chat_log.insert(tk.END, f"\n\nAssistant: {response}\n")
            log_chat("assistant", response)
            chat_log.see(tk.END)
        
        threading.Thread(target=handle_response).start()


    root = tk.Tk()
    root.title("Virtual Assistant")

    chat_log = ScrolledText(root, wrap=tk.WORD, height=40, width=120)
    chat_log.pack(padx=10, pady=10)
    
    todays_log = load_chat_history()
    
    if len(todays_log):
        for message in todays_log:
            chat_log.insert(tk.END, f"\n\n{message['message']}\n")
    else:
        chat_log.insert(tk.END, get_greeting())

    entry = tk.Entry(root, width=50)
    entry.pack(padx=10, pady=(0,10))
    entry.bind("<Return>", lambda event: send())

    send_btn = tk.Button(root, text="Send", command=send)
    send_btn.pack(pady=(0, 10))

    root.mainloop()

if __name__ == "__main__":
    run_gui()

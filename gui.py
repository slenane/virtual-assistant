import sys
import threading
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PySide6.QtCore import Signal, QObject, QThread
from assistant import handle_custom_commands, get_greeting
from core import log_chat, load_chat_history, ask_llm_local, ensure_ollama_running

chat_history = []

# Run ollama in the background
ensure_ollama_running()

# Define a signal handler to fix threading issue when using an LLM
class Worker(QObject):
    finished = Signal(str)

    def __init__(self, user_input, chat_history):
        super().__init__()
        self.user_input = user_input
        self.chat_history = chat_history
    
    def run(self):
        response = handle_custom_commands(self.user_input)

        if response is None:
            response, self.chat_history = ask_llm_local(self.user_input, self.chat_history)

        self.finished.emit(response)

class VirtualAssistantApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle("Virtual Assistant")
        self.setGeometry(100, 100, 800, 600)

        # Layout
        self.layout = QVBoxLayout(self)

        # Chat log area (QTextEdit)
        self.chat_log = QTextEdit(self)
        self.chat_log.setReadOnly(True)  # Make it read-only so user can't type directly here
        self.layout.addWidget(self.chat_log)

        # User input field (QLineEdit)
        self.input_field = QLineEdit(self)
        self.layout.addWidget(self.input_field)

        # Send button
        self.send_button = QPushButton("Send", self)
        self.layout.addWidget(self.send_button)

        # Connect send button to action
        self.send_button.clicked.connect(self.on_send)

        # Connect Enter/Return key in QLineEdit to trigger the button
        self.input_field.returnPressed.connect(self.send_button.click)

        # Always show the greeting
        self.chat_log.append(get_greeting())

        # Load today's chat history
        todays_log = load_chat_history()

        # If there's chat history, display it, otherwise show a greeting
        if len(todays_log):
            for message in todays_log:
                self.chat_log.append(message['message'])

    def on_send(self):
        global chat_history
        # Get the user input and display it
        user_input = self.input_field.text()
        if user_input.strip():
            self.chat_log.append(f"\n\nYou: {user_input}")
            log_chat("You", user_input)
            self.input_field.clear()

            # Create a worker thread
            self.worker = Worker(user_input, chat_history)
            self.thread = QThread()
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.handle_response)  # <- FIX: connect worker's finished signal
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            self.thread.start()


    # Handle assistants response asynchronously 
    def handle_response(self, response):
        self.chat_log.append(f"\n\nAssistant: {response}")
        log_chat("Assistant", response)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VirtualAssistantApp()
    window.show()
    sys.exit(app.exec())
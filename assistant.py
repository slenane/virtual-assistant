import speech_recognition as sr
import pyttsx3

# Initialize the recognize and the TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text): 
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)
        try: 
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Sorry, I'm having trouble connecting to the internet")
            return ''
        
def main():
    speak("Hello! How can I help you?")
    while True:
        command  = listen()
        if "hello" in command:
            speak("Hi there!")
        elif "time" in command:
            from datetime import datetime
            now = datetime.now().strftime("%H:%M")
            speak(f'The time is {now}')
        elif "stop" in command or "bye" in command:
            speak("Goodbye!")
            break
        else:
            speak("I'm not sure how to help with that.")

if __name__ == "__main__":
    main()


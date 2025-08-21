import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os

# Initialize TTS engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change index for male/female
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wish_user():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis. How can I help you?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"You said: {query}")
    except Exception as e:
        print("Sorry, I didn't catch that. Please repeat.")
        speak("Sorry, I didn't catch that. Please repeat.")
        return "None"
    return query.lower()

def run_jarvis():
    wish_user()
    while True:
        query = take_command()

        if 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://google.com")

        elif 'play music' in query:
            music_dir = 'C:\\Users\\Public\\Music'  # Change this path
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'stop' in query or 'bye' in query:
            speak("Goodbye! Have a great day!")
            break

        else:
            speak("Sorry, I can't do that yet. Try something else.")

# Run Jarvis
run_jarvis()

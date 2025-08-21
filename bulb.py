import speech_recognition as sr
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to give speech feedback
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Simulating the light bulb state (ON/OFF)
light_on = False

# Function to list available microphones and choose one
def choose_microphone():
    # List all available microphones
    mic_list = sr.Microphone.list_microphone_names()
    if len(mic_list) == 0:
        print("No microphones found!")
        return None
    print("Available Microphones:")
    for index, name in enumerate(mic_list):
        print(f"{index}: {name}")
    
    # Ask the user to select a microphone
    mic_index = int(input("Enter the microphone index you want to use: "))
    
    if mic_index < 0 or mic_index >= len(mic_list):
        print("Invalid microphone index!")
        return None
    
    return mic_index

# Function to listen for voice commands (on/off)
def listen_for_command(mic_index):
    recognizer = sr.Recognizer()

    # Use the selected microphone index
    try:
        with sr.Microphone(device_index=mic_index) as source:
            print("Listening for command...")

            # Adjust for ambient noise before listening
            recognizer.adjust_for_ambient_noise(source)

            # Listen for the command from the user
            audio = recognizer.listen(source)
        
        # Recognizing the command using Google Speech Recognition
        command = recognizer.recognize_google(audio).lower()
        print(f"Command received: {command}")

        if 'on' in command:
            return 'on'
        elif 'off' in command:
            return 'off'
        else:
            return None
    except Exception as e:
        print(f"Error during listening: {e}")
        return None

# Main control loop to turn the light on/off
def control_light():
    global light_on
    
    # Choose the microphone to use
    mic_index = choose_microphone()

    if mic_index is None:
        print("No microphone selected. Exiting.")
        return

    while True:
        # Listen for commands and act based on the command
        command = listen_for_command(mic_index)

        if command == 'on' and not light_on:
            light_on = True
            speak("The light is now ON.")
            print("Light is ON")
        elif command == 'off' and light_on:
            light_on = False
            speak("The light is now OFF.")
            print("Light is OFF")
        elif command == 'on' and light_on:
            speak("The light is already ON.")
            print("The light is already ON")
        elif command == 'off' and not light_on:
            speak("The light is already OFF.")
            print("The light is already OFF")
        else:
            speak("Please say 'on' to turn the light on or 'off' to turn it off.")
            print("Please say 'on' or 'off'")

if __name__ == "__main__":
    control_light()

import pyttsx3

def speak_response(text):
    engine = (
        pyttsx3.init()
    )  # Re-initialize the engine to prevent hanging/skipping
    engine.say(text)
    engine.runAndWait()


# Call this function for your first prompt
speak_response("Hello, how are you?")

# Call it again for the second prompt
speak_response("I am doing great!")

"""
import pyttsx3

engine = pyttsx3.init()

# Store your prompts in a list
prompts = ["First prompt", "Second prompt", "Third prompt"]

# Combine them into a single block of text
combined_speech = ", ".join(prompts)

# Say it all at once
engine.say(combined_speech)
engine.runAndWait()
"""

"""
import pyttsx3

engine = pyttsx3.init()

engine.say("Hello")
engine.say("Second message")
engine.say("Third message")

engine.runAndWait()
"""

"""
import win32com.client

speaker = win32com.client.Dispatch("SAPI.SpVoice")

speaker.Speak("Hello")
speaker.Speak("Second")
speaker.Speak("Third")
"""
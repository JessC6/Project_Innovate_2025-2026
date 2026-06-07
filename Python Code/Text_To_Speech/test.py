import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[173].id)
engine.setProperty('rate', 150)
print("""
Moods
1. Happy
2. Sad
3. Neutral
4. Surprised
""")
emotion = input("What mood are you in today?: ")

if emotion.lower() == "happy" or emotion == '1':
    text = "You are looking amazing today. Keep smiling!"
elif emotion.lower() == "sad" or emotion == '2':
    text = "You are looking too good to have this sad face on you. Cheer up! The world needs your smile!"
elif emotion.lower() == "neutral" or emotion == '3':
    text = "You are not expressing any emotions right now. Smile more!"
elif emotion.lower() == "surprised" or emotion == '4':
    text = "Wow you look surprised. What happened? Tell me all about it."
else:
    text = "Not a valid emotion"

engine.say(text)
engine.runAndWait()


# voices 20 - closest to Bulgarian
#18, 19, 21, 23, 24, 38, 39, 51, 53, 55, 56, 69, 70, 82, 86, 88, 89, 102, 107, 110, 111, 113, 114, 125, 127, 128, 140, 142, 143, 158, 159, 172, 173, 177 179, 183,
#good voices - 19, 23, 24,38,39, 53- singing, 55,56, 69,70, 86, 88 - okayish, 89, 102 - nice one, 107 - robot voice, 125,127. 140, 168,172,173 - best,
import os
from pathlib import Path

import pyttsx3
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in .env file")

client = Anthropic(api_key=api_key)

engine = pyttsx3.init()
voices = engine.getProperty("voices")

if len(voices) > 173:
    engine.setProperty("voice", voices[173].id)

engine.setProperty("rate", 150)

print("""
Moods
1. Happy
2. Sad
3. Neutral
4. Surprised
""")

emotion = input("What mood are you in today?: ").strip().lower()

emotion_map = {
    "1": "happy",
    "2": "sad",
    "3": "neutral",
    "4": "surprised",
    "happy": "happy",
    "sad": "sad",
    "neutral": "neutral",
    "surprised": "surprised",
}

detected_emotion = emotion_map.get(emotion)

if not detected_emotion:
    text = "That is not a valid emotion."
else:
    prompt = f"""
A university campus robot detected that a student is feeling {detected_emotion}.
Reply with one short, kind, natural sentence.
Make it supportive, friendly, and good for text-to-speech.
Keep it under 25 words.
Do not use emojis.
"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=80,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        text = response.content[0].text.strip()
    except Exception:
        text = "I am sorry, I cannot respond right now."

print(text)
engine.say(text)
engine.runAndWait()
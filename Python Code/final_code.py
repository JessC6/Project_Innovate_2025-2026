import cv2
import time
import pyttsx3
from fer.fer import FER

import os
from pathlib import Path

from dotenv import load_dotenv
from anthropic import Anthropic

# ---------- LOADING API KEY -----------
""" 
 Each person should change this following variable to state the correct location of the 
.env file with the api key, relative to this file. 
"""
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError(
        "ANTHROPIC_API_KEY not found in .env file"
    )

client = Anthropic(api_key=api_key)

# ---------- CONFIG ----------
MAX_ATTEMPTS = 3
CAPTURE_DELAY = 3
MIN_CONFIDENCE = 0.40

ALLOWED_EMOTIONS = ["happy", "neutral", "sad", "surprise", "angry", "disgust", "fear"]

# ---------- SPEECH SYSTEM ----------
def speak(text):
    print(f"Robot: {text}")

    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        print("Speech Error:", e)

# ---------- AI GENERATED RESPONSE -----------
def generate_response(emotion):
    prompt = f"""
    A university campus robot detected that a student is feeling {emotion}.
    Reply with one short, kind, natural sentence.
    Make it:
    - supportive
    - friendly
    - suitable for text-to-speech
    - under 25 words
    Do not use emojis.
    """

    try:
        response = client.messages.create(model="claude-sonnet-4-6",
                                          max_tokens=80,
                                          messages=[{"role": "user", "content": prompt}])

        return response.content[0].text.strip()

    except Exception as e:
        print("Claude Error:", e)
        return ("I am sorry. I cannot respond right now.")

# -----------------------------
# IMAGE CHECKS
# -----------------------------
def check_brightness(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = gray.mean()

    if brightness < 50:
        return False, "Too Dark"

    if brightness > 220:
        return False, "Too Bright"

    return True, "OK"

def check_blur(frame):
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    blur_value = cv2.Laplacian(gray, cv2.CV_64F).var()

    if blur_value < 100:
        return False, "Too Blurry"

    return True, "OK"


def check_face_size(face_width):
    if face_width < 120:
        return False, "Move Closer"

    return True, "OK"


# -----------------------------
# EMOTION DETECTION
# -----------------------------
def detect_emotion():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Could not open camera.")
        return "unknown", False

    detector = FER(mtcnn=True)
    # If Raspberry Pi struggles use instead:
    # detector = FER()

    speak("Hello. Please stand in front of the camera at arm's length so I can analyze your facial expression.")

    attempts = 0

    try:
        while attempts < MAX_ATTEMPTS:
            print(f"\nAttempt {attempts + 1} of {MAX_ATTEMPTS}")

            face_detected_time = None
            face_announced = False

            while True:
                ret, frame = camera.read()

                if not ret:
                    continue

                status = (f"Attempt {attempts + 1}/{MAX_ATTEMPTS}")

                result = detector.detect_emotions(frame)

                if result:
                    x, y, w, h = result[0]["box"]

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    brightness_ok, brightness_msg = (check_brightness(frame))
                    blur_ok, blur_msg = (check_blur(frame))
                    face_ok, face_msg = (check_face_size(w))

                    if not brightness_ok:
                        status = brightness_msg
                        face_detected_time = None

                    elif not blur_ok:
                        status = blur_msg
                        face_detected_time = None

                    elif not face_ok:
                        status = face_msg
                        face_detected_time = None

                    else:
                        if face_detected_time is None:
                            face_detected_time = time.time()

                            if not face_announced:
                                speak("Face detected. Please hold still.")

                                face_announced = True

                        elapsed = (time.time() - face_detected_time)
                        current_second = max(0, int(CAPTURE_DELAY - elapsed) + 1)
                        status = (f"Capturing in {current_second}")

                        # -----------------
                        # Capture image
                        # -----------------

                        if elapsed >= CAPTURE_DELAY:
                            speak("Picture captured.")

                            status = "Analyzing emotion..."

                            image_name = (f"attempt_{attempts + 1}.jpg")

                            cv2.imwrite(image_name, frame)

                            result = detector.detect_emotions(frame)

                            if not result:
                                 emotion = "unknown"
                                 confidence = 0.0
                                 
                            else:
                                 emotions = result[0]["emotions"]
                                 emotion = max(emotions, key=emotions.get)
                                 confidence = emotions[emotion]

                            print(f"Detected: {emotion}")
                            print(f"Confidence: "f"{confidence:.2f}")

                            if (emotion not in ALLOWED_EMOTIONS):
                                emotion = "unknown"

                            elif (confidence < MIN_CONFIDENCE):
                                emotion = "unknown"

                            print(f"Validated emotion: {emotion}")

                            # -----------------
                            # SUCCESS
                            # -----------------

                            if emotion != "unknown":
                                return emotion, True

                            # -----------------
                            # RETRY
                            # -----------------

                            attempts += 1

                            speak("I am not confident enough in my analysis.")
                            
                            if attempts < MAX_ATTEMPTS:
                                speak("Let's try again.")

                            break

                else:
                    face_detected_time = None
                    face_announced = False

                    status = (f"Attempt {attempts + 1}/"f"{MAX_ATTEMPTS} - "f"Looking for face...")

                cv2.putText(frame, status, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                cv2.imshow("Emotion Robot", frame)

                key = cv2.waitKey(1)

                if (key == ord('q') or key == 27):
                    return "unknown", False

        speak("I'm sorry. I am unable to determine your emotion at this time. Please try again later.")

        return "unknown", False

    finally:
        camera.release()
        cv2.destroyAllWindows()

# -----------------------------
# MAIN
# -----------------------------
emotion, success = detect_emotion()

print("\nFINAL RESULT")
print("Emotion:", emotion)
print("Success:", success)

if success:
    print(f"Emotion '{emotion}' detected.")

    response = generate_response(emotion)

    print(f"AI Response: {response}")

    speak(response)
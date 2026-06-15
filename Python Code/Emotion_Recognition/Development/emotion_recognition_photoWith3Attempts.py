import cv2
import time
from fer.fer import FER

# -----------------------------
# CONFIG
# -----------------------------
MAX_ATTEMPTS = 3
CAPTURE_DELAY = 2
MIN_CONFIDENCE = 0.40

ALLOWED_EMOTIONS = [
    "happy",
    "neutral",
    "sad",
    "surprise"
]

# -----------------------------
# IMAGE QUALITY CHECKS
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

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blur_value = cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()

    if blur_value < 100:
        return False, "Too Blurry"

    return True, "OK"


def check_face_size(face_width):

    if face_width < 120:
        return False, "Move Closer"

    return True, "OK"


# -----------------------------
# MAIN DETECTOR
# -----------------------------
def detect_emotion():

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Could not open camera.")
        return "unknown", False

    detector = FER(mtcnn=True)

    print("Emotion detection started...")

    attempts = 0

    try:

        while attempts < MAX_ATTEMPTS:

            print(
                f"\nAttempt {attempts + 1} of {MAX_ATTEMPTS}"
            )

            face_detected_time = None

            while True:

                ret, frame = camera.read()

                if not ret:
                    break

                status = (
                    f"Attempt {attempts + 1}/{MAX_ATTEMPTS}"
                )

                result = detector.detect_emotions(frame)

                if result:

                    x, y, w, h = result[0]["box"]

                    cv2.rectangle(
                        frame,
                        (x, y),
                        (x + w, y + h),
                        (0, 255, 0),
                        2
                    )

                    # -------------------------
                    # Quality Checks
                    # -------------------------
                    brightness_ok, brightness_msg = (
                        check_brightness(frame)
                    )

                    blur_ok, blur_msg = (
                        check_blur(frame)
                    )

                    face_ok, face_msg = (
                        check_face_size(w)
                    )

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

                        elapsed = (
                            time.time()
                            - face_detected_time
                        )

                        countdown = max(
                            0,
                            CAPTURE_DELAY - int(elapsed)
                        )

                        status = (
                            f"Capturing in {countdown}"
                        )

                        if elapsed >= CAPTURE_DELAY:

                            print(
                                "Picture captured!"
                            )

                            image_name = (
                                f"attempt_{attempts + 1}.jpg"
                            )

                            cv2.imwrite(
                                image_name,
                                frame
                            )

                            emotions = (
                                result[0]["emotions"]
                            )

                            emotion = max(
                                emotions,
                                key=emotions.get
                            )

                            confidence = (
                                emotions[emotion]
                            )

                            print(
                                f"Detected: {emotion}"
                            )

                            print(
                                f"Confidence: "
                                f"{confidence:.2f}"
                            )

                            # -------------------------
                            # Confidence Check
                            # -------------------------

                            if (
                                emotion
                                not in ALLOWED_EMOTIONS
                            ):
                                emotion = "unknown"

                            elif (
                                confidence
                                < MIN_CONFIDENCE
                            ):
                                emotion = "unknown"

                            # -------------------------
                            # SUCCESS
                            # -------------------------

                            if emotion != "unknown":

                                print(
                                    "Emotion accepted."
                                )

                                return emotion, True

                            # -------------------------
                            # RETRY
                            # -------------------------

                            attempts += 1

                            print(
                                "\nEmotion unclear."
                            )

                            if attempts < MAX_ATTEMPTS:

                                print(
                                    "Please try again..."
                                )

                                time.sleep(2)

                            break

                else:

                    face_detected_time = None

                    status = (
                        f"Attempt {attempts + 1}/"
                        f"{MAX_ATTEMPTS} - "
                        f"Looking for face..."
                    )

                # -------------------------
                # DISPLAY
                # -------------------------

                cv2.putText(
                    frame,
                    status,
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    2
                )

                cv2.imshow(
                    "Emotion Robot",
                    frame
                )

                key = cv2.waitKey(1)

                if (
                    key == ord('q')
                    or key == 27
                ):
                    return "unknown", False

        # -------------------------
        # ALL ATTEMPTS FAILED
        # -------------------------

        print(
            "\nUnable to determine emotion "
            "after 3 attempts."
        )

        return "unknown", False

    finally:

        camera.release()
        cv2.destroyAllWindows()


# -----------------------------
# MAIN PROGRAM
# -----------------------------

emotion, success = detect_emotion()

print("\nFINAL RESULT")
print("Emotion:", emotion)
print("Success:", success)
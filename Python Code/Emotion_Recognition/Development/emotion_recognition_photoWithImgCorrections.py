import cv2
import time
from fer.fer import FER


# -----------------------------
# Image Quality Checks
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
        return False, "Image Blurry"

    return True, "OK"


def check_face_size(face_width):

    if face_width < 120:
        return False, "Move Closer"

    return True, "OK"


# -----------------------------
# Emotion Detection Function
# -----------------------------

def detect_emotion():

    camera = cv2.VideoCapture(0)

    detector = FER(mtcnn=True)

    print("Looking for a face...")

    face_detected_time = None

    while True:

        ret, frame = camera.read()

        if not ret:
            break

        result = detector.detect_emotions(frame)

        status_message = "Searching..."

        if result:

            # Face coordinates
            x, y, w, h = result[0]["box"]

            # Draw face rectangle
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            # -----------------------------
            # Quality Checks
            # -----------------------------

            brightness_ok, brightness_msg = check_brightness(frame)
            blur_ok, blur_msg = check_blur(frame)
            face_ok, face_msg = check_face_size(w)

            if not brightness_ok:
                status_message = brightness_msg

            elif not blur_ok:
                status_message = blur_msg

            elif not face_ok:
                status_message = face_msg

            else:

                status_message = "Hold Still..."

                if face_detected_time is None:
                    face_detected_time = time.time()

                elapsed = time.time() - face_detected_time

                countdown = max(
                    0,
                    2 - int(elapsed)
                )

                status_message = (
                    f"Capturing in {countdown}"
                )

                if elapsed >= 2:

                    print("Picture captured!")

                    cv2.imwrite(
                        "captured_face.jpg",
                        frame
                    )

                    emotions = result[0]["emotions"]

                    emotion = max(
                        emotions,
                        key=emotions.get
                    )

                    allowed = [
                        "happy",
                        "neutral",
                        "sad",
                        "surprise"
                    ]

                    if emotion not in allowed:
                        emotion = "unknown"

                    camera.release()
                    cv2.destroyAllWindows()

                    return emotion

        else:
            face_detected_time = None

        # -----------------------------
        # Status Text
        # -----------------------------

        cv2.putText(
            frame,
            status_message,
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

        if key == ord('q') or key == 27:
            break

    camera.release()
    cv2.destroyAllWindows()

    return "unknown"


# -----------------------------
# Main Program
# -----------------------------

emotion = detect_emotion()

print(f"Detected emotion: {emotion}")
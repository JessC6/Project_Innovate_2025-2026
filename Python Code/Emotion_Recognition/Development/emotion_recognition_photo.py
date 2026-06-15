import cv2
import time
from fer.fer import FER

def detect_emotion():

    # Open camera
    camera = cv2.VideoCapture(0)

    # Emotion detector
    detector = FER(mtcnn=True)

    print("Looking for a face...")

    face_detected_time = None

    while True:

        ret, frame = camera.read()

        if not ret:
            break

        # Detect faces/emotions
        result = detector.detect_emotions(frame)

        if result:

            # Start timer only once
            if face_detected_time is None:
                face_detected_time = time.time()

            elapsed = time.time() - face_detected_time

            # Face box
            x, y, w, h = result[0]["box"]

            # Draw rectangle
            cv2.rectangle(frame,
                          (x, y),
                          (x+w, y+h),
                          (0, 255, 0),
                          2)

            # Show countdown
            countdown = max(0, 2 - int(elapsed))

            cv2.putText(frame,
                        f"Capturing in {countdown}",
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 255),
                        2)

            # Wait 2 seconds before capture
            if elapsed >= 2:

                print("Picture captured!")

                cv2.imwrite("captured_face.jpg", frame)

                emotions = result[0]["emotions"]

                emotion = max(emotions, key=emotions.get)

                allowed = ["happy", "neutral", "sad", "surprise"]

                if emotion not in allowed:
                    emotion = "unknown"

                camera.release()
                cv2.destroyAllWindows()

                return emotion

        else:
            face_detected_time = None

        cv2.imshow("Emotion Robot", frame)

        key = cv2.waitKey(1)

        if key == ord('q') or key == 27:
            break

    camera.release()
    cv2.destroyAllWindows()

    return "unknown"


# Main program

emotion = detect_emotion()

print(f"Detected emotion: {emotion}")
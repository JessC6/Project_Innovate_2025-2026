import cv2
from fer.fer import FER

# Open webcam
camera = cv2.VideoCapture(0)

# Initialize detector
detector = FER(mtcnn=True)

while True:

    # Capture frame
    ret, frame = camera.read()

    if not ret:
        break

    # Detect emotions
    result = detector.detect_emotions(frame)

    # If face detected
    if result:

        emotions = result[0]["emotions"]

        # Get strongest emotion
        emotion = max(emotions, key=emotions.get)

        # Allowed emotions only
        allowed = ["happy", "neutral", "sad", "surprise"]

        if emotion not in allowed:
            emotion = "unknown"

        # Face coordinates
        x, y, w, h = result[0]["box"]

        # Draw rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0 ,0), 2)

        # Show emotion
        cv2.putText(
            frame,
            emotion.upper(),
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )

    # Display webcam
    cv2.imshow("Emotion Robot", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
camera.release()
cv2.destroyAllWindows()
import serial
import subprocess

arduino = serial.Serial('/dev/ttyUSB0', 9600)

while True:
    message = arduino.readline().decode().strip()

    if message == "START":
        subprocess.run(["python3", "emotion_recognition_system.py"])
        # if it doesn't work attempt:
        # subprocess.run(["python", "emotion_recognition_system.py"])
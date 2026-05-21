# Project Innovate (2025-2026)

## Project Overview
This repository contains the development process, research, testing, and implementation of our Innovate 2025–2026 project: an interactive campus robot capable of recognising basic human emotions through facial expression analysis.

The goal of the project is to design and build a robot that can safely move around an indoor campus environment and interact with users in a simple and engaging way. Once activated through a trigger mechanism, the robot captures the user’s face using an integrated camera, analyses the detected facial expression, and responds through voice output

The project combines several important areas within Information Technology, including:

- Embedded systems
- Hardware/software integration
- Team-based development

This repository documents the complete development process from planning and subsystem testing to the final integrated prototype.

## Main Features
The robot is intended to support the following core functionalities:

- Safe indoor navigation (pre-planned)
- Obstacle detection and avoidance
- User-triggered interaction system
- Camera with facial detection software
- Basic emotion recognition
- Visual and/or audio feedback responses
- Integration between Raspberry Pi and Arduino systems

## Initial Emotional Recognition Scope
To maintain realistic project scope and improve system reliability, the first implementation focuses on recognising the following four emotions:

- Happy
- Neutral
- Sad
- Surprised

Additional emotions may be added in future development stages if time allows.

## Hardware Used
The robot uses the following hardware components:

- Arduino-compatible microcontroller
- 2 DC motors with motor driver

## Pin Mapping (final version)

|         Component         | Pin |
|         ---------         | --- |
|    Left Motor Forward     | D10 |
|    Left Motor Backward    | D11 |
|    Right Motor Forward    | D9  |
|    Right Motor Backward   | D6  |
|   Left Encoder(rotation)  | D2  |
|  Right Encoder(rotation)  | D3  |
|    Ultrasonic Trigger     | D4  |
|      Ultrasonic Echo      | D13 |
|       Start Button        | D7  |
|   Line Sensor Most Left   | A7  |
|  Line Sensor Center Left  | A6  |
|  Line Sensor Right Left   | A5  |
|  Line Sensor Left Center  | A4  |
|  Line Sensor Right Center | A3  |
|  Line Sensor Left Right   | A2  |
|  Line Sensor Center Right | A1  |
|   Line Sensor Most Right  | A0  |
|       Gripper Servo       | D12 |

## Proposed System Architecture
The project follows a dual-controller architecture:

|       Component      	|                 Main Responsibility                |
|       ---------       |                 -------------------                |
|      Raspberry Pi     |	Emotion recognition, camera processing, main logic |
|        Arduino        |	     Motor control, sensors, movement handling     |
| USB Serial Connection |	        Communication between both systems         |

This structure separates high-level processing from real-time hardware control.

## Software / Library Requirements
The following tools and libraries are required:

| Tool / Library 	|              Purpose             |
| --------------  |              -------             |
|     Python     	|     Main programming language    |
|     OpenCV      |	Camera access and face detection |
|  FER / DeepFace	|       Emotion recognition        |
|     PySerial	   |     Pi-Arduino communication     |
|   Arduino IDE  	|  Arduino development environment |
|     Arduino     |  C/C++	Motor and sensor control  |
|      NumPy      |	      Numerical operations       |

Install Python dependencies in Command Prompt / Git Bash with:
```
pip install *dependency name* (example: opencv-python, fer, tensorflow, pyserial, numpy)
```

## Emotion Recognition Workflow
The planned interaction workflow is:

1. Robot moves through environment
2. User activates interaction mode
3. Robot stops safely
4. Camera captures user face
5. Emotion recognition system analyses expression
6. Robot responds through audio
7. Robot resumes movement

## How To Run
1. Install Python requirements
2. Connect webcam
3. Run the Python script:
```
python main.py
```
4. Present face to camera
5. Emotion label will appear on screen


## Notes / Known Limitations
- Emotion recognition accuracy depends heavily on lighting conditions
- Camera angle and distance may affect detection reliability
- The first prototype supports only a limited emotion set
- Voice interaction may be implemented later depending on project progress
- Battery duration may vary depending on motor load and processing usage

## Authors

1 Year Students (2025-2026) of Group B, IT:
 - Franz Petev (Hybrid/Integration team)
 - Ngangfor Amungwa (Hybrid/Integration team)
 - Kristian Endrev (Software team)
 - Jessica Camacho (Software team)
 - Kyra Kovács (Hardware team)
 - Herbert Dorothea (Hardware team)

Course project for:
 `IT - Project Innovation (2025-2026)`

Institution:
 `NHL Stenden University Of Applied Sciences`

## License

This repository is submitted for educational purposes as part of a course project.

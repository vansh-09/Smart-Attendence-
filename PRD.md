Good — this is a solid mini-project and very doable with your constraints.
sidenote: 2 photos is nothing, so we’ll design this correctly (transfer learning + face embeddings), not a naïve CNN classifier.

Below is a clean PRD you can paste directly into GitHub Copilot / Cursor.

⸻

📌 Product Requirements Document (PRD)

Project: Smart Attendance Tracker (Face Recognition using TensorFlow)

⸻

1. Objective

Build a real-time smart attendance system that:
	•	Opens the webcam
	•	Detects a face in each frame
	•	Draws a bounding box around the detected face
	•	Identifies the person using face embeddings
	•	Displays a dialog box with:
	•	Name
	•	Roll Number
	•	Marks attendance for the session

The system must work with only 2 reference images of the user.

⸻

2. Non-Goals
	•	Multi-person recognition
	•	Cloud deployment
	•	High-scale database integration
	•	Anti-spoofing (out of scope)

⸻

3. Tech Stack
	•	Language: Python 3.9+
	•	Deep Learning: TensorFlow / Keras
	•	Computer Vision: OpenCV
	•	Face Detection: Haar Cascade or MTCNN
	•	Face Embeddings: Pretrained CNN (FaceNet-style)
	•	UI Overlay: OpenCV drawing utilities

⸻

4. Architecture Overview

Webcam Feed
    ↓
Face Detection (MTCNN / Haar)
    ↓
Face Crop & Resize (160x160)
    ↓
Embedding Generation (CNN)
    ↓
Cosine Similarity Matching
    ↓
Identity Decision
    ↓
Bounding Box + Dialog Box Overlay


⸻

5. Core Components

5.1 Face Detection Module
	•	Load pretrained face detector
	•	Detect faces in real-time frames
	•	Return bounding box coordinates

Requirements
	•	Must work in real time (≥15 FPS)
	•	Handle partial face visibility

⸻

5.2 Face Embedding Model
	•	Use a pretrained CNN (FaceNet-style)
	•	Output a fixed-length embedding vector
	•	Do NOT train from scratch

Requirements
	•	Freeze model weights
	•	Normalize embeddings
	•	Input size: 160x160x3

⸻

5.3 Reference Embedding Generator
	•	Load the 2 reference images
	•	Generate embeddings
	•	Store mean embedding for the user

Data Structure Example

{
  "name": "Vansh Jain",
  "roll_no": "AI23DS042",
  "embedding": [0.012, -0.44, ...]
}


⸻

5.4 Recognition Logic
	•	Compute cosine similarity between:
	•	Live frame embedding
	•	Stored reference embedding
	•	Apply threshold (e.g. 0.6)

Decision Rules
	•	If similarity > threshold → recognized
	•	Else → unknown

⸻

5.5 UI Overlay System
	•	Draw bounding box around detected face
	•	Draw label box above face
	•	Display:
	•	Name
	•	Roll Number
	•	Use OpenCV overlays (rectangle + text)

Example

┌──────────────┐
│ Vansh Jain   │
│ Roll: 042    │
└──────────────┘


⸻

5.6 Attendance Logger (Optional v1)
	•	Mark attendance once per session
	•	Save to CSV:

name, roll_no, timestamp


⸻

6. Functional Requirements

ID	Requirement
FR1	System opens webcam automatically
FR2	Detects face in real time
FR3	Draws bounding box on detected face
FR4	Recognizes user with 2 reference images
FR5	Displays name & roll number in dialog box
FR6	Runs fully offline
FR7	Uses TensorFlow for inference


⸻

7. Non-Functional Requirements
	•	Latency < 200ms per frame
	•	CPU-compatible (GPU optional)
	•	Modular, readable code
	•	Clear separation of detection, recognition, and UI

⸻

8. Folder Structure

smart-attendance/
│
├── data/
│   └── reference/
│       ├── img1.jpg
│       └── img2.jpg
│
├── models/
│   └── facenet_model.h5
│
├── src/
│   ├── camera.ipynb
│   ├── face_detector.ipynb
│   ├── embedder.ipynb
│   ├── recognizer.ipynb
│   ├── ui_overlay.ipynb
│   └── attendance_logger.ipynb
│
├── main.py
├── requirements.txt
└── README.md


⸻

9. Acceptance Criteria
	•	Webcam opens successfully
	•	Face detected within 1 second
	•	Bounding box tracks face movement
	•	Name + roll number displayed correctly
	•	Recognition works with just 2 images
	•	No crashes during runtime

⸻

10. Future Enhancements (Out of Scope)
	•	Multiple students
	•	Anti-spoofing
	•	Mobile app
	•	Cloud sync
	•	Liveness detection

⸻

11. Notes for Copilot
	•	Prefer pretrained models
	•	Avoid training deep CNNs from scratch
	•	Prioritize clarity over cleverness
	•	Comment non-obvious logic


# Smart Attendance Tracker (Face Recognition)

A real-time, offline attendance system using webcam face detection and FaceNet embeddings (TensorFlow) per the PRD.

## Features

- Real-time face detection (MTCNN)
- Face embeddings via pretrained FaceNet (keras-facenet)
- Cosine similarity recognition with two reference images
- OpenCV overlay with name and roll number
- Attendance logged once per session to CSV

## Setup (macOS)

1. Ensure Python 3.9+.
2. Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

Apple Silicon (M1/M2) note: If TensorFlow GPU/CPU wheels conflict, install:

```bash
pip uninstall -y tensorflow
pip install tensorflow-macos tensorflow-metal
pip install keras-facenet mtcnn opencv-python Pillow numpy
```

## Enroll Reference Images

Place two clear face images in `data/reference/` (e.g., `img1.jpg`, `img2.jpg`). Then generate the reference embedding (name and roll are required):

```bash
python main.py --enroll --name "Vansh Jain" --roll "AI23DS042"
```

This creates `data/reference/embedding.json`.

## Run

Start the webcam attendance app (you can tweak the threshold):

```bash
python main.py --threshold 0.6
```

Press `q` to quit. Attendance is saved to `logs/attendance.csv` once per session.

## Folder Structure

```
smart-attendance/
├── data/
│   └── reference/
│       ├── img1.jpg
│       └── img2.jpg
├── logs/
│   └── attendance.csv
├── src/
│   ├── detector.py
│   ├── embedder.py
│   ├── reference.py
│   ├── recognizer.py
│   ├── ui.py
│   └── attendance.py
├── main.py
├── requirements.txt
└── README.md
```

## Troubleshooting

- SSL certificate error on macOS (Python 3.12):
  - Run the `Install Certificates.command` for your Python:
    - Open Finder → Applications → Python 3.12 → `Install Certificates.command`
    - Or in Terminal:
      ```bash
      open "/Applications/Python 3.12/Install Certificates.command"
      ```
  - Alternatively, set the cert bundle via `certifi`:
    ```bash
    python -c "import certifi; print(certifi.where())"
    export SSL_CERT_FILE=$(python -c "import certifi; print(certifi.where())")
    export REQUESTS_CA_BUNDLE=$SSL_CERT_FILE
    ```
- Offline/air-gapped usage:
  - The first run of `keras-facenet` downloads FaceNet weights. Our code caches them under `smart-attendance/models/`.
  - If downloading is blocked, prefetch on a networked machine (same Python+TF setup), then copy the cache contents into `smart-attendance/models/`.

## Notes

- Runs offline after the FaceNet weights are cached locally in `models/`.
- Recognition threshold can be tuned via CLI (`--threshold 0.55` / `0.50`) or in `src/recognizer.py`.
- For performance on CPU, ensure images are well-lit and frontal.
- Recommended Python versions for TensorFlow on macOS: 3.10–3.11.

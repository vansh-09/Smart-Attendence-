import argparse
import os
import sys

import cv2
import numpy as np

from src.detector import FaceDetector
from src.embedder import FaceEmbedder
from src.reference import build_reference_embedding, load_reference_embedding, EMBEDDING_PATH
from src.recognizer import Recognizer
from src.ui import draw_box, draw_label
from src.attendance import AttendanceLogger


BASE_DIR = os.path.dirname(__file__)
CSV_LOG = os.path.join(BASE_DIR, 'logs', 'attendance.csv')


def enroll(name: str, roll: str):
    path = build_reference_embedding(name, roll)
    print(f"Reference embedding saved to: {path}")


def run(threshold: float = 0.6):
    ref = load_reference_embedding(EMBEDDING_PATH)
    if ref is None:
        print("No reference embedding found. Please enroll first with --enroll.")
        sys.exit(1)

    name = ref['name']
    roll_no = ref['roll_no']
    ref_emb = np.array(ref['embedding'], dtype=np.float32)

    recognizer = Recognizer(ref_emb, threshold=threshold)
    detector = FaceDetector()
    embedder = FaceEmbedder()
    logger = AttendanceLogger(CSV_LOG)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Unable to open webcam.")
        sys.exit(1)

    print("Press 'q' to quit.")
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        detections = detector.detect(frame)
        if detections:
            det = max(detections, key=lambda d: d['confidence'])
            box = FaceDetector.clamp_box(det['box'], frame.shape[1], frame.shape[0], margin=10)
            draw_box(frame, box)
            face = embedder.crop_and_resize(frame, box)
            emb = embedder.embed(face)
            sim, is_recognized = recognizer.recognize(emb) if emb is not None else (0.0, False)

            label = f"Unknown (sim={sim:.2f})"
            if is_recognized:
                label = f"{name} | Roll: {roll_no}"
                logger.mark_once(name, roll_no)
            draw_label(frame, label, box)

        cv2.imshow('Smart Attendance', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Smart Attendance Tracker')
    parser.add_argument('--enroll', action='store_true', help='Generate reference embedding from images')
    parser.add_argument('--name', type=str, help='Full name for enrollment')
    parser.add_argument('--roll', type=str, help='Roll number for enrollment')
    parser.add_argument('--threshold', type=float, default=0.6, help='Recognition similarity threshold (default 0.6)')
    args = parser.parse_args()

    if args.enroll:
        if not args.name or not args.roll:
            print('--name and --roll are required with --enroll')
            sys.exit(1)
        enroll(args.name, args.roll)
    else:
        run(args.threshold)

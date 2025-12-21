import argparse
import os
import sys

import cv2
import numpy as np

from src.detector import FaceDetector
from src.embedder import FaceEmbedder
from src.reference import (
    build_reference_embedding, 
    load_reference_embedding, 
    load_students_embeddings,
    train_batch,
    cleanup_student_photos,
    EMBEDDING_PATH,
    STUDENTS_EMBEDDING_PATH
)
from src.recognizer import Recognizer
from src.ui import draw_box, draw_label
from src.attendance import AttendanceLogger


BASE_DIR = os.path.dirname(__file__)
CSV_LOG = os.path.join(BASE_DIR, 'logs', 'attendance.csv')


def enroll(name: str, roll: str):
    path = build_reference_embedding(name, roll)
    print(f"Reference embedding saved to: {path}")


def run(threshold: float = 0.6, batch: bool = False):
    """Run attendance recognition.
    
    Args:
        threshold: Similarity threshold for recognition
        batch: If True, use batch embeddings (multiple students)
               If False, use single student embedding (legacy)
    """
    if batch:
        # Load multiple students
        students_emb = load_students_embeddings(STUDENTS_EMBEDDING_PATH)
        if not students_emb:
            print("❌ No batch embeddings found. Please run --train-batch first.")
            sys.exit(1)
        print(f"✅ Loaded {len(students_emb)} students")
        run_batch_recognition(students_emb, threshold)
    else:
        # Legacy: single student
        ref = load_reference_embedding(EMBEDDING_PATH)
        if ref is None:
            print("❌ No reference embedding found. Please enroll first with --enroll.")
            sys.exit(1)
        
        name = ref['name']
        roll_no = ref['roll_no']
        ref_emb = np.array(ref['embedding'], dtype=np.float32)
        
        recognizer = Recognizer(ref_emb, threshold=threshold)
        run_single_recognition(recognizer, name, roll_no)


def run_single_recognition(recognizer: Recognizer, name: str, roll_no: str):
    """Run recognition for single student (legacy mode)."""
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


def run_batch_recognition(students_emb: dict, threshold: float = 0.6):
    """Run recognition for multiple students."""
    detector = FaceDetector()
    embedder = FaceEmbedder()
    logger = AttendanceLogger(CSV_LOG)
    
    # Prepare embeddings for all students
    recognizers = {}
    for roll_no, data in students_emb.items():
        emb = np.array(data['embedding'], dtype=np.float32)
        recognizers[roll_no] = {
            'name': data['name'],
            'recognizer': Recognizer(emb, threshold=threshold)
        }

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Unable to open webcam.")
        sys.exit(1)

    print(f"🎥 Running batch recognition with {len(recognizers)} students")
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
            
            label = "Unknown"
            if emb is not None:
                # Compare with all students
                best_sim = -1
                best_roll = None
                best_name = None
                
                for roll_no, data in recognizers.items():
                    recognizer = data['recognizer']
                    sim, is_recognized = recognizer.recognize(emb)
                    
                    if is_recognized and sim > best_sim:
                        best_sim = sim
                        best_roll = roll_no
                        best_name = data['name']
                
                if best_roll:
                    label = f"{best_name} | Roll: {best_roll}"
                    logger.mark_once(best_name, best_roll)
                else:
                    label = f"Unknown (best sim={best_sim:.2f})"
            
            draw_label(frame, label, box)

        cv2.imshow('Smart Attendance', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Smart Attendance Tracker')
    
    # Single student (legacy)
    parser.add_argument('--enroll', action='store_true', 
                        help='Generate reference embedding from 2 images (legacy single-student mode)')
    parser.add_argument('--name', type=str, 
                        help='Full name for enrollment')
    parser.add_argument('--roll', type=str, 
                        help='Roll number for enrollment')
    
    # Batch operations (new)
    parser.add_argument('--train-batch', action='store_true',
                        help='Train embeddings for all students from CSV and photo folders')
    parser.add_argument('--recognize', action='store_true',
                        help='Run attendance recognition (auto-detects batch vs single mode)')
    parser.add_argument('--cleanup-photos', action='store_true',
                        help='Delete all student photos after training to save space')
    parser.add_argument('--cleanup-dry-run', action='store_true',
                        help='Show what would be deleted without deleting')
    
    # Recognition settings
    parser.add_argument('--threshold', type=float, default=0.6, 
                        help='Recognition similarity threshold (default 0.6)')
    
    args = parser.parse_args()

    # Handle legacy single-student enrollment
    if args.enroll:
        if not args.name or not args.roll:
            print('❌ --name and --roll are required with --enroll')
            sys.exit(1)
        enroll(args.name, args.roll)
    
    # Handle batch training
    elif args.train_batch:
        train_batch()
    
    # Handle photo cleanup
    elif args.cleanup_photos or args.cleanup_dry_run:
        dry_run = args.cleanup_dry_run
        deleted = cleanup_student_photos(dry_run=dry_run)
        if dry_run:
            print(f"\n🔍 Would delete {deleted} photos")
        else:
            print(f"\n🗑️  Deleted {deleted} photos")
    
    # Handle recognition (auto-detect batch vs single)
    elif args.recognize:
        # Check if batch embeddings exist
        if os.path.exists(STUDENTS_EMBEDDING_PATH):
            run(args.threshold, batch=True)
        elif os.path.exists(EMBEDDING_PATH):
            run(args.threshold, batch=False)
        else:
            print("❌ No embeddings found. Please train first:")
            print("   For batch: python main.py --train-batch")
            print("   For single student: python main.py --enroll --name 'Name' --roll 'Roll'")
            sys.exit(1)
    
    # Default: run recognition
    else:
        # Check if batch embeddings exist
        if os.path.exists(STUDENTS_EMBEDDING_PATH):
            run(args.threshold, batch=True)
        elif os.path.exists(EMBEDDING_PATH):
            run(args.threshold, batch=False)
        else:
            print("❌ No embeddings found. Please train first:")
            print("   For batch: python main.py --train-batch")
            print("   For single student: python main.py --enroll --name 'Name' --roll 'Roll'")
            sys.exit(1)


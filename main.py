"""
Smart Attendance System
Batch facial recognition for attendance tracking
"""

import argparse
import os
import sys
import json
import csv

import cv2
import numpy as np

from src.model import FaceModel
from src.reference import load_embeddings, train_embeddings, EMBEDDINGS_FILE, STUDENTS_CSV
from src.ui import draw_box, draw_label
from src.attendance import AttendanceLogger


BASE_DIR = os.path.dirname(__file__)
CSV_LOG = os.path.join(BASE_DIR, 'logs', 'attendance.csv')


def train():
    """Train embeddings for all students."""
    print("Training embeddings...")
    train_embeddings()


def recognize(threshold=0.6):
    """Run real-time attendance recognition."""
    embeddings = load_embeddings()
    if not embeddings:
        print("No embeddings found. Run 'python main.py --train' first.")
        return
    
    model = FaceModel()
    logger = AttendanceLogger(CSV_LOG)
    
    cap = cv2.VideoCapture(0)
    print(f"Recognizing {len(embeddings)} students. Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        emb, box = model.detect_and_embed(frame)
        
        if emb is not None and box is not None:
            # Find best match
            best_sim = 0
            best_roll = None
            best_name = None
            
            for roll_no, data in embeddings.items():
                ref_emb = data['embedding']
                sim = model.compare_embeddings(emb, ref_emb)
                
                if sim > best_sim:
                    best_sim = sim
                    best_roll = roll_no
                    best_name = data['name']
            
            draw_box(frame, box)
            
            if best_sim >= threshold:
                label = f"{best_name} ({best_roll})"
                logger.mark_once(best_name, best_roll)
            else:
                label = f"Unknown ({best_sim:.2f})"
            
            draw_label(frame, label, box)
        
        cv2.imshow('Smart Attendance', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Smart Attendance System')
    parser.add_argument('--train', action='store_true', help='Train embeddings for all students')
    parser.add_argument('--recognize', action='store_true', help='Run attendance recognition')
    parser.add_argument('--threshold', type=float, default=0.6, help='Recognition threshold')
    args = parser.parse_args()
    
    if args.train:
        train()
    elif args.recognize:
        recognize(args.threshold)
    else:
        recognize(args.threshold)


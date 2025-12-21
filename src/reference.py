"""
Reference Embedding Management
Handles loading/saving student embeddings
"""

import json
import os
import glob
import csv
import numpy as np
from .model import FaceModel


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EMBEDDINGS_FILE = os.path.join(BASE_DIR, "reference", "embeddings.json")
STUDENTS_CSV = os.path.join(BASE_DIR, "data", "students", "students.csv")
STUDENTS_DIR = os.path.join(BASE_DIR, "data", "students")


def load_embeddings():
    """Load all student embeddings from JSON."""
    if not os.path.exists(EMBEDDINGS_FILE):
        return {}
    with open(EMBEDDINGS_FILE, "r") as f:
        return json.load(f)


def save_embeddings(embeddings):
    """Save embeddings to JSON."""
    os.makedirs(os.path.dirname(EMBEDDINGS_FILE), exist_ok=True)
    with open(EMBEDDINGS_FILE, "w") as f:
        json.dump(embeddings, f)


def train_embeddings():
    """Generate embeddings for all students from photos."""
    if not os.path.exists(STUDENTS_CSV):
        print("No students.csv found")
        return
    
    # Read student info
    students = {}
    with open(STUDENTS_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            roll = row['roll_number'].strip()
            name = row['name'].strip()
            students[roll] = name
    
    # Generate embeddings
    model = FaceModel()
    embeddings = {}
    
    for roll_no, name in students.items():
        student_dir = os.path.join(STUDENTS_DIR, roll_no)
        if not os.path.isdir(student_dir):
            continue
        
        photos = sorted(
            glob.glob(os.path.join(student_dir, "*.jpg")) +
            glob.glob(os.path.join(student_dir, "*.jpeg")) +
            glob.glob(os.path.join(student_dir, "*.png"))
        )
        
        if len(photos) < 2:
            print(f"Skipping {roll_no} - need at least 2 photos")
            continue
        
        # Generate embeddings from all photos
        embs = []
        for photo_path in photos:
            import cv2
            img = cv2.imread(photo_path)
            emb, _ = model.detect_and_embed(img)
            if emb is not None:
                embs.append(emb)
        
        if not embs:
            print(f"Skipping {roll_no} - no valid faces detected")
            continue
        
        # Compute mean embedding
        mean_emb = np.mean(np.stack(embs, axis=0), axis=0)
        mean_emb = (mean_emb / (np.linalg.norm(mean_emb) + 1e-8)).tolist()
        
        embeddings[roll_no] = {
            "name": name,
            "embedding": mean_emb
        }
        print(f"✓ {roll_no}: {name}")
    
    save_embeddings(embeddings)
    print(f"\nTrained {len(embeddings)} students")

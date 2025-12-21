import json
import os
import glob
import csv

import cv2
import numpy as np

from .detector import FaceDetector
from .embedder import FaceEmbedder


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Use root-level 'reference/' folder to match current project structure
EMBEDDING_PATH = os.path.join(BASE_DIR, "reference", "embedding.json")
STUDENTS_EMBEDDING_PATH = os.path.join(BASE_DIR, "reference", "students_embeddings.json")
REFERENCE_DIR = os.path.join(BASE_DIR, "reference")
STUDENTS_DATA_DIR = os.path.join(BASE_DIR, "data", "students")
STUDENTS_CSV_PATH = os.path.join(STUDENTS_DATA_DIR, "students.csv")


def build_reference_embedding(name: str, roll_no: str, reference_dir: str = None) -> str:
    """Compute mean embedding from two reference images and save as JSON.
    Returns the path to the saved JSON.
    """
    reference_dir = reference_dir or REFERENCE_DIR
    files = sorted(glob.glob(os.path.join(reference_dir, "*.jpg"))) + \
            sorted(glob.glob(os.path.join(reference_dir, "*.png")))
    if len(files) < 2:
        raise ValueError("Expected at least 2 reference images in data/reference/")

    detector = FaceDetector()
    embedder = FaceEmbedder()

    embeddings = []
    for fp in files[:2]:
        img = cv2.imread(fp)
        if img is None:
            continue
        dets = detector.detect(img)
        if not dets:
            continue
        # Use the highest-confidence face
        det = max(dets, key=lambda d: d['confidence'])
        box = FaceDetector.clamp_box(det['box'], img.shape[1], img.shape[0], margin=10)
        face = embedder.crop_and_resize(img, box)
        emb = embedder.embed(face)
        if emb is not None:
            embeddings.append(emb)

    if len(embeddings) < 2:
        raise RuntimeError("Could not generate embeddings from both images. Check image quality.")

    mean_emb = np.mean(np.stack(embeddings, axis=0), axis=0)
    # Normalize embedding
    mean_emb = (mean_emb / (np.linalg.norm(mean_emb) + 1e-8)).tolist()

    payload = {
        "name": name,
        "roll_no": roll_no,
        "embedding": mean_emb,
    }

    os.makedirs(os.path.dirname(EMBEDDING_PATH), exist_ok=True)
    with open(EMBEDDING_PATH, "w") as f:
        json.dump(payload, f)
    return EMBEDDING_PATH


def load_reference_embedding(path: str = None):
    path = path or EMBEDDING_PATH
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)


def load_students_embeddings(path: str = None):
    """Load all students' embeddings from batch file.
    
    Returns:
        dict: {roll_no: {'name': str, 'embedding': list, ...}}
    """
    path = path or STUDENTS_EMBEDDING_PATH
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        data = json.load(f)
    return data


def read_students_csv(csv_path: str = None) -> dict:
    """Read students from CSV file.
    
    Expected format:
    roll_number,name
    101,John Doe
    102,Jane Smith
    
    Returns:
        dict: {roll_no: name}
    """
    csv_path = csv_path or STUDENTS_CSV_PATH
    students = {}
    if not os.path.exists(csv_path):
        return students
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            roll = row.get('roll_number', '').strip()
            name = row.get('name', '').strip()
            if roll and name:
                students[roll] = name
    return students


def build_batch_embeddings(students_data_dir: str = None) -> dict:
    """Generate embeddings for all students from photo folders.
    
    Expects folder structure:
    students_data_dir/
        101/
            photo1.jpg
            photo2.jpg
        102/
            photo1.jpg
            photo2.jpg
    
    Args:
        students_data_dir: Path to students data directory
        
    Returns:
        dict: {roll_no: {'name': str, 'embedding': list, 'photo_count': int}}
    """
    students_data_dir = students_data_dir or STUDENTS_DATA_DIR
    
    # Read student info from CSV
    students_info = read_students_csv()
    
    detector = FaceDetector()
    embedder = FaceEmbedder()
    
    result = {}
    
    # Process each student folder
    for roll_no, name in students_info.items():
        student_folder = os.path.join(students_data_dir, roll_no)
        
        if not os.path.isdir(student_folder):
            print(f"⚠️  Skipping {roll_no} - no folder found at {student_folder}")
            continue
        
        # Get all image files
        images = (
            sorted(glob.glob(os.path.join(student_folder, "*.jpg"))) +
            sorted(glob.glob(os.path.join(student_folder, "*.jpeg"))) +
            sorted(glob.glob(os.path.join(student_folder, "*.png")))
        )
        
        if len(images) < 2:
            print(f"⚠️  Skipping {roll_no} ({name}) - need at least 2 photos, found {len(images)}")
            continue
        
        embeddings = []
        for img_path in images:
            img = cv2.imread(img_path)
            if img is None:
                print(f"  ⚠️  Could not read {os.path.basename(img_path)}")
                continue
            
            dets = detector.detect(img)
            if not dets:
                print(f"  ⚠️  No face detected in {os.path.basename(img_path)}")
                continue
            
            # Use highest-confidence face
            det = max(dets, key=lambda d: d['confidence'])
            box = FaceDetector.clamp_box(det['box'], img.shape[1], img.shape[0], margin=10)
            face = embedder.crop_and_resize(img, box)
            emb = embedder.embed(face)
            if emb is not None:
                embeddings.append(emb)
        
        if len(embeddings) < 2:
            print(f"⚠️  Skipping {roll_no} ({name}) - could only generate {len(embeddings)} valid embeddings")
            continue
        
        # Compute mean embedding
        mean_emb = np.mean(np.stack(embeddings, axis=0), axis=0)
        mean_emb = (mean_emb / (np.linalg.norm(mean_emb) + 1e-8)).tolist()
        
        result[roll_no] = {
            "name": name,
            "embedding": mean_emb,
            "photo_count": len(images),
            "valid_faces": len(embeddings)
        }
        
        print(f"✅ {roll_no}: {name} ({len(embeddings)} valid faces from {len(images)} photos)")
    
    return result


def save_batch_embeddings(embeddings: dict, output_path: str = None) -> str:
    """Save batch embeddings to JSON file.
    
    Args:
        embeddings: dict from build_batch_embeddings()
        output_path: Path to save JSON
        
    Returns:
        str: Path to saved file
    """
    output_path = output_path or STUDENTS_EMBEDDING_PATH
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(embeddings, f, indent=2)
    
    print(f"💾 Saved {len(embeddings)} student embeddings to {output_path}")
    return output_path


def train_batch(students_data_dir: str = None, output_path: str = None) -> dict:
    """One-shot function to train all student embeddings.
    
    Args:
        students_data_dir: Path to students data directory
        output_path: Path to save embeddings JSON
        
    Returns:
        dict: Generated embeddings
    """
    print(f"\n🎯 Starting batch training...\n")
    embeddings = build_batch_embeddings(students_data_dir)
    
    if not embeddings:
        print("❌ No valid student embeddings generated!")
        return {}
    
    save_batch_embeddings(embeddings, output_path)
    print(f"\n✨ Training complete! Enrolled {len(embeddings)} students.\n")
    return embeddings


def cleanup_student_photos(students_data_dir: str = None, dry_run: bool = False) -> int:
    """Delete all student photos to save space after training.
    
    Args:
        students_data_dir: Path to students data directory
        dry_run: If True, only print what would be deleted
        
    Returns:
        int: Number of photos deleted
    """
    students_data_dir = students_data_dir or STUDENTS_DATA_DIR
    
    if not os.path.isdir(students_data_dir):
        print(f"Directory not found: {students_data_dir}")
        return 0
    
    count = 0
    for roll_no in os.listdir(students_data_dir):
        student_folder = os.path.join(students_data_dir, roll_no)
        if not os.path.isdir(student_folder):
            continue
        
        for ext in ["*.jpg", "*.jpeg", "*.png"]:
            for img_path in glob.glob(os.path.join(student_folder, ext)):
                if dry_run:
                    print(f"Would delete: {img_path}")
                else:
                    os.remove(img_path)
                    print(f"Deleted: {img_path}")
                count += 1
    
    # Try to remove empty student folders
    for roll_no in os.listdir(students_data_dir):
        student_folder = os.path.join(students_data_dir, roll_no)
        if os.path.isdir(student_folder) and not os.listdir(student_folder):
            try:
                os.rmdir(student_folder)
                print(f"Removed empty folder: {student_folder}")
            except:
                pass
    
    return count


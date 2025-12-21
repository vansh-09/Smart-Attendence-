import json
import os
import glob

import cv2
import numpy as np

from .detector import FaceDetector
from .embedder import FaceEmbedder


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Use root-level 'reference/' folder to match current project structure
EMBEDDING_PATH = os.path.join(BASE_DIR, "reference", "embedding.json")
REFERENCE_DIR = os.path.join(BASE_DIR, "reference")


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

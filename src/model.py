"""
Face Detection and Embedding Model
Encapsulates FaceNet and MTCNN functionality
"""

import cv2
import numpy as np
from .detector import FaceDetector
from .embedder import FaceEmbedder


class FaceModel:
    """Simple wrapper for face detection and embedding."""
    
    def __init__(self):
        self.detector = FaceDetector()
        self.embedder = FaceEmbedder()
    
    def detect_and_embed(self, image):
        """Detect face and generate embedding from image.
        
        Returns:
            tuple: (embedding, box) or (None, None) if no face detected
        """
        detections = self.detector.detect(image)
        if not detections:
            return None, None
        
        det = max(detections, key=lambda d: d['confidence'])
        box = FaceDetector.clamp_box(det['box'], image.shape[1], image.shape[0], margin=10)
        face = self.embedder.crop_and_resize(image, box)
        emb = self.embedder.embed(face)
        
        return emb, box
    
    def compare_embeddings(self, emb1, emb2):
        """Compute cosine similarity between two embeddings."""
        if emb1 is None or emb2 is None:
            return 0.0
        
        emb1 = np.array(emb1, dtype=np.float32)
        emb2 = np.array(emb2, dtype=np.float32)
        
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(np.dot(emb1, emb2) / (norm1 * norm2))

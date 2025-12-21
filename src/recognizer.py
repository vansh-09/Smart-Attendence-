import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    if a is None or b is None:
        return -1.0
    a = a.astype(np.float32)
    b = b.astype(np.float32)
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-8
    return float(np.dot(a, b) / denom)


class Recognizer:
    def __init__(self, reference_embedding: np.ndarray, threshold: float = 0.6):
        self.reference_embedding = reference_embedding.astype(np.float32)
        self.threshold = threshold

    def recognize(self, probe_embedding: np.ndarray):
        sim = cosine_similarity(self.reference_embedding, probe_embedding)
        return sim, sim >= self.threshold

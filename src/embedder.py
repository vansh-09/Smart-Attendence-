import os
import cv2
import numpy as np
from PIL import Image
from urllib.error import URLError
from keras_facenet import FaceNet


class FaceEmbedder:
    def __init__(self):
        # Prefer a local cache inside the project to keep weights offline once fetched
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        cache_dir = os.path.join(base_dir, "models")
        os.makedirs(cache_dir, exist_ok=True)
        try:
            # Loads pretrained FaceNet (TensorFlow/Keras backend)
            self.model = FaceNet(cache_folder=cache_dir)
        except (URLError, Exception) as e:
            # Provide actionable guidance for SSL cert issues or offline usage
            raise RuntimeError(
                "Failed to initialize FaceNet model. If you see SSL certificate errors on macOS, "
                "run 'Install Certificates.command' for your Python version, or set SSL_CERT_FILE to certifi.where(). "
                "Alternatively, pre-download the FaceNet weights on a networked machine and place them under 'smart-attendance/models/'. "
                f"Original error: {e}"
            )

    @staticmethod
    def crop_and_resize(frame_bgr, box, size=160):
        x, y, w, h = box
        h_img, w_img = frame_bgr.shape[:2]
        x = max(0, x)
        y = max(0, y)
        x2 = min(w_img, x + w)
        y2 = min(h_img, y + h)
        face_bgr = frame_bgr[y:y2, x:x2]
        if face_bgr.size == 0:
            return None
        face_rgb = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(face_rgb)
        pil_img = pil_img.resize((size, size))
        return np.asarray(pil_img)

    def embed(self, face_rgb_160):
        """Generate 512-d embedding for a single 160x160 RGB face image."""
        if face_rgb_160 is None:
            return None
        # Model expects a batch
        embeddings = self.model.embeddings([face_rgb_160])
        # embeddings shape: (1, 512)
        return embeddings[0].astype(np.float32)

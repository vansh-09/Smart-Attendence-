import cv2
from mtcnn import MTCNN


class FaceDetector:
    def __init__(self):
        self.detector = MTCNN()

    def detect(self, frame_bgr):
        """Detect faces in a BGR frame, return list of detections.
        Each detection: { 'box': [x, y, w, h], 'confidence': float }
        """
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results = self.detector.detect_faces(rgb)
        detections = []
        for r in results:
            box = r.get('box', [0, 0, 0, 0])
            conf = r.get('confidence', 0.0)
            detections.append({'box': box, 'confidence': conf})
        return detections

    @staticmethod
    def clamp_box(box, width, height, margin=0):
        x, y, w, h = box
        x = max(0, x - margin)
        y = max(0, y - margin)
        w = w + 2 * margin
        h = h + 2 * margin
        x2 = min(width, x + w)
        y2 = min(height, y + h)
        x = max(0, x)
        y = max(0, y)
        w = max(1, x2 - x)
        h = max(1, y2 - y)
        return [x, y, w, h]

import os
import cv2
from deepface import DeepFace

EMBEDDINGS_DIR = "models/embeddings"
MODEL_NAME = "Facenet"
DISTANCE_METRIC = "cosine"
THRESHOLD = 0.4


class FaceRecognitionEngine:
    def __init__(self):
        if not os.path.exists(EMBEDDINGS_DIR):
            os.makedirs(EMBEDDINGS_DIR)

    def recognize(self, frame):
        """
        frame: image BGR (OpenCV)
        return: (recognized, user_id, distance)
        """
        try:
            results = DeepFace.find(
                img_path=frame,
                db_path=EMBEDDINGS_DIR,
                model_name=MODEL_NAME,
                distance_metric=DISTANCE_METRIC,
                enforce_detection=True
            )

            if len(results) == 0 or results[0].empty:
                return False, None, None

            best_match = results[0].iloc[0]
            distance = float(best_match["distance"])
            identity_path = best_match["identity"]

            user_id = int(os.path.splitext(os.path.basename(identity_path))[0])

            if distance <= THRESHOLD:
                return True, user_id, distance

            return False, None, distance

        except Exception:
            return False, None, None

    def register_user(self, user_id, frame):
        """
        Sauvegarde une image de référence pour un utilisateur
        """
        try:
            path = os.path.join(EMBEDDINGS_DIR, f"{user_id}.jpg")
            cv2.imwrite(path, frame)
            return True
        except Exception:
            return False

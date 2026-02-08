import cv2


class Camera:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise RuntimeError("Impossible d'accéder à la caméra")

    def capture_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def release(self):
        self.cap.release()

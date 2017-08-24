import cv2
import numpy as np
from atlasbuggy.camera.pipeline import Pipeline

class LeonaPipeline(Pipeline):
    def __init__(self, enabled=True, log_level=None):
        super(LeonaPipeline, self).__init__(enabled, log_level)

        self.face_detector = None

        self.results_service_tag = "results"
        self.add_service(self.results_service_tag, self.results_post_service)

    def results_post_service(self, data):
        return data

    def start(self):
        self.face_detector = FaceDetector(self.logger)

    def pipeline(self,frame):
        frame = self.face_detector.haar(frame)
        # print(self.face_detector.face, self.face_detector.face_size)
        self.post((self.face_detector.face, self.face_detector.face_size), service=self.results_service_tag)

class FaceDetector:
    def __init__(self, logger):
        self.logger = logger
        self.F_face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.1.0/data/haarcascades/haarcascade_frontalface_default.xml')
        self.face = None
        self.face_size = None

    def haar(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        F_faces = self.F_face_cascade.detectMultiScale(gray, 1.3, 5)

        (x_0, y_0, w_0, h_0) = (0, 0, 0, 0)
        face = None
        for (x, y, w, h) in F_faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if (w > w_0 and h > h_0):
                (x_0, y_0, w_0, h_0) = (x, y, w, h)
                face = (x_0, y_0, w_0, h_0)
        
        self.face = face

        if self.face is not None:
            (x, y, w, h) = self.face
            self.face_size = w * h
        else:
            self.face_size = None
        return frame

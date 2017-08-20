import os
import cv2
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
import numpy as np

from atlasbuggy.cameras.cvpipeline import CvPipeline


class Pipeline(CvPipeline):
    def __init__(self, enabled=True, log_level=None, generate_database=False):
        super(Pipeline, self).__init__(enabled, log_level, generate_bytes=True)
        self.actuators = None
        self.autonomous_mode = False

        # self.orb = cv2.ORB_create()
        self.num_segments = 50
        self.kernel = np.ones((5, 5), np.uint8)
        self.generate_database = generate_database
        self.F_face_cascade = cv2.CascadeClassifier('...haarcascades\haarcascade_frontalface_default.xml')
        # self.U_body_cascade = cv2.CascadeClassifier('...haarcascades\haarcascade_upperbody.xml')

        # directory = BaseFile.format_path_as_time("", None, "", "%Y_%b_%d %H;%M;%S", )[1]
        # self.database_dir = BaseFile("", directory, "", "", False, self.generate_bytes, False, False, False)
        # if self.generate_database:
        #     self.database_dir.make_dir()

    def take(self):
        self.capture = self.streams["capture"]
        # self.actuators = self.streams["actuators"]

    def haar(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        F_faces = F_face_cascade.detectMultiScale(gray, 1.3, 5)
        # U_bodies = U_body_cascade.detectMultiScale(gray, 1.3, 5)

        (x_0, y_0, w_0, h_0) = (0, 0, 0, 0)
        for (x, y, w, h) in F_faces:
            if (w > w_0 & h > h_0):
                (x_0, y_0, w_0, h_0) = (x, y, w, h)



        # for (x, y, w, h) in U_bodies:
        #     # print((x, y, w, h))
        #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #     roi_gray = gray[y:y + h, x:x + w]
        #         roi_color = frame[y:y + h, x:x + w]

        # cv2.imshow('img', frame)

    def pipeline(self):
import cv2
import mediapipe as mp
import numpy as np

class PoseDetector:
    def __init__(self, mode=False, model_complexity=1, smooth=True, detectionCon=0.5, trackCon=0.5):
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(
            static_image_mode=mode,
            model_complexity=model_complexity,
            smooth_landmarks=smooth,
            min_detection_confidence=detectionCon,
            min_tracking_confidence=trackCon
        )
        self.results = None

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks and draw:
            self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def findAngle(self, img, p1, p2, p3, draw=True):
        if not self.results or not self.results.pose_landmarks:
            return None
        lmList = self.results.pose_landmarks.landmark
        h, w, _ = img.shape
        a = np.array([lmList[p1].x * w, lmList[p1].y * h])
        b = np.array([lmList[p2].x * w, lmList[p2].y * h])
        c = np.array([lmList[p3].x * w, lmList[p3].y * h])
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180:
            angle = 360 - angle
        return angle

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

        if draw:
            cv2.putText(img, str(int(angle)), tuple(b.astype(int)), 
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

        return angle

# Initialize detector
detector = PoseDetector()

# Start webcam capture
cap = cv2.VideoCapture(0)

# Set camera resolution (optional)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Create full screen window
cv2.namedWindow("Squat Detector", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Squat Detector", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    success, img = cap.read()
    if not success:
        break

    img = detector.findPose(img)
    angle = detector.findAngle(img, 23, 25, 27)  # left leg: hip-knee-ankle

    if angle is not None:
        if angle < 90:
            cv2.putText(img, "Squat Detected", (50, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)
        else:
            cv2.putText(img, "Stand Up Straight", (50, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

    cv2.imshow("Squat Detector", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

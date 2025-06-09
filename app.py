import gradio as gr
import cv2
import numpy as np
from pose_detector import PoseDetector  # make sure this file exists

detector = PoseDetector()

# 🎥 Upload Video Function
def process_uploaded_video(video):
    cap = cv2.VideoCapture(video)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = detector.findPose(frame)
        angle = detector.findAngle(frame, 23, 25, 27)
        if angle is not None:
            if angle < 90:
                cv2.putText(frame, "Squat Detected", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)
            else:
                cv2.putText(frame, "Stand Up Straight", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
        frames.append(frame)
    cap.release()
    if frames:
        return frames[0]
    return None

# 📷 Webcam Frame Processing
def process_webcam_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame = detector.findPose(frame)
    angle = detector.findAngle(frame, 23, 25, 27)
    if angle is not None:
        if angle < 90:
            cv2.putText(frame, "Squat Detected", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)
        else:
            cv2.putText(frame, "Stand Up Straight", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# 🎛️ Upload Tab
upload_interface = gr.Interface(
    fn=process_uploaded_video,
    inputs=gr.Video(label="Upload a Squat Video"),
    outputs=gr.Image(label="First Frame Feedback"),
    title="📤 Squat Detection - Upload"
)

# 🎛️ Webcam Live Tab using gr.Live
webcam_interface = gr.Interface(
    fn=process_webcam_frame,
    inputs=gr.Image(streaming=True, label="Webcam Feed"),
    outputs=gr.Image(label="Processed Frame"),
    live=True,
    title="📷 Squat Detection - Webcam"
)

# 🚀 Launch the Tabbed App
demo = gr.TabbedInterface(
    [upload_interface, webcam_interface],
    ["Upload Video", "Live Webcam"]
)

demo.launch()
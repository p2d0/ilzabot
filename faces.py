import cv2
import os
import random
from moviepy.editor import VideoFileClip
# from pytube import YouTube
from collections import deque

def rect_contains_point(rect, point):
    x1, y1, w, h = rect
    x2, y2 = x1 + w, y1 + h
    px, py = point
    return x1 <= px <= x2 and y1 <= py <= y2

class FaceTracker:
    def __init__(self, face_cascade):
        self.face_cascade = face_cascade
        self.trackers = []
        self.names = ["@ahmetoff", "@androncerx"]
        self.unused_names = deque(self.names)
        self.face_ids = {}

    def update(self, frame):
        frame = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # First, update all existing trackers and remove any that are no longer tracking a face
        updated_trackers = []
        for tracker, name, face_id in self.trackers:
            ok, bbox = tracker.update(frame)

            if ok:
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))

                text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)  # Update the font scale and thickness
                text_x = p1[0] + (p2[0] - p1[0]) // 2 - text_size[0] // 2
                text_y = p1[1] - 10
                cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)  # Update the font scale

                updated_trackers.append((tracker, name, face_id, bbox))
            else:
                self.unused_names.append((name, face_id))

        # Then, initialize new trackers for any remaining faces
        for x, y, w, h in faces:
            face_point = (x + w // 2, y + h // 2)
            has_tracker = any([rect_contains_point(bbox, face_point) for _, _, _, bbox in updated_trackers])
            if has_tracker:
                continue

            if len(self.unused_names) == 0:
                self.unused_names = deque([(name, face_id) for name, face_id in self.face_ids.items()])

            if len(updated_trackers) >= len(self.names):
                break

            name, face_id = self.unused_names.popleft()
            self.face_ids[face_id] = name
            tracker = cv2.TrackerKCF_create()
            tracker.init(frame, (x, y, w, h))
            updated_trackers.append((tracker, name, face_id, (x, y, w, h)))

        self.trackers = [(tracker, name, face_id) for tracker, name, face_id, _ in updated_trackers]
        return frame

def facetrack_video(input_video):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face_tracker = FaceTracker(face_cascade)

    clip = VideoFileClip(input_video)

    # Modify the output_video filename by adding "_output" before the .mp4 extension
    output_filename = os.path.splitext(input_video)[0]
    output_extension = os.path.splitext(input_video)[1]
    output_video = f"{output_filename}_output{output_extension}"

    processed_clip = clip.fl_image(lambda frame: face_tracker.update(frame))
    processed_clip.write_videofile(output_video, audio=True)

    return output_video

def main():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face_tracker = FaceTracker(face_cascade)
    input_video = "input_video.mp4"
    output_video = "kekoutput.mp4"

    clip = VideoFileClip(input_video)
    processed_clip = clip.fl_image(lambda frame: face_tracker.update(frame))
    processed_clip.write_videofile(output_video, audio=True)

if __name__ == "__main__":
    main()

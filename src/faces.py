import cv2
import os
import random
from moviepy.editor import VideoFileClip
# from pytube import YouTube
from collections import deque
import dlib
face_detector = dlib.get_frontal_face_detector()

class FaceTracker:
    def __init__(self):
        self.trackers = []
        self.names = ["@ahmetoff", "@androncerx", "@Arsn17", "@serene_boy"]
        self.unused_names = deque(self.names)

    def rect_contains_point(self,rect, point):
        x1, y1, w, h = rect
        x2, y2 = x1 + w, y1 + h
        px, py = point
        return x1 <= px <= x2 and y1 <= py <= y2

    def update(self, frame):
        frame = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_detector(gray)

        # Convert the Dlib rectangles to OpenCV format
        faces = [(x.left(), x.top(), x.right() - x.left(), x.bottom() - x.top()) for x in faces]

        # First, update all existing trackers and remove any that are no longer tracking a face
        updated_trackers = []
        for tracker, name in self.trackers:
            ok, bbox = tracker.update(frame)

            if ok:
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))

                text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)  # Update the font scale and thickness
                text_x = p1[0] + (p2[0] - p1[0]) // 2 - text_size[0] // 2
                text_y = p1[1] - 10
                cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)  # Update the font scale

                updated_trackers.append((tracker, name, bbox))
            else:
                self.unused_names.append(name)

        # Then, initialize new trackers for any remaining faces
        for x, y, w, h in faces:
            face_point = (x + w // 2, y + h // 2)
            has_tracker = any([self.rect_contains_point(bbox, face_point) for _, _, bbox in updated_trackers])
            if has_tracker:
                continue

            if len(self.unused_names) == 0:
                self.unused_names = deque(self.names)

            if len(updated_trackers) >= len(self.names):
                break

            name = self.unused_names.popleft()
            tracker = cv2.TrackerKCF_create()
            tracker.init(frame, (x, y, w, h))
            updated_trackers.append((tracker, name, (x, y, w, h)))

        self.trackers = [(tracker, name) for tracker, name, _ in updated_trackers]
        return frame

def facetrack_video(input_video):
    face_tracker = FaceTracker()

    clip = VideoFileClip(input_video)

    # Modify the output_video filename by adding "_output" before the .mp4 extension
    output_filename = os.path.splitext(input_video)[0]
    output_extension = os.path.splitext(input_video)[1]
    output_video = f"{output_filename}_output{output_extension}"

    processed_clip = clip.fl_image(lambda frame: face_tracker.update(frame))
    processed_clip.write_videofile(output_video, audio=True)

    return output_video

def main():
    face_tracker = FaceTracker()
    input_video = "input_video.mp4"
    output_video = "kekoutput.mp4"

    clip = VideoFileClip(input_video)
    processed_clip = clip.fl_image(lambda frame: face_tracker.update(frame))
    processed_clip.write_videofile(output_video, audio=True)

if __name__ == "__main__":
    main()

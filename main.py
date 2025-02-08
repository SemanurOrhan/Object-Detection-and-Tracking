from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse  
import cv2
import imutils
import time

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())

color_ranges = {
    "green": ((35, 100, 100), (85, 255, 255)),  
    "blue": ((100, 100, 100), (130, 255, 255)),
    "yellow": ((20, 100, 100), (30, 255, 255))
}
draw_colors = {
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
    "yellow": (0, 255, 255)
}

object_history = {}

if not args.get("video", False):
    vs = VideoStream(src=0).start()
else:
    vs = cv2.VideoCapture(args["video"])
time.sleep(2.0)

while True:
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame

    if frame is None:
        break

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    for color, (lower, upper) in color_ranges.items():
        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        if len(cnts) > 0:
            for c in cnts:
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                if M["m00"] != 0:
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                else:
                    center = (0, 0)
                if radius > 10:
                    object_id = None
                    min_distance = float("inf")
                    for obj_id, history in object_history.items():
                        if obj_id.startswith(color):  
                            last_center = history[0] if len(history) > 0 else None
                            if last_center is not None:
                                distance = np.linalg.norm(np.array(center) - np.array(last_center))
                                if distance < min_distance: 
                                    min_distance = distance
                                    object_id = obj_id

                    if object_id is None or min_distance > 50: 
                        object_id = f"{color}_{len(object_history) + 1}"
                        object_history[object_id] = deque(maxlen=args["buffer"])
                    object_history[object_id].appendleft(center)

                    cv2.circle(frame, (int(x), int(y)), int(radius),
                               draw_colors[color], 2)
                    cv2.circle(frame, center, 5, draw_colors[color], -1)

                    for i in range(1, len(object_history[object_id])):
                        if object_history[object_id][i - 1] is None or object_history[object_id][i] is None:
                            continue

                        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                        cv2.line(frame, object_history[object_id][i - 1], object_history[object_id][i],
                                 draw_colors[color], thickness)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
if not args.get("video", False):
    vs.stop()
else:
    vs.release()
cv2.destroyAllWindows() 

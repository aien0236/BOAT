# import the necessary packages
import argparse
import cv2
import numpy as np
from imutils.video import VideoStream
import time


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", required=True, help="path to input video file")
#ap.add_argument("-o", "--output", required=True, help="path to output png")
args = vars(ap.parse_args())
try:
    # cap = VideoStream(src=0).start()
    cap = cv2.VideoCapture(0)

    pass
except:
    cap = cv2.VideoCapture(0)

blackLower = (0, 0, 0)
blackUpper = (150, 150, 150)

width = int(cap.get(3))  # float
height = int(cap.get(4))  # float
resultFrame = np.empty((height, width), dtype=np.uint8)
resultFrame.fill(255)
i = 0
while 0:
    boolen, frame = cap.read()  # get the frame

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (1, 1), 0)
    # gray = cv2.erode(gray, None, iterations=2)

    edged = cv2.Canny(gray, 35, 125)
    # edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.bitwise_not(edged)
    if i < 10:
        resultFrame = np.minimum(resultFrame, edged)
        i+=1

    resf = cv2.flip(resultFrame, 1)
    cv2.imshow('final', resf)
    # cv2.imshow('final', np.hstack([resf,redmasked,yellowmasked,greenmasked]))

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    # time.sleep(1)
resf = cv2.imread('painting4.jpg',0)  # get the frame
print(resf)
resf = cv2.cvtColor(resf, cv2.COLOR_GRAY2BGR)
cv2.imshow('RGB',resf)
cv2.imwrite('sketch.jpg', resf)
cap.release()
cv2.destroyAllWindows()

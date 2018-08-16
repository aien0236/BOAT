# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py

# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
# greenLower = (50, 150, 0)
# greenUpper = (150, 255, 100)

greenLower = (255, 255, 255)
greenUpper = (255, 255, 255)

# greenLower = (0, 0, 150)
# greenUpper = (255, 255, 255)

# redLower = (150, 150, 50)
# redUpper = (255, 255, 150)

redLower = (0, 200, 50)
redUpper = (50, 255, 255)

# whiteLower = (100, 50, 200)
# whiteUpper = (150, 100, 255)

whiteLower = (255, 255, 255)
whiteUpper = (255, 255, 255)

bgLower = (0,0,0)
bgUpper = (255,255,255)

gpts = deque(maxlen=args["buffer"])
rpts = deque(maxlen=args["buffer"])
wpts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start()

# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])

# allow the camera or video file to warm up
time.sleep(2.0)

# keep looping
while True:
	# grab the current frame
	frame = vs.read()

	# handle the frame from VideoCapture or VideoStream
	frame = frame[1] if args.get("video", False) else frame

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		break

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	greenmask = cv2.inRange(hsv, greenLower, greenUpper)
	greenmask = cv2.erode(greenmask, None, iterations=2)
	greenmask = cv2.dilate(greenmask, None, iterations=2)

	redmask = cv2.inRange(hsv, redLower, redUpper)
	redmask = cv2.erode(redmask, None, iterations=2)
	redmask = cv2.dilate(redmask, None, iterations=2)

	whitemask = cv2.inRange(hsv, whiteLower, whiteUpper)
	whitemask = cv2.erode(whitemask, None, iterations=2)
	whitemask = cv2.dilate(whitemask, None, iterations=2)

	bg = cv2.inRange(hsv, bgLower, bgUpper)
	bg = cv2.erode(bg, None, iterations=2)
	bg = cv2.dilate(bg, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	greencnts = cv2.findContours(greenmask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	greencnts = greencnts[0] if imutils.is_cv2() else greencnts[1]
	greencenter = None

	redcnts = cv2.findContours(redmask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	redcnts = redcnts[1] #if imutils.is_cv2() else redcnts[1]
	cv2.imshow("image", redcnts)
	cv2.waitKey(0)
	redcenter = None

	whitecnts = cv2.findContours(whitemask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	whitecnts = whitecnts[0] if imutils.is_cv2() else whitecnts[1]
	whitecenter = None

	# only proceed if at least one contour was found
	if len(greencnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		gc = max(greencnts, key=cv2.contourArea)
		((gx, gy), gradius) = cv2.minEnclosingCircle(gc)
		gM = cv2.moments(gc)
		greencenter = (int(gM["m10"] / gM["m00"]), int(gM["m01"] / gM["m00"]))
		# only proceed if the radius meets a minimum size
		if gradius > 10 and gradius < 30:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(gx), int(gy)), int(gradius),
				(0, 255, 0), 2)
			cv2.circle(frame, greencenter, 5, (0, 255, 0), -1)

			# cv2.circle(bg, (int(x), int(y)), int(radius),
			# 	(0, 255, 255), 2)
			# cv2.circle(bg, center, 5, (0, 255, 255), -1)
	if len(redcnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		rc = max(redcnts, key=cv2.contourArea)
		((rx, ry), rradius) = cv2.minEnclosingCircle(rc)
		rM = cv2.moments(rc)
		redcenter = (int(rM["m10"] / rM["m00"]), int(rM["m01"] / rM["m00"]))
		if rradius > 10 and rradius < 100:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(rx), int(ry)), int(rradius),
				(0, 0, 255), 2)
			cv2.circle(frame, redcenter, 5, (0, 0, 255), -1)

			# cv2.circle(bg, (int(x), int(y)), int(radius),
			# 	(0, 255, 255), 2)
			# cv2.circle(bg, center, 5, (0, 255, 255), -1)
	if len(whitecnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		wc = max(whitecnts, key=cv2.contourArea)
		((wx, wy), wradius) = cv2.minEnclosingCircle(wc)
		wM = cv2.moments(wc)
		whitecenter = (int(wM["m10"] / wM["m00"]), int(wM["m01"] / wM["m00"]))
		if wradius > 10 and wradius < 30:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(wx), int(wy)), int(wradius),
				(255, 255, 255), 2)
			cv2.circle(frame, whitecenter, 5, (255, 255, 255), -1)

			# cv2.circle(bg, (int(x), int(y)), int(radius),
			# 	(0, 255, 255), 2)
			# cv2.circle(bg, center, 5, (0, 255, 255), -1)
	# update the points queue
	gpts.appendleft(greencenter)
	rpts.appendleft(redcenter)
	wpts.appendleft(whitecenter)

	# loop over the set of tracked points
	for i in range(1, len(gpts)):
		# if either of the tracked points are None, ignore
		# them
		if gpts[i - 1] is None or gpts[i] is None:
			continue

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		gthickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, gpts[i - 1], gpts[i], (0, 255, 0), gthickness)
		# cv2.line(bg, pts[i - 1], pts[i], (0, 255, 255), thickness)
	for i in range(1, len(rpts)):
		# if either of the tracked points are None, ignore
		# them
		if rpts[i - 1] is None or rpts[i] is None:
			continue

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		rthickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, rpts[i - 1], rpts[i], (0, 0, 255), rthickness)
		# cv2.line(bg, pts[i - 1], pts[i], (0, 255, 255), thickness)
	for i in range(1, len(wpts)):
		# if either of the tracked points are None, ignore
		# them
		if wpts[i - 1] is None or wpts[i] is None:
			continue

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		wthickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, wpts[i - 1], wpts[i], (255, 255, 255), wthickness)
		# cv2.line(bg, pts[i - 1], pts[i], (0, 255, 255), thickness)

	# show the frame to our screen
	masked = cv2.bitwise_and(frame, frame, mask=redmask)

	# cv2.imshow("Frame", frame)
	cv2.imshow("Frame", redmask)
	# cv2.imshow("Frame", masked)
	# cv2.imshow("Frame", np.hstack([frame, masked]))

	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()

# otherwise, release the camera
else:
	vs.release()

# close all windows
cv2.destroyAllWindows()
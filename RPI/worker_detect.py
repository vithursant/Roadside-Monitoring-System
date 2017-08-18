# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py


# for open cv in virtual env
# > source ~/.profile
# > workon cv

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import running_avg
from running_avg import RunningAverage
import xbee_tx 
from xbee_tx import *
from picamera.array import PiRGBArray
from picamera import PiCamera


ra = RunningAverage(20)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=16,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (71, 157, 72)
greenUpper = (216, 255, 218)
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = PiCamera()
	camera.resolution = (640,480)
	camera.framerate = 32
	rawCapture = PiRGBArray(camera, size=(640,480))

# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])


# keep looping
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the current frame
	#(grabbed, frame) = camera.read()
	frame = frame.array	

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	#if args.get("video") and frame
	#	break

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			ra.add_value(1)
			print "detected!",ra.calc_speed()
	else:
		ra.add_value(0)
		print "........",ra.calc_speed()


	xbee_write(ra.calc_speed())	
	

	# update the points queue
	pts.appendleft(center)

	# loop over the set of tracked points
	for i in xrange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	rawCapture.truncate(0);

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
#camera.release()
cv2.destroyAllWindows()

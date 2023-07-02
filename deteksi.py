from collections import deque
from imutils.video import VideoStream
import numpy as np
# import argparse
import cv2
import imutils
import time

# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video",
# 	help="video file")
# ap.add_argument("-b", "--buffer", type=int, default=64,
# 	help="max buffer size")
# args = vars(ap.parse_args())
hsvLow = (10, 70, 80)
hsvMax = (30, 255, 255)

colors = []
# pts = deque(maxlen=args["buffer"])
pts = deque(maxlen=64)

def on_mouse_click (event, x, y, flags, frame):
    if event == cv2.EVENT_LBUTTONUP:
        colors.append(frame_hsv[y,x].tolist())

# vs = cv2.VideoCapture(args['video'])
vs = cv2.VideoCapture(0)

# time.sleep(2.0)
while True:
	# grab the current frame
	frame = vs.read()
	frame = frame[1]
	
	if frame is None:
		# print("Frame Break", frame)
		break
	
	frame = imutils.resize(frame, width=600)
	
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	## MASKING 
	mask = cv2.inRange(hsv, hsvLow, hsvMax)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	
 	## Mencari Contur
	contur = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	contur = imutils.grab_contours(contur)
	center = None
	
	frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS_FULL)
	if colors:
		cv2.putText(frame_hsv, str(colors[-1]), (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
	cv2.imshow("Frame HSV", frame_hsv)
	cv2.setMouseCallback("Frame HSV", on_mouse_click, hsv)
	
	if len(contur) > 0:
		# cari kontur terluar (border)
		c = max(contur, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
  
		print(radius)
		# titik tengah
		center = (int(M["m10"] / M["m00"]), 
            int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		if radius > 20:
			## Gambar lingkaran bola
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
	
	
	cv2.imshow("Frame", frame)
	cv2.imshow("Mask", mask)
	cv2.imshow("Frame HSV", frame_hsv)

	key = cv2.waitKey(1) & 0xFF
	# Break Loop jika tekan q
	if key == ord("q"):
		break

minb = min(c[0] for c in colors)
ming = min(c[1] for c in colors)
minr = min(c[2] for c in colors)
maxb = max(c[0] for c in colors)
maxg = max(c[1] for c in colors)
maxr = max(c[2] for c in colors)
print("Colors: ",colors)
print ("Min Red: {} - Min Green: {} - Min Blue: {} ".format(minr, ming, minb))
print("Min Red: {} - Min Green: {} - Min Blue: {}".format( maxr, maxg, maxb))

## Update HSV Low and Max
hsvLow = (minb,ming,minr)
hsvMax = (maxb,maxg,maxr)
print("hsv Max: {}".format(hsvMax))
print("hsv Low: {}".format(hsvLow))

# vs.stop()
vs.release()
cv2.destroyAllWindows()

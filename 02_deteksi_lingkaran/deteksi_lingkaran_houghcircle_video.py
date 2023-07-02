# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
# import argparse
import cv2
import imutils
import time

hsvLow = (10, 60, 80)
hsvUp  = (30, 255, 255)
buffer = deque(maxlen=64)

# vs = VideoStream(src = 0).start()

# vs = cv2.VideoCapture(0)

vs = cv2.VideoCapture("out2.mkv")
# time.sleep(2.0)

while True:
    ret, frame = vs.read()
    # frame = frame[1]
    if frame is None:
        break   
    frame = imutils.resize(frame, width = 300)
    
    
    # MASKING 
    maskBlur = cv2.GaussianBlur (frame, (11, 11), 0)
    hsv = cv2.cvtColor(maskBlur, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, hsvLow, hsvUp)
    mask = cv2.erode(mask, None, iterations = 2)
    mask = cv2.dilate(mask, None, iterations = 2)
    
    
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayBlur  = cv2.blur(grayFrame, (3, 3))
    detectBola = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 2, param1 = 100, param2 = 50, minRadius = 0, maxRadius = 0)
     
    if detectBola is not None:
        
        detectBola = np.uint16(np.around(detectBola))
        
        for pt in detectBola[0, :]:
            
            a, b, r = pt[0], pt [1], pt[2]
            # print(r)
            cv2.circle(frame, (a, b), r, (0, 255, 0), 2)
            
            cv2.circle(frame, (a, b), 1, (0, 0, 255), 3)
    
    cv2.imshow("coiaw", frame)
    cv2.imshow("Hitam Putih", grayFrame)
    cv2.imshow("Hitam Putih Blurred", grayBlur)
    cv2.imshow("Masking", mask)
    
    tunggu = cv2.waitKey(1) & 0xFF
    
    if tunggu == ord("q") :
        break
    
    # else: 
    #     continue
    # print(tunggu)

vs.release()
cv2.destroyAllWindows()
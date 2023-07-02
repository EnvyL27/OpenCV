# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
# import argparse
import cv2
import imutils
import time


hsvLow = (7, 20, 109)
hsvUp  = (211, 225, 225)
buffer = deque(maxlen=64)

colors = []

# vs = VideoStream(src = 0).start()

def on_mouse_click (event, x, y, flags, frame):
    if event == cv2.EVENT_LBUTTONUP:
        colors.append(frame_hsv[y,x].tolist())


vs = cv2.VideoCapture(0)
# time.sleep(2.0)

while True:
    ret, frame = vs.read()
    # frame = frame[1]
    if frame is None:
        break   
    
    frame = imutils.resize(frame, width = 500)
    
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayBlur  = cv2.blur(grayFrame, (3, 3))
    canny = cv2.Canny(grayBlur,100,200)
        
    # MASKING 
    maskBlur = cv2.GaussianBlur (frame, (11, 11), 0)
    hsv = cv2.cvtColor(maskBlur, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, hsvLow, hsvUp)
    mask = cv2.erode(mask, None, iterations = 2)
    mask = cv2.dilate(mask, None, iterations = 2)
    
    # Hough Circle
    detectBola = cv2.HoughCircles(canny, cv2.HOUGH_GRADIENT, 1, 10, param1 = 200, param2 = 100, minRadius = 0, maxRadius = 0)
    detected_circles = cv2.HoughCircles(grayBlur,  
                cv2.HOUGH_GRADIENT, 1, 20, param1 = 40, 
            param2 = 30, minRadius = 0, maxRadius = 250)
    
    # Draw circles that are detected. 
    if detected_circles is not None: 

    # Convert the circle parameters a, b and r to integers. 
        detected_circles = np.uint16(np.around(detected_circles)) 
    # detected_circles = np.round(detected_circles[0, :]).astype("int")
 

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
    if colors:
        cv2.putText(frame_hsv, str(colors[-1]), (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
    cv2.imshow("Frame HSV", frame_hsv)
    cv2.setMouseCallback("Frame HSV", on_mouse_click, hsv)
	

    if detectBola is not None:
        
        detectBola = np.uint16(np.around(detectBola))
        
        for pt in detectBola[0, :]:
            a, b, r = pt[0], pt [1], pt[2]
            
            cv2.circle(frame, (a, b), r, (0, 255, 0), 2)
            
            cv2.circle(frame, (a, b), 1, (0, 0, 255), 3)
    
    cv2.imshow("ciaow", frame)
    # cv2.imshow("Hitam Putih", grayFrame)
    cv2.imshow("Canny", canny)
    cv2.imshow("Masking", mask)
    cv2.imshow("Frame HSV", frame_hsv)

    
    tunggu = cv2.waitKey(1) & 0xFF
    
    if tunggu == ord("q") :
        break
    
    # else: 
    #     continue
    # print(tunggu)


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
##
## Morphological Transformation => Mengurangi blur saat gambar bergerak
##

import cv2
import numpy as np
import imutils
import time
# hsvLow = (17, 15, 100)
# hsvMax = (50, 56, 200)

def nothing(x):
    pass
    

hsvLow = np.array([10, 70, 80])
hsvMax = np.array([30, 255, 255])

# hsvLow = np.array([50, 85, 115])
# hsvMax = np.array([70, 105, 195])


#
warnaHsv = None
image_hsv = None
colors =[]

# vs = cv2.VideoCapture(0)

# vs = cv2.VideoCapture("../video/out2.mkv")

cv2.namedWindow("Trackbars")
# cv2.resizeWindow("Trackbars", 600, 600)

cv2.createTrackbar("Low Hue", "Trackbars", hsvLow[0], 179, nothing)
cv2.createTrackbar("Low Sat", "Trackbars", hsvLow[1], 255, nothing)
cv2.createTrackbar("Low Val", "Trackbars", hsvLow[2], 255, nothing)
cv2.createTrackbar("Max Hue", "Trackbars", hsvMax[0], 179, nothing)
cv2.createTrackbar("Max Sat", "Trackbars", hsvMax[1], 255, nothing)
cv2.createTrackbar("Max Val", "Trackbars", hsvMax[2], 255, nothing)


def pick_color(event,x,y,flags,param):
    global hsvMax, hsvLow

    if event == cv2.EVENT_LBUTTONDOWN:
        # pixel = image_hsv[y, x]

        print("Clicked: ",frame[0][0])
          
        pixel = np.uint8([[[frame[y, x, 0], frame[y, x, 1], frame[y, x, 2] ]]])
        pixel = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)
        
        print("Frame HSV",pixel)        
          
        # cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)
        #you might want to adjust the ranges(+-10, etc):
        # hsvMax = np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
        hsvMax = np.array([pixel[0][0][0] + 10, pixel[0][0][1] + 10, pixel[0][0][2] + 40])
        
        # hsvMax = np.array(pixel[0][0][0] - 10, )
        hsvLow = np.array([pixel[0][0][0] - 10, pixel[0][0][1] - 10, pixel[0][0][2] - 40])
        
        
        print("NEW HSV LOw", hsvLow)
        print("NEW HSV Max", hsvMax)
        # time.sleep(1.0)
            
        if hsvLow[0] < 0:
            hsvLow[0] = 0
        if hsvLow[1] < 0:
            hsvLow[1] = 0
        if hsvLow[2] < 0:
            hsvLow[2] = 0
        
        if hsvMax[0] < 0:
            hsvMax[0] = 0
        if hsvMax[1] < 0:
            hsvMax[1] = 0
        if hsvMax[2] < 0:
            hsvMax[2] = 0
            
        cv2.createTrackbar("Low Hue", "Trackbars", hsvLow[0], 179, nothing)
        cv2.createTrackbar("Low Sat", "Trackbars", hsvLow[1], 255, nothing)
        cv2.createTrackbar("Low Val", "Trackbars", hsvLow[2], 255, nothing)
        cv2.createTrackbar("Max Hue", "Trackbars", hsvMax[0], 179, nothing)
        cv2.createTrackbar("Max Sat", "Trackbars", hsvMax[1], 255, nothing)
        cv2.createTrackbar("Max Val", "Trackbars", hsvMax[2], 255, nothing)

        # print("Pixel : {} \nHSV Low : {} \nHSV High : {}".format(pixel, hsvLow, hsvMax))
        # image_mask = cv2.inRange(image_hsv, hsvLow, hsvMax)

        # cv2.imshow("mask", image_mask)

# while vs.isOpened():

# _, frame = vs.read()

frame = cv2.imread("../image/input.jpg")
## Ambil Nilai Trackbar
trackbar_LowHue = cv2.getTrackbarPos("Low Hue", "Trackbars")
trackbar_LowSat = cv2.getTrackbarPos("Low Sat", "Trackbars")
trackbar_LowVal = cv2.getTrackbarPos("Low Val", "Trackbars")
trackbar_MaxHue = cv2.getTrackbarPos("Max Hue", "Trackbars")
trackbar_MaxSat = cv2.getTrackbarPos("Max Sat", "Trackbars")
trackbar_MaxVal = cv2.getTrackbarPos("Max Val", "Trackbars")

# # print(trackbar_LowHue)

hsvLow = np.array([trackbar_LowHue, trackbar_LowSat, trackbar_LowVal])
hsvMax = np.array([trackbar_MaxHue, trackbar_MaxSat, trackbar_MaxVal])

# print("/n/nlowhsv", hsvLow)
# print("mashsv", hsvMax)


# Exception jika Video Selesai
if frame is None:
    break
# frame_hsv = frame.copy()

frame =imutils.resize(frame, width=300)
# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)



cv2.namedWindow("Input")
cv2.setMouseCallback('Input', pick_color)

# cv2.imshow("Input", frame)

# image_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
# find the colors within the specified boundaries and apply
# the mask


pre_mask = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
image_mask = cv2.inRange(pre_mask, hsvLow, hsvMax)


kernel = np.ones((4, 4), np.uint8)
erosion = cv2.erode(image_mask, kernel)
dilation = cv2.dilate(image_mask, kernel)

opening = cv2.morphologyEx(image_mask, cv2.MORPH_OPEN, kernel, iterations=2)
closing = cv2.morphologyEx(image_mask, cv2.MORPH_CLOSE, kernel)

output_masking = cv2.bitwise_and(frame, frame, mask=image_mask)
output_blurred = cv2.GaussianBlur(output_masking, (3, 3), 0)
# konversi masking ke gray
image_gray = cv2.cvtColor(output_masking, cv2.COLOR_BGR2GRAY)
# pertajam dengan threshold
ret, treshold = cv2.threshold(image_gray, 127, 255, 0)
# treshold = cv2.Canny(image_gray, 100, 200)
# treshold = cv2.Canny(treshold, 100, 200)

# cari kontur 
# contur, hirarki = cv2.findContours(image_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
##Plan 2
contur = cv2.findContours(treshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contur = imutils.grab_contours(contur)
center = None

# erode = cv2.erode(output_masking,None,iterations = 3)
# dilate = cv2.dilate(erode,None,iterations = 10)
# contours,hierarchy = cv2.findContours(output_masking,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE) 

# for cnt in contur:

#     x,y,w,h = cv2.boundingRect(cnt)
#     print(w, h)
#     # if(w < 60 or h < 60):
#     #     continue

#     cx,cy = x+w/2, y+h/2

#     if 20 < output_masking.item(cy,cx,0) < 30:
#         cv2.rectangle(frame,(x,y),(x+w,y+h),[0,255,255],2)
#         print("yellow :", x,y,w,h)
#     elif 100 < int(output_masking.item(cy,cx,0)) < 120:
#          cv2.rectangle(frame,(x,y),(x+w,y+h),[255,0,0],2)
#          print("blue :", x,y,w,h)
#          detected = True

if len(contur) > 0:
    # cari kontur terluar (border)
    c = max(contur, key=cv2.contourArea)
    ((x, y), radius) = cv2.minEnclosingCircle(c)
    M = cv2.moments(c)
    
    #Execption ketika pembagi = 0
    if M["m00"] == 0:
        M["m00"] = 0.0000000000001
        
    # print("Nilai Radius: {} - Nilai X: {} - Nilai Y: {}".format(radius, x, y))
    # titik tengah
    center = (int(M["m10"] / M["m00"]), 
        int(M["m01"] / M["m00"]))
    # only proceed  if the radius meets a minimum size
    if radius > 0.1:
        ## Gambar lingkaran bola
        # cv2.circle(frame, (int(x), int(y)), int(radius)+2,
            # (0, 255, 255), 2)
        pass
        # cv2.circle(frame, center, 1, (0, 0, 255), -1)

# print(frame[0][0])
# print("HSV LOw", hsvLow)
# print("HSV Max", hsvMax)

# show the images
cv2.imshow("Input", frame)
cv2.imshow("Output", output_blurred)
cv2.imshow("Opening", opening)
cv2.imshow("Closing", closing)
# cv2.resizeWindow("Output Treshold",500,500)
cv2.imshow("Output Treshold", treshold)
# cv2.imwrite("../image/input.jpg",frame)
key = cv2.waitKey(0) 
if key == ord("q"):
    break


vs.release()
cv2.destroyAllWindows()
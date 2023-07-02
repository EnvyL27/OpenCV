import cv2
import numpy as np
import imutils
# hsvLow = (17, 15, 100)
# hsvMax = (50, 56, 200)

hsvLow = (10, 70, 80)
hsvMax = (30, 255, 255)
#
warnaHsv = None
image_hsv = None
colors =[]

# vs = cv2.VideoCapture(0)
vs = cv2.VideoCapture("../video/out2.mkv")

def pick_color(event,x,y,flags,param):
    global hsvMax, hsvLow

    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image_hsv[y, x]
        pixel2 = image_hsv[y, x]
        pixel3 = image_hsv[y, x]

        #you might want to adjust the ranges(+-10, etc):
        hsvMax = np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
        hsvLow = np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])

        print("Pixel : {} \nHSV Low : {} \nHSV High : {}".format(pixel, hsvLow, hsvMax))
        image_mask = cv2.inRange(image_hsv, hsvLow, hsvMax)

        # cv2.imshow("mask", image_mask)

while vs.isOpened():

    _, frame = vs.read()

    # Exception jika Video Selesai
    if frame is None:
        break
    frame_hsv = frame.copy()

    frame =imutils.resize(frame, width=300)
    
    cv2.namedWindow("Input")
    cv2.setMouseCallback('Input', pick_color)

    # cv2.imshow("Input", frame)

    image_hsv = cv2.cvtColor(frame_hsv, cv2.COLOR_BGR2HSV)
    # find the colors within the specified boundaries and apply
    # the mask
    image_mask = cv2.inRange(frame, hsvLow, hsvMax)
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
            
        print("Nilai Radius: {} - Nilai X: {} - Nilai Y: {}".format(radius, x, y))
        # titik tengah
        center = (int(M["m10"] / M["m00"]), 
            int(M["m01"] / M["m00"]))
        # only proceed  if the radius meets a minimum size
        if radius > 0.1:
            ## Gambar lingkaran bola
            cv2.circle(frame, (int(x), int(y)), int(radius)+2,
                (0, 255, 255), 2)
            cv2.circle(frame, center, 1, (0, 0, 255), -1)


    # show the images
    cv2.imshow("Input", frame)
    cv2.imshow("Output", output_blurred)
    cv2.imshow("Output Canny ", treshold)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break


vs.release()
cv2.destroyAllWindows()
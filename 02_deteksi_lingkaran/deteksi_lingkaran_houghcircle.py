
import cv2 
import numpy as np 
  
# Read image. 
img = cv2.imread('../image/circle.jpg', cv2.IMREAD_COLOR) 
# image = cv2.imread(args["image"])
output = img.copy()
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Convert to grayscale. 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
  
# Blur using 3 * 3 kernel. 
gray_blurred = cv2.blur(gray, (3, 3)) 
  

    # Apply Hough transform on the blurred image. 
detected_circles = cv2.HoughCircles(gray_blurred,  
                cv2.HOUGH_GRADIENT, 1, 20, param1 = 40, 
            param2 = 30, minRadius = 0, maxRadius = 250) 

# detected_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2,100 )
# Draw circles that are detected. 
if detected_circles is not None: 

    # Convert the circle parameters a, b and r to integers. 
    detected_circles = np.uint16(np.around(detected_circles)) 
    # detected_circles = np.round(detected_circles[0, :]).astype("int")

    for pt in detected_circles[0, :]: 
        a, b, r = pt[0], pt[1], pt[2] 

    #     # Draw the circumference of the circle. 
    #     cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
    #     cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
        cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
    #     # Draw a small circle (of radius 1) to show the center. 
        cv2.circle(img, (a, b), 1, (0, 0, 255), 3) 
        
cv2.namedWindow("Out", cv2.WINDOW_NORMAL)
cv2.imshow("Out", img)
cv2.waitKey(0)       


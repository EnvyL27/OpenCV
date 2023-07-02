# import numpy as np
# import cv2
# import imutils 



# ## Load Gambar
# img = cv2.imread("../image/circle.jpg", cv2.IMREAD_COLOR)
# img_copy = img.copy() ## Mengcopy gambar
# img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) ## Konversi Gambar BGR jadi Grey

# detect_circle = cv2.HoughCircles(img_grey, cv2.HOUGH_GRADIENT, 1.2, 100)

# if detect_circle is not None:
    
#     detect_circle = np.round(detect_circle[0, :]).astype("int")

#     for (x, y, r) in detect_circle:
# 		# draw the circle in the output image, then draw a rectangle
# 		# corresponding to the center of the circle
#         cv2.circle(img_copy, (x, y), r, (0, 255, 0), 4)
#         cv2.rectangle(img_copy, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        
#         cv2.imshow("Detected", img)
#         cv2.imshow("Input", img_copy)
        
#     cv2.imshow("output", np.hstack([img, img_copy]))
#     cv2.waitKey(0)

# # load the image, clone it for output, and then convert it to grayscale
# image = cv2.imread("../image/circle.jpg")
# output = image.copy()
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# while True:
    
#     # detect circles in the image
#     circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)

#     # ensure at least some circles were found
#     if circles is not None:
#         # convert the (x, y) coordinates and radius of the circles to integers
#         circles = np.round(circles[0, :]).astype("int")
#         # loop over the (x, y) coordinates and radius of the circles
#         for (x, y, r) in circles:
#             # draw the circle in the output image, then draw a rectangle
#             # corresponding to the center of the circle
#             cv2.circle(output, (x, y), r, (0, 255, 0), 4)
#             cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
#         # show the output image
#         cv2.imshow("output", np.hstack([image, output]))
#         cv2.waitKey(0)



import cv2 
import numpy as np 
  
# Read image. 
img = cv2.imread('../image/circle.jpg', cv2.IMREAD_COLOR) 
  
# Convert to grayscale. 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
  
# Blur using 3 * 3 kernel. 
gray_blurred = cv2.blur(gray, (3, 3)) 
  
while True:
    # Apply Hough transform on the blurred image. 
    detected_circles = cv2.HoughCircles(gray_blurred,  
                    cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
                param2 = 30, minRadius = 1, maxRadius = 40) 
    
    # Draw circles that are detected. 
    if detected_circles is not None: 
    
        # Convert the circle parameters a, b and r to integers. 
        detected_circles = np.uint16(np.around(detected_circles)) 
    
        for pt in detected_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2] 
    
            # Draw the circumference of the circle. 
            cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
            # cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
            # cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
            # Draw a small circle (of radius 1) to show the center. 
            cv2.circle(img, (a, b), 1, (0, 0, 255), 3) 
            
        cv2.imshow("Detected Circle", img) 
        key = cv2.waitKey(0)
        
        if key != None:
            break
 
        

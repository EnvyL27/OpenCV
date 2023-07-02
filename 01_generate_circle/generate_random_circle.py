import cv2 as cv
import numpy as np

canvas = np.zeros((500, 500, 3), dtype= "uint8")

while True:

    for i in range(100):
        color = np.random.randint(0, high=255, size= (3, )).tolist()
        radius = np.random.randint(30, high=50)
        center = np.random.randint(100, high=canvas.shape[1]-100, size=(2, ))
    
        cv.circle(canvas, tuple(center), radius, color, -1)
    

    cv.imshow("Canvas", canvas)
    key =  cv.waitKey(0)

    if key != None:
        break

cv.imwrite('../image/circle.jpg', canvas)
cv.destroyAllWindows()

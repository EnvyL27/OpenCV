import cv2
import numpy
import imutils


## Mebuat Canvas
canvas = numpy.zeros((300, 300, 3), dtype = "uint8")

## membuat 3 lingkran, random center point
for i in range(3):
    radius = numpy.random.randint(20, high=50)
    center_pt = numpy.random.randint(50, high=250, size=(2,))
    color = numpy.random.randint(0, high=255, size=(3,)).tolist()

    cv2.circle(canvas, tuple(center_pt), radius , color, -1)
    cv2.rectangle(canvas, (20,20), (100, 100), (255, 0, 0), -1) 
    
cv2.imshow("output", canvas)
cv2.imwrite("../image/circle.jpg", canvas)
cv2.waitKey(0)
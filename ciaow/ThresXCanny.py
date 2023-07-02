import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('Jokowi.jpg',0)
edges = cv2.Canny(img,100,200)
ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

images = [img, edges, ret]

for i in range(3): 
    plt.subplot(1,3,i*3+1),plt.imshow(images[i*3], 'gray')
    plt.title('Original'), plt.xticks([]), plt.yticks([])
    plt.subplot(1,3,i*3+2),plt.imshow(images[i*3+1], 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(1,3,i*3+3),plt.imshow(images[i*3+2],'gray')
    plt.title('thres'), plt.xticks([]), plt.yticks([])

cv2.imshow("Caw", img)
cv2.imshow("Canny Edges", edges)
cv2.imshow("Thres", ret)

plt.show()
# 
# 
# 
    # plt.subplot(3,3,i*3+1),plt.imshow(images[i*3],'gray')
    # plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])
    # plt.subplot(3,3,i*3+2),plt.hist(images[i*3].ravel(),256)
    # plt.title(titles[i*3+1]), plt.xticks([]), plt.yticks([])
    # plt.subplot(3,3,i*3+3),plt.imshow(images[i*3+2],'gray')
    # plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])
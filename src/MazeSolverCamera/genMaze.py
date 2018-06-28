import cv2
import numpy as np

img = np.zeros((850, 1100, 3), np.uint8)
img[:,:] = (255, 255, 255)

thickness = 25

for row in range(50, 850, 250):
    cv2.line(img, (50, row), (1050, row), (0, 0, 0), thickness)

for col in range(50, 1100, 250):
    cv2.line(img, (col, 50), (col, 800), (0, 0, 0), thickness)

cv2.imwrite("mazeBase.png", img)

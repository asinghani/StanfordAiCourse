import numpy as np
import cv2
import cv2.aruco as aruco

arucoDict = aruco.Dictionary_get(aruco.DICT_6X6_250)

for i in range(250):
    img = aruco.drawMarker(arucoDict, i, 700)
    cv2.imwrite("marker{}.jpg".format(i), img)

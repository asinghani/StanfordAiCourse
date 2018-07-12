import numpy as np
import cv2

def solidity(contour):
    area = cv2.contourArea(contour)
    hull = np.int0(cv2.boxPoints(cv2.minAreaRect(contour)))
    hull_area = cv2.contourArea(hull)
    if hull_area > 0.03:
        solidity = float(area) / hull_area
        return solidity
    else:
        return 0.0

def pipeline(img):
    s = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[:,:,1]
    _, thresh = cv2.threshold(s.copy(), 90, 255, cv2.THRESH_BINARY)
    cv2.imwrite("thresh.png", thresh)
    im2, contours2, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cg = [c for c in contours2 if cv2.contourArea(c) > 1700 and cv2.contourArea(c) < 3500]
    cg = [c for c in cg if solidity(c) > 0.8]
    boundingRects = [np.int0(cv2.boxPoints(cv2.minAreaRect(c))) for c in cg]
    #boundingBoxes = [cv2.boundingRect(c) for c in cg]
    #boundingBoxes = [((x - 10, y - 10), (x+w + 10, y+h + 10)) for x, y, w, h in boundingBoxes]
    return boundingRects

def getObstaclePositions(image, transformMatrix):
    boundingRects = pipeline(image)
    obstacles = []
    for rect in boundingRects:
        robotPoint = np.array(rect, dtype=np.float32)
        robotPoint = np.array([robotPoint])
        rect = cv2.perspectiveTransform(robotPoint, transformMatrix)
        obstacles.append(rect)
    return np.array(obstacles, dtype=np.float32)

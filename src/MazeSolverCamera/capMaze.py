import cv2
import sys, os
import imutils.perspective
import skimage.filters
import numpy as np

DEBUG = False

def getMazeData(img, full=True):
    if DEBUG:
        cv2.imshow("src image", cv2.resize(img, (480, 270)))

    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grey = cv2.GaussianBlur(grey, (5, 5), 0)

    if DEBUG:
        cv2.imshow("grey blurred", cv2.resize(grey, (480, 270)))

    edges = cv2.Canny(grey, 45, 220)

    if DEBUG:
        cv2.imshow("edges", cv2.resize(edges, (480, 270)))

    contours = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[1]
    contours = sorted(contours, key = cv2.contourArea, reverse=True)[:5] # find 5 largest contours

    if DEBUG:
        contourImg = img.copy()
        cv2.drawContours(contourImg, contours, -1, (0, 255, 0), 2)
        cv2.imshow("contours", cv2.resize(contourImg, (480, 270)))

    finalContour = None

    for contour in contours:
        rect = cv2.approxPolyDP(contour, 0.005 * cv2.arcLength(contour, True), True)
        if len(rect) == 4:
            finalContour = rect
            break

    if finalContour is None:
        # print("No paper found")
        contourImg = img.copy()
        cv2.drawContours(contourImg, contours, -1, (0, 255, 0), 2)
        return contourImg, [] 
        sys.exit(0)

    if not full:
        finalContourImg = img.copy()
        cv2.drawContours(finalContourImg, [finalContour], -1, (0, 255, 0), 4)
        return finalContourImg, None

    if DEBUG:
        finalContourImg = img.copy()
        cv2.drawContours(finalContourImg, [finalContour], -1, (0, 255, 0), 4)
        cv2.imshow("paper", cv2.resize(finalContourImg, (480, 270)))

    mazeImg = imutils.perspective.four_point_transform(img, finalContour.reshape(4, 2))
    mazeImg = cv2.resize(mazeImg, (1100, 850))
    mazeImgGrey = cv2.cvtColor(mazeImg, cv2.COLOR_BGR2GRAY)

    if DEBUG:
        cv2.imshow("top down view", cv2.resize(mazeImgGrey, (550, 425)))

    mazeImgThreshold = mazeImgGrey.copy()
    mazeImgThreshold[mazeImgThreshold > 90] = 1
    mazeImgThreshold[mazeImgThreshold != 1] = 0
    #print(mazeImgThreshold)

    mazeImgThresholdDisp = mazeImgThreshold.copy()
    mazeImgThresholdDisp[mazeImgThresholdDisp == 1] = 255

    # 0 = left, 1 = right, 2 = up, 3 = down
    accessGrid = [[[] for i in range(4)] for j in range(3)]

    for y in range(3):
        for x in range(4):
            xC = 175 + 250 * x
            yC = 175 + 250 * y
            # x1, x2, y1, y2
            top = (xC - 110, xC + 110, yC - 140, yC - 110)
            bottom = (xC - 110, xC + 110, yC + 110, yC + 140)
            left = (xC - 140, xC - 110, yC - 110, yC + 110)
            right = (xC + 110, xC + 140, yC - 110, yC + 110)


            if np.average(mazeImgThreshold[left[2]:left[3], left[0]:left[1]].flatten()) > 0.7:
                accessGrid[y][x].append(0)

            if np.average(mazeImgThreshold[right[2]:right[3], right[0]:right[1]].flatten()) > 0.7:
                accessGrid[y][x].append(1)

            if np.average(mazeImgThreshold[top[2]:top[3], top[0]:top[1]].flatten()) > 0.7:
                accessGrid[y][x].append(2)

            if np.average(mazeImgThreshold[bottom[2]:bottom[3], bottom[0]:bottom[1]].flatten()) > 0.7:
                accessGrid[y][x].append(3)

    cv2.imshow("flat display", mazeImgThresholdDisp)
    #cv2.waitKey(25000)
    return mazeImgThresholdDisp, accessGrid

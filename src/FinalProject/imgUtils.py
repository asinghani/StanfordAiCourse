import numpy as np
import cv2
import math

def overlayImages(img1, img2):
    newImg = np.copy(img1)
    rows, cols, channels = img2.shape
    roi = img1[0:rows, 0:cols]

    maskimg = np.copy(img2).astype(np.uint8)
    maskimg[(maskimg == [0, 0, 0]).all(axis=2)] = [255, 255, 255]

    cv2.imwrite("aaa.png", maskimg)

    _, mask = cv2.threshold(cv2.cvtColor(maskimg, cv2.COLOR_BGR2GRAY), 150, 255, cv2.THRESH_BINARY_INV)
    _, invmask = cv2.threshold(cv2.cvtColor(maskimg, cv2.COLOR_BGR2GRAY), 150, 255, cv2.THRESH_BINARY)

    overlay = cv2.bitwise_and(roi, roi, mask = invmask)
    background = cv2.bitwise_and(img2, img2, mask = mask)

    cv2.imwrite("mask.png", mask)
    cv2.imwrite("invmask.png", invmask)
    cv2.imwrite("overlay.png", overlay)
    cv2.imwrite("background.png", background)

    newImg[0:rows, 0:cols] = cv2.add(overlay, background)
    return newImg

def resizeContour(contour, scale):
    contour = np.copy(contour)
    contour_ = np.swapaxes(contour, 0, 1)
    centreX = np.average(contour_[0])
    centreY = np.average(contour_[1])

    contour = contour - (centreX, centreY)
    contour = contour * scale
    contour = contour + (centreX, centreY)

    return contour

def splitVector(vec):
    mag = math.sqrt(vec[0] ** 2 + vec[1] ** 2)
    return mag, vec[0] / mag, vec[1] / mag

def extendVector(point1, point2, distance):
    # returns new point2
    x0 = point1[0]
    y0 = point1[1]

    x = point2[0] - x0
    y = point2[1] - y0

    mag, unitX, unitY = splitVector((x, y))
    mag = mag + distance
    return (x0 + unitX * mag, y0 + unitY * mag)

def expandContour(contour, distance):
    try:
        cornerDist = distance * math.sqrt(2.0)
        contour = np.copy(contour)
        contour_ = np.swapaxes(contour, 0, 1)
        centerX = np.average(contour_[0])
        centerY = np.average(contour_[1])
        center = (centerX, centerY)

        corner1 = extendVector(center, contour[0], distance)
        corner2 = extendVector(center, contour[1], distance)
        corner3 = extendVector(center, contour[2], distance)
        corner4 = extendVector(center, contour[3], distance)

        #print(corner1, corner2, corner3, corner4)

        return np.array([corner1, corner2, corner3, corner4], dtype=np.float32)

    except:
        return contour

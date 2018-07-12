### TODO: calibrate with proper points in order to output robot position in centimeteres

import numpy as np
import cv2
import cv2.aruco as aruco
import math
from imutils import perspective
import time

cameraMatrix = np.array([[800.00,  0.0000,  506.74],
                         [0.0000,  799.52,  295.31],
                         [0.0000,  0.0000,  1.0000]])

distortionCoefficients = np.array([2.02398690e-02, -7.49331991e-01, 1.86798290e-03, 9.14052734e-04, 1.96948175e+00])

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()
parameters.maxMarkerPerimeterRate = 10.0

def baseround(x, base=5):
    return int(base * round(float(x) / base))

def roundArray(A, base=1):
    return np.array([baseround(v, base) for v in A])

def rotationMatrixToEulerAngles(R):
    R = cv2.Rodrigues(R)[0]

    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return np.array([x, y, z])

def getForwardVectorImagePoints(_rvec, _tvec, length):
    objectPoints = np.array([(0, 0, 0), (0, length, 0)])
    imagePoints, _ = cv2.projectPoints(objectPoints, _rvec, _tvec, cameraMatrix, distortionCoefficients)

    return [imagePoints[0], imagePoints[1]]

def drawForwardAxis(image, _rvec, _tvec, length):
    try:
        initialPoint, terminalPoint = getForwardVectorImagePoints(_rvec, _tvec, length)
        x1 = max(int(initialPoint[0, 0]), 0)
        y1 = max(int(initialPoint[0, 1]), 0)
        x2 = max(int(terminalPoint[0, 0]), 0)
        y2 = max(int(terminalPoint[0, 1]), 0)

        cv2.arrowedLine(image, (x1, y1), (x2, y2), (0, 255, 0), thickness=3)
    except:
        pass

def setup(imgs):
    calibPoints = []
    reprojectionPoints = []

    for image in imgs:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        ids = ids.flatten()

        if np.all(ids != None):
            markers = {}

            baseCorners = np.array([corners[i] for i in range(len(corners)) if ids[i] != 0])
            ids = np.array([ids[i] for i in range(len(ids)) if ids[i] != 0])
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(baseCorners, 4.5, cameraMatrix, distortionCoefficients)

            for i in range(len(ids)):
                markers[ids[i]] = (rvec[i], tvec[i])

            points = []
            for id in ids:
                if id == 0:
                    continue
                points.append(markers[id][1][0][:2])

            points = np.array(points, dtype=np.float32)
            points = perspective.order_points(points)

            calibPoints.append(points)

            tagPoints = []
            for id in ids:
                if id == 0:
                    continue
                i = np.where(ids == id)
                tag = baseCorners[i][0][0]
                #print(tag.shape)
                tag = np.swapaxes(tag, 0, 1)
                centreX = np.average(tag[0])
                centreY = np.average(tag[1])
                tagPoints.append((centreX, centreY))

            tagPoints = np.array(tagPoints, dtype=np.float32)
            tagPoints = perspective.order_points(tagPoints)

            reprojectionPoints.append(tagPoints)


    points = np.zeros_like(calibPoints[0])
    for p in calibPoints:
        points = points + p
    points = points / len(calibPoints)

    points = np.zeros_like(reprojectionPoints[0])
    for p in reprojectionPoints:
        points = points + p
    points = points / len(reprojectionPoints)
    dstPoints = np.array([(0, 0), (810, 0), (810, 500), (0, 500)], dtype=np.float32)
    reprojectionMatrix = cv2.getPerspectiveTransform(dstPoints, points)

    dstPoints = np.array([(-20.25, -12.5), (20.25, -12.5), (20.25, 12.5), (-20.25, 12.5)], dtype=np.float32)
    transformMatrix = cv2.getPerspectiveTransform(points, dstPoints)

    return transformMatrix, reprojectionMatrix

def getRobotPosition(image, transformMatrix):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    drawnImage = np.copy(image)
    x = y = theta = None

    if ids is None:
        return None, None, None, drawnImage
    ids = ids.flatten()

    try:
        if 0 not in ids:
            raise Exception()
        if np.all(ids != None):
            markers = {}

            robotCorners = np.array([corners[i] for i in range(len(corners)) if ids[i] == 0])
            robotIds = np.array([ids[i] for i in range(len(ids)) if ids[i] == 0])
            robotRvec, robotTvec, _ = aruco.estimatePoseSingleMarkers(robotCorners, 2.5, cameraMatrix, distortionCoefficients)

            i = np.where(robotIds == 0)
            tag = robotCorners[i][0][0]
            #print(tag.shape)
            tag_ = np.swapaxes(tag, 0, 1)
            centreX = np.average(tag_[0])
            centreY = np.average(tag_[1])
            #for i in range(len(robotIds)):
            #    markers[robotIds[i]] = (robotRvec[i], robotTvec[i])

            #euler = rotationMatrixToEulerAngles(robotRvec)
            #x = robotTvec[0, 0, 0]
            #y = robotTvec[0, 0, 1]
            #theta = euler[2] * -1 + math.pi / 2.0
            #if theta < 0:
            #    theta = theta + 2.0 * math.pi

            #x2 = x + math.cos(theta) * 0 - math.sin(theta) * 100.0
            #y2 = y + math.sin(theta) * 0 + math.cos(theta) * 100.0
            theta = 0

            robotPoint = np.array([(centreX, centreY)], dtype=np.float32)
            robotPoint = np.array([robotPoint])
            #print(robotPoint.shape)
            newPts = cv2.perspectiveTransform(robotPoint, transformMatrix)
            x = newPts[0][0][0]
            y = newPts[0][0][1]
            #print(x, y)

            tag1 = 1
            tag2 = 0
            theta = math.atan2(tag[tag1][0] - tag[tag2][0], tag[tag1][1] - tag[tag2][1])
            #theta = euler[2] * -1 + math.pi / 2.0
            if theta < 0:
                theta = theta + 2.0 * math.pi

            #print(math.degrees(theta))
            #print(newPts[0, 0])

            aruco.drawDetectedMarkers(drawnImage, corners)
            #drawForwardAxis(drawnImage, rvec, tvec, 0.05)
    except:
        return None, None, None, drawnImage

    return x, y, theta, drawnImage

if __name__ == "__main__":
    cap = cv2.VideoCapture(3)
    cap.set(3, 960)
    cap.set(4, 540)

    print("Setting up...")
    setupImgs = []
    for i in range(15):
        frame = cap.read()[1]
        setupImgs.append(frame)

        time.sleep(0.1)

    transformMatrix = setup(setupImgs)

    while True:
        frame = cap.read()[1]

        x, y, theta, outImage = getRobotPosition(frame, transformMatrix)
        print(x, y, theta)
        print("")
        cv2.imshow("output", outImage)
        cv2.waitKey(10)

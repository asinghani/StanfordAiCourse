### TODO: calibrate with proper points in order to output robot position in centimeteres

import numpy as np
import cv2
import cv2.aruco as aruco
import math

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

def getRobotPosition(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    drawnImage = np.copy(image)

    x = y = theta = None

    if np.all(ids != None):
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners[0], 0.05, cameraMatrix, distortionCoefficients)

        euler = rotationMatrixToEulerAngles(rvec)
        x = tvec[0, 0, 0]
        y = tvec[0, 0, 1]
        theta = euler[2] * -1 + math.pi / 2.0
        if theta < 0:
            theta = theta + 2.0 * math.pi

        aruco.drawDetectedMarkers(drawnImage, corners)
        drawForwardAxis(drawnImage, rvec, tvec, 0.05)

    return x, y, theta, drawnImage

if __name__ == "__main__":
    cap = cv2.VideoCapture(2)

    while True:
        frame = cap.read()[1]

        x, y, theta, outImage = getRobotPosition(frame)
        print(x, y, theta)
        print("")
        cv2.imshow("output", outImage)
        cv2.waitKey(10)

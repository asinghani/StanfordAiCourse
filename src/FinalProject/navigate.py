import cv2
from WebcamVideoStream import WebcamVideoStream
from threading import Thread
import sys
sys.path.append("../")
from robotTrackerFinal import getRobotPosition, setup, cameraMatrix, distortionCoefficients
import time
from final_base import start, end, tankDrive, turn, forward, getFloor, getProximity, stop, beepSync, setMusicNote, updateImage, updateImage2
import math
import numpy as np
from environment import Environment, Spline
from pure_pursuit import PurePursuit
from obstacleDetector import getObstaclePositions
from imgUtils import overlayImages
import time
import imutils


LOOKAHEAD = 2.5

goalPoint = (-10000, -10000)
goalChanged = False
x = y = theta = None
outImage = np.zeros((1, 1, 3), dtype=np.uint8)
frame = None
reprojMatrix = None
transformMatrix = None
started = False
initFinished = False
following = False
newPath = False

env = Environment(4.0)
env.generatePath(goalPoint)

pp = PurePursuit([(0.0, 0.0)], LOOKAHEAD, 0.5)

lastReset = 0

def angleDiff(a, b):
    diff = abs(a - b) % math.pi
    if diff > math.pi:
        diff = 2.0 * math.pi - diff

    if (a - b >= 0 and a - b <= math.pi) or (a - b <= -math.pi and a - b >= -2.0 * math.pi):
        diff = 1 * diff
    else:
        diff = -1 * (math.pi - diff)

    return diff

def getPathAngleError(robotPos, lookahead, theta):
    x, y = robotPos

    pathAngle = math.atan2(y - lookahead[1], x - lookahead[0])
    pathAngle = -1 * pathAngle + math.pi / 2.0
    if pathAngle < 0:
        pathAngle = pathAngle + 2.0 * math.pi

    angleError = theta - pathAngle - math.pi / 2.0
    if angleError < 0:
        angleError = angleError + 2.0 * math.pi
    angleError = angleDiff(angleError, 0.0)

    return angleError

def updateUI():
    global reprojMatrix, started

    while True:
        if started:
            m = env.visualizeMap()

            out = cv2.warpPerspective(m, reprojMatrix, (outImage.shape[1], outImage.shape[0]))
            out = overlayImages(outImage, out)
            updateImage(imutils.rotate(out, angle=180))
            updateImage2(imutils.rotate(m, angle=180))

        time.sleep(0.05)

def updateRobotPos():
    global x, y, theta, env, outImage, started, reprojMatrix, pp, frame, transformMatrix, initFinished
    cap = WebcamVideoStream(src=int(sys.argv[1]))
    cap.start()

    print("Setting up...")
    setupImgs = []
    for i in range(15):
        frame = cap.read()
        setupImgs.append(frame)

        time.sleep(0.1)

    transformMatrix, reprojMatrix = setup(setupImgs)

    initFinished = True
    while True:
        frame = cap.read()
        x, y, theta, outImage = getRobotPosition(frame, transformMatrix)
        env.setRobotPose(x, y, theta)

        time.sleep(0.01)

def updatePath():
    global x, y, theta, env, outImage, started, reprojMatrix, pp, transformMatrix, initFinished, goalPoint, goalChanged, following, newPath

    realTimeObs = True
    replanOnError = True

    while True:
        if initFinished and frame is not None:
            obstacles = getObstaclePositions(frame, transformMatrix)
            if realTimeObs or not started:
                env.setObstacles(np.squeeze(obstacles))

            if not started:
                started = True

            if (realTimeObs and env.newObstacles()) or (replanOnError and pp.highError) or goalChanged:
                goalChanged = False
                newPath = True

                try:
                    env.generatePath(goalPoint)
                    if env.splinePoints is None or len(env.splinePoints) == 0:
                        pp = PurePursuit([(x, y)], LOOKAHEAD, 10000.0)
                    else:
                        pp = PurePursuit(env.splinePoints, LOOKAHEAD, 0.5)

                    following = True
                    started = True
                except:
                    pass

        time.sleep(0.1)

def periodicFunc(robot):
    global x, y, theta, goalPoint, following, env, newPath
    if x is None or y is None or theta is None or not following:
        tankDrive(0, 0)
    else:
        l, r, lookahead, pt, done = pp.getControl((x, y), theta)
        if done:
            tankDrive(0, 0)
            following = False
            env.splinePoints = None
            env.waypoints = None
        else:
            env.setLookahead(lookahead[0], lookahead[1])
            if newPath:
                angleError = getPathAngleError((x, y), lookahead, theta)
                if abs(angleError) < 0.5:
                    newPath = False
                else:
                    sp = 10.0 * angleError
                    tankDrive(int(sp), int(-sp))
            else:
                tankDrive(int(l), int(r))

    time.sleep(0.05)

def updateGoal(event):
    _x = event.x / 20.0 - 20.5
    _y = event.y / 20.0 - 12.5
    global goalPoint, goalChanged
    point = (-_x, -_y)

    if env.validPoint(point):
        goalPoint = point
        goalChanged = True

def updateGoal2(event):
    return
    global goalPoint, goalChanged, transformMatrix
    print(event.x, event.y)
    point = cv2.perspectiveTransform(np.array([[(960 - event.x, 540 - event.y)]], dtype=np.float32), transformMatrix)
    point = (point[0][0][0], point[0][0][1])

    if env.validPoint(point):
        goalPoint = point
        goalChanged = True

Thread(target=updateRobotPos).start()
Thread(target=updateUI).start()
Thread(target=updatePath).start()

start(periodicFunc, updateGoal, updateGoal2)


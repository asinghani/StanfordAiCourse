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

LOOKAHEAD = 2.5

goalPoint = (-18.0, -6.0)
goalChanged = False
x = y = theta = None
outImage = np.zeros((1, 1, 3), dtype=np.uint8)
frame = None
reprojMatrix = None
started = False
initFinished = False

env = Environment(4.0)
env.generatePath(goalPoint)

pp = PurePursuit([(0.0, 0.0)], LOOKAHEAD, 0.5)

lastReset = 0

def updateUI():
    global reprojMatrix, started

    while True:
        if started:
            m = env.visualizeMap()

            out = cv2.warpPerspective(m, reprojMatrix, (outImage.shape[1], outImage.shape[0]))
            out = overlayImages(outImage, out)
            updateImage(out)
            updateImage2(m)

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
    global x, y, theta, env, outImage, started, reprojMatrix, pp, transformMatrix, initFinished, goalPoint, goalChanged

    realTimeObs = False
    replanOnError = False

    while True:
        if initFinished and frame is not None:
            obstacles = getObstaclePositions(frame, transformMatrix)
            if realTimeObs or not started:
                env.setObstacles(np.squeeze(obstacles))

            if not started or (realTimeObs and env.newObstacles()) or (replanOnError and pp.highError) or goalChanged:
                goalChanged = False
                env.generatePath(goalPoint)
                if env.splinePoints is None or len(env.splinePoints) == 0:
                    pp = PurePursuit([(0.0, 0.0)], LOOKAHEAD, 10000.0)
                else:
                    pp = PurePursuit(env.splinePoints, LOOKAHEAD, 0.5)

                started = True

        time.sleep(0.1)

def periodicFunc(robot):
    global x, y, theta, goalPoint
    if x is None or y is None or theta is None:
        tankDrive(0, 0)
    else:
        l, r, lookahead, pt = pp.getControl((x, y), theta)
        env.setLookahead(lookahead[0], lookahead[1])

        pathAngle = math.atan2(x - lookahead[0], y - lookahead[1])
        pathAngle = pathAngle - math.pi / 2.0
        if pathAngle < 0:
            pathAngle = pathAngle + 2.0 * math.pi

        angleError = theta - pathAngle
        print(theta, pathAngle)
        print()
        if False and abs(angleError) > 0.5 and l > 0.01 and r > 0.01:
            speed = 10 * angleError
            tankDrive(int(speed), int(-speed))
        else:
            tankDrive(int(l), int(r))

    time.sleep(0.05)

def updateGoal(event):
    _x = event.x / 20.0 - 20.5
    _y = event.y / 20.0 - 12.5
    global goalPoint, goalChanged
    goalPoint = (_x, _y)
    goalChanged = True

Thread(target=updateRobotPos).start()
Thread(target=updateUI).start()
Thread(target=updatePath).start()

start(periodicFunc, updateGoal)

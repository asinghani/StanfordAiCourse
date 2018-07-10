#from __future__ import print_function

import sys
sys.path.append("../")
import cv2
from robotTracker import getRobotPosition
from final_base import start, end, tankDrive, turn, forward, getFloor, getProximity, stop, beepSync, setMusicNote, updateImage
from threading import Thread
import time
import math

cap = cv2.VideoCapture(2)
cap.set(3, 960)
cap.set(4, 540)

robotX = None
robotY = None
robotTheta = None

def updateRobotPos():
    global robotTheta, robotX, robotY
    while True:
        img = cap.read()[1]
        if img is not None:
            x, y, theta, newImg = getRobotPosition(img)
            #print(x, y, theta)
            robotTheta = theta
            robotX = x
            robotY = y
            updateImage(newImg)
        else:
            robotTheta = None

        time.sleep(0.05)

def periodicFunc(robot):
    if robotTheta is None:
        tankDrive(0, 0)
    else:
        #print(robotX, robotY)
        targetTheta = math.atan2(robotX, -robotY)
        print(targetTheta, robotTheta)
        speed = -1 * int((targetTheta - robotTheta) * 15.0)
        tankDrive(speed, -speed)

    time.sleep(0.05)

Thread(target=updateRobotPos).start()
start(periodicFunc)

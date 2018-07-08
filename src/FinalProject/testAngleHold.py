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

robotTheta = None

def updateRobotPos():
    global robotTheta
    while True:
        img = cap.read()[1]
        if img is not None:
            x, y, theta, newImg = getRobotPosition(img)
            print(x, y, theta)
            robotTheta = theta
            updateImage(newImg)
        else:
            robotTheta = None

        time.sleep(0.05)

def periodicFunc(robot):
    if robotTheta is None:
        tankDrive(0, 0)
    else:
        speed = -1 * int((math.pi / 2.0 - robotTheta) * 25.0)
        tankDrive(speed, -speed)

    time.sleep(0.05)

Thread(target=updateRobotPos).start()
start(periodicFunc)

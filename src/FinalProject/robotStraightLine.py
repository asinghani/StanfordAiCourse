import cv2
from WebcamVideoStream import WebcamVideoStream
from threading import Thread
import sys
sys.path.append("../")
from robotTrackerFinal import getRobotPosition, setup
import time
from final_base import start, end, tankDrive, turn, forward, getFloor, getProximity, stop, beepSync, setMusicNote, updateImage
import math

x = y = theta = None
cte = None

def updateRobotPos():
    global cte, x, y, theta
    cap = WebcamVideoStream(src=1)
    cap.start()

    print("Setting up...")
    setupImgs = []
    for i in range(15):
        frame = cap.read()
        setupImgs.append(frame)

        time.sleep(0.1)

    transformMatrix = setup(setupImgs)

    while True:
        frame = cap.read()
        #print(frame[50:60, 50:60, 1])

        x, y, theta, outImage = getRobotPosition(frame, transformMatrix)
        print(x, y, theta)
        print("")

        cte = y
        updateImage(outImage)
        time.sleep(0.01)
        #cv2.imshow("output", outImage)
        #cv2.waitKey(10)


def periodicFunc(robot):
    global cte, x, y, theta
    if cte is None:
        tankDrive(0, 0)
    else:
        print("cte", cte)
        speed = int(round(cte * -3.0) + round((math.pi - theta) * 2.0))
        tankDrive(20 + speed, 20 - speed)

    time.sleep(0.05)

Thread(target=updateRobotPos).start()
start(periodicFunc)

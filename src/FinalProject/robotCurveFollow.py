import cv2
from WebcamVideoStream import WebcamVideoStream
from threading import Thread
import sys
sys.path.append("../")
from robotTrackerFinal import getRobotPosition, setup
import time
from final_base import start, end, tankDrive, turn, forward, getFloor, getProximity, stop, beepSync, setMusicNote, updateImage, updateImage2
import math
import numpy as np
from environment import Environment, Spline
from pure_pursuit import PurePursuit

x = y = theta = None
cte = None

env = Environment()
#path = [(x, 0.0) for x in np.linspace(-10, 10, 200)]
#env.waypoints = [(-10, 0), (10, 0)]
#env.splinePoints = path # TODO remove
env.generatePath(None)
pp = PurePursuit(env.splinePoints, 2.5, 0.5)

def updateRobotPos():
    global cte, x, y, theta, env
    cap = WebcamVideoStream(src=int(sys.argv[1]))
    cap.start()

    print("Setting up...")
    setupImgs = []
    for i in range(15):
        frame = cap.read()
        setupImgs.append(frame)

        time.sleep(0.1)

    transformMatrix, reprojMatrix = setup(setupImgs)

    while True:
        frame = cap.read()
        #print(frame[50:60, 50:60, 1])

        x, y, theta, outImage = getRobotPosition(frame, transformMatrix)
        print(x, y, theta)
        print("")

        cte = y
        #updateImage(outImage)
        env.setRobotPose(x, y, theta)
        m = env.visualizeMap()
        #out = cv2.warpPerspective(m, reprojMatrix, (outImage.shape[1], outImage.shape[0]))
        #out = cv2.addWeighted(out, 0.5, outImage, 1 - 0.5, 0)
        updateImage(outImage)
        updateImage2(m)

        time.sleep(0.01)
        #cv2.imshow("output", outImage)
        #cv2.waitKey(10)


def periodicFunc(robot):
    global cte, x, y, theta
    if cte is None:
        tankDrive(0, 0)
    else:
        #print("cte", cte)
        #speed = int(round(cte * -3.0) + round((math.pi - theta) * 2.0))
        l, r, lookahead, pt = pp.getControl((x, y), theta)
        env.setLookahead(lookahead[0], lookahead[1])
        tankDrive(int(l), int(r))

        #tankDrive(20 + speed, 20 - speed)

    time.sleep(0.05)

Thread(target=updateRobotPos).start()
start(periodicFunc)

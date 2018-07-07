from GridGraph import graphFromGrid
import os
import cv2

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

plt.ion()
plt.show()

def viewGraph():
    """img = cv2.imread("graph.png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.draw()
    plt.pause(0.01)"""
    pass


grid = [[0, 1, 1],
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0]]

startPt = (3, 0)
endPt = (0, 0)

g, nodesGrid = graphFromGrid(grid, includeUnconnected=True)
pathNodes = g.dijsktraSearch(g.getNodeByCoords(startPt[0], startPt[1]),
        g.getNodeByCoords(endPt[0], endPt[1]))

g.visualizeGraphWithPath(pathNodes, showCost=True)
viewGraph()

path = [None]
for node in pathNodes:
    x, y = node.data.replace("(", "").replace(")", "").replace(" ", "").split(",")
    x = int(x)
    y = int(y)
    path.append((x, y))

# 0 = left, 1 = right, 2 = up, 3 = down
heading = 0

def getHeadingFromPoints(pt1, pt2):
    if pt1[1] > pt2[1]:
        return 2
    elif pt1[1] < pt2[1]:
        return 3
    else:
        if pt1[0] > pt2[0]:
            return 0
        else:
            return 1

# 0 = left turn, 1 = right turn, 2 = fwd
cmds = []
prev = None
for i in range(len(path)):
    if prev:
        lastHeading = heading
        heading = getHeadingFromPoints(prev, path[i])
        if heading == lastHeading:
            cmds.append(2)
        else:
            if lastHeading == 0:
                if heading == 2:
                    cmds.append(0)
                if heading == 3:
                    cmds.append(1)

            if lastHeading == 1:
                if heading == 2:
                    cmds.append(1)
                if heading == 3:
                    cmds.append(0)

            if lastHeading == 2:
                if heading == 1:
                    cmds.append(0)
                if heading == 0:
                    cmds.append(1)

            if lastHeading == 3:
                if heading == 1:
                    cmds.append(1)
                if heading == 0:
                    cmds.append(0)

    prev = path[i]

from base import start, end, tankDrive, turn, forward, getFloor, getProximity, stop, beepSync, setMusicNote, getBattery
import time, random

def getVel():
    battery = getBattery()
    if battery < 1.0:
        battery = 3.5

    vel = 8
    vel = round(vel * 3.88 / battery)
    print(vel)
    return int(vel)

def turnLeft():
    print("LEFT")
    vel = getVel()
    tankDrive(vel, vel)
    time.sleep(1.3)
    tankDrive(-vel, vel)
    time.sleep(2.2)
    stop()

def turnRight():
    print("RIGHT")
    vel = getVel()
    tankDrive(vel, vel)
    time.sleep(1.3)
    tankDrive(vel, -vel)
    time.sleep(2.2)
    stop()

def forwardAtIntersection():
    print("FWD")
    vel = getVel()
    tankDrive(vel, vel)
    time.sleep(1.3)
    stop()

# 0 = left turn, 1 = right turn, 2 = fwd, 3 = end
cmds = [1, 2, 0, 2, 0, 2, 1, 3]
currentPoint = 0

def periodicFunc(robot):
    global cmds, currentPoint

    l1 = robot.get_floor(0)
    l2 = robot.get_floor(1)
    if l1 + l2 < 80:
        currentPoint = currentPoint + 1
        stop()

        g.visualizeGraphWithPath(pathNodes, showCost=True, currentPos=path[currentPoint])
        viewGraph()


        time.sleep(0.1)
        robot.set_musical_note(40)
        time.sleep(0.5)
        robot.set_musical_note(0)
        time.sleep(0.1)

        cmd = cmds[0]
        cmds = cmds[1:]

        if cmd == 0:
            turnLeft()
        elif cmd == 1:
            turnRight()
        elif cmd == 2:
            forwardAtIntersection()

        stop()


        if cmd == 3:
            end()
            return

        if len(cmds) == 0:
            end()
            return

        g.visualizeGraphWithPath(pathNodes, showCost=True, currentEdge=[path[currentPoint], path[currentPoint + 1]])
        viewGraph()

    else:
        error = l1 - l2
        speed = 15
        kP = 0.3
        tankDrive(int(speed + error * kP), int(speed - error * kP))

    time.sleep(0.05)
start(periodicFunc)

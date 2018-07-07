from world import World
import sys
sys.path.append("../")
from base_web import inputDict, outputDict
import base_web
import time
import random
import thread

world = World(1000, 1000, 0)
world.robot.x = -9.5

def addObstacle(x, y, w, h):
    world.addObstacle(x, y, w, h)

extraLines = []

def updateOutput():
    global world, extraLines
    # width, height, timestamp, proxL, proxR, pointL, pointR
    # obstacles: array of {x, y, w, h}
    # robot x, y, theta, size, leftSensorPos, rightSensorPos
    base_web.outputDict = {
        "worldWidth": world.width,
        "worldHeight": world.height,
        "timestamp": world.timestamp,
        "proxL": world.proxL,
        "proxR": world.proxR,
        "pointL": world.pointL.serialize() if world.pointL else None,
        "pointR": world.pointR.serialize() if world.pointR else None,
        "robotX": world.robot.x,
        "robotY": world.robot.y,
        "robotTheta": world.robot.theta,
        "robotWidth": world.robot.robotSize[0],
        "robotHeight": world.robot.robotSize[1],
        "robotLeftSensorPos": world.robot.getLeftSensorPos().serialize(),
        "robotRightSensorPos": world.robot.getRightSensorPos().serialize(),
        "robotLeftFloorSensorPos": world.robot.getLeftFloorSensorPos().serialize(),
        "robotRightFloorSensorPos": world.robot.getRightFloorSensorPos().serialize(),
        "obstacles": [obs.serialize() for obs in world.obstacles],
        "extraLines": extraLines
    }

left = 0
right = 0

def tankDrive(l, r):
    global left, right
    left = l
    right = r

def forward(speed, t):
    tankDrive(speed, speed)
    time.sleep(t)
    tankDrive(0, 0)

def turn(speed, t):
    tankDrive(speed, -speed)
    time.sleep(t)
    tankDrive(0, 0)

def stop():
    tankDrive(0, 0)

finished = False

def end():
    finished = True

def getExactOdom():
    return (world.robot.x, world.robot.y, world.robot.theta)

def getProximity():
    global world
    return (world.proxL, world.proxR)

def start(periodicFunc):
    global left, right
    updateOutput()
    base_web.start("viz.html", "viz.js", {"l": 0, "r": 0}, None)

    def run():
        while True:
            if not finished:
                periodicFunc(None)
            time.sleep(0.01)

    thread.start_new_thread(run, ())

    while True:
        x, y, t = world.robot.x, world.robot.y, world.robot.theta
        world.simulate(left, right, 0.03)
        if world.checkCollision():
            world.robot.x, world.robot.y, world.robot.theta = x, y, t

        updateOutput()
        time.sleep(0.03)

from world import World
import sys
sys.path.append("../")
from base_web import start, inputDict, outputDict
import base_web
import time
import random

world = World(1000, 1000, 0)
world.robot.x = -9.5

def genObstacles():
    del world.obstacles[:]

    def createObstacle(xRange, yRange, widthRange, heightRange):
        world.addObstacle(random.randint(xRange[0], xRange[1]),
                random.randint(yRange[0], yRange[1]),
                random.randint(widthRange[0], widthRange[1]),
                random.randint(heightRange[0], heightRange[1]))

    for i in range(random.randint(10, 15)):
        createObstacle((-6, 12), (-8, 8), (1, 2), (1, 2))

    # Walls
    world.addObstacle(0, 7.5, 24, 1)
    world.addObstacle(0, -7.5, 24, 1)
    world.addObstacle(-11.5, 0, 1, 16)
    world.addObstacle(11.5, 0, 1, 16)

genObstacles()

def updateOutput():
    global world
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
        "obstacles": [obs.serialize() for obs in world.obstacles]
    }

updateOutput()
start("viz.html", "viz.js", {"l": 0, "r": 0}, None)

while True:
    x, y, t = world.robot.x, world.robot.y, world.robot.theta
    world.simulate(float(base_web.inputDict["l"] if "l" in base_web.inputDict else 0), float(base_web.inputDict["r"] if "r" in base_web.inputDict else 0), 0.03)
    if world.checkCollision():
        world.robot.x, world.robot.y, world.robot.theta = x, y, t

    updateOutput()
    time.sleep(0.03)

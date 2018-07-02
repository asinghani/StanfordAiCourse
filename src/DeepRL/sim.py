from world import World
import sys
sys.path.append("../")
from base_web import start, inputDict, outputDict
import base_web
import time

world = World(1000, 1000, 0)

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
        "obstacles": [obs.serialize() for obs in world.obstacles]
    }

updateOutput()
start("viz.html", "viz.js", outputDict, None)

while True:
    world.simulate(3.5, 2.5, 0.03)
    updateOutput()
    time.sleep(0.03)

from __future__ import print_function
import sys
sys.path.append("../")
import numpy as np
import base_web
from robot import Robot

# Obstacle class (only rectangles)
class Obstacle:
    def __init__(self, cX, cY, width, height):
        self.x = cX
        self.y = cY
        self.width = width
        self.height = height
        _x1 = cX - (float(width) / 2.0)
        _x2 = cX + (float(width) / 2.0)
        self.x1 = min(_x1, _x2)
        self.x2 = max(_x1, _x2)

        _y1 = cY - (float(height) / 2.0)
        _y2 = cY + (float(height) / 2.0)
        self.y1 = min(_y1, _y2)
        self.y2 = max(_y1, _y2)

        self.pt1 = (self.x1, self.y1)
        self.pt2 = (self.x2, self.y1)
        self.pt3 = (self.x2, self.y2)
        self.pt4 = (self.x1, self.y2)

    def containsPoint(self, pt):
        return pt[0] > self.x1 and pt[0] < self.x2 and pt[1] > self.y1 and pt[1] < self.y2


class World:
    def __init__(self, width, height, timestamp):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.timestamp = timestamp
        self.robot = Robot(timestamp = timestamp)
        self.proxL = -1
        self.proxR = -1

    def simulate(self, velR, velL, timestep):
        self.timestamp = self.timestamp + timestep
        self.robot.simulate(velR, velL, self.timestamp)


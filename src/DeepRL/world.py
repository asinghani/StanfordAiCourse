from __future__ import print_function
import numpy as np
from robot import Robot
from point import Pt, _epsilonEquals

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

        self.pt1 = Pt(self.x1, self.y1)
        self.pt2 = Pt(self.x2, self.y1)
        self.pt3 = Pt(self.x2, self.y2)
        self.pt4 = Pt(self.x1, self.y2)

        # Array of (p, r)
        self.segments = [
            (self.pt1, self.pt2 - self.pt1),
            (self.pt2, self.pt3 - self.pt2),
            (self.pt3, self.pt4 - self.pt3),
            (self.pt4, self.pt1 - self.pt4)
        ]

    def containsPoint(self, pt):
        return pt.x > self.x1 and pt.x < self.x2 and pt.y > self.y1 and pt.y < self.y2

    def intersect(self, pt, angle, maxLen):
        q = pt
        s = Pt(maxLen, 0.0).rotate(angle)
        intersections = []

        for seg in self.segments:
            r = seg[1]
            a = (q - seg[0])
            b = r.cross(s)

            if _epsilonEquals(b, 0):
                pass
            else:
                t = a.cross(s) / b
                u = a.cross(r) / b

                if t >= 0 and t <= 1 and u >= 0 and u <= 1 and seg[0] + r*t == q + s*u:
                    intersections.append(q + s*u)

        if len(intersections) == 0:
            return None
        else:
            return min(intersections, key=lambda p: p.dist(pt))

    def serialize(self):
        return {"x": self.x, "y": self.y, "w": self.width, "h": self.height}

class World:
    def __init__(self, width, height, timestamp):
        self.width = width
        self.height = height
        self.timestamp = timestamp
        self.robot = Robot(timestamp = timestamp)
        self.proxL = None
        self.proxR = None
        self.pointL = None
        self.pointR = None
        self.obstacles = []

    def addObstacle(self, x, y, w, h):
        self.obstacles.append(Obstacle(x, y, w, h))

    def raycast(self, point, angle, maxLen):
        intersections = []
        for obs in self.obstacles:
            i = obs.intersect(point, angle, maxLen)
            if i is not None:
                intersections.append(i)

        if len(intersections) == 0:
            return None
        else:
            return min(intersections, key=lambda p: p.dist(point))

    def getLeftDist(self):
        point = self.raycast(self.robot.getLeftSensorPos(), self.robot.theta, self.robot.sensorRange)
        if point is not None:
            return self.robot.getLeftSensorPos().dist(point), point
        else:
            return None, None

    def getRightDist(self):
        point = self.raycast(self.robot.getRightSensorPos(), self.robot.theta, self.robot.sensorRange)
        if point is not None:
            return self.robot.getRightSensorPos().dist(point), point
        else:
            return None, None

    def simulate(self, velR, velL, timestep):
        self.timestamp = self.timestamp + timestep
        self.robot.simulate(velR, velL, self.timestamp)

        self.proxL, self.pointL = self.getLeftDist()
        self.proxR, self.pointR = self.getRightDist()

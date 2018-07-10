import scipy.interpolate as interp
import numpy as np
import cv2
import math
from colors import w3c as colors

def cvColor(rgbColor):
    return (rgbColor.blue, rgbColor.green, rgbColor.red)

class Spline:
    def __init__(self, points, smoothing=0.1):
        x = [pt[0] for pt in points]
        y = [pt[1] for pt in points]
        splineInfo = interp.splprep([x, y], s=smoothing)
        self.spline = splineInfo[0]

    def interpolate(self, numSamples):
        xout, yout = interp.splev(np.arange(0.0, 1.0, 1.0 / float(numSamples)), self.spline)
        return np.column_stack((xout, yout))

class Environment:
    def __init__(self):
        self.width = 40.5
        self.height = 25.0
        self.robotX = None
        self.robotY = None
        self.robotTheta = None
        self.splinePoints = None
        self.waypoints = None

    def setRobotPose(self, x, y, theta):
        self.robotX = x
        self.robotY = y
        self.robotTheta = theta

    def getPathWaypoints(self, startPoint, endPoint):
        # TODO implement pathfinding
        return [(-15, -10), (-10, -9), (-5, -3), (3, 10), (10, 4)]

    def generatePath(self, endPoint):
        self.waypoints = self.getPathWaypoints((self.robotX, self.robotY), endPoint)
        self.spline = Spline(self.waypoints, smoothing=0.1)
        self.splinePoints = self.spline.interpolate(200)

    def visualizeMap(self):
        mapImg = np.zeros((20 * self.height, 20 * self.width, 3), dtype=np.uint8)
        mapImg[:, :, :] = 255

        # Draw Robot
        cosT = math.cos(self.robotTheta - math.pi / 2.0)
        sinT = math.sin(self.robotTheta - math.pi / 2.0)

        x
        pt1 = ()

        # Draw Spline
        if self.splinePoints is not None and self.waypoints is not None:
            for pt in self.waypoints:
                cv2.circle(mapImg, (pt[0], pt[1]), 3, cvColor(colors.darkgreen), -1)

            for i in range(len(self.splinePoints) - 1):
                pt = self.splinePoints[i]
                pt2 = self.splinePoints[i + 1]
                cv2.line(mapImg, (pt[0], pt[1]), (pt2[0], pt2[1]), cvColor(colors.lightgreen), 2)


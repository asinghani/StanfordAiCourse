import scipy.interpolate as interp
import numpy as np
import cv2
import math
from colors import w3c as colors
import pyvisgraph as vg
from imgUtils import expandContour
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.ops import cascaded_union

def cvColor(rgbColor):
    return (rgbColor.blue, rgbColor.green, rgbColor.red)

def scalePoint(point, scale=20, wOffset = 20.25, hOffset = 12.5):
    try:
        return (int((point[0] + wOffset) * scale), int((point[1] + hOffset) * scale))
    except:
        return(0, 0)

def mergePolygons(sourcePolygons):
    try:
        polygons = []
        for poly in sourcePolygons:
            polygons.append(Polygon(poly))

        combined = cascaded_union(polygons)

        out = []
        if type(combined) is Polygon:
            # single obj
            out.append(list(combined.exterior.coords))
        else:
            # multiple
            for polygon in combined:
                out.append(list(polygon.exterior.coords))

        return out

    except:
        return sourcePolygons


class Spline:
    def __init__(self, points, smoothing=0.1, mode="segments"):
        self.mode = mode
        if mode == "segments":
            self.points = points
            if len(self.points) == 1:
                self.points.append(self.points[0])
            return

        x = [pt[0] for pt in points]
        y = [pt[1] for pt in points]
        deg = 3
        if len(x) == 3:
            deg = 2
        elif len(x) == 2:
            deg = 1
        elif len(x) < 2:
            deg = 0

        if deg > 0:
            splineInfo = interp.splprep([x, y], s=smoothing, k=deg)
            self.spline = splineInfo[0]
        else:
            self.spline = None
            if len(points) > 0:
                self.pt = points[0]
            else:
                self.pt = None

    def interpolate(self, numSamples):
        if self.mode == "segments":
            numSegments = len(self.points) - 1
            samplesPerSeg = int(numSamples / numSegments)
            points = np.array([], dtype=np.float32)
            points.shape = (0, 2)
            for i in range(numSegments):
                pt1 = np.array(self.points[i], dtype=np.float32)
                pt2 = self.points[i + 1]
                vec = np.array([pt2[0] - pt1[0], pt2[1] - pt1[1]], dtype=np.float32)
                pts = np.arange(0.0, 1.0, 1.0 / float(samplesPerSeg))
                pts = np.array([vec * pt + pt1 for pt in pts], dtype=np.float32)
                points = np.append(points, pts, axis=0)

            return points


        if self.spline is not None:
            xout, yout = interp.splev(np.arange(0.0, 1.0, 1.0 / float(numSamples)), self.spline)
            return np.column_stack((xout, yout))
        else:
            if self.pt is None:
                return np.array([(0, 0)] * numSamples, dtype=np.float32)
            else:
                return np.array([self.pt] * numSamples, dtype=np.float32)

class Environment:
    def __init__(self, margin):
        self.width = 40.5
        self.height = 25.0
        self.robotX = None
        self.robotY = None
        self.robotTheta = None
        self.splinePoints = None
        self.waypoints = None
        self.lookaheadX = 0
        self.lookaheadY = 0
        self.obstacles = np.array([], dtype=np.float32)
        self.cSpaceObstacles = np.array([], dtype=np.float32)
        self.cSpaceMargin = margin

    def setObstacles(self, obstacles):
        self.obstacles = obstacles
        if self.obstacles is not None:

            oldObs = np.sort(np.array(self.cSpaceObstacles, dtype=np.float32).copy().flatten())
            self.cSpaceObstacles = [expandContour(c, self.cSpaceMargin) for c in self.obstacles]
            newObs = np.sort(np.array(self.cSpaceObstacles, dtype=np.float32).copy().flatten())

            if len(oldObs) == len(newObs):
                mse = np.mean((oldObs - newObs) ** 2)
                if mse > 0.35:
                    self.updated = True
            else:
                self.updated = True

    def newObstacles(self):
        if self.updated:
            self.updated = False
            return True
        else:
            return False


    def setRobotPose(self, x, y, theta):
        self.robotX = x
        self.robotY = y
        self.robotTheta = theta

    def setLookahead(self, x, y):
        self.lookaheadX = x
        self.lookaheadY = y

    def getPathWaypoints(self, startPoint, endPoint):
        if startPoint is None or startPoint[0] is None or startPoint[1] is None:
            return None

        graph = vg.VisGraph()

        obstacles = mergePolygons(self.cSpaceObstacles)

        finalObs = []

        for obs in obstacles:
            #print("OBS", obs)
            obstacleData = []
            for p in obs:
                try:
                    x = p[0]
                    y = p[1]
                    obstacleData.append(vg.Point(x, y))
                except:
                    pass

            finalObs.append(obstacleData)

        try:
            graph.build(finalObs)
            path = graph.shortest_path(vg.Point(startPoint[0], startPoint[1]), vg.Point(endPoint[0], endPoint[1]))
            return [(p.x, p.y) for p in path]
        except:
            return [startPoint]

    def generatePath(self, endPoint):
        self.waypoints = self.getPathWaypoints((self.robotX, self.robotY), endPoint)
        if self.waypoints is None:
            self.spline = None
            self.splinePoints = None
            return

        self.spline = Spline(self.waypoints, smoothing=0.1)
        self.splinePoints = self.spline.interpolate(200)

    def visualizeMap(self):
        mapImg = np.zeros((int(math.ceil(20 * self.height)), int(math.ceil(20 * self.width)), 3), dtype=np.uint8)
        mapImg[:, :, :] = 255
        #mapImg[:, :, 1] = 255
        #mapImg[:, :, 2] = 255
        #mapImg[:, :, 3] = 0

        cv2.circle(mapImg, scalePoint((self.lookaheadX, self.lookaheadY)), 6, cvColor(colors.red), -1)

        # Draw Robot
        if self.robotX is not None and self.robotY is not None and self.robotTheta is not None:
            cosT = math.cos(-1 * self.robotTheta - math.pi / 2.0)
            sinT = math.sin(-1 * self.robotTheta - math.pi / 2.0)

            x = self.robotX
            y = self.robotY
            pt1 = (x + 1.7 * cosT - 2.3 * sinT, y + 1.7 * sinT + 2.3 * cosT)
            pt2 = (x - 1.7 * cosT - 2.3 * sinT, y - 1.7 * sinT + 2.3 * cosT)
            pt3 = (x - 1.7 * cosT + 1.7 * sinT, y - 1.7 * sinT - 1.7 * cosT)
            pt4 = (x + 1.7 * cosT + 1.7 * sinT, y + 1.7 * sinT - 1.7 * cosT)

            frontPoint = (x + 0 * cosT - 2.0 * sinT, y + 0 * sinT + 2.0 * cosT)

            cv2.line(mapImg, scalePoint(pt1), scalePoint(pt2), cvColor(colors.darkgreen), 2)
            cv2.line(mapImg, scalePoint(pt2), scalePoint(pt3), cvColor(colors.darkgreen), 2)
            cv2.line(mapImg, scalePoint(pt3), scalePoint(pt4), cvColor(colors.darkgreen), 2)
            cv2.line(mapImg, scalePoint(pt4), scalePoint(pt1), cvColor(colors.darkgreen), 2)

            cv2.circle(mapImg, scalePoint(frontPoint), 2, cvColor(colors.darkgreen), -1)
            cv2.circle(mapImg, scalePoint((x, y)), 8, cvColor(colors.red), -1)

        # Draw Spline
        if self.splinePoints is not None and self.waypoints is not None:
            for pt in self.waypoints:
                cv2.circle(mapImg, scalePoint((pt[0], pt[1])), 5, cvColor(colors.blue), -1)

            for i in range(len(self.splinePoints) - 1):
                pt = self.splinePoints[i]
                pt2 = self.splinePoints[i + 1]
                cv2.line(mapImg, scalePoint((pt[0], pt[1])), scalePoint((pt2[0], pt2[1])), cvColor(colors.blue), 2)


        if self.obstacles is not None and len(self.obstacles) != 0:
            for pts in self.obstacles:
                pts_ = np.array([scalePoint(pt) for pt in pts])
                cv2.drawContours(mapImg, [pts_], -1, color = cvColor(colors.purple), thickness = 3)

        if self.cSpaceObstacles is not None and len(self.cSpaceObstacles) != 0:
            for pts in self.cSpaceObstacles:
                pts_ = np.array([scalePoint(pt) for pt in pts])
                cv2.drawContours(mapImg, [pts_], -1, color = cvColor(colors.red), thickness = 3)

        return mapImg


# Test
if __name__ == "__main__":
    env = Environment()
    env.setRobotPose(0, 0, 1.5)
    env.generatePath(None)
    m = env.visualizeMap()
    cv2.imshow("map", m)
    cv2.waitKey(5000000)

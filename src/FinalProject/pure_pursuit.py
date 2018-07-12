from __future__ import print_function
import math

class PurePursuit:
    def __init__(self, points, lookahead, targetEpsilon):
        self.points = [(float(p[0]), float(p[1])) for p in points]
        self.lookahead = lookahead
        self.distances = [0.0]
        self.targetEpsilon = targetEpsilon
        prev = points[0]

        for point in points[1:]:
            self.distances.append(self.distances[-1] + self.__dist__(point, prev))
            prev = point

        self.pathLen = self.distances[-1]

        self.lastLookAhead = 0
        self.highError = False

    def __dist__(self, point1, point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def __getLookAheadPoint__(self, point):
        for i in range(self.lastLookAhead, self.points.__len__()):
            #print(i)
            if (self.__dist__(point, self.points[i]) > self.lookahead): # and (self.distances[i] > self.__dist__(point, self.points[0]) - 0.1):
                self.lastLookAhead = i
                return self.points[i]

        #print(" ")
        return self.points[-1]

    def __poseToPoint__(self, pos, angle, newPoint):
        x = newPoint[0] - pos[0]
        y = newPoint[1] - pos[1]

        angleRad = angle # + (3.1415926 / 2.0)
        return (x * math.sin(angleRad) + y * math.cos(angleRad),
                x * math.cos(angleRad) - y * math.sin(angleRad))

    def __arcToTank__(self, curvature, vel):
        dtOpenLoopFactor = 1.0 # / 0.998371769 * 3857.0 / 3858.0
        wheelBase = 3.5

        if abs(curvature) < 0.01:
            return dtOpenLoopFactor * vel, dtOpenLoopFactor * vel
        else:
            left = dtOpenLoopFactor * vel * curvature * ( (1.0 / float(curvature)) + (wheelBase / 2.0) )
            right = dtOpenLoopFactor * vel * curvature * ( (1.0 / float(curvature)) - (wheelBase / 2.0) )
            return left, right


    def getControl(self, currentPos, currentAngle):
        if self.__dist__(currentPos, self.points[-1]) < self.targetEpsilon:
            return 0.0, 0.0, (0.0, 0.0), (0.0, 0.0)

        lookahead = self.__getLookAheadPoint__(currentPos)

        pt = self.__poseToPoint__(currentPos, currentAngle, lookahead)

        error = float(pt[0]**2 + pt[1]**2)
        self.highError = error > self.lookahead * 5.0

        curvature = 2.0 * pt[0] / float(pt[0]**2 + pt[1]**2)

        velocity = 13.0

        #print("C", curvature, velocity)

        tankLeft, tankRight = self.__arcToTank__(curvature, velocity)

        linvel = (tankLeft + tankRight) / 2.0
        angvel = (tankRight - tankLeft) / 2.0

        return tankLeft, tankRight, lookahead, pt

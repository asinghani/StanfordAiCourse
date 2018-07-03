from math import sin, cos, pi
from point import Pt

# TODO: tune these values
WHEEL_SPACING = 1.5
TRACK_SCRUB = 1.0 # [1.0, 
EPSILON = 1.0e-6
DRIVING_STRAIGHT = 0.1

B = float(WHEEL_SPACING * TRACK_SCRUB)

def _isZero(val, epsilon = EPSILON):
    return abs(val) < epsilon

SENSOR_MIN_RANGE = 0.5
SENSOR_MAX_RANGE = 8.0

class Robot:
    # Coords = robot wheelbase center
    def __init__(self, x = 0.0, y = 0.0, theta = 0.0, timestamp = 0.0):
        self.x = x
        self.y = y
        self.theta = theta
        self.time = timestamp
        self.robotSize = (2.0, 2.0)
        self.leftSensorOffset = Pt(1.0, 0.8)
        self.rightSensorOffset = Pt(1.0, -0.8)
        self.sensorRange = SENSOR_MAX_RANGE # cm
        self.minRange = SENSOR_MIN_RANGE


    def getPoints(self):
        pt1 = Pt(self.x - self.robotSize[0] / 2.0, self.y - self.robotSize[1] / 2.0)
        pt2 = Pt(self.x + self.robotSize[0] / 2.0, self.y - self.robotSize[1] / 2.0)
        pt3 = Pt(self.x + self.robotSize[0] / 2.0, self.y + self.robotSize[1] / 2.0)
        pt4 = Pt(self.x - self.robotSize[0] / 2.0, self.y + self.robotSize[1] / 2.0)
        return [pt1, pt2, pt3, pt4]

    def simulate(self, velR, velL, timestamp):
        dt = float(timestamp - self.time)
        self.time = timestamp

        if _isZero(velR - velL, DRIVING_STRAIGHT):
            vel = float(velR + velL) / 2
            self.x = self.x + vel * dt * cos(self.theta)
            self.y = self.y + vel * dt * sin(self.theta)
        else:
            oldTheta = float(self.theta)
            theta = (velR - velL) * dt / B + oldTheta

            coeff = float(B * (velR + velL)) / float(2.0 * (velR - velL))
            self.x = self.x + coeff * (sin(theta) - sin(oldTheta))
            self.y = self.y - coeff * (cos(theta) - cos(oldTheta))

            self.theta = theta % (2 * pi)

    def getPosition(self):
        return Pt(self.x, self.y)

    def getOrientation(self):
        return self.theta

    def getLeftSensorPoint(self, dist):
        point = Pt(self.x, self.y)
        point = point + self.leftSensorOffset.rotate(self.theta)
        point = point + Pt(dist, 0.0).rotate(self.theta)

        return point

    def getRightSensorPoint(self, dist):
        point = Pt(self.x, self.y)
        point = point + self.rightSensorOffset.rotate(self.theta)
        point = point + Pt(dist, 0.0).rotate(self.theta)

        return point

    def getLeftSensorPos(self):
        return self.getLeftSensorPoint(0.0)

    def getRightSensorPos(self):
        return self.getRightSensorPoint(0.0)

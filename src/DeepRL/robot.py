from math import sin, cos

# TODO: tune these values
WHEEL_SPACING = 1.5
TRACK_SCRUB = 1.0 # [1.0, 
EPSILON = 1.0e-6
DRIVING_STRAIGHT = 0.1

B = float(WHEEL_SPACING * TRACK_SCRUB)

def _isZero(val, epsilon = EPSILON):
    return abs(val) < epsilon

def _scaleTuple(t, s):
    return (t[0] * s, t[1] * s)

def _add(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

def _rotate(vec, theta):
    return (vec[0] * cos(theta) - vec[1] * sin(theta), vec[1] * cos(theta) + vec[0] * sin(theta))

class Robot:
    # Coords = robot wheelbase center
    def __init__(self, x = 0.0, y = 0.0, theta = 0.0, timestamp = 0.0):
        self.x = x
        self.y = y
        self.theta = theta
        self.time = timestamp
        self.robotSize = (2.0, 2.0)
        self.leftSensorOffset = (1.0, 0.8)
        self.rightSensorOffset = (1.0, -0.8)
        self.sensorRange = 8.0 # cm

    def simulate(self, velR, velL, timestamp):
        dt = float(timestamp - self.time)
        self.time = timestamp

        if _isZero(velR - velL, DRIVING_STRAIGHT):
            vel = float(velR + velL) / 2
            self.x = self.x + vel * dt * sin(self.theta)
            self.y = self.y + vel * dt * cos(self.theta)
        else:
            oldTheta = float(self.theta)
            theta = (velR - velL) * dt / B + oldTheta

            coeff = float(B * (velR + velL)) / float(2.0 * (velR - velL))
            self.x = self.x + coeff * (sin(theta) - sin(oldTheta))
            self.y = self.y - coeff * (cos(theta) - cos(oldTheta))

            self.theta = theta

    def getPosition(self):
        return (self.x, self.y)

    def getOrientation(self):
        return self.theta

    def getLeftSensorPoint(self, dist):
        point = (self.x, self.y)
        point = _add(point, _rotate(self.leftSensorOffset, self.theta))
        point = _add(point, _rotate((dist, 0.0), self.theta))

        return point

    def getRightSensorPoint(self, dist):
        point = (self.x, self.y)
        point = _add(point, _rotate(self.rightSensorOffset, self.theta))
        point = _add(point, _rotate((dist, 0.0), self.theta))

        return point


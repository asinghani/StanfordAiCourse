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

class Robot:
    def __init__(self, x = 0.0, y = 0.0, theta = 0.0, timestamp = 0.0):
        self.x = x
        self.y = y
        self.theta = theta
        self.time = timestamp

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

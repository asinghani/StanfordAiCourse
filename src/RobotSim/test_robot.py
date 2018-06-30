import turtle, time
from robot import Robot, _scaleTuple
import math

robot = Robot(timestamp = time.time())
while True:
    robot.simulate(3.0, 1.5, time.time())
    turtle.goto(_scaleTuple(robot.getPosition(), 25.0))
    turtle.setheading(math.degrees(robot.getOrientation()))

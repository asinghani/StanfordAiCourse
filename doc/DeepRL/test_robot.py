import turtle, time
from robot import Robot, _scaleTuple
import math

turtle2 = turtle.Turtle()
turtle2.pencolor("green")
turtle2.shape("circle")
turtle2.shapesize(0.2)
turtle2.turtlesize(0.2)

turtle3 = turtle.Turtle()
turtle3.pencolor("green")
turtle3.shape("circle")
turtle3.shapesize(0.2)
turtle3.turtlesize(0.2)

turtle.mode(mode="standard")
turtle.speed(0)
turtle2.speed(0)
turtle3.speed(0)

robot = Robot(timestamp = time.time())
while True:
    robot.simulate(1.5, 0.5, time.time())
    turtle.goto(_scaleTuple(robot.getPosition(), 25.0))
    turtle.setheading(math.degrees(robot.getOrientation()))
    pos = robot.getPosition()
    turtle2.goto(_scaleTuple(robot.getLeftSensorPoint(5), 25.0))
    turtle3.goto(_scaleTuple(robot.getRightSensorPoint(5), 25.0))
    time.sleep(0.01)

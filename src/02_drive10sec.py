from base import start, end
import time

def periodicFunc(robot):

    robot.set_wheel(1, 15)
    robot.set_wheel(0, 15)
    time.sleep(3.5)
    robot.set_wheel(1, 0)
    robot.set_wheel(0, 0)
    end()

start(periodicFunc)

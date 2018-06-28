from base import start, end
import time

def periodicFunc(robot):

    robot.set_wheel(1, 30)
    robot.set_wheel(0, 30)
    time.sleep(2)
    robot.set_wheel(1, 0)
    robot.set_wheel(0, 0)
    end()

start(periodicFunc)

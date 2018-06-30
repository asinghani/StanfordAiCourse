from base import start, end
import time

# 0 = right turn, 1 = left turn, 2 = fwd
sol = [2, 2, 2, 0, 2, 0, 2, 1, 2, 1, 2]

def periodicFunc(robot):
    for i in sol:
        if i == 2:
            robot.set_wheel(1, 15)
            robot.set_wheel(0, 15)
            time.sleep(3.5)
            robot.set_wheel(1, 0)
            robot.set_wheel(0, 0)
        if i == 0:
            robot.set_wheel(1, -25)
            robot.set_wheel(0, 25)
            time.sleep(1.02)
            robot.set_wheel(0, 0)
            robot.set_wheel(1, 0)
        if i == 1:
            robot.set_wheel(1, 25)
            robot.set_wheel(0, -25)
            time.sleep(1.02)
            robot.set_wheel(0, 0)
            robot.set_wheel(1, 0)
    end()

start(periodicFunc)

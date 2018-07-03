from base import start, end
import time, sys


def periodicFunc(robot):
    print("Bal:")
    robot.set_wheel_balance(int(sys.stdin.readline()))
    print("Enter speed: ")
    speed = int(sys.stdin.readline())
    print("Enter time: ")
    time_ = float(sys.stdin.readline())

    robot.set_wheel(1, speed)
    robot.set_wheel(0, speed)
    time.sleep(time_)
    robot.set_wheel(1, 0)
    robot.set_wheel(0, 0)
    time.sleep(0.5)

start(periodicFunc)

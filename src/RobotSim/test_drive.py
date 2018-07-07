from base_sim import start, end, tankDrive
import time, sys


def periodicFunc(robot):
    print("Enter speed: ")
    speed = int(sys.stdin.readline())
    print("Enter time: ")
    time_ = float(sys.stdin.readline())

    tankDrive(speed, speed)
    time.sleep(time_)
    tankDrive(speed, -speed)
    time.sleep(time_)
    tankDrive(speed, speed)
    time.sleep(time_)
    tankDrive(-speed, speed)
    time.sleep(time_)
    tankDrive(speed, speed)
    time.sleep(time_)
    tankDrive(0, 0)
    time.sleep(0.5)

start(periodicFunc)

from base import start, end, tankDrive
import time

def periodicFunc(robot):
    for i in range(0, 200):
        print(i)
        tankDrive(int(i/4.0), int(i/4.0))
        time.sleep(1.0 / 200.0)

    tankDrive(50, 50)
    time.sleep(3.0)
    tankDrive(50,50)

    for r in range(0, 200):
        i = 200 - r
        print(i)
        tankDrive(int(i/4.0), int(i/4.0))
        time.sleep(1.0 / 200.0)

    end()

start(periodicFunc)

from base import start, end
import time

def periodicFunc(robot):
    def tankDrive(left, right):
        robot.set_wheel(0, left)
        robot.set_wheel(1, right)

    def stop():
        tankDrive(0, 0)

    def turnLeft():
        tankDrive(-25, 25)
        time.sleep(1.3)
        stop()

    def turnRight():
        tankDrive(25, -25)
        time.sleep(1.3)
        stop()

    l1 = robot.get_floor(0)
    l2 = robot.get_floor(1)
    if l1 + l2 < 80:
        stop()
        time.sleep(0.1)
        robot.set_musical_note(40)
        time.sleep(0.5)
        robot.set_musical_note(0)
        time.sleep(0.1)
        turnLeft()
        time.sleep(0.5)
        turnRight()
        turnRight()
        time.sleep(0.5)
        turnLeft()
        time.sleep(0.5)
        tankDrive(25, 25)
        time.sleep(0.75)
        stop()
        time.sleep(0.3)
    else:
        error = l1 - l2
        speed = 15
        kP = 0.3
        tankDrive(int(speed + error * kP), int(speed - error * kP))
    time.sleep(0.1)

start(periodicFunc)

from base import start, end, tankDrive, turn, forward, getFloor, getProximity, stop, beepSync, setMusicNote, getBattery
import time, random

def getVel():
    battery = getBattery()
    if battery < 1.0:
        battery = 3.9

    vel = 10
    vel = vel * 3.88 / battery
    print(vel)
    return int(vel)

def turnLeft():
    print("LEFT")
    vel = getVel()
    tankDrive(vel, vel)
    time.sleep(1.3)
    tankDrive(-vel, vel)
    time.sleep(2.2)
    stop()

def turnRight():
    print("RIGHT")
    vel = getVel()
    tankDrive(vel, vel)
    time.sleep(1.3)
    tankDrive(vel, -vel)
    time.sleep(2.2)
    stop()

def forwardAtIntersection():
    print("FWD")
    vel = getVel()
    tankDrive(vel, vel)
    time.sleep(1.3)
    stop()

# 0 = left turn, 1 = right turn, 2 = fwd, 3 = end
cmds = [1, 2, 0, 2, 0, 2, 1, 3]

def periodicFunc(robot):
    global cmds

    l1 = robot.get_floor(0)
    l2 = robot.get_floor(1)
    if l1 + l2 < 80:
        stop()
        time.sleep(0.1)
        robot.set_musical_note(40)
        time.sleep(0.5)
        robot.set_musical_note(0)
        time.sleep(0.1)

        cmd = cmds[0]
        cmds = cmds[1:]

        if cmd == 0:
            turnLeft()
        elif cmd == 1:
            turnRight()
        elif cmd == 2:
            forwardAtIntersection()

        stop()

        if cmd == 3:
            end()

        if len(cmds) == 0:
            end()

    else:
        error = l1 - l2
        speed = 15
        kP = 0.3
        tankDrive(int(speed + error * kP), int(speed - error * kP))

    time.sleep(0.05)
start(periodicFunc)

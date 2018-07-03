from base import start, end, tankDrive, turn, forward, getFloor, getProximity, stop, beepSync, setMusicNote
import time
from fsm import FSM
from threading import Thread, Timer
import random

endAll = False
numLeft = 3

PROX_THRESHOLD = 60
FLOOR_THRESHOLD = 50

def stopBeep():
    stop()
    beepSync(0.5)

started = False

fsm = FSM(["free", "rotating", "aligning", "pushing", "reversing", "completed"], "free", failActionSilently = True, verbose = True)
fsm.addTransition("start", "free", "free")
fsm.addTransition("seeLine", "free", "rotating")
fsm.addTransition("rotateCompleted", "rotating", "free")
fsm.addTransition("seeTrash", "free", "aligning", beforeChange = lambda a, b, c: stopBeep())
fsm.addTransition("alignCompleted", "aligning", "pushing")
fsm.addTransition("seeLine", "pushing", "reversing", beforeChange = lambda a, b, c: stopBeep())
fsm.addTransition("finish", "reversing", "completed")

def backupCompletedCb():
    global numLeft
    numLeft = numLeft - 1
    print("{} Pieces Left".format(numLeft))
    if numLeft == 0:
        return "completed"
    else:
        return "rotating"

fsm.addTransition("backupCompleted", "reversing", backupCompletedCb)

def alignCb():
    stop()
    beepSync(0.5)

fsm.setEnterCallback("aligning", alignCb)

fsm.setEnterCallback("free", lambda: tankDrive(45, 45))

def startRotating():
    tankDrive(-40, 40)

    def stopRotating():
        fsm.runAction("rotateCompleted")

    Timer(random.uniform(0.3, 0.7), stopRotating).start()

fsm.setEnterCallback("rotating", startRotating)

fsm.setEnterCallback("pushing", lambda: tankDrive(100, 100))

def startReversing():
    tankDrive(-70, -70)

    def stopReversing():
        fsm.runAction("backupCompleted")

    Timer(1.5, stopReversing).start()

fsm.setEnterCallback("reversing", startReversing)

def playEndMusic():
    stop()
    music = [
    (60, 0.7),
    (20, 0.2),
    (40, 0.1)
    ] * 5
    for note in music:
        setMusicNote(note[0])
        time.sleep(note[1])
    setMusicNote(0)

fsm.setEnterCallback("completed", playEndMusic)


def updateSensors():
    global endAll

    while not endAll:
        prox = getProximity()
        floor = getFloor()

        if (floor[0] < FLOOR_THRESHOLD or floor[1] < FLOOR_THRESHOLD) and floor[0] != 0 and floor[1] != 0:
            fsm.runAction("seeLine")
        elif (prox[0] + prox[1]) / 2 > PROX_THRESHOLD:
            fsm.runAction("seeTrash")

        time.sleep(0.03)

def periodicFunc(robot):
    global started
    if not started:
        fsm.runAction("start")
        started = True

    if fsm.getState() == "aligning":
        prox = getProximity()
        if abs(prox[0] - prox[1]) < 3:
            fsm.runAction("alignCompleted")
            pass
        else:
            speed = int(0.5 * (prox[1] - prox[0]))
            tankDrive(speed, -speed)

    time.sleep(0.1)

Thread(target=updateSensors).start()
start(periodicFunc)

from base import start, end, tankDrive, turn, forward, getFloor, getProximity, stop, beepSync, setMusicNote
import time
import base_web
from Queue import Queue
from fsm import FSM
from threading import Thread

uiQueue = Queue(maxsize=1)
endAll = False

PROX_THRESHOLD = 40
FLOOR_THRESHOLD = 50

fsm = FSM(["free", "turnLeft", "turnRight", "exit"], "free", failActionSilently = True, verbose = True)
fsm.addTransition("obstacleLeft", "free", "turnLeft", )
fsm.addTransition("obstacleRight", "free", "turnRight")
fsm.addMultipleTransitions("noObstacle", ["turnLeft", "turnRight"], "free")
fsm.addTransition("line", "free", "exit")


def freeCb():
    tankDrive(50, 50)

def turnLeftCb():
    tankDrive(-50, 50)

def turnRightCb():
    tankDrive(50, -50)

def exitCb():
    stop()
    beepSync(0.5)
    forward(50, 1.5)
    beepSync(0.5)
    end()

fsm.setEnterCallback("free", freeCb)
fsm.setEnterCallback("turnLeft", turnLeftCb)
fsm.setEnterCallback("turnRight", turnRightCb)
fsm.setEnterCallback("exit", exitCb)

def updateSensors():
    global queue
    global uiQueue
    global endAll
    while not endAll:
        prox = getProximity()
        floor = getFloor()

        try:
            uiQueue.put([prox[0], prox[1], floor[0], floor[1]], block = False)
        except:
            pass

        if (floor[0] < FLOOR_THRESHOLD or floor[1] < FLOOR_THRESHOLD) and floor[0] != 0 and floor[1] != 0:
            fsm.runAction("line")
        elif (prox[0] + prox[1]) / 2 > PROX_THRESHOLD:
            if prox[0] > prox[1]:
                fsm.runAction("obstacleRight")
            else:
                fsm.runAction("obstacleLeft")
        else:
            fsm.runAction("noObstacle")

        time.sleep(0.03)

def updateUI():
    global uiQueue
    global endAll
    while not endAll:
        data = uiQueue.get(block = True)

        base_web.readDict["leftProx"] = data[0]
        base_web.readDict["rightProx"] = data[1]
        base_web.readDict["leftFloor"] = data[2]
        base_web.readDict["rightFloor"] = data[3]


def playEndMusic():
    music = [
    (60, 0.7),
    (20, 0.2),
    (40, 0.1)
    ] * 2
    for note in music:
        setMusicNote(note[0])
        time.sleep(note[1])
    setMusicNote(0)

def periodicFunc(robot):
    time.sleep(0.1)

Thread(target=updateSensors).start()
Thread(target=updateUI).start()
base_web.start("03_escape_ui.html", "03_escape.js", {"leftProx": 0, "rightProx": 0, "leftFloor": 0, "rightFloor": 0}, None)
start(periodicFunc)

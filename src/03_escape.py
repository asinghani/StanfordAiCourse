from base import start, end, tankDrive, turn, forward, getFloor, getProximity, stop, beepSync, setMusicNote
import time
import base_web
from Queue import Queue
from threading import Thread

queue = Queue(maxsize=1)
uiQueue = Queue(maxsize=1)
endAll = False

PROX_THRESHOLD = 40
FLOOR_THRESHOLD = 50

EVENT_BORDER = 1
EVENT_NONE = 2

def updateSensors():
    global queue
    global uiQueue
    global endAll
    while not endAll:
        prox = getProximity()
        floor = getFloor()

        try:
            uiQueue.put([prox[0], prox[1], floor[0], floor[1]], block = True)

            if (floor[0] < FLOOR_THRESHOLD or floor[1] < FLOOR_THRESHOLD) and floor[0] != 0 and floor[1] != 0:
                queue.put(EVENT_BORDER, block = True)
                print("EVENT_BORDER")
                print(floor[0], floor[1])
            elif (prox[0] + prox[1]) / 2 > PROX_THRESHOLD:
                queue.put((prox[0] + prox[1]) / 2, block = False)
                print("EVENT_OBSTACLE")
            else:
                queue.put(EVENT_NONE, block = False)
                print("EVENT_NONE")
        except:
            pass

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
    command = -1
    try:
        command = queue.get(block = True)
    except:
        pass
    if command > 10:
        x = command / 5
        tankDrive(-(5+x), 5+x)
    elif command == EVENT_BORDER:
        stop()
        beepSync(0.5)
        forward(40, 2.0)
        playEndMusic()
        endAll = True
        print("FINISHED")
        end()
    else:
        tankDrive(30, 30)

    time.sleep(0.1)

Thread(target=updateSensors).start()
Thread(target=updateUI).start()
base_web.start("03_escape_ui.html", "03_escape.js", {"leftProx": 0, "rightProx": 0, "leftFloor": 0, "rightFloor": 0}, None)
start(periodicFunc)

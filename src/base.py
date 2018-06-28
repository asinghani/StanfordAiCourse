import Tkinter as tk
import time
from HamsterAPI.comm_ble import RobotComm
from threading import Thread

robotList = None
endVar = False
func = lambda a: a
robot = None


def tankDrive(left, right):
    global robot
    robot.set_wheel(0, left)
    robot.set_wheel(1, right)

def forward(speed, time):
    tankDrive(speed, speed)
    time.sleep(time)
    tankDrive(0, 0)

def turn(speed, time):
    tankDrive(speed, -speed)
    time.sleep(time)
    tankDrive(0, 0)

def stop():
    tankDrive(0, 0)

def getProximity():
    global robot
    return (robot.get_proximity(0), robot.get_proximity(1))

def getFloor():
    global robot
    return (robot.get_floor(0), robot.get_floor(1))

def getBattery():
    global robot
    return robot.get_battery()

def getAccel():
    global robot
    return (robot.get_acceleration(0), robot.get_acceleration(1), robot.get_acceleration(2))

COLOR_WHITE = 7
COLOR_YELLOW = 6
COLOR_MAGENTA = 5
COLOR_RED = 4
COLOR_CYAN = 3
COLOR_GREEN = 2
COLOR_BLUE = 1
COLOR_NONE = 0

def setLeds(left, right):
    global robot
    robot.set_led(0, left)
    robot.set_led(1, right)

def setLEDs(left, right):
    return setLeds(left, right)

def setMusicNote(note):
    global robot
    robot.set_musical_note(note)

def beepSync(t=0.5):
    setMusicNote(40)
    time.sleep(t)
    setMusicNote(0)

def end():
    global endVar
    endVar = True

def runRobot():
    global endVar, robotList, func, robot
    i = 0
    while not endVar:
        if len(robotList) > 0 and not (robotList[0] is None):
            i = i + 1
            if i > 10:
                robot = robotList[0]
                func(robotList[0])
            else:
                robot = None
                time.sleep(0.1)
    robotList[0].reset()


def start(periodicFunc):
    global robotList, func
    func = periodicFunc
    comm = RobotComm(1)
    comm.start()
    print("Bluetooth running...")

    robotList = comm.robotList

    window = tk.Tk()
    canvas = tk.Canvas(window, bg="white", width=300, height= 300)
    canvas.pack()

    button = tk.Button(window, text="Exit")
    button.pack()
    button.bind("<Button-1>", lambda: window.quit())

    robotThread = Thread(target = runRobot)
    robotThread.start()
    window.mainloop()

    comm.stop()
    comm.join()

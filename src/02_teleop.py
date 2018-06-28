from base import start, end
import time
from flask import Flask, request
import thread

# Load HTML
html = "error"
with open("02_teleop_index.html", "r") as file:
    html = file.read()

leftDist = 0
rightDist = 0
leftFloor = 0
rightFloor = 0

leftDrive = 0
rightDrive = 0

def periodicFunc(robot):
    global leftDist, rightDist, leftFloor, rightFloor, leftDrive, rightDrive
    leftDist = robot.get_proximity(0)
    rightDist = robot.get_proximity(1)
    leftFloor = robot.get_floor(0)
    rightFloor = robot.get_floor(1)

    robot.set_wheel(0, leftDrive)
    robot.set_wheel(1, rightDrive)

    time.sleep(0.05)

app = Flask(__name__)

@app.route("/get")
def getData():
    return "{},{},{},{}".format(leftDist, rightDist, leftFloor, rightFloor)

@app.route("/set")
def setData():
    global leftDrive, rightDrive
    leftDrive = int(request.args.get("left"))
    rightDrive = int(request.args.get("right"))
    return ""

@app.route("/drive")
def drivePage():
    return html

thread.start_new_thread(app.run, ())

start(periodicFunc)

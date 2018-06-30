from base import start, end
import time
import curses
from threading import Thread

value = 0
string = ""

def periodicFunc(robot):
    global string
    string = """
Version: {}
Topology: {}
Network ID: {}

Command: {}
Security: {}
Signal: {}

Left Prox: {}
Right Prox: {}

Left Floor: {}
Right Floor: {}

Accel: {}, {}, {}

Flag: {}
Light: {}
Temp: {}
Battery: {}

IO Mode 0: {}
IO Mode 1: {}

Port 0: {}
Port 1: {}
Linetracer State: {}
    """.format(
        robot.get_version(),
        robot.get_topology(),
        robot.get_network_id(),
        robot.get_command(),
        robot.get_security(),
        robot.get_signal(),
        robot.get_proximity(0),
        robot.get_proximity(1),
        robot.get_floor(0),
        robot.get_floor(1),
        robot.get_acceleration(0),
        robot.get_acceleration(1),
        robot.get_acceleration(2),
        robot.get_flag(),
        robot.get_light(),
        robot.get_temperature(),
        robot.get_battery(),
        robot.get_io_mode(0),
        robot.get_io_mode(1),
        robot.get_port(0),
        robot.get_port(1),
        robot.get_linetracer_state()
    ).strip()
    #print(string)
    time.sleep(0.1)


def runCursesUI(scr):
    global string
    scr.nodelay(True)
    scr.clear()
    while True:
        scr.getch()
        curses.flushinp()
        scr.clear()
        scr.addstr(string)
        time.sleep(0.1)

def startUI():
    curses.wrapper(runCursesUI)

Thread(target=startUI).start()
start(periodicFunc)


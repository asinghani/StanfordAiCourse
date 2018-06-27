import sys, time, threading

# Replace with comm_usb if using dongle
from HamsterAPI.comm_ble import RobotComm
import Tkinter as tk


class RobotThread(threading.Thread):
    def __init__(self, robotList, func):
        super(RobotThread, self).__init__()
        self.stopThread = False
        self.robotList = robotList
        self.robot = None
        self.func = func
        return

    def rot(self):
        self.robot.set_wheel(0, -30)
        time.sleep(10)

    def run(self):
        while not self.stopThread:
            if self.robotList and len(self.robotList) > 0:
                self.robot = self.robotList[0]
                self.robotList = None
                print("Started")
            if self.robot:
                while True:
                    print(self.robot.get_proximity(1))
                    time.sleep(0.1)
                    p = self.robot.get_proximity(1)
                    if p > 25:
                        self.robot.set_wheel(0, -30)
                        self.robot.set_wheel(1, -30)
                    else:
                        self.robot.set_wheel(0, 0)
                        self.robot.set_wheel(1, 0)





                self.robot.reset()
                time.sleep(1)
                print("Finished")
                self.stopThread = True

def start():
    comm = RobotComm(1)
    comm.start()
    time.sleep(2)

    RobotThread(comm.robotList, None).start()

    frame = tk.Tk()
    frame.mainloop()

    comm.stop()
    comm.join()

start()

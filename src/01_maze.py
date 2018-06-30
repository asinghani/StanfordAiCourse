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
        self.turning = False
        self.turnIters = 0
        while not self.stopThread:
            if self.robotList and len(self.robotList) > 0:
                self.robot = self.robotList[0]
                self.robotList = None
                print("Started")
            if self.robot:
                while True:
                    fwd = self.robot.get_proximity(0)
                    right = self.robot.get_proximity(1)
                    print(fwd, right)
                    time.sleep(0.1)

                    if self.turning and self.turnIters < 35:
                        self.turnIters = self.turnIters + 1
                        self.robot.set_wheel(0, 25)
                        self.robot.set_wheel(1, -20)
                    else:
                        self.turning = False

                    if right < 10:
                        self.turning = True
                        self.turnIters = 0
                        print("RIGHT")
                        # TURN RIGHT
                        self.robot.set_wheel(0, 25)
                        self.robot.set_wheel(1, -20)

                    fwd = self.robot.get_proximity(0)

                    if fwd < 45:
                        print("FORWARD")
                        self.robot.set_wheel(0, 50)
                        self.robot.set_wheel(1, 50)

                    if right > 10 and fwd >= 45:
                        print("LEFT")
                        self.robot.set_wheel(0, -20)
                        self.robot.set_wheel(1, 20)
                        time.sleep(1.33)
                        self.robot.set_wheel(0, 0)
                        self.robot.set_wheel(1, 0)





                self.robot.reset()
                time.sleep(1)
                print("Finished")
                self.stopThread = True

def start():
    comm = RobotComm(1)
    comm.start()

    RobotThread(comm.robotList, None).start()

    frame = tk.Tk()
    frame.mainloop()

    comm.stop()
    comm.join()

start()

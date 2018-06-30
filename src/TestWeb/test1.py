import time
import base_web

def func(event):
    print("event: "+event)

base_web.start("test1.html", "test1.js", {"time": 0}, func)

while True:
    base_web.readDict["time"] = base_web.readDict["time"] + 1
    print(base_web.writeDict)
    time.sleep(0.25)


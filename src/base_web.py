import time
from flask import Flask, request
import json
import logging
import sys

if (sys.version_info > (3, 0)):
    import _thread as thread
else:
    import thread

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

outputDict = {}
inputDict = {}

def start(htmlFile, jsFile, baseDict, eventCallback):
    global outputDict, inputDict
    inputDict = baseDict

    app = Flask(__name__)

    html = "error"
    with open(htmlFile, "r") as file:
        html = file.read()

    js = "error"
    with open(jsFile, "r") as file:
        js = file.read()

    basejs = "error"
    with open("base.js", "r") as file:
        basejs = file.read()

    @app.route("/update")
    def getData():
        global inputDict, outputDict
        jsonData = request.args.get("data")
        data = json.loads(jsonData)
        for key in data.keys():
            inputDict[key] = data[key]

        return json.dumps(outputDict)

    @app.route("/event")
    def event():
        eventCallback(request.args.get("eventType"))
        return ""

    @app.route("/")
    def indexPage():
        return html

    @app.route("/base.js")
    def baseJS():
        return basejs

    @app.route("/"+jsFile)
    def appJS():
        return js

    thread.start_new_thread(app.run, ())

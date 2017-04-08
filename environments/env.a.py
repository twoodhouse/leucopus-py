#!/usr/bin/python3
from flask import Flask
import random
app = Flask(__name__)
app.config['SERVER_NAME'] = 'env.a:5001'
lightIsOn = False
#
@app.route("/")
def hello():
    return "This is a button and a lightbulb! Note that the button stays depressed once it is touched (unless it is reset)"

@app.route("/resetall")
def resetAll():
    global lightIsOn
    lightIsOn = False
    return ""

@app.route("/pushbutton")
def pushButton():
    global lightIsOn
    if lightIsOn:
        return ""
    else:
        lightIsOn = True
        return ""

@app.route("/resetbutton")
def releaseButton():
    global lightIsOn
    if lightIsOn:
        lightIsOn = False
        return ""
    else:
        return ""

@app.route("/checklight")
def checkLight():
    global lightIsOn
    # lightIsOn = bool(random.getrandbits(1))
    if lightIsOn:
        return "true"
    else:
        return "false"

if __name__ == "__main__":
    app.run()

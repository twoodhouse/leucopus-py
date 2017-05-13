#!/usr/bin/python3
from flask import Flask
app = Flask(__name__)
app.config['SERVER_NAME'] = 'env.d:5001'
lightIsOn = False
pressCount = 0
#
@app.route("/")
def hello():
    return "This is a button and a lightbulb! The light turns on after two presses. Turns off when reset is pressed."

@app.route("/resetall")
def resetAll():
    global lightIsOn, pressCount
    lightIsOn = False
    pressCount = 0
    return ""

@app.route("/pushbutton")
def pushButton():
    global lightIsOn, pressCount
    if pressCount >= 1:
        lightIsOn = True
    pressCount = pressCount + 1
    return ""

@app.route("/resetbutton")
def resetButton():
    global lightIsOn, pressCount
    lightIsOn = False
    pressCount = 0
    return ""

@app.route("/checklight")
def checkLight():
    global lightIsOn
    if lightIsOn:
        return "true"
    else:
        return "false"

if __name__ == "__main__":
    app.run()

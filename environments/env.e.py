#!/usr/bin/python3
from flask import Flask
app = Flask(__name__)
app.config['SERVER_NAME'] = 'env.e:5002'
lightIsOn1 = False
lightIsOn2 = False
pressCount1 = 0
pressCount2 = 0
#
@app.route("/")
def hello():
    return "This is 2 buttons and 2 lightbulbs! One light toggles every two presses. The other light toggles every four presses."

@app.route("/resetall")
def resetAll():
    global lightIsOn1, lightIsOn2, pressCount1, pressCount2
    lightIsOn1 = False
    lightIsOn2 = False
    pressCount1 = 0
    pressCount2 = 0
    return ""

@app.route("/pushbutton1")
def pushButton1():
    global lightIsOn1, pressCount1
    if pressCount1 == 1:
        pressCount1 = 0
        lightIsOn1 = not lightIsOn1
        return ""
    else:
        pressCount1 = pressCount1 + 1
        return ""

@app.route("/pushbutton2")
def pushButton2():
    global lightIsOn2, pressCount2
    if pressCount2 == 3:
        pressCount2 = 0
        lightIsOn2 = not lightIsOn2
        return ""
    else:
        pressCount2 = pressCount2 + 1
        return ""

@app.route("/checklight1")
def checkLight1():
    global lightIsOn1, pressCount1
    if lightIsOn1:
        return "true"
    else:
        return "false"

@app.route("/checklight2")
def checkLight2():
    global lightIsOn2, pressCount2
    if lightIsOn2:
        return "true"
    else:
        return "false"

if __name__ == "__main__":
    app.run()

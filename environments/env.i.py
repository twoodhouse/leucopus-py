#!/usr/bin/python3
from flask import Flask
app = Flask(__name__)
app.config['SERVER_NAME'] = 'env.i:5002'
pressCount1 = 0
pressCount2 = 0
pressCount3 = 0
lightIsOn1 = False
lightIsOn2 = False
lightIsOn3 = False
#
@app.route("/")
def hello():
    return "This is 3 buttons and 3 lightbulbs! The light turns on temporarily every two presses. The other light turns on temporarily every four presses. The final light turns on temporarily every eight presses."

@app.route("/resetall")
def resetAll():
    global pressCount1, lightIsOn1, pressCount2, lightIsOn2
    pressCount1 = 0
    pressCount2 = 0
    pressCount3 = 0
    lightIsOn1 = False
    lightIsOn3 = False
    lightIsOn2 = False
    return ""

@app.route("/pushbutton1")
def pushButton1():
    global pressCount1, lightIsOn1
    if pressCount1 == 1:
        pressCount1 = 0
        lightIsOn1 = True
    else:
        pressCount1 = pressCount1 + 1
    return ""

@app.route("/checklight1")
def checkLight1():
    global lightIsOn1, pressCount1
    if lightIsOn1:
        lightIsOn1 = False
        return "true"
    else:
        lightIsOn1 = False
        return "false"

@app.route("/pushbutton2")
def pushButton2():
    global pressCount2, lightIsOn2
    if pressCount2 == 3:
        pressCount2 = 0
        lightIsOn2 = True
    else:
        pressCount2 = pressCount2 + 1
    return ""

@app.route("/checklight2")
def checkLight2():
    global lightIsOn2, pressCount2
    if lightIsOn2:
        lightIsOn2 = False
        return "true"
    else:
        lightIsOn2 = False
        return "false"

@app.route("/pushbutton3")
def pushButton3():
    global pressCount3, lightIsOn3
    if pressCount3 == 7:
        pressCount3 = 0
        lightIsOn3 = True
    else:
        pressCount3 = pressCount3 + 1
    return ""

@app.route("/checklight3")
def checkLight3():
    global lightIsOn3, pressCount3
    if lightIsOn3:
        lightIsOn3 = False
        return "true"
    else:
        lightIsOn3 = False
        return "false"

if __name__ == "__main__":
    app.run()

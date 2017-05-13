#!/usr/bin/python3
from flask import Flask
app = Flask(__name__)
app.config['SERVER_NAME'] = 'env.g:5002'
pressCount1 = 0
lightIsOn1 = False
#
@app.route("/")
def hello():
    return "This is a button and a lightbulb! The light turns on temporarily every two presses."

@app.route("/resetall")
def resetAll():
    global pressCount1, lightIsOn1
    pressCount1 = 0
    lightIsOn1 = False
    return ""

@app.route("/pushbutton")
def pushButton():
    global pressCount1, lightIsOn1
    if pressCount1 == 1:
        pressCount1 = 0
        lightIsOn1 = True
    else:
        pressCount1 = pressCount1 + 1
    return ""

@app.route("/checklight")
def checkLight():
    global lightIsOn1, pressCount1
    if lightIsOn1:
        lightIsOn1 = False
        return "true"
    else:
        lightIsOn1 = False
        return "false"

if __name__ == "__main__":
    app.run()

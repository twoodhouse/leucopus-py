#!/usr/bin/python3.5
from deluge import Deluge
from dm import RandomDM
from environments import *
from random import randint
import sys

env = TempButtons1248()
dm = RandomDM(env)
deluge = Deluge(env, dm, [0, 0, 0, 0])
sys.setrecursionlimit(10000)

for i in range(300):
    deluge.processNextFrame(printOp = True)

print("********************")
for i in range(40):
    deluge.TryExplanation()
deluge.startNewPrediction()

for i in range(100):
    deluge.processNextPFrame(printOp = True)

deluge.printHyps()

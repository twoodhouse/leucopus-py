#!/usr/bin/python3.5
from deluge import Deluge
from dm import RandomDM
from environments import *
from random import randint
import sys
from hyp import Hyp
from tt import TT
from logUtility import tStart, tEnd

env = TempButtons1248()
dm = RandomDM(env)
deluge = Deluge(env, dm, [0, 0, 0, 0])
sys.setrecursionlimit(10000)

for i in range(300):
    deluge.processNextFrame(printOp = True)

print("********************")
hyp = Hyp(infoIndeces = [], actionIndeces = [1], tts = [TT([0,1,1,0])], iniTats = [0], rHyps = [], rHypLocations = [], iniRat = 0)
deluge.trySpecificExplanation(1, hyp)
for i in range(40):
    deluge.tryExplanation()

deluge.startNewPrediction()

for i in range(100):
    deluge.processNextPFrame(printOp = True)

deluge.printHyps()

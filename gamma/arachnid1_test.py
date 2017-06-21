#!/usr/bin/python3.5
from arachnid import Arachnid
from dm import RandomDM
from environments import TempButton, ToggleButton, TwoTempButton, TempButtons1248
import sys

sys.setrecursionlimit(10000)

env = TempButtons1248()
dm = RandomDM(env)
arachnid = Arachnid(env, dm)
arachnid.getFrames(100)
print(arachnid.inputFrames)

maxScore = 0
for i in range(100000):
    score = arachnid.spinRandomWeb(100)[1]
    print(score)
    if score > maxScore:
        maxScore = score
    print("max: " + str(maxScore))

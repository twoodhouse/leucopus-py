#!/usr/bin/python3.5

from palette import Palette
from hyp import Hyp
from tt import TT
from environments import *
from random import randint

def genRandomFrameActions(numActionsPerFrame, numFrames):
    frameActions = []
    for i in range(numFrames):
        frameAction = []
        for j in range(numActionsPerFrame):
            randVal = randint(0, 1)
            frameAction.append(randVal)
        frameActions.append(frameAction)
    return frameActions

env = TwoTempButtonFourTempButton()

tt1 = TT([0,1,1,0,0,1,1,0])
hyp1 = Hyp(infoIndeces = [0], actionIndeces = [0], tts = [tt1], iniTats = [0], rHyps = [], rHypLocations = [], iniRat = 0)
hyp2 = Hyp(infoIndeces = [0], actionIndeces = [], tts = [], iniTats = [], rHyps = [], rHypLocations = [], iniRat = 0)

# frameActionSet = [[1], [0], [1], [1], [1], [1], [1], [1], [1], [1], [0], [0], [0], [1], [1], [1], [1], [1], [0]]
frameActionSet = genRandomFrameActions(2, 20)

initialIats, initialAats = env.runFrame(frameActionSet[0])
foundationPalette = Palette(iats = initialIats, aats = initialAats, isFoundation = True, hyps = [hyp1, hyp2])
print(foundationPalette.iats, foundationPalette.aats, foundationPalette.rats)
palette = foundationPalette
# print("[---------->"+str(palette.cases[0].genFullAttributes()))
for frameActions in frameActionSet[1:]:
    newIats, newAats = env.runFrame(frameActions)
    palette = palette.genNext(iats = newIats, aats = newAats)
    print(palette.iats, palette.aats, palette.rats)
    # print("[---------->"+str(palette.cases[0].genFullAttributes()))

print("*******************")
env.reset()
print(foundationPalette.trainHypsUsingDownstreamAts())

rHyp = hyp1.copy()
tt2 = tt1.copy()
rHyp.actionIndeces = [1]
modHyp2 = Hyp(infoIndeces = [], actionIndeces = [], tts = [tt1], iniTats = [0], rHyps = [rHyp], rHypLocations = [0], iniRat = 0)
print(foundationPalette.trainDifferentHyp(modHyp2, 1))
print(foundationPalette)

# pFrameActionSet = [[1], [0], [1], [1], [1], [1], [1], [1], [1], [1], [0], [0], [0], [1], [1], [1], [1], [1], [0]]
pFrameActionSet = frameActionSet

print(foundationPalette.iats, foundationPalette.aats, foundationPalette.rats)
palette = foundationPalette
# print("[---------->"+str(palette.cases[0].genFullAttributes()))
for pFrameActions in pFrameActionSet[1:]:
    newIats, newAats = env.runFrame(pFrameActions)
    palette = palette.genNext(aats = newAats)
    print(palette.iats, palette.aats, palette.rats)
    # print("[---------->"+str(palette.cases[0].genFullAttributes()))

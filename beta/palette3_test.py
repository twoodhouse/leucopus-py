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

env = TempButtons1248()

hyp1 = Hyp(infoIndeces = [0], actionIndeces = [], tts = [], iniTats = [], rHyps = [], rHypLocations = [], iniRat = 0)
hyp2 = Hyp(infoIndeces = [0], actionIndeces = [], tts = [], iniTats = [], rHyps = [], rHypLocations = [], iniRat = 0)
hyp3 = Hyp(infoIndeces = [0], actionIndeces = [], tts = [], iniTats = [], rHyps = [], rHypLocations = [], iniRat = 0)
hyp4 = Hyp(infoIndeces = [0], actionIndeces = [], tts = [], iniTats = [], rHyps = [], rHypLocations = [], iniRat = 0)

frameActionSet = genRandomFrameActions(4, 50)

initialIats, initialAats = env.runFrame(frameActionSet[0])
foundationPalette = Palette(iats = initialIats, aats = initialAats, isFoundation = True, hyps = [hyp1, hyp2, hyp3, hyp4])
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

newHyp1 = Hyp(infoIndeces = [], actionIndeces = [0], tts = [], iniTats = [], rHyps = [], rHypLocations = [], iniRat = 0)
print(foundationPalette.trainDifferentHyp(newHyp1, 0))

newHyp2 = Hyp(infoIndeces = [], actionIndeces = [1], tts = [TT([0,1,1,0])], iniTats = [0], rHyps = [], rHypLocations = [], iniRat = 0)
print(foundationPalette.trainDifferentHyp(newHyp2, 1))

rHyp3a = newHyp2.copy()
rHyp3a.actionIndeces = [2]
newHyp3 = Hyp(infoIndeces = [], actionIndeces = [], tts = [TT([0,1,1,0])], iniTats = [0], rHyps = [rHyp3a], rHypLocations = [0], iniRat = 0)
print(foundationPalette.trainDifferentHyp(newHyp3, 2))

rHyp4a = newHyp3.copy()
rHyp4a.rHyps[0].actionIndeces = [3] #Question: How do I iterate to get to this point?
newHyp4 = Hyp(infoIndeces = [], actionIndeces = [], tts = [TT([0,1,1,0])], iniTats = [0], rHyps = [rHyp4a], rHypLocations = [0], iniRat = 0)
print(foundationPalette.trainDifferentHyp(newHyp4, 3))

foundationPalette.infoPrintAll()
# foundationPalette.infoPrintAttClasses(2)
# newHyp3 = Hyp(infoIndeces = [], actionIndeces = [2], tts = [TT([0,0,1,1,0,1,1,0]), TT([0,1,0,1,1,0,1,0])], iniTats = [0,0], rHyps = [], rHypLocations = [], iniRat = 0)
# print(foundationPalette.trainDifferentHyp(newHyp3, 2))
#
# rHyp = newHyp3.copy()
# rHyp.actionIndeces = [3]
# newHyp4 = Hyp(infoIndeces = [], actionIndeces = [], tts = [TT([0,1,1,0])], iniTats = [0], rHyps = [rHyp], rHypLocations = [0], iniRat = 0)
# print(foundationPalette.trainDifferentHyp(newHyp4, 3))
# foundationPalette.infoPrintCase(3) #TODO: This output is incorrect

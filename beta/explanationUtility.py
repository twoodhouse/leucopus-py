import random
import math
from tt import TT
from hyp import Hyp
from logUtility import tStart, tEnd


def attemptNewExplanation(palette):
    if palette.hyps == None or palette.scores == None:
        raise ValueError("Must be foundational Palette (and already fitted) to attempt new explanation")
    indexToMod = chooseIndexToMod(palette) #can be selected based off what infos have poor scores and how often they have been attempted
    # indexToMod = 1
    # print(indexToMod)
    oldHyp = palette.hyps[indexToMod]
    oldScores = []
    for score in palette.scores:
        oldScores.append(score)
    #Generate Hyp attributes
    tts, iniTats, numInputs = chooseTableInfo(oldHyp, palette.attemptCounter[indexToMod]) #can be selected based off the tts chosen by related hyps and modified from these (or chosen randomly)
    # infoIndeces, actionIndeces, rHyps, rHypLocations, iniRat = chooseRelationalInfo(palette, oldHyp)
    infoIndeces, actionIndeces, rHyps, rHypLocations, iniRat = chooseRelationalInfo_simple(palette, oldHyp, numInputs)
    # for tt in tts:
    #     print(str(tt))
    # print(infoIndeces, actionIndeces)
    #generate hyp
    hyp = Hyp(infoIndeces = infoIndeces, actionIndeces = actionIndeces, tts = tts, iniTats = iniTats, rHyps = rHyps, rHypLocations = rHypLocations, iniRat = iniRat)
    #try it out
    trainResult = palette.trainDifferentHyp(hyp, indexToMod)
    print(trainResult)
    scoreLess = False
    for index, score in enumerate(palette.scores): #Efficiency here can be improved by switching to a while statement and exiting early
        if score < oldScores[index]:
            scoreLess = True
    if scoreLess:
        palette.trainDifferentHyp(oldHyp, indexToMod)
    #indicate that another attempt has been made
    palette.attemptCounter[indexToMod] = palette.attemptCounter[indexToMod] + 1

def attemptSpecificExplanation(palette, index, hyp):
    if palette.hyps == None or palette.scores == None:
        raise ValueError("Must be foundational Palette (and already fitted) to attempt new explanation")
    indexToMod = index #can be selected based off what infos have poor scores and how often they have been attempted
    oldHyp = palette.hyps[indexToMod]
    oldScores = []
    for score in palette.scores:
        oldScores.append(score)
    #try it out
    print(palette.trainDifferentHyp(hyp, indexToMod))
    scoreLess = False
    for index, score in enumerate(palette.scores): #Efficiency here can be improved by switching to a while statement and exiting early
        if score < oldScores[index]:
            scoreLess = True
    if scoreLess:
        palette.trainDifferentHyp(oldHyp, indexToMod)
    #indicate that another attempt has been made
    palette.attemptCounter[indexToMod] = palette.attemptCounter[indexToMod] + 1

def chooseIndexToMod(palette):
    #the highest score will be chosen to investigate
    MODIFIER = float(1)
    maxModScore = 0
    maxModScoreIndex = 0
    for i in range(len(palette.hyps)):
        modScore = MODIFIER/(float(palette.scores[i])*float(palette.attemptCounter[i])+1)
        if modScore > maxModScore:
            maxModScore = modScore
            maxModScoreIndex = i
    return maxModScoreIndex

def chooseNumInputs(oldHyp, priorAttempts):
    FULL_RANDOM_CHANCE = 1
    if FULL_RANDOM_CHANCE >= random.uniform(0,1):
        num = 1
        ATTEMPTS_WEIGHT = .001
        N2 = .85
        N3 = .9
        N4 = .97
        N5 = .997
        dVal = random.uniform(0,1)+(ATTEMPTS_WEIGHT*priorAttempts)
        if dVal > N5:
            num = 5
        elif dVal > N4:
            num = 4
        elif dVal > N3:
            num = 3
        elif dVal > N2:
            num = 2
    else:
        #TODO: create this portion to reuse tt info from related hyps
        pass
    return num

def chooseTableInfo(oldHyp, priorAttempts):
    FULL_RANDOM_CHANCE = 1
    tts = []
    iniTats = []
    if FULL_RANDOM_CHANCE >= random.uniform(0,1):
        numInputs = chooseNumInputs(oldHyp, priorAttempts)
        depth = 0
        ATTEMPTS_WEIGHT = .001
        D1 = .4
        D2 = .9
        D3 = .97
        D4 = .997
        dVal = random.uniform(0,1)+(ATTEMPTS_WEIGHT*priorAttempts)
        if dVal > D4:
            depth = 4
        elif dVal > D3:
            depth = 3
        elif dVal > D2:
            depth = 2
        elif dVal > D1:
            depth = 1
        for i in range(depth):
            ttOutputs = []
            numOutputs = int(math.pow(2, numInputs+depth))
            for j in range(numOutputs):
                ttOutputs.append(int(random.getrandbits(1)))
            tts.append(TT(ttOutputs))
            iniTats.append(int(random.getrandbits(1)))
    else:
        #TODO: create this portion to reuse tt info from related hyps
        pass
    return tts, iniTats, numInputs

def chooseRelationalInfo_simple(palette, oldHyp, numInputs):
    choiceArray = range(len(palette.iats) + len(palette.aats) - 1)
    chosenIndeces = random.sample(choiceArray, numInputs)
    infoIndeces = []
    actionIndeces = []
    for index in chosenIndeces:
        if index < len(palette.iats):
            infoIndeces.append(index)
        else:
            actionIndeces.append(index - len(palette.iats))
    return infoIndeces, actionIndeces, [], [], 0

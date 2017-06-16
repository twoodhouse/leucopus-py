import random
import math
from tt import TT
from hyp import Hyp
from logUtility import tStart, tEnd

baseHypUsage = {}
hypsByUid = {}

def attemptNewExplanation(palette):
    if len(baseHypUsage) == 0:
        defaultHyp = Hyp(infoIndeces = [0], actionIndeces = [], tts = [], iniTats = [], rHyps = [], rHypLocations = [], iniRat = 0)
        baseHypUsage[defaultHyp.uid] = 1 #NOTE: be careful that this safeguard doesn't break things down the road
        hypsByUid[defaultHyp.uid] = defaultHyp
    if palette.hyps == None or palette.scores == None:
        raise ValueError("Must be foundational Palette (and already fitted) to attempt new explanation")
    indexToMod = chooseIndexToMod(palette) #can be selected based off what infos have poor scores and how often they have been attempted
    oldHyp = palette.hyps[indexToMod]
    oldScores = []
    for score in palette.scores:
        oldScores.append(score)
    #Generate Hyp attributes
    FULL_RANDOM_CHANCE = .1
    if FULL_RANDOM_CHANCE >= random.uniform(0,1):
        hyp = hypFactory_simple(oldHyp, palette, indexToMod)
        trainAndPossiblyRevert(hyp, oldHyp, palette, indexToMod, oldScores)
    else: #Here is the logic for choosing the related hyp to base things off of and also modifying it
        #Related Hyp: make a weighted choice based on past usage of hyps
        hyp, registerHypPairs = hypFactory_reuse(oldHyp, palette, indexToMod)
        success = trainAndPossiblyRevert(hyp, oldHyp, palette, indexToMod, oldScores)
        if success:
            for registerHypPair in registerHypPairs:
                registerHypPair[0].registerHyp(registerHypPair[1])

def trainAndPossiblyRevert(hyp, oldHyp, palette, indexToMod, oldScores):
    #indicate that another attempt has been made
    palette.attemptCounter[indexToMod] = palette.attemptCounter[indexToMod] + 1
    trainingResult = palette.trainDifferentHyp(hyp, indexToMod)
    print(trainingResult)
    scoreMore = False
    for index, score in enumerate(palette.scores): #Efficiency here can be improved by switching to a while statement and exiting early
        if score > oldScores[index]:
            scoreMore = True
    if not scoreMore:
        global baseHypUsage, hypsByUid
        if not oldHyp.uid in hypsByUid:
            hypsByUid[oldHyp.uid] = oldHyp
        if oldHyp.uid in baseHypUsage:
            baseHypUsage[oldHyp.uid] = baseHypUsage[oldHyp.uid] + .01
        else:
            baseHypUsage[oldHyp.uid] = 1
        palette.trainDifferentHyp(oldHyp, indexToMod)
        return False
    else:
        global baseHypUsage, hypsByUid
        if not hyp.uid in hypsByUid:
            hypsByUid[hyp.uid] = hyp
        if hyp.uid in baseHypUsage:
            baseHypUsage[hyp.uid] = baseHypUsage[hyp.uid] + 1
        else:
            baseHypUsage[hyp.uid] = 1
        return True

def attemptSpecificExplanation(palette, index, hyp):
    if palette.hyps == None or palette.scores == None:
        raise ValueError("Must be foundational Palette (and already fitted) to attempt new explanation")
    indexToMod = index #can be selected based off what infos have poor scores and how often they have been attempted
    oldHyp = palette.hyps[indexToMod]
    oldScores = []
    for score in palette.scores:
        oldScores.append(score)
    #try it out
    trainAndPossiblyRevert(hyp, oldHyp, palette, indexToMod, oldScores)

def chooseIndexToMod(palette):
    #the highest score will be chosen to investigate
    MODIFIER = float(1)
    SCORE_WEIGHT = 4
    ATTEMPT_WEIGHT = .1
    maxModScore = 0
    maxModScoreIndex = 0
    for i in range(len(palette.hyps)):
        modScore = MODIFIER/((float(palette.scores[i])**SCORE_WEIGHT)*(float(palette.attemptCounter[i])**ATTEMPT_WEIGHT)+1)
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

def hypFactory_simple(oldHyp, palette, indexToMod):
    tts, iniTats, numInputs = chooseTableInfo_simple(oldHyp, palette.attemptCounter[indexToMod]) #can be selected based off the tts chosen by related hyps and modified from these (or chosen randomly)
    # infoIndeces, actionIndeces, rHyps, rHypLocations, iniRat = chooseRelationalInfo(palette, oldHyp)
    infoIndeces, actionIndeces, rHyps, rHypLocations, iniRat = chooseRelationalInfo_simple(palette, oldHyp, numInputs)
    #generate hyp
    hyp = Hyp(infoIndeces = infoIndeces, actionIndeces = actionIndeces, tts = tts, iniTats = iniTats, rHyps = rHyps, rHypLocations = rHypLocations, iniRat = iniRat)
    return hyp

def chooseTableInfo_simple(oldHyp, priorAttempts):
    tts = []
    iniTats = []
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

def hypFactory_reuse(oldHyp, palette, indexToMod):
    #1. Make a weighted choice of baseline Hyp based on usage of hyps in the near vicinity (TODO? consider some lower levels also in determining weights)
    global baseHypUsage, hypsByUid
    registerHypPairs = []
    hypChoice = hypsByUid[weighted_choice(baseHypUsage.items())]
    topLevelHyp = hypChoice.copy()
    #2. Consider modifying sources or truthTables (depends on how well-used each portion of the vanilla hyp is - use flavor map)
    #3. Recursively do step 2 for lower reuse Hyps
    reassign_random(topLevelHyp, palette)
    registerHypPairs.append((hypChoice, topLevelHyp))
    return topLevelHyp, registerHypPairs

def reassign_random(topLevelHyp, palette):
    INPUT_REASSIGN_CHANCE = .1
    HYP_REASSIGN_CHANCE = .1
    HYP_NEW_REPLACE_CHANCE = .1
    for index, infoIndex in enumerate(topLevelHyp.infoIndeces):
        if INPUT_REASSIGN_CHANCE >= random.uniform(0,1):
            topLevelHyp.infoIndeces[index] = random.choice(range(len(palette.iats)))
    for index, actionIndex in enumerate(topLevelHyp.actionIndeces):
        if INPUT_REASSIGN_CHANCE >= random.uniform(0,1):
            topLevelHyp.actionIndeces[index] = random.choice(range(len(palette.aats)))
    for i in range(len(topLevelHyp.infoIndeces)+len(topLevelHyp.actionIndeces)):
        if HYP_NEW_REPLACE_CHANCE >= random.uniform(0,1):
            #select hyp
            hypChoice = hypsByUid[weighted_choice(baseHypUsage.items())].copy()
            print(len(hypChoice.infoIndeces)+len(hypChoice.actionIndeces)+len(hypChoice.rHyps))
            # reassign_random(hypChoice, palette)
            #determine location
            if i < len(topLevelHyp.infoIndeces):
                topLevelHyp.infoIndeces.pop(i)
            else:
                topLevelHyp.actionIndeces.pop(i-len(topLevelHyp.infoIndeces)-1)
            numHypBefore = 0
            for val in topLevelHyp.rHypLocations:
                if val <= i:
                    numHypBefore += 1
            topLevelHyp.rHyps.insert(numHypBefore, hypChoice)
            topLevelHyp.rHypLocations.insert(numHypBefore, i+numHypBefore)
            print(len(hypChoice.infoIndeces)+len(hypChoice.actionIndeces)+len(hypChoice.rHyps))

def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w >= r:
         return c
      upto += w
   raise ValueError("Shouldn't get here (found this online)")

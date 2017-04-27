import random

class RHManager():
    def __init__(self):
        self.currentUidCounter = 0
        self.rhList = []
        self.topHypotheses = {}
    def newReuseHypothesis(self, originalHypothesis, numTruthTableMod, isTopHypothesis = False, relatedInfoRoute = ""):
        rh = ReuseHypothesis(self, self.currentUidCounter, originalHypothesis, numTruthTableMod)
        if isTopHypothesis:
            self.topHypotheses[relatedInfoRoute] = rh
            for infoRoute, topHypothesis in self.topHypotheses.items():
                rh.linkReuseHypothesis(topHypothesis)
                topHypothesis.linkReuseHypothesis(rh)
        self.currentUidCounter = self.currentUidCounter + 1
        self.rhList.append(rh)
        return rh

class ReuseHypothesis():
    def __init__(self, rhManager, uid, originalHypothesis, numTruthTableMod): #remember that this class does not decide what infos/actions are associated with certain attribute inputs
        #NOTE: Maybe make this so that the originalHypothesis input can be either a ReuseHypothesis or an ICHypothesis?
        self.rhManager = rhManager
        self.uid = uid
        self.originalHypothesis = originalHypothesis
        self.clf = originalHypothesis.clf
        self.numTruthTableMod = numTruthTableMod
        self.depth = originalHypothesis.depth
        self.temporalCaseManager = self.originalHypothesis.temporalCaseManager
        self.infoRoutes = []
        for infoRoute in self.temporalCaseManager.chosenInfoRoutes:
            self.infoRoutes.append(infoRoute)
        self.actionRoutes = []
        for actionRoute in self.temporalCaseManager.chosenActionRoutes:
            self.actionRoutes.append(actionRoute)
        self.truthTables = []
        self.usedBy = []
        self.using = []
        #NOTE: This next line may not be the best choice, but I can't think of a better starting IAttribute situation.
        self.recentFullAttributes = originalHypothesis.icases[-1].fullAttributes #start with the last attribute case from the source
        for truthTable in originalHypothesis.truthTables:
            self.truthTables.append(truthTable.copy())
        for index in range(numTruthTableMod):
            print("modifying truth table")
            tableToModify = random.choice(self.truthTables)
            numberToModify = random.randint(0, len(tableToModify.outputs)-1)
            if tableToModify.outputs[numberToModify] == 0:
                tableToModify.outputs[numberToModify] = 1
            else:
                tableToModify.outputs[numberToModify] = 0
    def linkReuseHypothesis(self, reuseHypothesis):
        self.using.append(reuseHypothesis)
        reuseHypothesis.usedBy.append(self)
    def getOutput(self, inputs): #TODO: Test this method
        fullInputs = inputs
        # Generate all I attributes from previous state
        iAttributes = []
        for truthTable in self.truthTables:
            iAttributes.append(truthTable.retrieve(self.recentFullAttributes))
        fullInputs = fullInputs + iAttributes
        self.recentFullAttributes = fullInputs
        # print(fullInputs)
        # use the clf predict function to get output
        # print(self.clf.predict([fullInputs])[0])
        return self.clf.predict([fullInputs])[0] #should this just take the 0 index?
    def partialClone(self): #NOTE: this is untested
        rh = self.rhManager.newReuseHypothesis(self.originalHypothesis, 0)
        rh.numTruthTableMod = self.numTruthTableMod
        rh.truthTables = []
        for truthTable in self.truthTables:
            rh.truthTables.append(truthTable.copy())
        rh.usedBy = []
        for e in self.usedBy:
            rh.usedBy.append(e)
        rh.using = []
        for e in self.using:
            rh.using.append(e)
        rh.recentFullAttributes = []
        for e in self.recentFullAttributes:
            rh.recentFullAttributes.append(e)
        return rh

def GetReuseHypothesisSuggestionFromReuseHypothesis(reuseHypothesis):
    return random.select(reuseHypothesis.using)

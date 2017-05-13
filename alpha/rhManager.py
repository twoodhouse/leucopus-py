import random

class RHManager():
    def __init__(self):
        self.currentUidCounter = 0
        self.rhList = []
        self.topHypotheses = {}
    def newReuseHypothesis(self, originalHypothesis, numTruthTableMod, isTopHypothesis = False, relatedInfoRoute = ""):
        # if isinstance(originalHypothesis, ReuseHypothesis):
        #     input("waiting for ")
        #     originalHypothesis = originalHypothesis.partialClone()
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
        if isinstance(originalHypothesis, ReuseHypothesis):
            self.initialFullAttributes = originalHypothesis.initialFullAttributes
        else:
            self.initialFullAttributes = originalHypothesis.icases[0].fullAttributes
        #NOTE: This next line may not be the best choice, but I can't think of a better starting IAttribute situation.
        # self.recentFullAttributes = originalHypothesis.icases[-1].fullAttributes #start with the last attribute case from the source
        self.olderRecentFullAttributes = self.initialFullAttributes
        self.recentFullAttributes = self.initialFullAttributes
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
    def getOutput(self, inputs, setRecent = False, backOneMode = False):
        # Generate all I attributes from previous state
        iAttributes = []
        for truthTable in self.truthTables:
            if backOneMode:
                iAttributes.append(truthTable.retrieve(self.olderRecentFullAttributes))
            else:
                iAttributes.append(truthTable.retrieve(self.recentFullAttributes))
        fullInputs = inputs + iAttributes
        print("inputs to rh: "+str(fullInputs))
        output = self.clf.predict([fullInputs])[0]
        if setRecent:
            self.olderRecentFullAttributes = self.recentFullAttributes
            self.recentFullAttributes = fullInputs
            print("rh output: " + str(output))
        return output #should this just take the 0 index?
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
    def __str__(self):
        return strHelper(self.infoRoutes, self.actionRoutes, 0)

def strHelper(infoRoutes, actionRoutes, tabDepth):
    strng = ""
    for i in range(tabDepth):
        strng += "\t"
    strng += "infoRoutes:\n"
    for infoRoute in infoRoutes:
        for i in range(tabDepth):
            strng += "\t"
        if not isinstance(infoRoute, ReuseHypothesis):
            strng += "\t"+infoRoute + "\n"
        else:
            strng += strHelper(infoRoute.infoRoutes, infoRoute.actionRoutes, tabDepth + 1)
    for i in range(tabDepth):
        strng += "\t"
    strng += "actionRoutes:\n"
    for actionRoute in actionRoutes:
        for i in range(tabDepth+1):
            strng += "\t"
        strng += actionRoute + "\n"
    return strng

def GetReuseHypothesisSuggestionFromReuseHypothesis(reuseHypothesis):
    return random.select(reuseHypothesis.using)

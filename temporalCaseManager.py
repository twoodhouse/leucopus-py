from sklearn import tree
from case import ICase
from truthTable import TruthTable
import math
import random

class TemporalCaseManager():
    def __init__(self, cases, depth, allRoutes = True, chosenInfoRoutes = [], chosenActionRoutes = []):
        self.cases = cases
        self.depth = depth
        self.allRoutes = allRoutes
        self.chosenInfoRoutes = chosenInfoRoutes
        self.chosenActionRoutes = chosenActionRoutes
        self.bestHypothesis = None
    def iterate(self, count, printIndex = 100):
        fullAttributeNum = len(self.cases[0].attributes)+self.depth
        truthTableOutputNum = int(math.pow(2, fullAttributeNum))
        for i in range(count):
            if i%printIndex == 0:
                print("\t"+str(i)+"/"+str(count-1))
                print("\t\t"+str(self.getAccuracy()))
            #assign new truthTables randomly
            truthTables = []
            for i in range(self.depth):
                binaryList = []
                for i in range(truthTableOutputNum):
                    binaryList.append(int(random.getrandbits(1)))
                truthTables.append(TruthTable(binaryList))
            #OVERRIDE: TODO - remove
            # truthTables.append(TruthTable([0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0]))
            # truthTables.append(TruthTable([0,1,0,1,0,1,1,0,0,1,0,1,0,1,1,0]))
            # truthTables[1] = TruthTable([])
            #assign initial IAttributes randomly
            initialIAttributes = []
            for i in range(self.depth):
                initialIAttributes.append(int(random.getrandbits(1)))
            #assign ICHypothesis from truthTables and initial IAttributes
            icHypothesis = ICHypothesis(self, self.cases, self.depth, initialIAttributes, truthTables)
            #fit to determine score
            icHypothesis.fit()
            #override best set of truthtables if appropriate
            if self.bestHypothesis == None or icHypothesis.lastKnownScore > self.bestHypothesis.lastKnownScore:
                self.bestHypothesis = icHypothesis
    def getAccuracy(self):
        if self.bestHypothesis == None:
            return 0
        return self.bestHypothesis.lastKnownScore

class ICHypothesis():
    def __init__(self, temporalCaseManager, cases, depth, initialIAttributes, truthTables):
        if depth != len(initialIAttributes):
            raise ValueError("depth does not match length of initialIAttributes provided")
        if depth != len(truthTables):
            raise ValueError("depth does not match length of truthTables provided")
        self.cases = cases
        self.initialIAttributes = initialIAttributes
        self.temporalCaseManager = temporalCaseManager
        self.depth = depth
        self.lastKnownScore = 0
        self.clf = tree.DecisionTreeClassifier()
        self.icases = []
        self.icases.append(ICase(cases[0], self.depth, initialIAttributes))
        #note - this initial condition could alternatively be done by specifying the previous attribute initial conditions and using the truthtable
        self.truthTables = truthTables
        self.generateICaseForEachCase()
    def generateICaseForEachCase(self):
        for idx, case in enumerate(self.cases):
            if case != self.cases[0]: #the first case was already dealt with in the init portion
                iAttributes = []
                for truthTable in self.truthTables:
                    iAttributes.append(truthTable.retrieve(self.icases[idx-1].fullAttributes))
                self.icases.append(ICase(case, self.depth, iAttributes))
    def getNextIAttributesFromFullAttributes(self, fullAttributes):
        iAttributes = []
        for truthTable in self.truthTables:
            iAttributes.append(truthTable.retrieve(fullAttributes))
        return iAttributes
    def getCurrentIAttributesFromRecentFullAttributes(self):
        iAttributes = []
        for truthTable in self.truthTables:
            iAttributes.append(truthTable.retrieve(self.icases[-1].fullAttributes))
        return iAttributes
    def fit(self):
        self.clf.fit(self.getICasesAttributeSet(), self.getICasesClassSet())
        score = self.clf.score(self.getICasesAttributeSet(), self.getICasesClassSet())
        self.lastKnownScore = score
    def getICasesAttributeSet(self):
        icasesAttributeSet = []
        for icase in self.icases:
            icasesAttributeSet.append(icase.fullAttributes)
        return icasesAttributeSet
    def getICasesClassSet(self):
        icasesClassSet = []
        for icase in self.icases:
            icasesClassSet.append(icase.clss)
        return icasesClassSet
    def __str__(self):
        score = self.lastKnownScore
        strng = ""
        strng = strng + "initial: "+str(self.initialIAttributes)+"\n"
        strng = strng + "depth: "+str(self.depth)+"\n"
        for truthTable in self.truthTables:
            strng = strng +str(truthTable)+"\n"
        return strng

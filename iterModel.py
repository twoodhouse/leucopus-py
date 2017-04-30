import requests
from library import Librarian
from collector import RandomCollector
from temporalCaseManager import TemporalCaseManager, ICHypothesis
from rhManager import RHManager
import random
from time import sleep

class IterModel():
    def __init__(self, resetRoute, infoRoutes, actionRoutes, collector = None):
        self.resetPath = resetRoute
        self.reset()
        if collector == None:
            collector = RandomCollector() #update this to the optimal action collector (decision maker) once created
        self.tcmDict = {} #key is infoRoute, item is tcm
        self.infoRoutes = infoRoutes
        self.actionRoutes = actionRoutes
        self.collector = collector
        self.librarian = Librarian(self.infoRoutes, self.actionRoutes)
        self.collector.setLibrarian(self.librarian)
        self.rhManager = RHManager()
        for infoRoute in self.infoRoutes:
            self.tcmDict[infoRoute] = None

    def examine(self):
        self.collector.getActionsAndAddLibrarianRow()

    def consider(self):
        #select info to master
        masterInfoRoute = self.selectMasterInfo()
        print(masterInfoRoute)
        #select infos/actions to include as support
        supportInfoRoutes, supportActionRoutes = self.selectSupportInfosAndActions()
        #select depth
        depth = self.selectDepthToUse()
        #build cases
        print(supportInfoRoutes)
        print(supportActionRoutes)
        #send reuse component to librarian in supportInfoRoutes
        cases = self.librarian.buildCases(masterInfoRoute, allRoutes=False, chosenInfoRoutes = supportInfoRoutes, chosenActionRoutes = supportActionRoutes)
        tcm = TemporalCaseManager(cases, depth=depth, allRoutes = False, chosenInfoRoutes = supportInfoRoutes, chosenActionRoutes = supportActionRoutes)
        self.iterateAndReplaceBest(tcm, masterInfoRoute, depth)

    def considerReuse(self, reuseChance):
        #select info to master
        masterInfoRoute = self.selectMasterInfo()
        print(masterInfoRoute)
        #select infos/actions to include as support
        supportInfoRoutes, supportActionRoutes = self.selectSupportInfosAndActions(atLeast1Info = True)
        #object for reuse must be able to generate an attribute result for each case from the previous case in the librarian.
        reuseCase = False
        for idx, supportInfoRoute in enumerate(supportInfoRoutes):
            reuseChoiceUVal = random.uniform(0,1)
            if reuseChoiceUVal <= reuseChance and self.tcmDict[self.infoRoutes[0]] != None: #TODO: This must be updated with selection module
                reuseCase = True
                supportInfoRoutes[idx] = self.rhManager.newReuseHypothesis(self.tcmDict[self.infoRoutes[0]].bestHypothesis, 0) #TODO: update with selection module
        #select depth
        depth = self.selectDepthToUse()
        #build cases
        print(supportInfoRoutes)
        print(supportActionRoutes)
        #send reuse component to librarian in supportInfoRoutes
        cases = self.librarian.buildCases(masterInfoRoute, allRoutes=False, chosenInfoRoutes = supportInfoRoutes, chosenActionRoutes = supportActionRoutes)
        tcm = TemporalCaseManager(cases, depth=depth, allRoutes = False, chosenInfoRoutes = supportInfoRoutes, chosenActionRoutes = supportActionRoutes)
        #replace old tcm if appropriate. NOTE: No need to iterate since we are trying to preserver the truthTables
        tcm.iterate(40*(depth+1), 10)
        self.replaceBestWithTcmIfAppropriate(tcm, masterInfoRoute)

    def reset(self):
        requests.get(self.resetPath)
        sleep(.05)

    def getLowestAccuracyRoute(self):
        lowestAccuracy = 2 #above the highest possible
        lowestRoute = None
        masterInfoRoute = None
        for infoRoute in self.infoRoutes:
            tcmSel = self.tcmDict[infoRoute]
            if tcmSel == None:
                masterInfoRoute = infoRoute
            else:
                if tcmSel.getAccuracy() < lowestAccuracy:
                    lowestAccuracy = tcmSel.getAccuracy()
                    lowestRoute = infoRoute
        if masterInfoRoute == None and lowestRoute != None:
            masterInfoRoute = lowestRoute
        return masterInfoRoute

    def iterateAndReplaceBest(self, tcm, masterInfoRoute, depth):
        tcm.iterate(40*(depth+1), 10)
        self.replaceBestWithTcmIfAppropriate(tcm, masterInfoRoute)

    def replaceBestWithTcmIfAppropriate(self, tcm, masterInfoRoute):
        if self.tcmDict[masterInfoRoute] == None or self.tcmDict[masterInfoRoute].bestHypothesis == None:
            self.rhManager.topHypotheses[masterInfoRoute] = self.rhManager.newReuseHypothesis(tcm.bestHypothesis, 0)
            self.tcmDict[masterInfoRoute] = tcm
        else:
            priorTcm = self.tcmDict[masterInfoRoute]
            if tcm.getAccuracy() > priorTcm.getAccuracy():
                self.rhManager.topHypotheses[masterInfoRoute] = self.rhManager.newReuseHypothesis(tcm.bestHypothesis, 0)
                self.tcmDict[masterInfoRoute] = tcm
            elif tcm.getAccuracy() == priorTcm.getAccuracy():
                #if accuracy is the same, take the simpler option.
                currentComplexity = 5*tcm.bestHypothesis.depth + len(tcm.cases[0].attributes)
                priorComplexity = 5*priorTcm.bestHypothesis.depth + len(priorTcm.cases[0].attributes)
                if currentComplexity < priorComplexity:
                    self.rhManager.topHypotheses[masterInfoRoute] = self.rhManager.newReuseHypothesis(tcm.bestHypothesis, 0)
                    self.tcmDict[masterInfoRoute] = tcm

    def selectDepthToUse(self):
        depthUVal = random.uniform(0,1)
        depth = 0
        if depthUVal > .95:
            depth = 3
        elif depthUVal > .85:
            depth = 2
        elif depthUVal > .65:
            depth = 1
        else:
            depth = 0
        return depth

    def selectSupportInfosAndActions(self, atLeast1Info = False):
        supportInfoRoutes = self.selectSupportInfoRoutes_Random(atLeast1Info = atLeast1Info)
        supportActionRoutes = self.selectSupportActionRoutes_Random()
        if len(supportInfoRoutes) == 0 and len(supportActionRoutes) == 0:
            supportInfoRoutes = random.sample(self.infoRoutes, 1)
        return supportInfoRoutes, supportActionRoutes

    def selectMasterInfo(self):
        tryWorstUVal = random.uniform(0,1)
        if tryWorstUVal < .6:
            masterInfoRoute = self.getLowestAccuracyRoute()
        else:
            masterInfoRoute = random.choice(self.infoRoutes)
        return masterInfoRoute

    def selectSupportInfoRoutes_Random(self, atLeast1Info = False):
        infosUVal = random.uniform(0,1)
        numInfos = 1
        if infosUVal > .97:
            numInfos = 3
        elif infosUVal > .90:
            numInfos = 2
        elif infosUVal > .70:
            numInfos = 1
        else:
            numInfos = 1
        if numInfos > len(self.infoRoutes):
            numInfos = len(self.infoRoutes)
        supportInfoRoutes = [ self.infoRoutes[i] for i in sorted(random.sample(range(len(self.infoRoutes)), numInfos)) ]
        return supportInfoRoutes

    def selectSupportActionRoutes_Random(self):
        actionsUVal = random.uniform(0,1)
        numActions = 1
        if actionsUVal > .97:
            numActions = 3
        elif actionsUVal > .90:
            numActions = 2
        elif actionsUVal > .70:
            numActions = 1
        else:
            numActions = 0
        if numActions > len(self.actionRoutes):
            numActions = len(self.actionRoutes)
        supportActionRoutes = [ self.actionRoutes[i] for i in sorted(random.sample(range(len(self.actionRoutes)), numActions)) ]
        return supportActionRoutes

    def tryExplanation(self, masterInfoRoute, infoRoutes, actionRoutes, truthTables, initialIAttributes):
        cases = self.librarian.buildCases(masterInfoRoute, allRoutes=False, chosenInfoRoutes = infoRoutes, chosenActionRoutes = actionRoutes)
        tcm = TemporalCaseManager(cases, depth=len(truthTables), allRoutes = False, chosenInfoRoutes = infoRoutes, chosenActionRoutes = actionRoutes)
        icHypothesis = ICHypothesis(tcm, tcm.cases, tcm.depth, initialIAttributes, truthTables)
        icHypothesis.fit()
        tcm.bestHypothesis = icHypothesis
        self.replaceBestWithTcmIfAppropriate(tcm, masterInfoRoute)

    def tryReuseExplanation(self, masterInfoRoute, infoRoutes, actionRoutes, truthTables, initialIAttributes):
        cases = self.librarian.buildCases(masterInfoRoute, allRoutes=False, chosenInfoRoutes = infoRoutes, chosenActionRoutes = actionRoutes)
        # print("printing cases for reuseExplanation")
        tcm = TemporalCaseManager(cases, depth=len(truthTables), allRoutes = False, chosenInfoRoutes = infoRoutes, chosenActionRoutes = actionRoutes)
        icHypothesis = ICHypothesis(tcm, tcm.cases, tcm.depth, initialIAttributes, truthTables)
        for icase in icHypothesis.icases:
            print(icase)
        icHypothesis.fit()
        tcm.bestHypothesis = icHypothesis
        self.replaceBestWithTcmIfAppropriate(tcm, masterInfoRoute)

    def __str__(self):
        fullStr = ""
        fullStr += "*******************ITERMODEL********************\n"
        for infoRoute in self.infoRoutes:
            fullStr += ">>>" + infoRoute + "<<<\n"
            if infoRoute in self.tcmDict:
                tcm = self.tcmDict[infoRoute]
                for infoRoute in tcm.chosenInfoRoutes:
                    fullStr += "I: "+str(infoRoute) + "\n"
                for actionRoute in tcm.chosenActionRoutes:
                    fullStr += "A: "+str(actionRoute) + "\n"
                for index, truthTable in enumerate(tcm.bestHypothesis.truthTables):
                    fullStr += "IC: "+str(tcm.bestHypothesis.initialIAttributes[index])+", "+str(truthTable) + "\n"
                fullStr += "Accuracy: " + str(tcm.getAccuracy()) +"\n"
            else:
                fullStr += "<None>\n"
        return fullStr

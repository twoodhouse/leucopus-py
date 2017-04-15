import requests
from library import Librarian
from collector import RandomCollector
from temporalCaseManager import TemporalCaseManager, ReuseHypothesis
from rhManager import RHManager
import random

class IterModel():
    def __init__(self, resetRoute, infoRoutes, actionRoutes, collector = None):
        if collector == None:
            collector = RandomCollector() #update this to the optimal action collector (decision maker) once created
        self.resetPath = resetRoute
        self.tcmDict = {} #key is infoRoute, item is tcm
        self.infoRoutes = infoRoutes
        self.actionRoutes = actionRoutes
        self.collector = collector
        self.librarian = Librarian(self.infoRoutes, self.actionRoutes)
        self.collector.setLibrarian(self.librarian)
        self.reset()
        for infoRoute in self.infoRoutes:
            self.tcmDict[infoRoute] = None
    def examine(self):
        self.collector.getActionsAndAddLibrarianRow()
    def consider(self):
        #select info to master
        tryWorstUVal = random.uniform(0,1)
        if tryWorstUVal > .1:
            masterInfoRoute = self.getLowestAccuracyRoute()
        else:
            masterInfoRoute = random.choice(self.infoRoutes)
        #select infos/actions to include as support
        supportInfoRoutes, supportActionRoutes = self.selectSupportInfosAndActions()
        #### EDIT AREA BEGIN ####
        #object for reuse must be able to generate an attribute result for each case from the previous case in the librarian.
        for idx, supportInfoRoute in enumerate(supportInfoRoutes):
            reuseChoiceUVal = random.uniform(0,1)
            if reuseChoiceUVal > .4 and self.tcmDict[self.infoRoutes[0]]: #TODO: This must be updated with selection module
                supportInfoRoutes[idx] = RHManager.newReuseHypothesis(self.tcmDict[self.infoRoutes[0]].bestHypothesis, 0) #TODO: update with selection module
        #### EDIT AREA END ####
        #select depth
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
        #build cases
        print(supportInfoRoutes)
        print(supportActionRoutes)
        #send reuse component to librarian in supportInfoRoutes
        cases = self.librarian.buildCases(masterInfoRoute, allRoutes=False, chosenInfoRoutes = supportInfoRoutes, chosenActionRoutes = supportActionRoutes)
        tcm = TemporalCaseManager(cases, depth=depth, allRoutes = False, chosenInfoRoutes = supportInfoRoutes, chosenActionRoutes = supportActionRoutes)
        tcm.iterate(40*(depth+1), 10)
        if self.tcmDict[masterInfoRoute] == None or self.tcmDict[masterInfoRoute].bestHypothesis == None:
            self.tcmDict[masterInfoRoute] = tcm
        else:
            priorTcm = self.tcmDict[masterInfoRoute]
            if tcm.getAccuracy() > priorTcm.getAccuracy():
                self.tcmDict[masterInfoRoute] = tcm
            elif tcm.getAccuracy() == priorTcm.getAccuracy():
                #if accuracy is the same, take the simpler option.
                currentComplexity = 5*tcm.bestHypothesis.depth + len(tcm.cases[0].attributes)
                priorComplexity = 5*priorTcm.bestHypothesis.depth + len(priorTcm.cases[0].attributes)
                if currentComplexity < priorComplexity:
                    self.tcmDict[masterInfoRoute] = tcm

    def reset(self):
        requests.get(self.resetPath)

    def getLowestAccuracyRoute(self):
        lowestAccuracy = 1
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
        print(masterInfoRoute)
        return masterInfoRoute

    def selectSupportInfosAndActions(self):
        supportInfoRoutes = self.selectSupportInfoRoutes_Random()
        supportActionRoutes = self.selectSupportActionRoutes_Random()
        if len(supportInfoRoutes) == 0 and len(supportActionRoutes) == 0:
            supportInfoRoutes = random.sample(self.infoRoutes, 1)
        return supportInfoRoutes, supportActionRoutes

    def selectSupportInfoRoutes_Random(self):
        infosUVal = random.uniform(0,1)
        numInfos = 1
        if infosUVal > .97:
            numInfos = 3
        elif infosUVal > .90:
            numInfos = 2
        elif infosUVal > .70:
            numInfos = 1
        else:
            numInfos = 0
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

    def __str__(self):
        fullStr = ""
        fullStr += "*******************ITERMODEL********************\n"
        for infoRoute in self.infoRoutes:
            fullStr += ">>>" + infoRoute + "<<<\n"
            if infoRoute in self.tcmDict:
                tcm = self.tcmDict[infoRoute]
                print(tcm.chosenInfoRoutes)
                for infoRoute in tcm.chosenInfoRoutes:
                    fullStr += "I: "+str(infoRoute) + "\n"
                for actionRoute in tcm.chosenActionRoutes:
                    fullStr += "A: "+str(actionRoute) + "\n"
                for truthTable in tcm.bestHypothesis.truthTables:
                    fullStr += str(truthTable) + "\n"
                fullStr += "Accuracy: " + str(tcm.getAccuracy()) +"\n"
            else:
                fullStr += "<None>\n"
        return fullStr

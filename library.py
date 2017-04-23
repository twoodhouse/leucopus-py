import requests
import inspect
from case import Case
from rhManager import ReuseHypothesis
import random

class Librarian():
    def __init__(self, infoRoutes, actionRoutes, initialActions = [], maxCaseSize = None):
        self.infoRoutes = infoRoutes
        self.actionRoutes = actionRoutes
        self.allRoutes = infoRoutes + actionRoutes
        self.infoDict = {}
        self.actionDict = {}
        #When a new ReuseHypothesis is selected for reuse, I must generate classes from the ground up.
        #When the human mind attempts reuse, it must generate all classes for the interim node from river and cascades
        #   Why then do I have problems with this approach? It seems like it would take a lot of time (EACH iteration)
        #   to generate the interim classes. The beautiful part is that in the situation I am trying to solve,
        #   I only really need to try a few modifications to the ReuseHypothesis in order to solve it (assuming source mod is prefered)

        self.maxCaseSize = maxCaseSize
        self.size = 0
        for infoRoute in self.infoRoutes:
            self.infoDict[infoRoute] = []
        zeroList = []
        for actionRoute in self.actionRoutes:
            self.actionDict[actionRoute] = []
            zeroList.append(0)
        if len(initialActions) > 0:
            self.next(initialActions)
        else:
            self.next(zeroList)
    def next(self, actions):
        for infoRoute in self.infoRoutes:
            rqst = requests.get(infoRoute)
            #TODO: consider adding a delay here
            if rqst.text == "true":
                self.infoDict[infoRoute].append(1)
            elif rqst.text == "false":
                self.infoDict[infoRoute].append(0)
        if len(actions) != len(self.actionRoutes):
            raise ValueError("actions array length does not match length of known routes list")
        for idx, action in enumerate(actions):
            self.actionDict[self.actionRoutes[idx]].append(action)
            if action == 1:
                requests.get(self.actionRoutes[idx])
        self.size = self.size + 1
        if self.maxCaseSize != None:
            if self.size > self.maxCaseSize+1:
                self.removeFirst()
    def buildCases(self, masterRoute, allRoutes = False, chosenInfoRoutes = [], chosenActionRoutes = []):
        #### EDIT AREA BEGIN ####
        #separate reuseHypotheses out of chosenInfoRoutes
        reuseHypotheses = []
        chosenInfoRoutes_actual = []
        for infoRoute in chosenInfoRoutes:
            if inspect.isclass(infoRoute):
                reuseHypotheses.append(infoRoute) #note that in this case, the infoRoute is not actually an infoRoute, it is a reuseHypothesis
            else:
                chosenInfoRoutes_actual.append(infoRoute)
        chosenInfoRoutes_withRH = chosenInfoRoutes
        #create temporary attribute dictionaries TODO: LATER - consider modifying so that the most common reuseHypotheses have cases kept up to date to avoid re-calculating the case.
        # hypothesisDict = {}
        # for reuseHypothesis in reuseHypotheses:
        #     rhAttributes = self.recurseAttributeDevelopment(reuseHypotheses, masterRoute, allRoutes = allRoutes, chosenInfoRoutes = chosenInfoRoutes, chosenActionRoutes = chosenActionRoutes)
        #     hypothesisDict[reuseHypothesis] = rhAttributes
        #build cases
        cases = [] #info THEN action
        # print(masterRoute)
        for i in range(len(self.infoDict[masterRoute])-1):
            attributes = []
            if allRoutes: #NOTE: This portion is pretty much not used
                for infoRoute in self.infoRoutes:
                    attributes.append(self.infoDict[infoRoute][i])
                for actionRoute in self.actionRoutes:
                    attributes.append(self.actionDict[actionRoute][i])
            else: #Only this else portion will really be used
                attributesRow = self.getAttributesRowFromChosen(i, chosenInfoRoutes, chosenActionRoutes)
            clss = self.infoDict[masterRoute][i+1]
            case = Case(attributesRow, clss)
            cases.append(case)
        return cases
        #### EDIT AREA END ####
    # def recurseAttributeDevelopment(self, hypothesis, masterRoute, allRoutes = False, chosenInfoRoutes = [], chosenActionRoutes = []): #input is the hypothesis which should have cases produced
    #     #### EDIT AREA BEGIN ####
    #     attributes = []
    #     for i in range(len(self.infoDict[masterRoute])-1):
    #         reuseChoiceUVal = random.uniform(0,1)
    #         if reuseChoiceUVal < .3:
    #             #TODO: fix these 2 sections next
    #             reuseHypothesis = self.rhManager.newReuseHypothesis(self.tcmDict[self.infoRoutes[0]].bestHypothesis, 0) #TODO: update with selection module
    #             # attributes.append() = self.recurseAttributeDevelopment(reuseHypothesis)
    #         else:
    #
    #         attributesRow = self.getAttributesRowFromChosen(i, chosenInfoRoutes, chosenActionRoutes)
    #     return attributesRow
    #     #### EDIT AREA END ####
    def getAttributesRowFromChosen(self, index, chosenInfoRoutes, chosenActionRoutes):
        attributes = []
        for chosenInfoRoute in chosenInfoRoutes:
            if not isinstance(chosenInfoRoute, ReuseHypothesis):
                for route in self.infoRoutes:
                    if route == chosenInfoRoute:
                        attributes.append(self.infoDict[chosenInfoRoute][index])
            else:
                #The chosenInfoRoute is really a ReuseHypothesis
                reuseHypothesis = chosenInfoRoute.partialClone()
                #Decide if any of the truthTables in ReuseHypothesis will be changed
                #TODO: can delay this section for now
                #Decide if any of the inputs to the ReuseHypothesis will be changed
                for index, infoRoute in enumerate(reuseHypothesis.infoRoutes):
                    modifyInputUVal = random.uniform(0,1)
                    if modifyInputUVal < .6: #TODO: later change this to possibly choose a reuse hypothesis and smartly choose infos/actions
                        reuseHypothesis.infoRoutes[index] = random.choice(self.infoRoutes)
                for index, actionRoute in enumerate(reuseHypothesis.actionRoutes):
                    modifyInputUVal = random.uniform(0,1)
                    if modifyInputUVal < .6: #TODO: later change this to possibly choose a reuse hypothesis and smartly choose infos/actions
                        reuseHypothesis.actionRoutes[index] = random.choice(self.actionRoutes)
                #Remake any existing reuseHypotheses if they are set as inputs to this ReuseHypothesis
                for index, infoRoute in enumerate(reuseHypothesis.infoRoutes):
                    if isinstance(infoRoute, ReuseHypothesis):
                        reuseHypothesis.infoRoutes[index] = reuseHypothesis.rhManager.partialClone()
                #Assign inputs given the specific ordering of info/action routes and reuseHypotheses (replace source chance)
                inputs = self.getAttributesRowFromChosen(index, reuseHypothesis.infoRoutes, reuseHypothesis.actionRoutes)
                #Determine the values of all inputs to the reuseHypothesis
                attributes.append(reuseHypothesis.getOutput(inputs))
        for chosenActionRoute in chosenActionRoutes:
            for route in self.actionRoutes:
                if route == chosenActionRoute:
                    attributes.append(self.actionDict[chosenActionRoute][index])
        return attributes
    def removeFirst(self):
        for infoRoute in self.infoRoutes:
            self.infoDict[infoRoute].pop(0)
        for actionRoute in self.actionRoutes:
            self.actionDict[actionRoute].pop(0)
    def getMostRecentAttributes(self):
        attributes = []
        for infoRoute in self.infoRoutes:
            attributes.append(self.infoDict[infoRoute][-1])
        for actionRoute in self.actionRoutes:
            attributes.append(self.actionDict[actionRoute][-1])
        return attributes
    def getMostRecentInfoAttributes(self):
        attributes = []
        for infoRoute in self.infoRoutes:
            attributes.append(self.infoDict[infoRoute][-1])
        return attributes
    def printFullCases(self):
        for i in range(len(self.infoDict[self.infoRoutes[0]])):
            caseAttributes = []
            for infoRoute in self.infoRoutes:
                caseAttributes.append(self.infoDict[infoRoute][i])
            for actionRoute in self.actionRoutes:
                caseAttributes.append(self.actionDict[actionRoute][i])
            print(caseAttributes)

# class Visinator():
#     def __init__(self, masterRoute, infoRoutes):
#         self.masterRoute = masterRoute
#         self.infoRoutes = infoRoutes
#     def getMaster(self):
#         rqst = requests.get(self.masterRoute)
#         if rqst.text == "true":
#             return 1
#         elif rqst.text == "false":
#             return 0
#     def getInfos(self):
#         results = []
#         for infoRoute in self.infoRoutes:
#             rqst = requests.get(infoRoute)
#             if rqst.text == "true":
#                 results.append(1)
#             elif rqst.text == "false":
#                 results.append(0)
#         return results
#
#
# class Actinator():
#     def __init__(self, actionRoutes):
#         self.actionRoutes = actionRoutes
#     def sendActions(self, actions):
#         if len(actions) != len(self.actionRoutes):
#             raise ValueError("actions array length does not match length of known routes")
#         for idx, action in enumerate(actions):
#             if action == 1:
#                 requests.get(self.actionRoutes[idx])

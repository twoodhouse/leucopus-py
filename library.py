import requests
from case import Case

class Librarian():
    def __init__(self, infoRoutes, actionRoutes, initialActions = [], maxCaseSize = None):
        self.infoRoutes = infoRoutes
        self.actionRoutes = actionRoutes
        self.infoDict = {}
        self.actionDict = {}
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
        cases = [] #info THEN action
        for i in range(len(self.infoDict[masterRoute])-1):
            attributes = []
            if allRoutes:
                for infoRoute in self.infoRoutes:
                    attributes.append(self.infoDict[infoRoute][i])
                for actionRoute in self.actionRoutes:
                    attributes.append(self.actionDict[actionRoute][i])
            else:
                for infoRoute in self.infoRoutes:
                    chosen = False
                    for route in chosenInfoRoutes:
                        if route == infoRoute:
                            chosen = True
                    if chosen:
                        attributes.append(self.infoDict[infoRoute][i])
                for actionRoute in self.actionRoutes:
                    chosen = False
                    for route in chosenActionRoutes:
                        if route == actionRoute:
                            chosen = True
                    if chosen:
                        attributes.append(self.actionDict[actionRoute][i])
            clss = self.infoDict[masterRoute][i+1]
            case = Case(attributes, clss)
            cases.append(case)
        return cases
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

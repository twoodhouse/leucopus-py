from case import Case
from random import randint

class RandomCollector():
    def __init__(self, librarian = None):
        self.librarian = librarian
    def setLibrarian(self, librarian):
        self.librarian = librarian
    def collectCases(self, masterRoute, count, allRoutes = True, chosenInfoRoutes = [], chosenActionRoutes = []):
        for i in range(count):
            actions = []
            for actionRoute in self.librarian.actionRoutes:
                randVal = randint(0, 1)
                actions.append(randVal)
            self.librarian.next(actions)
        return self.librarian.buildCases(masterRoute, allRoutes, chosenInfoRoutes = chosenInfoRoutes, chosenActionRoutes = chosenActionRoutes)
    def getActionsAndAddLibrarianRow(self):
        actions = []
        for actionRoute in self.librarian.actionRoutes:
            randVal = randint(0, 1)
            actions.append(randVal)
        self.librarian.next(actions)

class DecisionCollector():
    def __init__(self, librarian):
        self.librarian = librarian
    def collect(self, masterRoute, count):
        pass

# class RandomCollector():
#     def __init__(self, actinator, visinator):
#         self.actinator = actinator
#         self.visinator = visinator
#     def collect(self, count):
#         cases = []
#         for i in range(count):
#             case = []
#             #collect master value
#             case.append(self.visinator.getMaster())
#             #collect info values
#             infoVals = self.visinator.getInfos()
#             for infoVal in infoVals:
#                 case.append(infoVal)
#             #generate random action values to be fed in. One for each action route.
#             actions = []
#             for actionRoute in self.actinator.actionRoutes:
#                 randVal = randint(0, 1)
#                 actions.append(randVal)
#                 case.append(randVal)
#             self.actinator.sendActions(actions)
#             #case is finished. Add to cases.
#             cases.append(case)
#         return cases

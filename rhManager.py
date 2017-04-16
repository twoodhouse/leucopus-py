from temporalCaseManager import ReuseHypothesis

class RHManager():
    def __init__(self):
        self.currentUidCounter = 0
        self.rhList = []
    def newReuseHypothesis(self, originalHypothesis, numTruthTableMod):
        rh = ReuseHypothesis(self.currentUidCounter, originalHypothesis, numTruthTableMod)
        self.currentUidCounter = self.currentUidCounter + 1
        self.rhList.append(rh)
        return rh

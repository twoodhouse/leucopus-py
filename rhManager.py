from temporalCaseManager import ReuseHypothesis

class RHManager():
    def __init__(self):
        self.currentUidCounter = 0
    def newReuseHypothesis(self, originalHypothesis, numTruthTableMod):
        rh = ReuseHypothesis(self.currentUidCounter, originalHypothesis, numTruthTableMod=)
        self.currentUidCounter = self.currentUidCounter + 1
        return rh

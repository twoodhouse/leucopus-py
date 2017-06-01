from palette import Palette
from hyp import Hyp
from explanationUtility import attemptNewExplanation

class Deluge():
    def __init__(self, env, dm, initialActions):
        self.env = env
        self.dm = dm
        dm.setDeluge(self)
        hyps = []
        for infoMethod in env.infoMethods:
            hyps.append(Hyp(infoIndeces = [0], actionIndeces = [], tts = [], iniTats = [], rHyps = [], rHypLocations = [], iniRat = 0))
        initialIats, initialAats = env.runFrame(initialActions)
        #TODO: add a function which allows a foundational palette to make the next palette foundational
        self.river = Palette(iats = initialIats, aats = initialAats, isFoundation = True, hyps = hyps)
        self.riverTop = self.river
        self.pRiver = self.river.copy()
        self.pRiverTop = self.pRiver
        self.cascades = []
        # self.river.trainHypsUsingDownstreamAts()
        # self.pRiver.trainHypsUsingDownstreamAts()
    def processNextFrame(self, printOp = False):
        actionSet = self.dm.getActionSet()
        newIats, newAats = self.env.runFrame(actionSet)
        self.riverTop = self.riverTop.genNext(iats = newIats, aats = newAats)
        if printOp:
            self.riverTop.infoPrintAll()
        self.river.trainHypsUsingDownstreamAts()
    def startNewPrediction(self):
        self.pRiver = self.river.copy()
        self.pRiverTop = self.pRiver
        self.pRiver.trainHypsUsingDownstreamAts()
    def processNextPFrame(self, printOp = False):
        actionSet = self.dm.getActionSet(isPrediction = True)
        newAats = actionSet
        self.pRiverTop = self.pRiverTop.genNext(aats = newAats)
        if printOp:
            self.pRiverTop.infoPrintAll()
    def TryExplanation(self):
        attemptNewExplanation(self.river)
        #TODO: insert logic for checking cascade scores also
    def addCascadeFromRiver(self):
        cascade = self.river.copy()
        self.cascades.append(cascade)
    def printHyps(self):
        for hyp in self.river.hyps:
            print(str(hyp))

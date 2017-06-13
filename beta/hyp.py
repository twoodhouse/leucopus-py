from sklearn import tree
import copy

class Hyp():
    def __init__(self, infoIndeces, actionIndeces, tts, iniTats, rHyps, rHypLocations, iniRat):
        if len(tts) != len(iniTats):
            raise ValueError("length of truth tables (" + str(len(tts)) + ") does not match length of initial table attributes (" + str(len(iniTats)) + ")")
        self.infoIndeces = infoIndeces
        self.actionIndeces = actionIndeces
        self.clf = tree.DecisionTreeClassifier()
        self.tts = tts
        self.iniTats = iniTats
        if len(rHyps) != len(rHypLocations):
            raise ValueError("length of rHyps (" + str(len(rHyps)) + ") does not match length of rHypLocations (" + str(len(rHypLocations)) + ")")
        self.rHyps = rHyps
        self.rHypLocations = rHypLocations
        self.iniRat = iniRat #Remember: all hyps need an iniRat in case they are copied and used in another instance
        self.sourceHyp = None
        self.totalRegisteredHyps = 0
        self.registeredHyps = []
    def fitAndScoreClf(self, attributes, classes):
        self.clf.fit(attributes, classes)
        score = self.clf.score(attributes, classes)
        return score
    def predictFromClf(self, attributes):
        output = self.clf.predict([attributes])[0]
        return output
    def getTTOutputs(self, attributes):
        outputs = []
        for tt in self.tts:
            outputs.append(tt.retrieve(attributes))
        return outputs
    def registerHyp(self, otherHyp): #NOTE: Do I need to include a "deregister" method also? Probably not. The point is to show that these similarities were useful in creating a new hypothesis, not that they were perfect.
        if len(self.infoIndeces) != len(otherHyp.infoIndeces) or len(self.actionIndeces) != len(otherHyp.actionIndeces) or len(self.tts) != len(otherHyp.tts):
            raise ValueError("num inputs and num tts must match to register a hyp")
        self.registeredHyps.append(otherHyp)
        self.totalRegisteredHyps = self.totalRegisteredHyps + 1
    def copy(self):
        cp = copy.deepcopy(self)
        cp.sourceHyp = self
        cp.registeredHyps = [] #NOTE: if a problem arises, make sure this statement should be here
        return cp
    def __str__(self):
        st = "***********HYP***********\n"
        st += str(self.infoIndeces) + "\n"
        st += str(self.actionIndeces) + "\n"
        for tt in self.tts:
            st += str(tt) + "\n"
        return st

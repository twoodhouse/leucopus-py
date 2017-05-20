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
        self.iniRat = iniRat
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
    def copy(self):
        return copy.deepcopy(self)

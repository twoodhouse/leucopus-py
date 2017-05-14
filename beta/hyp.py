from sklearn import tree
import copy

class Hyp():
    def __init__(self, infoUids, actionUids, tts, iniTat):
        if len(tts) != len(iniTat):
            raise ValueError("length of truth tables (" + str(len(tts)) + ") does not match length of initial table attributes (" + str(len(iniTat)) + ")")
        self.infoUids = infoUids
        self.actionUids = actionUids
        self.clf = tree.DecisionTreeClassifier()
        self.tts = tts
        self.iniTat = iniTat
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

from rhManager import ReuseHypothesis

class Branch():
    def __init__(self, librarian, actions, hypotheses = None, branch = None):
        # self.finalAttributeRow = hypothesis.icases[len(hypothesis.icases)-1].fullAttributes
        self.isBranchRef = False
        self.sinkBranch = None
        self.sourceBranch = None
        self.actions = actions
        self.librarian = librarian
        self.infos = []
        self.attributes = []
        self.hypothesesIAttributes = {}
        self.attributes = []
        if len(self.actions) != len(self.librarian.actionRoutes):
            raise ValueError("Number of actions input does not match the number of actions that the librarian has")
        if hypotheses == None and branch == None:
            raise ValueError("Must input either a hypothesis or a Branch into the Branch class")
        if hypotheses != None:
            self.hypotheses = hypotheses
        if branch != None:
            self.sourceBranch = branch
            self.sourceBranch.setSink(self)
            self.isBranchRef = True
            self.hypotheses = self.sourceBranch.hypotheses
        if not self.isBranchRef and len(hypotheses) != len(self.librarian.infoRoutes):
            raise ValueError("Incorrect number of hypotheses. Need same number of info points that librarian has.")
        #first add attributes for infos (one for each hypothesis)
        if self.isBranchRef:
            infos = [] #TODO: next - fix the "setRecent" portion. It is updating at the wrong times
            for hypothesis in self.hypotheses:
                #EXPERIMENTAL
                if hypothesis.temporalCaseManager.allRoutes == False: #logic dealing with only using certain attributes
                    # print("getting attributes")
                    attributesNeeded = self.getAttributesNeeded(hypothesis.temporalCaseManager.chosenInfoRoutes, hypothesis.temporalCaseManager.chosenActionRoutes, setRecent = True)
                    # print(attributesNeeded + self.sourceBranch.hypothesesIAttributes[hypothesis])
                    info = hypothesis.clf.predict([attributesNeeded + self.sourceBranch.hypothesesIAttributes[hypothesis]])[0]
                else:
                    info = hypothesis.clf.predict([self.sourceBranch.attributes + self.sourceBranch.hypothesesIAttributes[hypothesis]])[0]
                infos.append(info)
            self.infos = infos
            for hypothesis in self.hypotheses:
                if not hypothesis in self.hypothesesIAttributes:
                    self.hypothesesIAttributes[hypothesis] = []
                for truthTable in hypothesis.truthTables:
                    if hypothesis.temporalCaseManager.allRoutes == False: #logic dealing with only using certain attributes
                        attributesNeeded = self.getAttributesNeeded(hypothesis.temporalCaseManager.chosenInfoRoutes, hypothesis.temporalCaseManager.chosenActionRoutes, setRecent = False)
                        iAttribute = truthTable.retrieve(attributesNeeded + self.sourceBranch.hypothesesIAttributes[hypothesis])
                        # print("iattribute determination: "+ str(self.sourceBranch.attributes + self.sourceBranch.hypothesesIAttributes[hypothesis]))
                        # print("iattribute: "+str(iAttribute))
                    else:
                        iAttribute = truthTable.retrieve(self.sourceBranch.attributes + self.sourceBranch.hypothesesIAttributes[hypothesis])
                    self.hypothesesIAttributes[hypothesis].append(iAttribute)
            self.attributes = self.infos + self.actions
        else:
            self.infos = self.librarian.getMostRecentInfoAttributes()
            for hypothesis in self.hypotheses:
                iAttributes = hypothesis.getCurrentIAttributesFromRecentFullAttributes()
                self.hypothesesIAttributes[hypothesis] = iAttributes
            self.attributes = self.infos + self.actions
        print("final: "+str(self.attributes)) #don't comment this out

    def getAttributesNeeded(self, chosenInfoRoutes, chosenActionRoutes, setRecent = False):
        # print("starting")
        attributesNeeded = []
        for infoRoute in chosenInfoRoutes:
            if not isinstance(infoRoute, ReuseHypothesis):
                index = None
                for librarianIdx, librarianInfoRoute in enumerate(self.librarian.infoRoutes):
                    if infoRoute == librarianInfoRoute:
                        index = librarianIdx
                if index == None:
                    raise ValueError("Couldn't find info route in librarian")
                attributesNeeded.append(self.sourceBranch.attributes[index])
            else:
                #infoRoute is actually ReuseHypothesis
                reuseHypothesis = infoRoute
                inputs = self.getAttributesNeeded(reuseHypothesis.infoRoutes, reuseHypothesis.actionRoutes)
                # print("in get attributes")
                x = reuseHypothesis.getOutput(inputs, setRecent = setRecent)
                attributesNeeded.append(x)
        for actionRoute in chosenActionRoutes:
            index = None
            for librarianIdx, librarianActionRoute in enumerate(self.librarian.actionRoutes):
                if actionRoute == librarianActionRoute:
                    index = librarianIdx
            if index == None:
                raise ValueError("Couldn't find action route in librarian")
            attributesNeeded.append(self.sourceBranch.attributes[len(self.librarian.infoRoutes) + index])
        # print("concluding attr: " +str(attributesNeeded))
        return attributesNeeded

    def setSink(self, branch):
        self.sinkBranch = branch

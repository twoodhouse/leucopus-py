from rhManager import ReuseHypothesis

class Branch():
    def __init__(self, librarian, actions=None, hypotheses = None, branch = None):
        # self.finalAttributeRow = hypothesis.icases[len(hypothesis.icases)-1].fullAttributes
        if hypotheses != None and actions != None:
            raise ValueError("Can't input actions when starting a new branch with hypotheses")
        self.isBranchRef = False
        self.sinkBranch = None
        self.sourceBranch = None
        self.actions = actions
        self.librarian = librarian
        self.infos = []
        self.attributes = []
        self.hypothesesIAttributes = {}
        self.attributes = []
        if hypotheses == None and len(self.actions) != len(self.librarian.actionRoutes):
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
        iattributesToPrint = []
        if self.isBranchRef:
            infos = []
            for hypothesis in self.hypotheses:
                #EXPERIMENTAL
                if hypothesis.temporalCaseManager.allRoutes == False: #logic dealing with only using certain attributes
                    attributesNeeded = self.getAttributesNeeded(hypothesis.temporalCaseManager.chosenInfoRoutes, hypothesis.temporalCaseManager.chosenActionRoutes, setRecent = False)
                    # if hypothesis == self.hypotheses[1]:
                    #     print("attributes to create info for this: " + str(attributesNeeded + self.sourceBranch.hypothesesIAttributes[hypothesis]))
                    info = hypothesis.clf.predict([attributesNeeded + self.sourceBranch.hypothesesIAttributes[hypothesis]])[0]
                else:
                    raise ValueError("not implemented yet")
                    info = hypothesis.clf.predict([self.sourceBranch.attributes + self.sourceBranch.hypothesesIAttributes[hypothesis]])[0]
                infos.append(info)
            self.infos = infos
            for hypothesis in self.hypotheses:
                if not hypothesis in self.hypothesesIAttributes:
                    self.hypothesesIAttributes[hypothesis] = []
                for truthTable in hypothesis.truthTables:
                    if hypothesis.temporalCaseManager.allRoutes == False: #logic dealing with only using certain attributes
                        attributesNeeded = self.getAttributesNeeded(hypothesis.temporalCaseManager.chosenInfoRoutes, hypothesis.temporalCaseManager.chosenActionRoutes, setRecent = True)
                        # if hypothesis == self.hypotheses[1]:
                        #     print("inputs to the I1 truthTable for next hyp2: " + str(attributesNeeded + self.sourceBranch.hypothesesIAttributes[hypothesis]))
                        iAttribute = truthTable.retrieve(attributesNeeded + self.sourceBranch.hypothesesIAttributes[hypothesis])
                    else:
                        raise ValueError("not implemented yet")
                        iAttribute = truthTable.retrieve(self.sourceBranch.attributes + self.sourceBranch.hypothesesIAttributes[hypothesis])
                    self.hypothesesIAttributes[hypothesis].append(iAttribute)
                    iattributesToPrint.append(iAttribute)
            self.attributes = self.infos + self.actions
        else:
            self.infos = self.librarian.getMostRecentInfoAttributes()
            actions = self.librarian.getMostRecentActionAttributes()
            for hypothesis in self.hypotheses:
                iAttributes = hypothesis.getCurrentIAttributesFromRecentFullAttributes()
                if not hypothesis in self.hypothesesIAttributes:
                    self.hypothesesIAttributes[hypothesis] = []
                for truthTable in hypothesis.truthTables:
                    attributesNeeded = self.getAttributesNeeded(hypothesis.temporalCaseManager.chosenInfoRoutes, hypothesis.temporalCaseManager.chosenActionRoutes, setRecent = True, isBranchRef = False)
                    # if hypothesis == self.hypotheses[1]:
                        # print("inputs to the I1 truthTable for next hyp2: " + str(attributesNeeded + iAttributes))
                    iAttribute = truthTable.retrieve(attributesNeeded + iAttributes)
                    self.hypothesesIAttributes[hypothesis].append(iAttribute)
                    iattributesToPrint.append(iAttribute)
            self.attributes = self.infos + actions
        # print("iattributes for next hyp2: " + str(iattributesToPrint[1]))
        print("final: "+str(self.attributes)) #don't comment this out
        # print()

    def getAttributesNeeded(self, chosenInfoRoutes, chosenActionRoutes, setRecent = False, isBranchRef = True):
        attributesNeeded = []
        for infoRoute in chosenInfoRoutes:
            if not isinstance(infoRoute, ReuseHypothesis):
                if isBranchRef:
                    index = None
                    for librarianIdx, librarianInfoRoute in enumerate(self.librarian.infoRoutes):
                        if infoRoute == librarianInfoRoute:
                            index = librarianIdx
                    if index == None:
                        raise ValueError("Couldn't find info route in librarian")
                    attributesNeeded.append(self.sourceBranch.attributes[index])
                else:
                    attributesNeeded.append(self.librarian.infoDict[infoRoute][-1])
            else:
                #infoRoute is actually ReuseHypothesis
                reuseHypothesis = infoRoute
                inputs = self.getAttributesNeeded(reuseHypothesis.infoRoutes, reuseHypothesis.actionRoutes, setRecent = setRecent, isBranchRef = isBranchRef)
                x = reuseHypothesis.getOutput(inputs, setRecent = setRecent)
                attributesNeeded.append(x)
        for actionRoute in chosenActionRoutes:
            if isBranchRef:
                index = None
                for librarianIdx, librarianActionRoute in enumerate(self.librarian.actionRoutes):
                    if actionRoute == librarianActionRoute:
                        index = librarianIdx
                if index == None:
                    raise ValueError("Couldn't find action route in librarian")
                attributesNeeded.append(self.sourceBranch.attributes[len(self.librarian.infoRoutes) + index])
            else:
                attributesNeeded.append(self.librarian.actionDict[actionRoute][-1])
        return attributesNeeded

    def setSink(self, branch):
        self.sinkBranch = branch
